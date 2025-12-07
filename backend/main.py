from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import AnalyzeRequest, AnalysisResponse
import ingestion
import analysis
import json
import re
import ast
import asyncio
import os

app = FastAPI(title="Git Sense API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for results (replace with DB in production)
results_store = {}

def clean_json_string(json_str: str) -> str:
    """Removes markdown code blocks and extracts JSON list."""
    print(f"DEBUG: Raw JSON string length: {len(json_str)}")
    # Remove markdown code blocks
    pattern = r"```(?:json)?\s*(.*?)\s*```"
    match = re.search(pattern, json_str, re.DOTALL)
    if match:
        json_str = match.group(1)
    
    # Attempt to find the first [ and last ]
    start = json_str.find("[")
    end = json_str.rfind("]")
    
    if start != -1 and end != -1:
        return json_str[start : end + 1]
    
    # Fallback: if no list found, try to find { } for single object or return original
    # But we expect lists for most things.
    return json_str.strip()

def parse_json_safely(json_str: str):
    """Tries to parse JSON, falling back to ast.literal_eval."""
    cleaned = clean_json_string(json_str)
    try:
        return json.loads(cleaned, strict=False)
    except json.JSONDecodeError:
        try:
            # Fallback for Python-style dicts/lists (single quotes)
            return ast.literal_eval(cleaned)
        except (ValueError, SyntaxError):
            print(f"Failed to parse JSON: {cleaned[:100]}...")
            return []

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def get_cache_path(repo_id: str):
    return os.path.join(CACHE_DIR, f"{repo_id}.json")

def save_to_cache(repo_id: str, data: dict):
    try:
        with open(get_cache_path(repo_id), "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Failed to save cache for {repo_id}: {e}")

def load_from_cache(repo_id: str):
    try:
        path = get_cache_path(repo_id)
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"Failed to load cache for {repo_id}: {e}")
    return None

async def process_analysis(repo_url: str, repo_id: str):
    print(f"Starting analysis for {repo_id}...")
    
    # Check cache first
    cached_data = load_from_cache(repo_id)
    if cached_data:
        print(f"Loaded results from cache for {repo_id}")
        results_store[repo_id] = cached_data
        return

    # Initialize partial results
    results_store[repo_id] = {
        "status": "processing",
        "bugs": None,
        "suggestions": None,
        "readme": None,
        "structure": None,
        "file_summaries": None,
        "commits": None
    }

    try:
        # Ingestion (Blocking I/O, run in thread)
        repo_id, file_tree = await asyncio.to_thread(ingestion.process_repository, repo_url)
        
        # Analysis (Parallel Execution with Progressive Updates)
        print("Starting parallel analysis...")
        
        async def run_and_update(task_func, key, *args):
            try:
                result_raw = await asyncio.to_thread(task_func, *args)
                # Parse if it's one of the JSON fields
                if key in ["bugs", "suggestions", "file_summaries"]:
                    result = parse_json_safely(result_raw)
                else:
                    result = result_raw
                
                # Update store incrementally
                results_store[repo_id][key] = result
                print(f"Completed {key} for {repo_id}")
            except Exception as e:
                print(f"Failed {key} for {repo_id}: {e}")
                results_store[repo_id][key] = [] if key in ["bugs", "suggestions", "file_summaries", "commits"] else f"Error: {e}"

        # Define tasks
        tasks = [
            run_and_update(analysis.analyze_bugs, "bugs", repo_id),
            run_and_update(analysis.analyze_suggestions, "suggestions", repo_id),
            run_and_update(analysis.generate_readme, "readme", repo_id),
            run_and_update(analysis.analyze_structure, "structure", repo_id, file_tree),
            run_and_update(analysis.analyze_file_summaries, "file_summaries", repo_id),
            run_and_update(ingestion.get_recent_commits, "commits", repo_url)
        ]
        
        # Execute all tasks concurrently
        await asyncio.gather(*tasks)
        
        # Mark as completed and save to cache
        results_store[repo_id]["status"] = "completed"
        save_to_cache(repo_id, results_store[repo_id])
        
        print(f"Analysis for {repo_id} completed.")
    except Exception as e:
        print(f"Analysis failed: {e}")
        results_store[repo_id] = {
            "status": "failed",
            "error": str(e)
        }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_repo(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    repo_id = request.repo_url.split("/")[-1].replace(".git", "")
    results_store[repo_id] = {"status": "processing"}
    background_tasks.add_task(process_analysis, request.repo_url, repo_id)
    return {"message": "Analysis started", "repo_id": repo_id}

@app.get("/results/{repo_id}")
async def get_results(repo_id: str):
    result = results_store.get(repo_id)
    if not result:
        raise HTTPException(status_code=404, detail="Repo not found or analysis not started")
    return result

@app.get("/status")
def health_check():
    return {"status": "ok"}


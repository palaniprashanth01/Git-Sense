from pydantic import BaseModel
from typing import List, Optional

class AnalyzeRequest(BaseModel):
    repo_url: str
    branch: Optional[str] = None # Auto-detect if None

class AnalysisResponse(BaseModel):
    message: str
    repo_id: str

class QueryRequest(BaseModel):
    repo_id: str
    query: str

class PushRequest(BaseModel):
    repo_url: str
    file_path: str
    content: str
    commit_message: str
    branch: Optional[str] = "main"

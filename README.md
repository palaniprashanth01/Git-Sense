# Git Sense

**Git Sense** is an advanced AI-powered code analysis tool designed to help developers understand, improve, and document their repositories instantly. By leveraging Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs), Git Sense provides deep insights into codebase structure, security vulnerabilities, and code quality.

## Project Overview

Git Sense acts as an intelligent layer on top of your Git repositories. It ingests code, creates vector embeddings for semantic search, and uses high-performance LLMs (via Groq) to answer questions and perform automated audits. It features a modern, responsive React frontend and a robust FastAPI backend.

## Features

- **Automated Repository Analysis**: simply paste a GitHub URL to start.
- **Deep Code Understanding**: RAG-based engine (ChromaDB + LangChain) ensures accurate context.
- **Bug & Security Detection**: Automatically identifies potential security risks and logical errors.
- **Code Quality Suggestions**: Provides actionable refactoring advice to improve maintainability.
- **Structure Analysis**: Visualizes and explains the high-level architecture of the project.
- **Automatic README Generation**: Generates comprehensive documentation for undocumented projects.
- **Push to Git**: Directly commit and push generated artifacts (like READMEs) back to the repository.
- **Persistent Caching**: Caches analysis results for instant load times on subsequent visits.
- **Live Updates**: Real-time progress tracking of the analysis pipeline.

## Installation

### Prerequisites
- Node.js (v18+)
- Python (v3.10+)
- Git installed locally

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create customizable virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure Environment:
   Create a `.env` file in `backend/` and add your Groq API keys:
   ```env
   GROQ_API_KEYS=<your_groq_api_key>
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```

## Usage Examples

### 1. Start the Application
**Backend Terminal:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```
**Frontend Terminal:**
```bash
cd frontend
npm run dev
```

### 2. Analyze a Repo
1. Open your browser to `http://localhost:5173`.
2. Enter a public GitHub repository URL (e.g., `https://github.com/fastapi/fastapi`).
3. Click **Analyze**.
4. Explore the tabs: **Bugs**, **Suggestions**, **Structure**, etc.

### 3. Push Generated Content
1. Navigate to the **README** tab after analysis.
2. Review the generated README.
3. Click **Push to Git** to commit the file directly to the analyzed repository (requires local write access).

## Future Plans

- **User Authentication**: Multi-user support with private history.
- **Multi-LLM Support**: Integration with OpenAI and Anthropic models.
- **IDE Extensions**: VS Code plugin for inline analysis.
- **Cloud Deployment**: One-click deploy to Vercel/Render.
- **Custom Rule Engine**: Allow users to define custom linting rules for the AI.

## What Not To Do

- **Do Not Share API Keys**: Never commit your `.env` file containing API keys.
- **Do Not Run on Unverified Large Repos**: Indexing extremely large monorepos locally may consume significant CPU/RAM.
- **Do Not Push Without Review**: Always review the "Push to Git" content; AI can occasionally hallucinate details.
- **Do Not Ignore Security Warnings**: While the AI is good, it is not a replacement for a professional security audit.

---
*Built with ❤️ by Palani Prashanth.*

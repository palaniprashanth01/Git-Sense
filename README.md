# Git Sense

Git Sense is an advanced AI-powered repository analyzer that provides deep insights into your code. It features bug detection, refactoring suggestions, structure analysis, and more, all wrapped in a modern, responsive dashboard.

## Features

- **Deep Analysis**: Detects bugs, security vulnerabilities, and provides refactoring suggestions.
- **Structure Visualization**: Generates a file tree and high-level architectural overview.
- **File Summaries**: Automatically summarizes key files.
- **Commit History**: Retrieves and displays recent git commits.
- **Performance**: Parallel execution, result caching, and streaming updates for a fast experience.
- **Robustness**: Handles API rate limits with automatic key rotation.

## Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.10 or higher)
- **Git**

## Setup Instructions

### 1. Backend Setup

Navigate to the `backend` directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory with your Groq API keys:

```env
GROQ_API_KEYS=gsk_key1,gsk_key2,gsk_key3
```

Start the backend server:

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

### 2. Frontend Setup

Open a new terminal and navigate to the `frontend` directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`.

## Usage

1.  Open `http://localhost:5173` in your browser.
2.  Enter a public GitHub repository URL (e.g., `https://github.com/fastapi/fastapi`).
3.  Click **Analyze**.
4.  Watch as the results stream in!

## Troubleshooting

-   **Analysis Failed**: Check the backend logs. Ensure your Groq API keys are valid and you haven't exceeded your rate limits.
-   **Connection Refused**: Ensure both the backend (port 8000) and frontend (port 5173) servers are running.

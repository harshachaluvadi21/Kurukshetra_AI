# Kurukshetra AI

## Problem Statement
Early-stage founders struggle to validate startup ideas because market research, competitor analysis, financial feasibility, and business planning are scattered across multiple tools and require significant time, expertise, and resources. This often leads to poor decision-making, delayed execution, and a high risk of startup failure. There is a need for an AI-powered platform that can autonomously analyze business ideas, generate actionable insights, and provide data-driven recommendations in a single workflow.

## How It Works
Kurukshetra AI is a full-stack AI application powered by multiple Large Language Models (LLMs). It uses a Next.js frontend for an interactive user interface and a FastAPI backend to handle real-time communications via WebSockets, database operations, and AI orchestration using LangChain and various AI providers.

## Key Features
- **Multi-LLM Support:** Integrates with Google Gemini and Groq for fast and accurate AI responses.
- **Advanced Search & Retrieval:** Uses Tavily and Serper for web search, combined with ChromaDB for vector storage and retrieval.
- **Real-time Interaction:** Employs WebSockets for low-latency communication.
- **Secure Authentication:** Built-in Google OAuth integration for secure user login.
- **Modern Database:** Asynchronous operations with Neon PostgreSQL.

## Tech Stack
- **Frontend:** Next.js (Deployed on Vercel)
- **Backend:** FastAPI, Python 3.12.4 (Deployed on Render)
- **Database:** Neon PostgreSQL (Relational), ChromaDB (Vector Store)
- **AI / ML:** LangChain, Google Gemini API, Groq API, Tavily, Serper

## Architecture
The application is separated into a serverless frontend and a continuous backend service:
- **Frontend (Vercel):** Hosts the Next.js React application and manages Google OAuth redirects.
- **Backend (Render):** Hosts the FastAPI web service, processing API requests and WebSocket connections.
- **Database (Neon):** Hosts the PostgreSQL database, managed securely without exposing credentials.

## Environment Variables (.env)
To run this project, you need to configure the following environment variables. **Never commit real API keys to version control.**

### Backend (`backend/.env`)
```env
ENVIRONMENT=production
PYTHON_VERSION=3.12.4
DATABASE_URL=<your-neon-postgres-url>
GOOGLE_API_KEY=<your-gemini-api-key>
GROQ_API_KEY=<your-groq-api-key>
TAVILY_API_KEY=<your-tavily-api-key>
SERPER_API_KEY=<your-serper-api-key>
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHROMA_HOST=
CHROMA_API_KEY=
CHROMA_TENANT=
CHROMA_DATABASE=
LANGCHAIN_TRACING_V2=false
LANGCHAIN_PROJECT=Kurukshetra_AI
GOOGLE_CLIENT_ID=<your-google-oauth-client-id>
GOOGLE_CLIENT_SECRET=<your-google-oauth-client-secret>
SECRET_KEY=<generate-a-long-random-secret>
CORS_ORIGINS=https://your-vercel-app.vercel.app,http://localhost:3000
```

### Frontend (`frontend/.env.local`)
```env
NEXT_PUBLIC_API_URL=https://your-render-service.onrender.com
GOOGLE_CLIENT_ID=<your-google-oauth-client-id>
NEXT_PUBLIC_GOOGLE_CLIENT_ID=<your-google-oauth-client-id>
```

## Installation Steps

### Local Development

**1. Backend Setup:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows. Use `source venv/bin/activate` on Mac/Linux
pip install -r requirements.txt
copy .env.example .env # Update with your keys
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**2. Frontend Setup:**
```bash
cd frontend
npm install
copy .env.example .env.local # Update with your keys
npm run dev
```
Open `http://localhost:3000` to view the application.

### Production Deployment

**1. Backend (Render):**
- Create a new **Web Service** on Render from the GitHub repo.
- Set Root directory: `backend`
- Set Runtime: **Python**
- Build command: `pip install -r requirements.txt`
- Start command: `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Add the backend environment variables in the Render dashboard.

**2. Frontend (Vercel):**
- Import the repo into Vercel.
- Set Root Directory: `frontend`
- Add the frontend environment variables in the Vercel dashboard.

**3. Google OAuth Setup:**
- In Google Cloud Console, add `https://your-vercel-app.vercel.app/api/auth/google/callback` to your authorized redirect URIs.


## Author Info
- **Name:** Sai Harsha Chaluvadi
- **GitHub:** [@harshachaluvadi21](https://github.com/harshachaluvadi21)
- **LinkedIn:** [@Sai Harsha Chaluvadi](https://www.linkedin.com/in/saiharshachaluvadi)
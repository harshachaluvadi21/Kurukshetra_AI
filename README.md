# Kurukshetra AI Deployment Guide

This repo has two deployable apps:

- `frontend/`: Next.js app, deploy on Vercel
- `backend/`: FastAPI app, deploy on Render
- Database: Neon PostgreSQL

Deploy the backend first. The frontend needs the backend public URL.

Never commit real API keys, database URLs, OAuth secrets, or `.env` files. Put production secrets only in Render and Vercel environment variables.

## Deployment Architecture

- Vercel hosts only the frontend.
- Render hosts only the FastAPI backend.
- Neon hosts the PostgreSQL database.
- Do not create or use a Render PostgreSQL database for this project.

## 1. Backend on Render

### Create the web service

1. Go to [Render](https://dashboard.render.com/).
2. Click **New +** -> **Blueprint**.
3. Connect the GitHub repository you pushed.
4. Select the repository root. Render will read `render.yaml`.
5. Create the service.
6. Skip any Render PostgreSQL/database creation prompts. The database is Neon.

If you deploy manually instead of using the blueprint, use:

- Service type: **Web Service**
- Root directory: `backend`
- Runtime: **Python**
- Build command: `pip install -r requirements.txt`
- Start command: `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Environment variable: `PYTHON_VERSION=3.12.4`

### Use Neon PostgreSQL

This project is configured to use Neon PostgreSQL. Render is only the backend host.

1. Go to the [Neon dashboard](https://console.neon.tech/).
2. Open your Neon project.
3. Open **Connection Details**.
4. Select the pooled connection string if Neon shows both pooled and direct options.
5. Copy the PostgreSQL connection string.
6. In Render, open the backend web service -> **Environment**.
7. Add the Neon connection string as `DATABASE_URL`.

Use this shape, replacing the password/host with your real Neon values inside Render only:

```env
DATABASE_URL=postgresql://neondb_owner:<password>@<neon-pooler-host>/neondb?sslmode=require&channel_binding=require
```

Do not paste the real Neon URL into `README.md`, `render.yaml`, `.env.example`, or any committed file.

The backend automatically converts Neon URLs like `postgresql://...` to the async SQLAlchemy format it needs, so you do not need to manually change it to `postgresql+asyncpg://...`.

### Add backend environment variables

In the Render backend service, open **Environment** and add:

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
CORS_ORIGINS=https://your-vercel-app.vercel.app
```

After the frontend is deployed, update `CORS_ORIGINS` to your real Vercel URL. For multiple allowed origins, use commas:

```env
CORS_ORIGINS=https://your-vercel-app.vercel.app,http://localhost:3000
```

### Verify backend

After Render finishes deploying, open this URL in your browser:

```text
https://your-render-service.onrender.com/
```

Expected response:

```json
{"name":"Kurukshetra AI Backend","status":"running","health":"/health","docs":"/docs"}
```

Then open the health check URL:

```text
https://your-render-service.onrender.com/health
```

Expected response:

```json
{"status":"healthy"}
```

If the deploy fails during `alembic upgrade head`, check:

- `DATABASE_URL` is set in Render.
- The Neon database is active.
- The connection string includes `sslmode=require`.
- You pasted the full URL, including query parameters.

If the deploy fails while installing `asyncpg`, check the Render logs for `cp314` or Python `3.14`. That means Render is using Python 3.14 instead of Python 3.12. Set this in Render -> backend service -> **Environment**:

```env
PYTHON_VERSION=3.12.4
```

Then trigger **Manual Deploy** -> **Clear build cache & deploy**.

## 2. Frontend on Vercel

### Import the frontend

1. Go to [Vercel](https://vercel.com/new).
2. Import the same GitHub repository.
3. Set **Root Directory** to `frontend`.
4. Keep framework as **Next.js**.
5. Build settings are already defined in `frontend/vercel.json`.

### Add frontend environment variables

In Vercel project settings, add:

```env
NEXT_PUBLIC_API_URL=https://your-render-service.onrender.com
GOOGLE_CLIENT_ID=<your-google-oauth-client-id>
NEXT_PUBLIC_GOOGLE_CLIENT_ID=<your-google-oauth-client-id>
```

Redeploy the frontend after adding or changing environment variables.

## 3. Google OAuth setup

In Google Cloud Console, open your OAuth client and add this authorized redirect URI:

```text
https://your-vercel-app.vercel.app/api/auth/google/callback
```

For local development, also keep:

```text
http://localhost:3000/api/auth/google/callback
```

Use the same `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in Render. Use the same client ID in Vercel.

## 4. Final deployment checklist

1. Push this repo to GitHub.
2. Deploy backend on Render from `render.yaml`.
3. Do not create a Render database.
4. Add the Neon URL as Render `DATABASE_URL`.
5. Add `PYTHON_VERSION=3.12.4` in Render.
6. Add all backend API keys and OAuth secrets in Render.
7. Wait until `https://your-render-service.onrender.com/health` returns `{"status":"healthy"}`.
8. Deploy frontend on Vercel with root directory `frontend`.
9. Add `NEXT_PUBLIC_API_URL=https://your-render-service.onrender.com` in Vercel.
10. Update Render `CORS_ORIGINS=https://your-vercel-app.vercel.app`.
11. Add Google OAuth redirect URI: `https://your-vercel-app.vercel.app/api/auth/google/callback`.
12. Redeploy both services after changing environment variables.
13. Run login and a sample analysis from the deployed frontend.

## Secret rotation note

If a real Neon connection string, API key, or OAuth secret is shared in chat, screenshots, logs, or committed code, rotate it in the provider dashboard and update the new value in Render/Vercel. This avoids surprise access to your database.

## Local Development

Backend:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:

```bash
cd frontend
npm install
copy .env.example .env.local
npm run dev
```

Open `http://localhost:3000`.

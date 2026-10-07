# InsightPath Production Deployment Guide

This guide details deployment procedures for the **InsightPath / RUSTY WOLVES** web application across modern cloud hosting providers.

---

## 1. System Architecture Overview

```
                      +-----------------------------+
                      |   Client Web Browser (HTTPS)|
                      +--------------+--------------+
                                     |
                +--------------------+--------------------+
                |                                         |
                v                                         v
     +-----------------------+                 +----------------------+
     |   Frontend (Next.js)  |                 |  Backend (FastAPI)   |
     |   Vercel / AWS Amplify|                 |  Railway / Docker    |
     +-----------+-----------+                 +----------+-----------+
                 |                                        |
                 | (Client-side Supabase SDK with RLS)     | (Read-Only FS Access)
                 v                                        v
     +-----------------------+                 +----------------------+
     |   Supabase PostgreSQL |                 | Models & Artifacts   |
     |   Auth & User Profiles|                 | models/ outputs/     |
     +-----------------------+                 +----------------------+
```

---

## 2. Database Setup (Supabase)

1. Create a new project in the [Supabase Dashboard](https://app.supabase.com).
2. Navigate to the **SQL Editor** tab.
3. Open [`supabase/migrations/20261008_auth_and_career_profiles.sql`](../../supabase/migrations/20261008_auth_and_career_profiles.sql).
4. Run the SQL script to provision:
   - `public.profiles`
   - `public.career_goals`
   - `public.assessments`
   - `public.assessment_scores`
   - `public.roadmap_items`
   - Row Level Security (RLS) policies for user data isolation
   - User creation triggers linked to `auth.users`
5. Copy your **Project URL** and **anon public key** from Project Settings $\to$ API.

---

## 3. Frontend Deployment (Vercel)

### Option A: Via Vercel CLI
```bash
cd frontend
vercel
```

### Option B: Via Git Integration (GitHub / GitLab)
1. Import repository into Vercel.
2. Set Root Directory to `frontend`.
3. Framework Preset: **Next.js**.
4. Configure Production Environment Variables:
   - `NEXT_PUBLIC_API_URL`: Your deployed FastAPI backend URL (e.g., `https://api.insightpath.ai`)
   - `NEXT_PUBLIC_SUPABASE_URL`: Your Supabase project URL
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Your Supabase anon public key
5. Deploy.

---

## 4. Backend Deployment (FastAPI)

### Containerization (Dockerfile)
Create or use the following production Dockerfile for the FastAPI backend:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Prevent Python from writing .pyc and enable buffer-less stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend, models, and analytical tables
COPY backend/ ./backend/
COPY models/ ./models/
COPY outputs/ ./outputs/
COPY data/ ./data/

# Expose port and launch via Uvicorn
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Deploying to Render (Blueprint or Native Web Service)
1. **Render Blueprint (Recommended)**: Use the included [`render.yaml`](../../render.yaml) by creating a new **Blueprint** service on the Render Dashboard.
2. **Manual Web Service**:
   - Environment: `Python` (version `3.11.9`)
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Health Check Path: `/health`
   - Environment Variables:
     - `ENVIRONMENT=production`
     - `HOST=0.0.0.0`
     - `CORS_ALLOWED_ORIGINS=https://your-app.vercel.app,http://localhost:3000`
     - `API_V1_STR=/api/v1`

See the root [`DEPLOYMENT_README.md`](../../DEPLOYMENT_README.md) for full step-by-step guidance.

---

## 5. Security & Pre-Launch Checklist

- [x] Service-role key is **never** included in `NEXT_PUBLIC_` variables.
- [x] All private database tables enforce PostgreSQL Row Level Security (`ALTER TABLE ... ENABLE ROW LEVEL SECURITY`).
- [x] CORS origins restricted to verified frontend domains in production.
- [x] Machine learning models and analytical tables remain strictly read-only on the backend.
- [x] Rate limiting configured on reverse proxy or API Gateway.

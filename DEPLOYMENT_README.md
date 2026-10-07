# InsightPath Production Deployment Guide

This guide provides end-to-end instructions for deploying the **InsightPath / RUSTY WOLVES** web application to production using **Render** (FastAPI Backend), **Vercel** (Next.js Frontend), and **Supabase** (PostgreSQL Auth & Career Profiles).

---

## 1. System Architecture

```
                               +-----------------------------+
                               |     Client Browser (HTTPS)  |
                               +--------------+--------------+
                                              |
                        +---------------------+---------------------+
                        |                                           |
                        v                                           v
       +---------------------------------+         +---------------------------------+
       |        Frontend (Next.js)       |         |        Backend (FastAPI)        |
       |        Hosted on Vercel         |         |        Hosted on Render         |
       |  - Server-Side & Static Render  |         |  - Uvicorn ASGI Server          |
       |  - Tailwind CSS + Lucide Icons  |         |  - Binds 0.0.0.0:$PORT          |
       |  - Client Supabase SDK (RLS)    |         |  - Consumes Phases 0-9 Outputs  |
       +----------------+----------------+         +----------------+----------------+
                        |                                           |
                        | (User Auth & Profile Data)                | (Read-Only FS Access)
                        v                                           v
       +---------------------------------+         +---------------------------------+
       |      Supabase PostgreSQL        |         |   Validated Artifacts & Models  |
       |  - Row Level Security (RLS)     |         |  - outputs/models/phase5/       |
       |  - Profiles, Goals, Assessments |         |  - outputs/models/phase6/       |
       |  - Career Roadmaps              |         |  - outputs/tables/              |
       +---------------------------------+         +---------------------------------+
```

---

## 2. Backend Deployment (Render)

The FastAPI backend consumes precomputed analytical tables and serialized champion scikit-learn models (`outputs/models/phase5/jds_champion_logistic_l2.joblib` and `outputs/models/phase6/sds_champion_logistic_l2.joblib`). It binds to `0.0.0.0` and listens on the dynamic `$PORT` assigned by Render.

### Option A: Automatic Deployment via Render Blueprint (Recommended)

1. Fork or push the repository to your GitHub/GitLab account.
2. Log in to [Render Dashboard](https://dashboard.render.com).
3. Click **New +** $\to$ **Blueprint**.
4. Select your `DataScienceTool` repository.
5. Render detects [`render.yaml`](render.yaml) automatically and provisions:
   - Service Name: `insightpath-backend`
   - Runtime: `Python 3.11.9`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Health Check Path: `/health`
6. Click **Apply**.
7. Note down your backend URL (e.g., `https://insightpath-backend.onrender.com`).

---

### Option B: Manual Web Service Setup via Render Dashboard

If you prefer configuring via the web UI:

1. In Render Dashboard, click **New +** $\to$ **Web Service**.
2. Connect your Git repository.
3. Configure the service settings:
   - **Name**: `insightpath-backend`
   - **Region**: `Oregon (US West)` or your closest region
   - **Branch**: `main`
   - **Root Directory**: `.` *(leave blank / project root)*
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free` or `Starter`
4. Expand **Advanced** $\to$ **Environment Variables**, and add:
   | Key | Value | Description |
   |---|---|---|
   | `PYTHON_VERSION` | `3.11.9` | Ensures exact scikit-learn/joblib compatibility |
   | `HOST` | `0.0.0.0` | Required for container network routing |
   | `ENVIRONMENT` | `production` | Enables production security logging |
   | `CORS_ALLOWED_ORIGINS` | `https://*.vercel.app,http://localhost:3000` | Allowed origins (replace with your frontend domain) |
   | `API_V1_STR` | `/api/v1` | Routing prefix |
5. Under **Health Check Path**, enter:
   ```
   /health
   ```
6. Click **Create Web Service**.

---

## 3. Frontend Deployment (Vercel)

The Next.js 15 frontend communicates with the Render backend via `NEXT_PUBLIC_API_URL` and directly with Supabase via client-side keys protected by PostgreSQL Row Level Security.

### Option A: Vercel Dashboard (Recommended)

1. Go to [Vercel Dashboard](https://vercel.com/dashboard) and click **Add New...** $\to$ **Project**.
2. Import your Git repository.
3. In **Project Configuration**:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: Click `Edit` and select `frontend`
   - **Build Command**: `npm run build` *(auto-detected)*
   - **Output Directory**: `.next` *(auto-detected)*
4. Expand **Environment Variables** and configure:
   | Variable | Value | Description |
   |---|---|---|
   | `NEXT_PUBLIC_API_URL` | `https://insightpath-backend.onrender.com` | Your deployed Render backend URL |
   | `NEXT_PUBLIC_SUPABASE_URL` | `https://<your-project>.supabase.co` | Supabase Project URL *(Optional)* |
   | `NEXT_PUBLIC_SUPABASE_ANON_KEY` | `<your-anon-key>` | Supabase Public Anonymous API Key *(Optional)* |

   > **Note on Supabase**: If `NEXT_PUBLIC_SUPABASE_URL` is omitted, the frontend automatically activates an in-memory/localStorage session mode for seamless evaluation and demo testing.

5. Click **Deploy**.
6. When complete, copy your production domain (e.g., `https://insightpath.vercel.app`).
7. Update the Render backend's `CORS_ALLOWED_ORIGINS` to include your new production domain:
   ```
   https://insightpath.vercel.app,http://localhost:3000
   ```

---

### Option B: Deploy via Vercel CLI

```bash
# Navigate to the frontend directory
cd frontend

# Install Vercel CLI if not already installed
npm install -g vercel

# Authenticate and link project
vercel login
vercel

# Deploy to production with environment variables
vercel --prod \
  --build-env NEXT_PUBLIC_API_URL="https://insightpath-backend.onrender.com"
```

---

## 4. Optional Database & Auth Setup (Supabase)

If you enable persistent multi-user authentication and cloud profile storage:

1. Create a project at [supabase.com](https://supabase.com).
2. In the Supabase Dashboard, go to the **SQL Editor**.
3. Copy and run the script in [`supabase/migrations/20261008_auth_and_career_profiles.sql`](supabase/migrations/20261008_auth_and_career_profiles.sql).
4. This provisions:
   - `profiles` table linked to `auth.users`
   - `career_goals`, `assessments`, `assessment_scores`, and `roadmap_items` tables
   - Automated triggers for new user registration
   - Strict Row Level Security (RLS) guaranteeing user-data isolation
5. Retrieve your project URL and `anon` key under **Project Settings** $\to$ **API**.
6. Add them to Vercel's Environment Variables (`NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`).
7. **CRITICAL SECURITY NOTE**: Never prefix `SUPABASE_SERVICE_ROLE_KEY` with `NEXT_PUBLIC_`. The frontend only uses the public anonymous key with RLS.

---

## 5. Verification & Health Checks

After both services have deployed, run the following verification checks:

### 1. Root & Production Health Endpoint
```bash
curl -i https://insightpath-backend.onrender.com/health
```
**Expected Response (HTTP 200)**:
```json
{
  "status": "ok",
  "version": "1.0.0",
  "service": "InsightPath API",
  "environment": "production",
  "artifacts_verified": true,
  "details": {
    "models": {
      "jds_model_loaded": true,
      "sds_model_loaded": true,
      "jds_champion_roc_auc": 0.9035,
      "sds_champion_roc_auc": 0.9699
    },
    "tables_dir_exists": true,
    "tables_count": 25,
    "host": "0.0.0.0",
    "port": 10000
  }
}
```

### 2. Market Data API Check
```bash
curl -i https://insightpath-backend.onrender.com/api/v1/market/overview
```
**Expected Response**: HTTP 200 with salary metrics, top roles, and sample size from Phase 3/4.

### 3. Career-Readiness Model Inference Test
```bash
curl -i -X POST https://insightpath-backend.onrender.com/api/v1/assessment/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "career_goal": "Senior Data Scientist",
    "experience_level": "Mid-Level",
    "maths_stats_score": 7.5,
    "coding_score": 8.0,
    "ai_ml_score": 7.0,
    "big_data_score": 6.5,
    "dashboarding_score": 6.0
  }'
```
**Expected Response**: HTTP 200 containing model readiness probability, percentile index, evidence-supported strengths, and priority development areas.

### 4. Frontend End-to-End Verification
1. Visit your Vercel deployment URL (e.g. `https://insightpath.vercel.app`).
2. Verify all dashboard tabs render data directly from the Render backend:
   - **Market Trends**: Bar charts, salary distributions, top skills.
   - **Skills Intelligence**: Premium skill ROI, frequency matrix.
   - **Career Assessment**: Interactive assessment evaluates inputs against the live champion model.
   - **Talent Roadmap**: 4-quadrant talent matrix and stage-gated milestones.
   - **Evidence Modal**: Traceability drawer links every insight back to analytical phases.

---

## 6. Environment Variables Reference

### Backend (`.env` or Render Dashboard)
| Variable | Default | Purpose |
|---|---|---|
| `HOST` | `0.0.0.0` | Network binding interface |
| `PORT` | `8000` | Dynamic port (Render sets `$PORT` automatically) |
| `ENVIRONMENT` | `production` | Operational environment string |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000` | Comma-separated list or JSON array of permitted origins |
| `PROJECT_ROOT` | *Auto-detected* | Optional override for project root path |
| `TABLES_DIR` | `outputs/tables` | Precomputed analytical tables directory |
| `MODELS_DIR` | `outputs/models` | Champion machine learning models directory |

### Frontend (`frontend/.env.local` or Vercel Dashboard)
| Variable | Default | Purpose |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Render backend URL |
| `NEXT_PUBLIC_SUPABASE_URL` | *None* | Supabase project endpoint |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | *None* | Supabase client anon key |

---

## 7. Troubleshooting & Operational Notes

- **Render Cold Starts**: Render's free tier spins down idle instances after 15 minutes. The first request after inactivity may take 30–50 seconds to initialize. For zero latency, upgrade to a paid Render Starter instance.
- **CORS Blocking**: If browser console reports `Blocked by CORS policy`, verify that your exact Vercel domain (with `https://`) is present in Render's `CORS_ALLOWED_ORIGINS` variable.
- **Model Files Availability**: All serialized champion models (`outputs/models/phase5/` and `outputs/models/phase6/`) and analytical tables (`outputs/tables/`) are committed to Git so Render can load them during container startup without external storage dependencies.

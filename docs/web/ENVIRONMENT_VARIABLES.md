# InsightPath Environment Variables Specification

This document details all configuration variables required by the **InsightPath / RUSTY WOLVES** platform across the Next.js frontend and FastAPI backend.

---

## 1. Frontend Environment Variables (`frontend/.env.local`)

All client-accessible variables must be prefixed with `NEXT_PUBLIC_` per Next.js security conventions.

| Variable Name | Required | Default | Scope | Description |
|---|---|---|---|---|
| `NEXT_PUBLIC_API_URL` | No | `http://localhost:8000` | Browser / SSR | URL of the deployed FastAPI backend serving models & analytical tables. |
| `NEXT_PUBLIC_SUPABASE_URL` | Yes (in prod) | `https://placeholder-project.supabase.co` | Browser / SSR | Supabase Project URL (`https://<project-id>.supabase.co`). |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Yes (in prod) | `placeholder-anon-key` | Browser / SSR | Supabase public anonymous API key for client-side authentication and RLS operations. |
| `SUPABASE_SERVICE_ROLE_KEY` | Optional | *None* | Server-Only | **CRITICAL**: Never prefix with `NEXT_PUBLIC_`. Reserved strictly for administrative backend tasks. |

> **Local Development Fallback**: When `NEXT_PUBLIC_SUPABASE_URL` is unset or points to a placeholder URL, the frontend automatically activates an in-memory/localStorage session simulation. This allows complete end-to-end testing of sign-in, profile calibration, assessment persistence, and roadmap state without requiring an active Supabase project.

---

## 2. Backend Environment Variables (`backend/config.py`)

Backend variables are managed via Pydantic `BaseSettings` and can be supplied via environment variables or a `.env` file in the project root.

| Variable Name | Required | Default | Description |
|---|---|---|---|
| `HOST` | No | `0.0.0.0` | Network binding interface. Must be `0.0.0.0` on Render/Docker. |
| `PORT` | No | `8000` | Port to listen on. Dynamically injected as `$PORT` by Render. |
| `PROJECT_NAME` | No | `InsightPath API` | Name of the FastAPI application. |
| `VERSION` | No | `1.0.0` | API version string. |
| `API_V1_STR` | No | `/api/v1` | Routing prefix for v1 endpoints. |
| `ENVIRONMENT` | No | `development` | Deployment environment (`development`, `staging`, `production`). |
| `CORS_ALLOWED_ORIGINS` | No | `http://localhost:3000` | Allowed CORS origins. Comma-separated strings, wildcard `*`, or JSON array. |
| `PROJECT_ROOT` | No | Auto-resolved | Absolute path to project root (auto-detected via pathlib). |
| `TABLES_DIR` | No | `outputs/tables` | Directory containing precomputed Phase 3-9 CSV tables. |
| `MODELS_DIR` | No | `outputs/models` | Directory containing champion serialized ML pipelines. |
| `JDS_MODEL_PATH` | No | `outputs/models/phase5/jds_champion_logistic_l2.joblib` | Path to Phase 5 JDS champion model. |
| `SDS_MODEL_PATH` | No | `outputs/models/phase6/sds_champion_logistic_l2.joblib` | Path to Phase 6 SDS champion model. |

---

## 3. Security Guidelines

1. **Never commit `.env` or `.env.local` to git repositories**: `.gitignore` is configured to prevent accidental commits.
2. **Never expose service-role keys to browser bundles**: Client authentication must strictly use anonymous keys with PostgreSQL Row Level Security (RLS) enforcement.
3. **CORS Isolation**: In production, ensure `CORS_ORIGINS` is restricted only to trusted domains hosting the Next.js frontend.

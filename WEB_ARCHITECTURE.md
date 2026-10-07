# InsightPath Web Product Architecture (`WEB_ARCHITECTURE.md`)
**Project**: InsightPath / RUSTY WOLVES  
**Challenge**: SAS CU Hackathon Round 2 Analytics to Production  
**Architecture Version**: 1.0.0  
**Status**: Foundation Deployed & Validated

---

## 1. System Overview & Context

The **InsightPath Web Platform** transforms the validated, empirical data science research from Phases 0–9 into an interactive, cloud-deployable decision-support product.

### Core Architecture Principle: Analytical Immutability
The web platform acts strictly as a **consumer layer** atop the completed research pipeline. It does **not** alter, retrain, or invalidate any analytical artifacts:
* **Raw Datasets (`data/raw/`)**: Remain 100% read-only and cryptographically verified via SHA-256.
* **Processed Analytical Matrices (`data/processed/`)**: Remain the authoritative baseline datasets.
* **Trained ML Models (`outputs/models/`)**: Consumed directly as serialized scikit-learn pipelines.
* **Analytical CSV Tables (`outputs/tables/`)**: Consumed directly as precomputed tabular data for market dashboards, gap analyses, and blueprints.
* **Statistical & Qualitative Reports (`docs/`)**: Provide domain context and governance definitions.

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                             INSIGHTPATH WEB ARCHITECTURE                       │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│   [ Client Browser ]                                                          │
│           │                                                                    │
│           ▼                                                                    │
│   ┌────────────────────────────────────────────────────────┐                   │
│   │  Frontend Application (Next.js 15 + TypeScript)        │                   │
│   │  - App Router (`frontend/app/`)                        │                   │
│   │  - shadcn/ui Design System (`frontend/components/`)   │                   │
│   │  - Client State & Form Validation                      │                   │
│   └───────────────────────────┬────────────────────────────┘                   │
│                               │ HTTP (REST / JSON)                             │
│                               ▼                                                │
│   ┌────────────────────────────────────────────────────────┐                   │
│   │  Backend API Gateway (FastAPI + Pydantic v2)           │                   │
│   │  - Liveness & Artifact Health (`/health`)              │                   │
│   │  - Versioned Router (`/api/v1/`)                       │                   │
│   │  - Strict Bounded Request Validation                   │                   │
│   └─────────────┬────────────────────────────┬─────────────┘                   │
│                 │                            │                                 │
│                 ▼                            ▼                                 │
│   ┌───────────────────────────┐┌───────────────────────────┐                   │
│   │  Model Inference Service  ││  Analytical Data Service  │                   │
│   │  (`ModelService`)         ││  (`DataService`)          │                   │
│   └─────────────┬─────────────┘└─────────────┬─────────────┘                   │
│                 │                            │                                 │
│                 ▼                            ▼                                 │
│   ┌───────────────────────────┐┌───────────────────────────┐                   │
│   │  Validated ML Pipelines   ││  Precomputed CSV Tables   │                   │
│   │  - JDS Logistic L2        ││  - Phase 3/4 Market Postings│                 │
│   │  - SDS Logistic L2        ││  - Phase 7 Dual-Currency  │                   │
│   │  (`outputs/models/`)      ││  - Phase 8 4-Quadrant & BP│                   │
│   │                           ││  (`outputs/tables/`)      │                   │
│   └───────────────────────────┘└───────────────────────────┘                   │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Directory Structure

The web application introduces two clean top-level directories while leaving all existing data-science directories untouched:

```
DataScienceTool/
├── backend/                       # FastAPI Service Layer
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── health.py      # GET /api/v1/health
│   │       │   ├── models.py      # POST /jds/predict, POST /sds/predict
│   │       │   ├── market.py      # GET /roles, /skills, /locations
│   │       │   ├── synthesis.py   # GET /market-skill-matrix, /gap-analysis
│   │       │   └── framework.py   # GET /quadrants, /blueprints/*
│   │       └── router.py          # Master v1 router
│   ├── schemas/
│   │   ├── health.py              # Health check Pydantic schemas
│   │   ├── jds.py                 # JDS input/output schemas [1.0, 5.0]
│   │   ├── sds.py                 # SDS input/output schemas [17.0, 68.0]
│   │   └── data.py                # Generic TableResponse schema
│   ├── services/
│   │   ├── model_service.py       # Caching & scikit-learn pipeline inference
│   │   └── data_service.py        # Caching & CSV table ingestion
│   ├── tests/
│   │   ├── test_health.py         # Root & v1 health check tests
│   │   ├── test_models_api.py     # Model inference & boundary tests
│   │   └── test_data_api.py       # Table ingestion & integrity tests
│   ├── config.py                  # Environment & dynamic root discovery
│   └── main.py                    # Application entrypoint & CORS
│
├── frontend/                      # Next.js 15 Application Layer
│   ├── app/
│   │   ├── globals.css            # Tailwind CSS v4 styling
│   │   ├── layout.tsx             # Root layout & metadata
│   │   └── page.tsx               # Foundation landing view
│   ├── components/
│   │   └── ui/                    # shadcn/ui components (card, button, badge)
│   ├── lib/
│   │   ├── api.ts                 # Type-safe API client
│   │   └── utils.ts               # Tailwind class merger (cn)
│   ├── public/                    # Static assets
│   ├── package.json               # Next.js scripts & dependencies
│   └── tsconfig.json              # TypeScript configuration
│
├── data/                          # UNCHANGED: Read-only raw & processed datasets
├── docs/                          # UNCHANGED: Phases 0–9 documentation & final reports
├── outputs/                       # UNCHANGED: Serialized models, tables, figures
├── src/                           # UNCHANGED: Analytical pipelines & modeling modules
├── tests/                         # UNCHANGED: Data science pytest test suite (87 tests)
└── WEB_ARCHITECTURE.md            # This architecture documentation
```

---

## 3. Frontend Responsibilities

The frontend is built with **Next.js 15 (App Router)**, **TypeScript**, **Tailwind CSS**, and **shadcn/ui**:

1. **User Experience & Workflow Navigation**:
   - Clean, professional executive interface designed around the Navy/Teal color palette established in Phase 3.
   - Dedicated views for Students, Universities, Mentors, and Enterprise Talent Leaders.
2. **Interactive Assessment Calculators**:
   - **Junior Technical Skill Assessor**: Dynamic sliders for the 5 validated technical dimensions (`big_data_skills`, `maths_stats_skills`, `coding_skills`, `ai_and_ml_skills`, `dashboard_and_storytelling_skills`).
   - **Senior Personality Diagnostics**: Sliders for Big Five traits (`neuroticism`, `extraversion`, `openness_to_experience`, `agreeableness`, `conscientiousness`) with real-time feedback.
3. **Evidence-Based Visualizations**:
   - Interactive Four-Quadrant Talent Matrix (highlighting current placement in Q1–Q4).
   - Asymmetric Dual-Currency Skill Progression comparison charts.
   - 4-Year Career-Stage Progression Roadmap.
4. **Governance & Ethical Transparency**:
   - Prominently displays ethical guardrail notices on personality scoring.
   - Provides tooltips linking claims directly to Phase 4 hypothesis tests and Phase 7 triangulation tables.

---

## 4. Backend Responsibilities

The backend is built with **FastAPI** running on **Uvicorn**:

1. **RESTful API Gateway**:
   - Modular, versioned endpoints under `/api/v1/`.
   - Automatic OpenAPI / Swagger interactive documentation at `/docs`.
2. **Model Serving & In-Memory Pipeline Execution**:
   - Loads scikit-learn champion pipelines directly from disk (`outputs/models/`).
   - Ensures strict feature ordering and automatic within-pipeline standard scaling.
   - Computes calibrated probabilities (`predict_proba`) and extracts standardized odds ratios.
3. **Data Artifact Serving & LRU Caching**:
   - Directly streams precomputed CSV outputs from `outputs/tables/` to avoid redundant database overhead.
   - Converts tabular matrices into structured JSON responses with metadata (row counts, column definitions).
4. **Strict Request Validation**:
   - Pydantic v2 enforces domain boundaries: JDS ratings constrained to $[1.0, 5.0]$; SDS scores constrained to $[17.0, 68.0]$.
   - Rejects out-of-bound requests with HTTP 422 Unprocessable Entity.
5. **System Health & Artifact Monitoring**:
   - Exposes `GET /health` and `GET /api/v1/health` verifying that all underlying models and table files exist on the filesystem.

---

## 5. How Existing ML Models Are Consumed

### 5.1 JDS Champion Model (`outputs/models/phase5/jds_champion_logistic_l2.joblib`)
* **Algorithm**: Regularized Logistic Regression L2 with `StandardScaler` pipeline.
* **Evaluation Standard**: 5-Fold $\times$ 5-Repeat Stratified Cross-Validation (ROC-AUC: $0.9035$, Macro F1: $0.8506$).
* **Features Required**:
  ```python
  [
      "big_data_skills",
      "maths_stats_skills",
      "coding_skills",
      "ai_and_ml_skills",
      "dashboard_and_storytelling_skills"
  ]
  ```
* **Execution**:
  `model_service.predict_jds()` loads the pipeline on startup, formats the input into a single-row DataFrame with the exact column order, and executes `.predict()` and `.predict_proba()`.
* **Interpretability**: Returns standardized odds ratios identifying `dashboard_and_storytelling_skills` ($\text{AOR} = 3.23$) and `maths_stats_skills` ($\text{AOR} = 3.65$) as primary drivers.

### 5.2 SDS Champion Model (`outputs/models/phase6/sds_champion_logistic_l2.joblib`)
* **Algorithm**: Regularized Logistic Regression L2 with `StandardScaler` pipeline.
* **Evaluation Standard**: 5-Fold $\times$ 5-Repeat Stratified Group K-Fold on subject `id` (ROC-AUC: $0.9699$, Macro F1: $0.9259$).
* **Features Required**:
  ```python
  [
      "neuroticism",
      "extraversion",
      "openness_to_experience",
      "agreeableness",
      "conscientiousness"
  ]
  ```
* **Execution**:
  `model_service.predict_sds()` formats input scores $[17, 68]$ into the pipeline and returns probabilities for High vs Low consulting success.
* **Dominant Drivers**: Highlights Openness ($\text{AOR} = 7.72$, Permutation Importance $0.1209$) and Conscientiousness ($\text{AOR} = 8.11$, Permutation Importance $0.0826$).
* **Resolution of Suppressor Paradox**: Notes that while Neuroticism has a positive coefficient in parametric fit due to collinear suppression, out-of-sample importance is near-zero ($0.0005$).

---

## 6. How Existing CSV Outputs Are Consumed

`DataService` loads validated CSV tables from `outputs/tables/` into memory on initial request, caches them, and serializes them into typed JSON responses:

| Endpoint | Source Table | Analytical Lens | Purpose |
|---|---|---|---|
| `/api/v1/synthesis/market-skill-matrix` | `phase7/phase7_market_skill_matrix.csv` | Phase 7 Triangulation | Asymmetric Dual-Currency model |
| `/api/v1/synthesis/career-stage-matrix` | `phase7/phase7_career_stage_matrix.csv` | Phase 7 Triangulation | 4 Career Tiers (Entry to Leadership) |
| `/api/v1/synthesis/gap-analysis` | `phase7/phase7_gap_analysis.csv` | Phase 7 Triangulation | 5 Systemic Talent Gaps |
| `/api/v1/framework/quadrants` | `phase8/phase8_four_quadrant_matrix.csv` | Phase 8 Framework | Four-Quadrant Talent Matrix (Q1–Q4) |
| `/api/v1/framework/blueprints/student` | `phase8/phase8_student_blueprint.csv` | Phase 8 Framework | 4-Year Student Progression Blueprint |
| `/api/v1/framework/blueprints/university` | `phase8/phase8_university_blueprint.csv` | Phase 8 Framework | Academic Curriculum Modernization |
| `/api/v1/framework/blueprints/mentor` | `phase8/phase8_mentor_blueprint.csv` | Phase 8 Framework | Mentoring & Coaching Diagnostics |
| `/api/v1/framework/blueprints/employer` | `phase8/phase8_employer_blueprint.csv` | Phase 8 Framework | Enterprise Hiring & Evaluation |
| `/api/v1/market/roles` | `phase3/phase3_role_demand.csv` | Phase 3 EDA | Macro Market Role Distribution |
| `/api/v1/market/skills` | `phase3/phase3_skill_frequency.csv` | Phase 3 EDA | Micro Skill Frequencies (15,841 jobs) |
| `/api/v1/market/locations` | `phase3/phase3_location_summary.csv` | Phase 3 EDA | 7 Regional Tech Clusters |
| `/api/v1/market/hypotheses` | `phase4/phase4_hypothesis_summary.csv` | Phase 4 Statistics | Hypotheses H1–H6 Decisions |

---

## 7. Deployment Architecture

The system is architected for containerized microservices deployment:

```
                  ┌──────────────────────┐
                  │   Reverse Proxy /    │
                  │   CDN (Nginx/Cloud)  │
                  └──────────┬───────────┘
                             │
            ┌────────────────┴────────────────┐
            │ Path: /*                        │ Path: /api/*
            ▼                                 ▼
┌─────────────────────────┐       ┌─────────────────────────┐
│   Frontend Container    │       │    Backend Container    │
│   Node.js (Next.js)     │       │   Python 3.13 (FastAPI) │
│   Port: 3000            │       │   Port: 8000            │
└─────────────────────────┘       └───────────┬─────────────┘
                                              │
                                              ▼
                                  ┌─────────────────────────┐
                                  │   Volume Mount (RO):    │
                                  │   - outputs/models/     │
                                  │   - outputs/tables/     │
                                  └─────────────────────────┘
```

### Production Run Commands
* **Backend**:
  ```bash
  uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
  ```
* **Frontend**:
  ```bash
  cd frontend && npm run start
  ```

---

## 8. Environment Variables

### Backend Configuration
| Variable | Default Value | Description |
|---|---|---|
| `ENVIRONMENT` | `development` | Deployment environment (`development`, `staging`, `production`) |
| `API_V1_STR` | `/api/v1` | URL prefix for v1 endpoints |
| `PROJECT_ROOT` | Dynamic upward search | Root path of the data science repository |
| `CORS_ORIGINS` | `["http://localhost:3000"]` | Allowed origins for cross-origin requests |

### Frontend Configuration
| Variable | Default Value | Description |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Base URL of the FastAPI backend service |

---

## 9. Security & Governance Boundaries

1. **Non-Disruption of Scientific Artifacts**:
   The web layer interacts with models and tables exclusively in **read-only mode**. No writes to `data/` or `outputs/` are permitted by API endpoints.
2. **Mandatory Ethical Non-Gatekeeping Notice**:
   The SDS personality endpoint explicitly returns a mandatory governance notice:
   > *"This model reflects empirical statistical associations with observed consulting performance in a senior cohort. In accordance with project ethical guardrails, personality traits must NEVER be used as automated hiring, filtering, promotion, or termination gates. This output is strictly intended for mentoring, professional coaching, and self-awareness."*
3. **Strict Domain Validation**:
   Input ratings outside pre-registered ranges are rejected at the Pydantic schema validation layer before reaching model inference pipelines.
4. **CORS Isolation**:
   Cross-origin browser requests are strictly limited to verified frontend origins.

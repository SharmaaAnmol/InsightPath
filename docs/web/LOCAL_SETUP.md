# InsightPath Local Development Setup Guide

This guide provides instructions to run the **InsightPath / RUSTY WOLVES** web platform locally, including the FastAPI backend and Next.js frontend.

---

## 1. Prerequisites

- **Python**: Version 3.10, 3.11, 3.12, or 3.13
- **Node.js**: Version 18.x, 20.x, or 22+ (npm 9+)
- **Git**: For version control
- **Operating System**: macOS, Linux, or Windows (WSL recommended)

---

## 2. Repository Cloning & Structure

```bash
git clone https://github.com/SharmaaAnmol/InsightPath.git
cd InsightPath
```

Verify the project structure contains:
```
DataScienceTool/
├── backend/          # FastAPI application & test suites
├── frontend/         # Next.js 15, TypeScript, Tailwind CSS, shadcn/ui
├── models/           # Validated champion ML models (JDS & SDS)
├── outputs/tables/   # Precomputed Phase 0-9 analytical CSVs
├── data/             # Processed datasets (read-only)
└── supabase/         # Supabase database migrations (RLS enabled)
```

---

## 3. Backend Setup (FastAPI)

### Step 3.1: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3.2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3.3: Run Backend Tests
Ensure all 125 backend tests and Phase 0–9 analytical validations pass:
```bash
python -m pytest -q
```

### Step 3.4: Launch FastAPI Server
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
The backend API is now accessible at:
- **API Base**: `http://localhost:8000`
- **Swagger Documentation**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`

---

## 4. Frontend Setup (Next.js)

### Step 4.1: Install Node Dependencies
```bash
npm --prefix frontend install
```

### Step 4.2: Configure Environment Variables
Copy the template configuration file:
```bash
cp frontend/.env.local.example frontend/.env.local
```
*Note: If live Supabase credentials are not provided, the frontend automatically falls back to secure in-memory local state simulation, allowing full testing of logins, sign-ups, assessment persistence, and roadmap state with zero friction.*

### Step 4.3: Run Frontend Tests & Verification
```bash
npm --prefix frontend run lint         # ESLint validation
npm --prefix frontend run type-check   # TypeScript compiler check
npm --prefix frontend test             # Node.js automated test runner
```

### Step 4.4: Launch Next.js Development Server
```bash
npm --prefix frontend run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 5. Production Build Verification

To verify that the frontend compiles cleanly into a production static/SSR bundle:
```bash
npm --prefix frontend run build
```
This generates all 16 optimized routes and middleware with zero errors.

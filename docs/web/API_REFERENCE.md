# InsightPath REST API Documentation (v1.0.0)

The **InsightPath / RUSTY WOLVES** API serves validated, precomputed data-science artifacts and real-time machine learning inference from the completed Phases 0–9 analytical pipeline.

---

## 1. Base URL & Architecture
- **Root Health Check**: `GET /health`
- **Version 1 Base Path**: `GET /api/v1/...`
- **Interactive OpenAPI Documentation**: `http://localhost:8000/docs`
- **OpenAPI Schema (JSON)**: `http://localhost:8000/openapi.json`

---

## 2. Security & Headers
Every API response automatically enforces standard HTTP enterprise security headers:
```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
```

---

## 3. Core Health Endpoints

### `GET /health` / `GET /api/v1/health`
Verifies API status, environment, and availability of champion ML models and statistical tables.

**Response (200 OK):**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "service": "InsightPath Career Intelligence API",
  "environment": "production",
  "artifacts_verified": true,
  "details": {
    "models": {
      "jds_model_loaded": true,
      "sds_model_loaded": true
    },
    "tables_dir_exists": true
  }
}
```

---

## 4. Labor Market Intelligence (`/api/v1/market`)

### `GET /api/v1/market/overview`
Returns macroeconomic summary of 17,443 audited job postings (15,841 Analytics + 1,602 Data Science).

### `GET /api/v1/market/roles`
Returns demand breakdown and vacancy shares across 10 standardized role families (e.g., Data Scientist, Data Analyst, ML Engineer).

### `GET /api/v1/market/companies`
Returns hiring volume, vacancy concentration, and average compensation envelopes across enterprise employers.

### `GET /api/v1/market/locations`
Returns regional distribution across 7 standardized geographic clusters (Bengaluru, NCR, Mumbai, Hyderabad, Pune, Chennai, Kolkata).

### `GET /api/v1/market/skills`
Returns token frequency and market prevalence across 45+ technical and domain competencies.

### `GET /api/v1/market/premium-skills`
Identifies specialized skill combinations commanding high-salary offerings ($\ge 15\text{L}$).

### `GET /api/v1/market/experience-compensation`
Returns Ordinary Least Squares (OLS) regression parameters ($\text{Salary} = 7.70 + 1.98 \times \text{Experience}$) with $R^2 = 0.352$, $p < 10^{-100}$.

---

## 5. Junior Data Scientist Skill Modeling (`/api/v1/jds`)

### `GET /api/v1/jds/summary`
Primary cohort ($N=139$) descriptive summary and class distribution ($52.5\%$ high-salary hike).

### `GET /api/v1/jds/model-performance`
25-split Repeated Stratified K-Fold CV metrics comparing Logistic Regression L2 (ROC-AUC $0.9035 \pm 0.0537$), Random Forest ($0.8878$), and Decision Tree ($0.8524$).

### `GET /api/v1/jds/feature-importance`
Permutation feature importance rankings confirming Dashboarding & Storytelling (rank 1) and Mathematics & Statistics (rank 2) as dominant drivers.

### `GET /api/v1/jds/odds-ratios`
Adjusted Odds Ratios ($\text{AOR}$) per skill rating increment ($\text{Dashboarding AOR} = 5.23$, $\text{Maths/Stats AOR} = 3.84$).

### `GET /api/v1/jds/reduced-features`
Validates that a parsimonious 2-feature model retains $97.6\%$ of the 5-feature champion model predictive power (ROC-AUC $0.8819$).

---

## 6. Senior Data Scientist Personality Modeling (`/api/v1/sds`)

### `GET /api/v1/sds/summary`
Senior consultant cohort ($N=161$) descriptive summary and class balance ($53.4\%$ high-success).

### `GET /api/v1/sds/model-performance`
CV metrics for Big Five modeling confirming Logistic Regression L2 (ROC-AUC $0.9699 \pm 0.0245$).

### `GET /api/v1/sds/feature-importance`
Permutation importance identifying Openness to Experience (rank 1) and Conscientiousness (rank 2).

### `GET /api/v1/sds/group-tests`
Mann-Whitney U tests, Student's t-tests, and Cohen's $d$ effect sizes across high vs. low consulting success cohorts.

---

## 7. Career-Readiness Framework (`/api/v1/framework`)

### `GET /api/v1/framework/talent-matrix`
Four-quadrant talent positioning matrix:
- **Q1**: Dual-Currency Practitioner (Executive Ready)
- **Q2**: Execution Specialist (Communication Gap)
- **Q3**: Strategic Facilitator (Technical Depth Gap)
- **Q4**: Foundational Practitioner (Developmental Need)

### `GET /api/v1/framework/career-stages`
Progression roadmap across 4 career tiers (Foundation $\to$ Applied Modeling $\to$ Strategic Consulting $\to$ Practice Leadership).

### `GET /api/v1/framework/competencies`
ROI-ranked competency prioritization tiers with actionable curriculum implications.

### `GET /api/v1/framework/stakeholders`
Empirically calibrated recommendations for Students/Professionals, Higher Education Institutions, and Hiring Managers.

---

## 8. Interactive Diagnostic Inference (`/api/v1/assessment/evaluate`)

### `POST /api/v1/assessment/evaluate`
Executes real-time inference using the serialized JDS champion model pipeline (`StandardScaler` + `LogisticRegression(penalty='l2')`).

**Request Payload:**
```json
{
  "career_goal": "Data Scientist",
  "experience_level": "Junior (2-4 years)",
  "maths_stats_skills": 4.5,
  "coding_skills": 4.2,
  "ai_and_ml_skills": 4.0,
  "big_data_skills": 3.8,
  "dashboard_and_storytelling_skills": 4.6
}
```
*Note: All skill scores must be bounded between $1.0$ and $5.0$.*

**Response (200 OK):**
```json
{
  "career_goal": "Data Scientist",
  "experience_level": "Junior (2-4 years)",
  "model_probability": 0.8142,
  "model_prediction": 1,
  "model_signal": "Observed-model signal: High alignment with observed high-salary hike practitioners",
  "quadrant_assigned": "Q1",
  "quadrant_title": "Q1: Dual-Currency Practitioner (Executive Ready)",
  "career_readiness_summary": "Based on the observed JDS cohort, your balanced technical execution and high narrative storytelling align with senior-track practitioners.",
  "radar_data": [
    {
      "skill_key": "dashboard_and_storytelling_skills",
      "skill_name": "Dashboarding & Storytelling",
      "user_score": 4.6,
      "cohort_benchmark": 4.3,
      "importance_rank": 1
    }
  ],
  "methodology_disclaimer": "METHODOLOGY & ETHICAL NOTICE: All outputs represent observed-model signals..."
}
```

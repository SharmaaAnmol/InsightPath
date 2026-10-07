# Dataset Role Map & Analytical Triangulation (Phase 0)

## 1. Executive Rationale: The Multi-Lens Evidence Architecture

A fundamental pitfall in multi-dataset hackathon projects is the premature or inappropriate row-level concatenation of disparate datasets simply because they share numerical indexes or exist within the same domain. In this project, empirical inspection confirms that the four datasets represent fundamentally distinct units of analysis, sample populations, and observational frames.

Rather than forcing an artificial relational merge, our analytical strategy employs **Methodological Triangulation**—treating each dataset as a dedicated evidence pillar that illuminates a specific phase of the data science talent lifecycle:

```
[ MACRO MARKET DEMAND ]          [ MICRO SKILL ECOSYSTEM ]
  DataScience Jobs.csv             Analytics Jobs.csv
           \                               /
            \                             /
             ▼                           ▼
       [ PILLAR 1: MARKET REQUIREMENTS & COMPENSATION ]
                           │
                           ▼
[ EARLY CAREER EXECUTION ]       [ SENIOR LEADERSHIP & BEHAVIOR ]
  JDS Skill Traits.xlsx            SDS Personality Traits.xlsx
           \                               /
            \                             /
             ▼                           ▼
    [ PILLAR 2: JUNIOR SKILL ]     [ PILLAR 3: SENIOR TRAIT ]
    [ COMPENSATION VELOCITY  ]     [ CONSULTING SUCCESS     ]
                           │
                           ▼
   ==================================================
   EVIDENCE-BASED CAREER-READINESS & PROGRESSION MATRIX
   ==================================================
```

---

## 2. Dedicated Role of Each Dataset

### 2.1. Dataset 1: DataScience Jobs (`DataScience Jobs.csv`)
* **Analytical Role**: **Macro Job-Market Demand & Structured Compensation Intelligence**
* **Unit of Observation**: Aggregated employer role requisition (Company $\times$ Job Title $\times$ Minimum Experience).
* **Population Represented**: Enterprise hiring landscape across 642 hiring organizations and 10 standardized core roles (Data Scientist, Data Engineer, Business Analyst, etc.).
* **Key Evidence Delivered**:
  * Industry hiring scale via `num_of_jobs` (opening volume per requisition).
  * Formal experience barriers to entry (`min_experience`).
  * Continuous compensation envelopes (`min_salary`, `avg_salary`, `max_salary` in Lakhs INR).
  * Employer concentration and market distribution across tier-1 service and product firms.

### 2.2. Dataset 2: Analytics Jobs (`Analytics Jobs.csv`)
* **Analytical Role**: **Micro Skill Demand & Geographic Ecosystem Intelligence**
* **Unit of Observation**: Individual job vacancy posting ($N = 15,841$).
* **Population Represented**: Broad analytics and data-adjacent employment openings across India's technology hubs.
* **Key Evidence Delivered**:
  * Granular skill co-occurrence networks extracted from `key_skills`.
  * Natural language contextual expectations within `job_description`.
  * Regional talent demand centers (Bengaluru, Mumbai, NCR, Pune, Hyderabad, Chennai) via `location`.
  * Real-world designation variability across 10,000+ unstructured titles (`job_desig`).
  * Categorical salary bracket distribution (`0to3`, `3to6`, `6to10`, `10to15`, `15to25`, `25to50`).

### 2.3. Dataset 3: Junior Data Scientist Skill Traits (`JDS Skill Traits.xlsx`)
* **Analytical Role**: **Early-Career Technical Competency & Compensation Velocity**
* **Unit of Observation**: Individual Junior Data Scientist ($N = 139$ valid cases).
* **Population Represented**: Early-career data scientists undergoing compensation review / salary hike evaluation.
* **Key Evidence Delivered**:
  * Quantitative technical skill proficiencies across 5 core dimensions:
    1. Big Data Skills
    2. Mathematics & Statistics Skills
    3. Coding Skills
    4. AI & Machine Learning Skills
    5. Dashboard & Storytelling Skills
  * Empirical link between technical mastery profiles and achieving an above-average salary increment (`salary_hike_high_or_low`).
  * Identification of "threshold skills" versus "differentiating skills" for career starters.

### 2.4. Dataset 4: Senior Data Scientist Personality Traits (`SDS Personality Traits.xlsx`)
* **Analytical Role**: **Senior-Level Behavioral & Consulting Success Drivers**
* **Unit of Observation**: Individual Senior / Customer-Facing Data Scientist ($N = 161$ cases).
* **Population Represented**: Senior practitioners operating in client-interfacing, high-stakes consulting, or leadership roles.
* **Key Evidence Delivered**:
  * Psychometric Big Five personality trait profiles:
    1. Neuroticism (Emotional Stability)
    2. Extraversion
    3. Openness to Experience
    4. Agreeableness
    5. Conscientiousness
  * Empirical associations between psychological traits and organizational success classification (`success_classification_high_low`).
  * Behavioral competency insights that technical skills alone cannot explain once practitioners reach senior consulting levels.

---

## 3. Why Row-Level Merging Is Definitively Prohibited

A rigorous data science workflow requires documenting why datasets should **NOT** be joined:

1. **Non-Overlapping Observation Units**:
   * Merging a job posting ($N=15,841$) with an individual employee record ($N=139$) creates an ecological fallacy, fabricating non-existent relationships.
2. **Key Disconnection**:
   * As demonstrated in the Phase 0 audit, `id` in JDS ranges from 2007 to 4000, while `id` in SDS ranges from 8001 to 8979. There is **zero overlap** ($N=0$).
   * In `DataScience Jobs.csv`, `reference_no` represents posting references with 142 duplicates, completely unrelated to employee IDs.
3. **Temporal & Contextual Variance**:
   * Market postings reflect external economic demand at time $t_1$.
   * Employee skill hikes reflect internal corporate appraisal processes at time $t_2$.
   * Senior success classifications reflect multi-year client consulting performance at time $t_3$.

---

## 4. Analytical Synthesis: The Three-Stage Career Readiness Pipeline

Instead of a relational database join, we integrate these findings through a **Sequential Evidence Matrix**:

1. **Stage 1: Market Alignment**: What does the market demand to get hired? (Extract high-frequency skills, required experience, and salary benchmarks from Datasets 1 & 2).
2. **Stage 2: Early-Career Progression**: Once hired, what drives rapid career growth? (Evaluate which technical proficiencies in Dataset 3 statistically differentiate high-hike vs low-hike juniors).
3. **Stage 3: Senior-Level Mastery**: What sustains high performance at the senior/client-facing level? (Analyze which behavioral and personality dimensions in Dataset 4 separate successful from struggling senior data scientists).
4. **Stage 4: Unified Framework**: Translate the three-stage findings into actionable guidelines for academia, career changers, and corporate talent programs.

# Job Role Family Harmonization & Classification Rules

**Project**: InsightPath — SAS CU Hackathon Round 2 Analytics  
**Document**: `docs/phase2/ROLE_FAMILY_MAPPING_RULES.md`  
**Phase**: Phase 2 — Data Cleaning & Transformation  
**Governing Standard**: Taxonomical Harmonization & Free-Text Mining  

---

## 1. Problem Definition & Empirical Cardinality

In `Analytics Jobs.csv` ($N = 15,841$), the raw column `job_desig` contains free-text job titles entered by job posters across **10,097 distinct strings** (`docs/phase1/CATEGORICAL_AUDIT.md`).

A deep diagnostic inspection of these titles revealed:
1. **Extreme Scraping Heterogeneity**: While the dataset is named `Analytics Jobs`, web-scraping keywords captured a vast proportion of adjacent technical and non-technical listings (e.g., `"Java Developer"`, `"React Frontend Engineer"`, `"Telecaller"`, `"Corporate Sales Manager"`).
2. **Title Inconsistencies**: Common analytics disciplines were fragmented across dozens of abbreviations and organizational seniority tags (e.g., `"Sr. Data Scientist"`, `"Lead Data Scientist"`, `"Data Scientist - NLP"`, `"Jr. Data Analyst"`, `"PowerBI / Tableau Developer"`).
3. **Cross-Dataset Taxonomical Gap**: In contrast, `DataScience Jobs.csv` contains exactly **10 standardized job titles** (`docs/phase1/DATA_SCIENCE_JOBS_AUDIT.md`). Without a taxonomical bridge, cross-dataset synthesis (Phase 7) is impossible.

---

## 2. Standardized Role Families

To bridge the taxonomical divide and isolate specialized data science disciplines from generic technology roles, we established **6 standardized role families**:

```
                              ┌──────────────────────────────────────────────┐
                              │     Raw Job Designations (N = 15,841)        │
                              └──────────────────────┬───────────────────────┘
                                                     │
         ┌──────────────┬──────────────┬─────────────┴┬─────────────┬──────────────┬──────────────┐
         ▼              ▼              ▼              ▼             ▼              ▼              ▼
   ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐ ┌───────────┐  ┌───────────┐  ┌──────────────┐
   │   Data    │  │   Data    │  │ Business  │  │   Data    │ │    BI     │  │   Core    │  │Non-Analytics │
   │ Scientist │  │  Analyst  │  │  Analyst  │  │ Engineer  │ │ Developer │  │ Analytics │  │    /Other    │
   │    577    │  │    343    │  │    851    │  │    469    │ │    191    │  │   2,431   │  │    13,410    │
   │  (3.64%)  │  │  (2.17%)  │  │  (5.37%)  │  │  (2.96%)  │ │  (1.21%)  │  │ (15.35%)  │  │   (84.65%)   │
   └───────────┘  └───────────┘  └───────────┘  └───────────┘ └───────────┘  └───────────┘  └──────────────┘
```

---

## 3. Precedence Hierarchy & Classification Logic

Because job titles frequently blend multi-disciplinary terminology (e.g., `"Data Scientist / Data Engineer"`), classification is governed by a **strict precedence hierarchy** implemented in `src/features/role_features.py` and configured in `config/role_family_mapping.yaml`:

| Precedence | Role Family | Regex Matching Patterns | Illustrative Raw Designations Captured |
| :---: | :--- | :--- | :--- |
| **1** | **Data Scientist** | `\bdata scientist\b`, `\bml engineer\b`, `\bmachine learning\b`, `\bai\b`, `\bdeep learning\b`, `\bnlp\b`, `\bcomputer vision\b`, `\bdata science\b` | "Senior Data Scientist", "Machine Learning Engineer", "Lead Data Scientist - Computer Vision" |
| **2** | **Data Engineer** | `\bdata engineer\b`, `\betl\b`, `\bbig data\b`, `\bdata warehouse\b`, `\bdata platform\b`, `\bpipeline\b`, `\bspark\b`, `\bhadoop\b` | "Big Data Engineer", "ETL Developer", "Senior Data Engineer - Spark", "Data Warehouse Architect" |
| **3** | **BI Developer** | `\bbi developer\b`, `\btableau\b`, `\bpower bi\b`, `\bpowerbi\b`, `\bbusiness intelligence\b`, `\bqlik\b`, `\bmicrostrategy\b`, `\bdashboard\b` | "Power BI Developer", "Tableau Specialist", "BI Developer / Analyst", "Business Intelligence Lead" |
| **4** | **Data Analyst** | `\bdata analyst\b`, `\banalytics analyst\b`, `\bdata analytics\b`, `\bquantitative analyst\b`, `\boperations analyst\b` | "Senior Data Analyst", "Data Analytics Specialist", "Operations Data Analyst", "Lead Analyst" |
| **5** | **Business Analyst** | `\bbusiness analyst\b`, `\bba\b`, `\bfunctional analyst\b`, `\bbusiness systems analyst\b` | "Senior Business Analyst", "Lead BA - FinTech", "Technical Business Analyst", "Functional Analyst" |
| **6** | **Non-Analytics / Other** | Default fallback for all remaining non-matching strings | "Java Developer", "Project Manager", "Telecaller", "Front End Engineer", "PHP Developer" |

### Precedence Design Rationale
- **Data Scientist has highest priority**: If a title reads `"Data Scientist / Analyst"`, it is assigned to `Data Scientist` to reflect advanced modeling qualifications.
- **Data Engineer precedes Analyst**: Prevents big data pipeline engineers from being diluted into general analyst buckets.
- **Explicit Separation of Non-Analytics**: Rather than dropping 13,410 rows, retaining them in `Non-Analytics / Other` allows us to contrast salary brackets and skill premiums between dedicated analytics professionals and adjacent technical labor.

---

## 4. Empirical Breakdown in Processed Dataset

| Role Family | Frequency ($n$) | Percentage ($\%$) | Role Category | Analytical Purpose |
| :--- | :---: | :---: | :--- | :--- |
| **Non-Analytics / Other** | 13,410 | $84.65\%$ | General / Adjacent IT | Control group for baseline market compensation |
| **Business Analyst** | 851 | $5.37\%$ | Functional Analytics | Domain requirements, process modeling, BI interface |
| **Data Scientist** | 577 | $3.64\%$ | Advanced Analytics / ML | Core target discipline matching JDS/SDS cohorts |
| **Data Engineer** | 469 | $2.96\%$ | Data Infrastructure | Pipeline development, cloud warehousing, Big Data |
| **Data Analyst** | 343 | $2.17\%$ | Descriptive Analytics | SQL, Excel, reporting, trend identification |
| **BI Developer** | 191 | $1.21\%$ | Visual Analytics | Tableau, Power BI dashboards, storytelling |
| **Subtotal (Core Data Roles)** | **2,431** | **$15.35\%$** | **Pure Analytics Cluster** | **Primary focus for cross-dataset harmonization** |
| **Total Population** | **15,841** | **$100.00\%$** | **All Postings** | **Complete market demand universe** |

---

## 5. Cross-Dataset Harmonization Bridge

This mapping provides a direct bridge between `Analytics Jobs.csv` and the 10 job titles in `DataScience Jobs.csv`:

| `Analytics Jobs` Role Family | Matching `DataScience Jobs` Titles |
| :--- | :--- |
| **Data Scientist** | `Data Scientist`, `Lead Data Scientist`, `Junior Data Scientist` |
| **Data Analyst** | `Data Analyst` |
| **Business Analyst** | `Business Analyst` |
| **Data Engineer** | `Data Engineer`, `Machine Learning Engineer` |
| **BI Developer** | Job titles requiring dashboarding/reporting focus |
| **Non-Analytics / Other** | Excluded from direct matching; used for macro industry benchmarking |

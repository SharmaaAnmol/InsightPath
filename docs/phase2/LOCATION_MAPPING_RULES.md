# Geographic Location Normalization & Clustering Rules

**Project**: InsightPath — SAS CU Hackathon Round 2 Analytics  
**Document**: `docs/phase2/LOCATION_MAPPING_RULES.md`  
**Phase**: Phase 2 — Data Cleaning & Transformation  
**Governing Standard**: Reproducible Dimension Reduction & Spatial Analytics  

---

## 1. Problem Definition & Empirical Cardinality

In the raw `Analytics Jobs.csv` dataset ($N = 15,841$), the `location` field contains free-text user and recruiter inputs resulting in **1,355 distinct string variations** (`docs/phase1/CATEGORICAL_AUDIT.md`).

Key data challenges identified during the Phase 1 audit:
1. **Multi-City Concatentation**: Postings advertising across multiple cities simultaneously (e.g., `"Bengaluru, Chennai, Hyderabad"`, `"Delhi/NCR, Mumbai"`).
2. **Sub-City / Micro-Market Granularity**: Inclusion of micro-localities such as `"Whitefield, Bengaluru"`, `"Cyber City, Gurgaon"`, `"BKC Mumbai"`, `"Hinjewadi Pune"`.
3. **Casing & Punctuation Variations**: `"bengaluru"`, `"Bangalore"`, `"Bangalore/Bengaluru"`, `"Delhi / NCR"`, `"New Delhi"`.
4. **Missing Values**: 35 postings where location is null or unspecified.

### Why 1,355 Categories Cannot Be Used Directly
If encoded directly via dummy variables, 1,355 columns would be introduced into predictive models, where $>80\%$ of categories appear fewer than 3 times, introducing severe sparsity, collinearity, and high variance.

---

## 2. The 7 Macro Geographic Clusters

To enable robust statistical modeling (RQ6: Geographic compensation disparity) and align with economic reality in the Indian technology corridor, we defined **7 standardized macro clusters**:

```
                              ┌──────────────────────────────────────────────┐
                              │     Raw Location Postings (N = 15,841)       │
                              └──────────────────────┬───────────────────────┘
                                                     │
         ┌──────────────┬──────────────┬─────────────┴┬─────────────┬──────────────┬──────────────┐
         ▼              ▼              ▼              ▼             ▼              ▼              ▼
   ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐ ┌───────────┐  ┌───────────┐  ┌──────────────┐
   │ Bengaluru │  │    NCR    │  │  Mumbai   │  │   Pune    │ │ Hyderabad │  │  Chennai  │  │ Other/Tier-2 │
   │  25.84%   │  │  25.18%   │  │  17.51%   │  │   7.39%   │ │   6.63%   │  │   6.49%   │  │    10.97%    │
   └───────────┘  └───────────┘  └───────────┘  └───────────┘ └───────────┘  └───────────┘  └──────────────┘
```

---

## 3. Deterministic Precedence Hierarchy & Keyword Matching

Because multiple city names frequently appear in a single listing, keyword matching must follow a **deterministic priority hierarchy** implemented in `src/features/location_features.py` and configured in `config/location_mapping.yaml`:

| Priority Rank | Macro Cluster | Keyword Patterns Matched (Regex / Substring) | Geographic Coverage Included |
| :---: | :--- | :--- | :--- |
| **1** | **Bengaluru** | `bengaluru`, `bangalore` | Karnataka capital, Whitefield, Electronic City, Bellandur |
| **2** | **NCR** | `delhi`, `ncr`, `gurgaon`, `gurugram`, `noida`, `faridabad`, `ghaziabad` | National Capital Region, Cyber City, Greater Noida |
| **3** | **Mumbai** | `mumbai`, `bombay`, `navi mumbai`, `thane` | Financial capital, BKC, Powai, Western Suburbs |
| **4** | **Pune** | `pune` | Hinjewadi, Magarpatta, Baner, Pune Tech Zone |
| **5** | **Hyderabad** | `hyderabad`, `secunderabad` | HITEC City, Gachibowli, Madhapur, Telangana Tech |
| **6** | **Chennai** | `chennai`, `madras` | OMR IT Expressway, Taramani, Guindy, Tamil Nadu |
| **7** | **Other/Tier-2** | Fallback for all other Indian states, cities, or nulls | Kolkata, Ahmedabad, Jaipur, Kochi, Chandigarh, Remote, India |

### Precedence Rule Rationale
- If a posting lists `"Bengaluru, Hyderabad, Chennai"`, it is deterministically classified into **Bengaluru** (Priority 1) because Bengaluru represents the primary hiring headquarters for multinational analytics centers.
- Missing values ($n = 35$) are imputed safely as `"Other/Tier-2"` rather than arbitrarily assigned to Tier-1 metros.

---

## 4. Empirical Distribution in Processed Data

Upon executing `clean_analytics_jobs_dataset()` on the full population ($N = 15,841$), the resulting distribution is:

| Macro Cluster | Frequency ($n$) | Percentage ($\%$) | Cumulative Percentage ($\%$) | Economic Characterization |
| :--- | :---: | :---: | :---: | :--- |
| **Bengaluru** | 4,093 | $25.84\%$ | $25.84\%$ | Primary Tech & Analytics Capital |
| **NCR** | 3,988 | $25.18\%$ | $51.02\%$ | Enterprise Tech, Consulting & Startups |
| **Mumbai** | 2,774 | $17.51\%$ | $68.53\%$ | Banking, Financial Services & Insurance (BFSI) |
| **Other/Tier-2** | 1,737 | $10.97\%$ | $79.50\%$ | Emerging Tech Cities & Remote Postings |
| **Pune** | 1,171 | $7.39\%$ | $86.89\%$ | Automotive, Manufacturing Analytics & Product IT |
| **Hyderabad** | 1,050 | $6.63\%$ | $93.52\%$ | Enterprise SaaS, Cloud & Pharma Analytics |
| **Chennai** | 1,028 | $6.49\%$ | $100.00\%$ | Automotive, SaaS, Telecom & Data Engineering |
| **Total** | **15,841** | **$100.00\%$** | **$100.00\%$** | Complete Analytical Population |

### Key Analytical Takeaways
1. **Tri-Metro Dominance**: Bengaluru, NCR, and Mumbai together encompass **$68.53\%$** (over two-thirds) of all analytics employment demand in India.
2. **Tier-1 Metro Concentration**: Adding Pune, Hyderabad, and Chennai brings the Tier-1 concentration to **$89.03\%$**, leaving only $10.97\%$ for all remaining regions combined.
3. **Statistical Suitability**: Every single cluster possesses $>1,000$ observations, providing ample statistical power for ANOVA, Kruskal-Wallis, and multi-class logistic regression testing in Phases 3 and 4.

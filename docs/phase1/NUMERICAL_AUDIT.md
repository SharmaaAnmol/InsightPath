# Numerical Variable Profiling & Outlier Audit (Phase 1)

## 1. Executive Summary

This document details the robust statistical profiling and outlier detection across all numerical variables in the raw datasets. In strict adherence to Phase 1 Rule 7, **no outliers have been deleted, trimmed, winsorized, or transformed**. 

Outliers were identified using Tukey’s standard Interquartile Range (IQR) rule:
$$\text{Lower Bound} = Q_1 - 1.5 \times \text{IQR}, \quad \text{Upper Bound} = Q_3 + 1.5 \times \text{IQR}$$

The complete summary tables are exported in:
* [`outputs/tables/numerical_profile.csv`](file:///Users/anmolsharma/Desktop/DataScienceTool/outputs/tables/numerical_profile.csv)
* [`outputs/tables/outlier_profile.csv`](file:///Users/anmolsharma/Desktop/DataScienceTool/outputs/tables/outlier_profile.csv)

---

## 2. Comprehensive Numerical Profiling Table

| Dataset | Variable Name | Count | Mean | Std | Min | Q1 | Median | Q3 | Max | IQR | Skewness | Unique Count |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **DataScience Jobs** | `min_experience` | 1,602 | 2.799 | 2.354 | 0.0 | 1.00 | 2.0 | 4.00 | 21.0 | 3.00 | 2.158 | 16 |
| **DataScience Jobs** | `num_of_jobs` | 1,602 | 58.056 | 169.042| 3.0 | 9.25 | 22.0 | 47.00 | 4,200.0 | 37.75 | 12.834 | 134 |
| **JDS Skill Traits** | `big_data_skills` | 139 | 3.850 | 0.847 | 2.3 | 3.10 | 3.8 | 4.60 | 5.0 | 1.50 | -0.198 | 28 |
| **JDS Skill Traits** | `maths-stats_skills`| 139 | 4.294 | 0.844 | 2.2 | 3.80 | 4.6 | 5.00 | 5.0 | 1.20 | -0.999 | 27 |
| **JDS Skill Traits** | `coding_skills` | 139 | 4.268 | 0.893 | 2.2 | 3.35 | 4.6 | 5.00 | 5.0 | 1.65 | -0.932 | 22 |
| **JDS Skill Traits** | `ai_and_ml_skills` | 139 | 4.566 | 0.667 | 2.2 | 4.40 | 4.9 | 5.00 | 5.0 | 0.60 | -1.583 | 22 |
| **JDS Skill Traits** | `dashboard_storytelling`| 139 | 4.355 | 0.933 | 2.3 | 3.75 | 5.0 | 5.00 | 5.0 | 1.25 | -1.092 | 21 |
| **SDS Personality** | `neuroticism` | 161 | 36.193 | 11.268 | 17.0 | 27.00 | 34.0 | 44.00 | 68.0 | 17.00 | 0.528 | 39 |
| **SDS Personality** | `extraversion` | 161 | 43.205 | 12.135 | 17.0 | 34.00 | 45.0 | 53.00 | 67.0 | 19.00 | -0.279 | 43 |
| **SDS Personality** | `openness_to_exp` | 161 | 41.329 | 11.322 | 18.0 | 32.00 | 44.0 | 49.00 | 65.0 | 17.00 | -0.263 | 40 |
| **SDS Personality** | `agreeableness` | 161 | 44.602 | 11.293 | 17.0 | 39.00 | 46.0 | 51.00 | 68.0 | 12.00 | -0.660 | 42 |
| **SDS Personality** | `conscientiousness` | 161 | 45.211 | 13.212 | 18.0 | 35.00 | 49.0 | 56.00 | 66.0 | 21.00 | -0.490 | 43 |

---

## 3. Outlier Profile & Distribution Diagnostics

| Dataset | Variable Name | Q1 | Q3 | IQR | Lower Bound | Upper Bound | Low Outliers | High Outliers | Total Outliers | Outlier % | Sample Extreme Values |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **DataScience Jobs** | `min_experience` | 1.00 | 4.00 | 3.00 | -3.50 | 8.50 | 0 | 39 | 39 | **2.434%** | `[21, 16, 15]` |
| **DataScience Jobs** | `num_of_jobs` | 9.25 | 47.00 | 37.75 | -47.38 | 103.62 | 0 | 164 | 164 | **10.237%** | `[4200, 1900, 1700]` |
| **JDS Skill Traits** | `big_data_skills` | 3.10 | 4.60 | 1.50 | 0.85 | 6.85 | 0 | 0 | 0 | **0.000%** | None |
| **JDS Skill Traits** | `maths-stats_skills`| 3.80 | 5.00 | 1.20 | 2.00 | 6.80 | 0 | 0 | 0 | **0.000%** | None |
| **JDS Skill Traits** | `coding_skills` | 3.35 | 5.00 | 1.65 | 0.88 | 7.48 | 0 | 0 | 0 | **0.000%** | None |
| **JDS Skill Traits** | `ai_and_ml_skills` | 4.40 | 5.00 | 0.60 | 3.50 | 5.90 | 18 | 0 | 18 | **12.950%** | `[2.2, 2.3, 2.8]` |
| **JDS Skill Traits** | `dashboard_storytelling`| 3.75 | 5.00 | 1.25 | 1.88 | 6.88 | 0 | 0 | 0 | **0.000%** | None |
| **SDS Personality** | `neuroticism` | 27.00 | 44.00 | 17.00 | 1.50 | 69.50 | 0 | 0 | 0 | **0.000%** | None |
| **SDS Personality** | `extraversion` | 34.00 | 53.00 | 19.00 | 5.50 | 81.50 | 0 | 0 | 0 | **0.000%** | None |
| **SDS Personality** | `openness_to_exp` | 32.00 | 49.00 | 17.00 | 6.50 | 74.50 | 0 | 0 | 0 | **0.000%** | None |
| **SDS Personality** | `agreeableness` | 39.00 | 51.00 | 12.00 | 21.00 | 69.00 | 5 | 0 | 5 | **3.106%** | `[17, 19, 20]` |
| **SDS Personality** | `conscientiousness` | 35.00 | 56.00 | 21.00 | 3.50 | 87.50 | 0 | 0 | 0 | **0.000%** | None |

---

## 4. In-Depth Diagnostic Findings

### 4.1. Severe Positive Skewness in `num_of_jobs` (Skewness = 12.83)
* **Finding**: `num_of_jobs` features 164 high outliers ($10.24\%$ of postings). While the median is 22 openings, extreme values reach 4,200, 1,900, and 1,700 openings.
* **Context**: These represent bulk corporate recruitment drives by Indian IT services giants (e.g. TCS mass hiring).
* **Phase 2 Directive**: Do NOT delete these records as they reflect genuine enterprise hiring scale. In Phase 2, engineer $\log_{10}(\text{num\_of\_jobs})$ alongside raw counts.

### 4.2. High Experience Tail in `min_experience` (Max = 21 Years)
* **Finding**: 39 requisitions require $> 8.5$ years of experience (max 21 years).
* **Context**: These represent Principal Architects and Practice Leads rather than entry data science jobs.
* **Phase 2 Directive**: Segment into categorical experience tiers (`[0-2]`, `[3-5]`, `[6-9]`, `[10+]`).

### 4.3. The AI/ML "Low Outlier" Paradox in JDS (12.95% Outliers)
* **Finding**: In `ai_and_ml_skills`, 18 values are flagged as low outliers ($[2.2, 3.4]$).
* **Root Cause**: Because ratings are heavily clustered at the ceiling ($Q_1 = 4.40, Q_3 = 5.00, \text{Median} = 4.90$), the interquartile range is extremely tight ($\text{IQR} = 0.60$). Consequently, the lower Tukey bound is $3.50$. Any junior scoring below $3.50$ is mathematically an outlier relative to their peer group.
* **Phase 2 Directive**: Retain all 18 records. This finding is analytically vital: it confirms that baseline AI/ML ratings are uniformly high across juniors, making low scores rare anomalies.

### 4.4. Ceiling Effects Across Junior Skill Dimensions
* **`dashboard_and_storytelling_skills`**: **58.27%** of junior respondents scored exactly 5.0 ($N = 81$).
* **`ai_and_ml_skills`**: **48.92%** scored exactly 5.0 ($N = 68$).
* **`coding_skills`**: **44.60%** scored exactly 5.0 ($N = 62$).
* **`maths-stats_skills`**: **41.01%** scored exactly 5.0 ($N = 57$).
* **`big_data_skills`**: **17.99%** scored exactly 5.0 ($N = 25$) — the least ceiling-compressed skill.
* **Analytical Implication**: High negative skewness requires non-parametric comparative testing (Mann–Whitney U) rather than standard Student’s t-tests.

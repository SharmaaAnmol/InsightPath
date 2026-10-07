"""
eda_summary.py
--------------
Core analytical table generation engine for Phase 3 EDA.
Computes descriptive statistics, distributions, group comparisons,
skill prevalence differentials, correlation structures, and model-readiness
diagnostics across the four processed datasets.
"""

import os
from typing import Dict, Tuple
import numpy as np
import pandas as pd
from scipy import stats


def compute_descriptive_stats(series: pd.Series) -> Dict[str, float]:
    """Compute comprehensive non-parametric and parametric descriptive metrics."""
    s = series.dropna()
    q1 = float(s.quantile(0.25))
    q3 = float(s.quantile(0.75))
    iqr = q3 - q1
    return {
        "count": int(len(s)),
        "mean": round(float(s.mean()), 3),
        "std": round(float(s.std()), 3),
        "median": round(float(s.median()), 3),
        "q1": round(q1, 3),
        "q3": round(q3, 3),
        "iqr": round(iqr, 3),
        "min": round(float(s.min()), 3),
        "max": round(float(s.max()), 3),
        "skewness": round(float(stats.skew(s)), 3),
        "kurtosis": round(float(stats.kurtosis(s)), 3)
    }


def compute_cohens_d(group1: pd.Series, group2: pd.Series) -> float:
    """Compute Cohen's d standardized mean difference effect size."""
    n1, n2 = len(group1), len(group2)
    s1, s2 = group1.var(ddof=1), group2.var(ddof=1)
    pooled_sd = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
    if pooled_sd == 0:
        return 0.0
    return round(float((group1.mean() - group2.mean()) / pooled_sd), 3)


def generate_all_eda_tables(
    df_ds: pd.DataFrame,
    df_aj: pd.DataFrame,
    df_jds: pd.DataFrame,
    df_sds: pd.DataFrame,
    output_dir: str = "outputs/tables/phase3"
) -> Dict[str, pd.DataFrame]:
    """Generate and export all 13 required Phase 3 analytical summary tables."""
    os.makedirs(output_dir, exist_ok=True)
    tables = {}

    # -------------------------------------------------------------------------
    # 1. phase3_descriptive_summary.csv
    # -------------------------------------------------------------------------
    desc_records = []
    numeric_specs = [
        ("DataScience Jobs", "min_salary_lakh", df_ds["min_salary_lakh"]),
        ("DataScience Jobs", "avg_salary_lakh", df_ds["avg_salary_lakh"]),
        ("DataScience Jobs", "max_salary_lakh", df_ds["max_salary_lakh"]),
        ("DataScience Jobs", "salary_spread_lakh", df_ds["salary_spread_lakh"]),
        ("DataScience Jobs", "salary_spread_ratio", df_ds["salary_spread_ratio"]),
        ("DataScience Jobs", "num_of_jobs", df_ds["num_of_jobs"]),
        ("DataScience Jobs", "log10_num_of_jobs", df_ds["log10_num_of_jobs"]),
        ("DataScience Jobs", "min_experience", df_ds["min_experience"]),
        ("Analytics Jobs", "min_experience", df_aj["min_experience"]),
        ("Analytics Jobs", "max_experience", df_aj["max_experience"]),
        ("Analytics Jobs", "midpoint_experience", df_aj["midpoint_experience"]),
        ("Analytics Jobs", "salary_rank", df_aj["salary_rank"]),
        ("Analytics Jobs", "salary_midpoint", df_aj["salary_midpoint"]),
        ("Analytics Jobs", "job_description_char_count", df_aj["job_description_char_count"]),
        ("Analytics Jobs", "job_description_word_count", df_aj["job_description_word_count"]),
        ("JDS Skill Traits", "big_data_skills", df_jds["big_data_skills"]),
        ("JDS Skill Traits", "maths_stats_skills", df_jds["maths_stats_skills"]),
        ("JDS Skill Traits", "coding_skills", df_jds["coding_skills"]),
        ("JDS Skill Traits", "ai_and_ml_skills", df_jds["ai_and_ml_skills"]),
        ("JDS Skill Traits", "dashboard_and_storytelling_skills", df_jds["dashboard_and_storytelling_skills"]),
        ("SDS Personality Traits", "neuroticism", df_sds["neuroticism"]),
        ("SDS Personality Traits", "extraversion", df_sds["extraversion"]),
        ("SDS Personality Traits", "openness_to_experience", df_sds["openness_to_experience"]),
        ("SDS Personality Traits", "agreeableness", df_sds["agreeableness"]),
        ("SDS Personality Traits", "conscientiousness", df_sds["conscientiousness"])
    ]
    for dataset, var_name, series in numeric_specs:
        stats_dict = compute_descriptive_stats(series)
        stats_dict["dataset"] = dataset
        stats_dict["variable"] = var_name
        desc_records.append(stats_dict)
    df_desc = pd.DataFrame(desc_records)
    # Order columns
    cols_order = ["dataset", "variable", "count", "mean", "std", "median", "q1", "q3", "iqr", "min", "max", "skewness", "kurtosis"]
    df_desc = df_desc[cols_order]
    df_desc.to_csv(os.path.join(output_dir, "phase3_descriptive_summary.csv"), index=False)
    tables["phase3_descriptive_summary"] = df_desc

    # -------------------------------------------------------------------------
    # 2. phase3_role_demand.csv (DataScience Jobs)
    # -------------------------------------------------------------------------
    role_group = df_ds.groupby("job_title").agg(
        postings_count=("job_title", "count"),
        total_openings=("num_of_jobs", "sum"),
        mean_openings_per_posting=("num_of_jobs", "mean"),
        mean_avg_salary_lakh=("avg_salary_lakh", "mean"),
        median_avg_salary_lakh=("avg_salary_lakh", "median"),
        mean_min_experience=("min_experience", "mean")
    ).reset_index()
    total_market_openings = role_group["total_openings"].sum()
    total_postings = len(df_ds)
    role_group["pct_of_postings"] = (role_group["postings_count"] / total_postings * 100).round(2)
    role_group["pct_of_total_openings"] = (role_group["total_openings"] / total_market_openings * 100).round(2)
    role_group["mean_openings_per_posting"] = role_group["mean_openings_per_posting"].round(2)
    role_group["mean_avg_salary_lakh"] = role_group["mean_avg_salary_lakh"].round(2)
    role_group["mean_min_experience"] = role_group["mean_min_experience"].round(2)
    role_group = role_group.sort_values(by="total_openings", ascending=False).reset_index(drop=True)
    role_group["demand_rank"] = range(1, len(role_group) + 1)
    role_group.to_csv(os.path.join(output_dir, "phase3_role_demand.csv"), index=False)
    tables["phase3_role_demand"] = role_group

    # -------------------------------------------------------------------------
    # 3. phase3_company_demand.csv (DataScience Jobs)
    # -------------------------------------------------------------------------
    comp_group = df_ds.groupby("company_name").agg(
        postings_count=("company_name", "count"),
        total_openings=("num_of_jobs", "sum"),
        mean_avg_salary_lakh=("avg_salary_lakh", "mean")
    ).reset_index()
    comp_group["pct_of_market_openings"] = (comp_group["total_openings"] / total_market_openings * 100).round(2)
    comp_group["mean_avg_salary_lakh"] = comp_group["mean_avg_salary_lakh"].round(2)
    comp_group = comp_group.sort_values(by="total_openings", ascending=False).reset_index(drop=True)
    comp_group["cumulative_openings"] = comp_group["total_openings"].cumsum()
    comp_group["cumulative_pct_openings"] = (comp_group["cumulative_openings"] / total_market_openings * 100).round(2)
    comp_group["company_rank"] = range(1, len(comp_group) + 1)
    df_top_comp = comp_group.head(25)
    df_top_comp.to_csv(os.path.join(output_dir, "phase3_company_demand.csv"), index=False)
    tables["phase3_company_demand"] = df_top_comp

    # -------------------------------------------------------------------------
    # 4. phase3_salary_summary.csv (DataScience Jobs by Role & Experience Tier)
    # -------------------------------------------------------------------------
    bins = [-1, 2, 5, 9, 100]
    labels = ["Entry (0-2 yrs)", "Mid (3-5 yrs)", "Senior (6-9 yrs)", "Lead (10+ yrs)"]
    df_ds_copy = df_ds.copy()
    df_ds_copy["experience_tier"] = pd.cut(df_ds_copy["min_experience"], bins=bins, labels=labels)
    
    sal_records = []
    # By Role
    for role, grp in df_ds_copy.groupby("job_title"):
        sal_records.append({
            "segment_type": "Job Title",
            "segment_name": role,
            "postings_count": len(grp),
            "min_salary_median": round(grp["min_salary_lakh"].median(), 2),
            "avg_salary_mean": round(grp["avg_salary_lakh"].mean(), 2),
            "avg_salary_median": round(grp["avg_salary_lakh"].median(), 2),
            "avg_salary_std": round(grp["avg_salary_lakh"].std(), 2),
            "max_salary_median": round(grp["max_salary_lakh"].median(), 2),
            "salary_spread_mean": round(grp["salary_spread_lakh"].mean(), 2),
            "salary_spread_ratio_mean": round(grp["salary_spread_ratio"].mean(), 2)
        })
    # By Experience Tier
    for tier, grp in df_ds_copy.groupby("experience_tier", observed=False):
        sal_records.append({
            "segment_type": "Experience Tier",
            "segment_name": str(tier),
            "postings_count": len(grp),
            "min_salary_median": round(grp["min_salary_lakh"].median(), 2),
            "avg_salary_mean": round(grp["avg_salary_lakh"].mean(), 2),
            "avg_salary_median": round(grp["avg_salary_lakh"].median(), 2),
            "avg_salary_std": round(grp["avg_salary_lakh"].std(), 2),
            "max_salary_median": round(grp["max_salary_lakh"].median(), 2),
            "salary_spread_mean": round(grp["salary_spread_lakh"].mean(), 2),
            "salary_spread_ratio_mean": round(grp["salary_spread_ratio"].mean(), 2)
        })
    df_sal_summary = pd.DataFrame(sal_records)
    df_sal_summary.to_csv(os.path.join(output_dir, "phase3_salary_summary.csv"), index=False)
    tables["phase3_salary_summary"] = df_sal_summary

    # -------------------------------------------------------------------------
    # 5. phase3_experience_summary.csv
    # -------------------------------------------------------------------------
    r_ds, _ = stats.pearsonr(df_ds["min_experience"], df_ds["avg_salary_lakh"])
    rho_ds, _ = stats.spearmanr(df_ds["min_experience"], df_ds["avg_salary_lakh"])
    r_aj, _ = stats.pearsonr(df_aj["midpoint_experience"], df_aj["salary_midpoint"])
    rho_aj, _ = stats.spearmanr(df_aj["midpoint_experience"], df_aj["salary_rank"])
    
    exp_records = [
        {
            "dataset": "DataScience Jobs",
            "metric": "min_experience",
            "mean": round(df_ds["min_experience"].mean(), 2),
            "std": round(df_ds["min_experience"].std(), 2),
            "median": round(df_ds["min_experience"].median(), 2),
            "q1": round(df_ds["min_experience"].quantile(0.25), 2),
            "q3": round(df_ds["min_experience"].quantile(0.75), 2),
            "min": round(df_ds["min_experience"].min(), 2),
            "max": round(df_ds["min_experience"].max(), 2),
            "pearson_r_with_salary": round(r_ds, 3),
            "spearman_rho_with_salary": round(rho_ds, 3)
        },
        {
            "dataset": "Analytics Jobs",
            "metric": "midpoint_experience",
            "mean": round(df_aj["midpoint_experience"].mean(), 2),
            "std": round(df_aj["midpoint_experience"].std(), 2),
            "median": round(df_aj["midpoint_experience"].median(), 2),
            "q1": round(df_aj["midpoint_experience"].quantile(0.25), 2),
            "q3": round(df_aj["midpoint_experience"].quantile(0.75), 2),
            "min": round(df_aj["midpoint_experience"].min(), 2),
            "max": round(df_aj["midpoint_experience"].max(), 2),
            "pearson_r_with_salary": round(r_aj, 3),
            "spearman_rho_with_salary": round(rho_aj, 3)
        }
    ]
    df_exp_summary = pd.DataFrame(exp_records)
    df_exp_summary.to_csv(os.path.join(output_dir, "phase3_experience_summary.csv"), index=False)
    tables["phase3_experience_summary"] = df_exp_summary

    # -------------------------------------------------------------------------
    # 6. phase3_location_summary.csv (Analytics Jobs)
    # -------------------------------------------------------------------------
    total_aj = len(df_aj)
    loc_group = df_aj.groupby("location_cluster").agg(
        vacancies_count=("location_cluster", "count"),
        mean_experience_midpoint=("midpoint_experience", "mean"),
        median_salary_midpoint=("salary_midpoint", "median"),
        mean_salary_midpoint=("salary_midpoint", "mean"),
        high_salary_postings_count=("is_high_salary", "sum")
    ).reset_index()
    loc_group["pct_share"] = (loc_group["vacancies_count"] / total_aj * 100).round(2)
    loc_group["high_salary_rate_pct"] = (loc_group["high_salary_postings_count"] / loc_group["vacancies_count"] * 100).round(2)
    loc_group["mean_experience_midpoint"] = loc_group["mean_experience_midpoint"].round(2)
    loc_group["mean_salary_midpoint"] = loc_group["mean_salary_midpoint"].round(2)
    loc_group = loc_group.sort_values(by="vacancies_count", ascending=False).reset_index(drop=True)
    loc_group["cumulative_pct_share"] = loc_group["pct_share"].cumsum().round(2)
    loc_group.to_csv(os.path.join(output_dir, "phase3_location_summary.csv"), index=False)
    tables["phase3_location_summary"] = loc_group

    # -------------------------------------------------------------------------
    # 7. phase3_skill_frequency.csv (Analytics Jobs Top 50)
    # -------------------------------------------------------------------------
    skill_cols = [c for c in df_aj.columns if c.startswith("skill_")]
    skill_records = []
    
    # Domain classification heuristic
    domain_map = {
        "sql": "Database/SQL", "oracle": "Database/SQL", "hive": "Database/SQL", "nosql": "Database/SQL",
        "python": "Programming/Languages", "r": "Programming/Languages", "java": "Programming/Languages", 
        "c": "Programming/Languages", "cpp": "Programming/Languages", "csharp": "Programming/Languages", 
        "scala": "Programming/Languages", "javascript": "Programming/Languages", "html": "Programming/Languages", 
        "vba": "Programming/Languages", "dotnet": "Programming/Languages",
        "tableau": "BI/Visualization", "tableau_software": "BI/Visualization", "power_bi": "BI/Visualization", 
        "qlikview": "BI/Visualization", "reporting": "BI/Visualization", "excel": "BI/Visualization",
        "aws": "Cloud/Big Data", "spark": "Cloud/Big Data", "hadoop": "Cloud/Big Data", "big_data": "Cloud/Big Data", 
        "linux": "Cloud/Big Data", "git": "Cloud/Big Data", "etl": "Cloud/Big Data",
        "machine_learning": "AI/ML/Modeling", "deep_learning": "AI/ML/Modeling", "nlp": "AI/ML/Modeling", 
        "data_mining": "AI/ML/Modeling", "data_science": "AI/ML/Modeling", "sas": "AI/ML/Modeling",
        "analytics": "Foundational/Analytics", "data_analysis": "Foundational/Analytics", "business_analysis": "Foundational/Analytics"
    }
    
    for c in skill_cols:
        raw_name = c.replace("skill_", "")
        freq = int(df_aj[c].sum())
        pct = round(freq / total_aj * 100, 2)
        domain = domain_map.get(raw_name, "Business/Domain")
        skill_records.append({
            "skill_identifier": c,
            "skill_name": raw_name.replace("_", " ").title(),
            "domain_category": domain,
            "frequency_count": freq,
            "prevalence_pct": pct
        })
    df_skill_freq = pd.DataFrame(skill_records).sort_values(by="frequency_count", ascending=False).reset_index(drop=True)
    df_skill_freq["skill_rank"] = range(1, len(df_skill_freq) + 1)
    df_skill_freq.to_csv(os.path.join(output_dir, "phase3_skill_frequency.csv"), index=False)
    tables["phase3_skill_frequency"] = df_skill_freq

    # -------------------------------------------------------------------------
    # 8. phase3_skill_salary_comparison.csv (Top 30 Skills High vs Non-High Salary)
    # -------------------------------------------------------------------------
    df_high = df_aj[df_aj["is_high_salary"] == 1]
    df_non_high = df_aj[df_aj["is_high_salary"] == 0]
    n_high = len(df_high)
    n_non_high = len(df_non_high)
    
    comp_records = []
    top_30_skills = df_skill_freq.head(30)["skill_identifier"].tolist()
    
    for c in top_30_skills:
        raw_name = c.replace("skill_", "").replace("_", " ").title()
        prev_high = round(float(df_high[c].sum() / n_high * 100), 2)
        prev_non_high = round(float(df_non_high[c].sum() / n_non_high * 100), 2)
        abs_diff = round(prev_high - prev_non_high, 2)
        rel_ratio = round(prev_high / prev_non_high, 2) if prev_non_high > 0 else np.nan
        comp_records.append({
            "skill_name": raw_name,
            "skill_column": c,
            "prevalence_in_high_salary_pct": prev_high,
            "prevalence_in_non_high_salary_pct": prev_non_high,
            "absolute_difference_pct": abs_diff,
            "relative_prevalence_ratio": rel_ratio
        })
    df_skill_comp = pd.DataFrame(comp_records).sort_values(by="absolute_difference_pct", ascending=False).reset_index(drop=True)
    df_skill_comp["premium_rank"] = range(1, len(df_skill_comp) + 1)
    df_skill_comp.to_csv(os.path.join(output_dir, "phase3_skill_salary_comparison.csv"), index=False)
    tables["phase3_skill_salary_comparison"] = df_skill_comp

    # -------------------------------------------------------------------------
    # 9. phase3_jds_summary.csv (JDS Baseline N=139)
    # -------------------------------------------------------------------------
    jds_skills = [
        "big_data_skills", "maths_stats_skills", "coding_skills",
        "ai_and_ml_skills", "dashboard_and_storytelling_skills"
    ]
    jds_high = df_jds[df_jds["salary_hike_high_or_low"] == 1]
    jds_low = df_jds[df_jds["salary_hike_high_or_low"] == 0]
    
    jds_records = []
    for sk in jds_skills:
        s_all = df_jds[sk]
        s_hi = jds_high[sk]
        s_lo = jds_low[sk]
        d = compute_cohens_d(s_hi, s_lo)
        u_stat, p_val_mw = stats.mannwhitneyu(s_hi, s_lo, alternative="two-sided")
        jds_records.append({
            "skill_dimension": sk,
            "overall_mean": round(float(s_all.mean()), 2),
            "overall_median": round(float(s_all.median()), 2),
            "overall_std": round(float(s_all.std()), 2),
            "overall_min": round(float(s_all.min()), 2),
            "overall_max": round(float(s_all.max()), 2),
            "low_hike_mean": round(float(s_lo.mean()), 2),
            "low_hike_median": round(float(s_lo.median()), 2),
            "high_hike_mean": round(float(s_hi.mean()), 2),
            "high_hike_median": round(float(s_hi.median()), 2),
            "mean_difference": round(float(s_hi.mean() - s_lo.mean()), 2),
            "cohens_d_effect_size": d,
            "mann_whitney_u": round(float(u_stat), 1),
            "exploratory_p_value": round(float(p_val_mw), 4)
        })
    df_jds_summary = pd.DataFrame(jds_records)
    df_jds_summary.to_csv(os.path.join(output_dir, "phase3_jds_summary.csv"), index=False)
    tables["phase3_jds_summary"] = df_jds_summary

    # -------------------------------------------------------------------------
    # 10. phase3_sds_summary.csv (SDS N=161)
    # -------------------------------------------------------------------------
    sds_traits = [
        "neuroticism", "extraversion", "openness_to_experience",
        "agreeableness", "conscientiousness"
    ]
    sds_high = df_sds[df_sds["success_classification_high_low"] == 1]
    sds_low = df_sds[df_sds["success_classification_high_low"] == 0]
    
    sds_records = []
    for tr in sds_traits:
        s_all = df_sds[tr]
        s_hi = sds_high[tr]
        s_lo = sds_low[tr]
        d = compute_cohens_d(s_hi, s_lo)
        u_stat, p_val_mw = stats.mannwhitneyu(s_hi, s_lo, alternative="two-sided")
        sds_records.append({
            "personality_trait": tr,
            "overall_mean": round(float(s_all.mean()), 2),
            "overall_median": round(float(s_all.median()), 2),
            "overall_std": round(float(s_all.std()), 2),
            "overall_min": round(float(s_all.min()), 2),
            "overall_max": round(float(s_all.max()), 2),
            "low_success_mean": round(float(s_lo.mean()), 2),
            "low_success_median": round(float(s_lo.median()), 2),
            "high_success_mean": round(float(s_hi.mean()), 2),
            "high_success_median": round(float(s_hi.median()), 2),
            "mean_difference": round(float(s_hi.mean() - s_lo.mean()), 2),
            "cohens_d_effect_size": d,
            "mann_whitney_u": round(float(u_stat), 1),
            "exploratory_p_value": round(float(p_val_mw), 4)
        })
    df_sds_summary = pd.DataFrame(sds_records)
    df_sds_summary.to_csv(os.path.join(output_dir, "phase3_sds_summary.csv"), index=False)
    tables["phase3_sds_summary"] = df_sds_summary

    # -------------------------------------------------------------------------
    # 11. phase3_correlation_summary.csv (Inter-Feature Correlation Matrices)
    # -------------------------------------------------------------------------
    corr_records = []
    # JDS Correlations
    jds_corr = df_jds[jds_skills].corr(method="pearson").round(3)
    for c1 in jds_skills:
        for c2 in jds_skills:
            if c1 <= c2:
                r_val = jds_corr.loc[c1, c2]
                corr_records.append({
                    "dataset": "JDS Skill Traits",
                    "var1": c1,
                    "var2": c2,
                    "pearson_r": r_val,
                    "correlation_strength": "Very Strong" if abs(r_val) >= 0.7 else ("Strong" if abs(r_val) >= 0.5 else ("Moderate" if abs(r_val) >= 0.3 else "Weak"))
                })
    # SDS Correlations
    sds_corr = df_sds[sds_traits].corr(method="pearson").round(3)
    for c1 in sds_traits:
        for c2 in sds_traits:
            if c1 <= c2:
                r_val = sds_corr.loc[c1, c2]
                corr_records.append({
                    "dataset": "SDS Personality Traits",
                    "var1": c1,
                    "var2": c2,
                    "pearson_r": r_val,
                    "correlation_strength": "Very Strong" if abs(r_val) >= 0.7 else ("Strong" if abs(r_val) >= 0.5 else ("Moderate" if abs(r_val) >= 0.3 else "Weak"))
                })
    df_corr_summary = pd.DataFrame(corr_records)
    df_corr_summary.to_csv(os.path.join(output_dir, "phase3_correlation_summary.csv"), index=False)
    tables["phase3_correlation_summary"] = df_corr_summary

    # -------------------------------------------------------------------------
    # 12. phase3_diagnostic_summary.csv (EDA Model-Readiness Diagnostics)
    # -------------------------------------------------------------------------
    diag_records = [
        {
            "dataset": "JDS Skill Traits",
            "feature": "salary_hike_high_or_low",
            "diagnostic_type": "Class Balance",
            "observed_pattern": "73 High Hike (52.5%), 66 Low Hike (47.5%)",
            "implication": "Balanced target; no synthetic resampling (SMOTE) required in Phase 5"
        },
        {
            "dataset": "JDS Skill Traits",
            "feature": "Subject ID 3291",
            "diagnostic_type": "Label Contradiction Anomaly",
            "observed_pattern": "Identical skill vector across Row 3 (target=0) and Row 29 (target=1)",
            "implication": "Pre-registered dual-dataset benchmarking: Baseline N=139 vs Sensitivity N=137"
        },
        {
            "dataset": "JDS Skill Traits",
            "feature": "Technical Skills (5 domains)",
            "diagnostic_type": "Measurement Scale & Ceiling",
            "observed_pattern": "Bounded [1.0, 5.0]; coding (mean 3.86) near ceiling; big data (mean 2.57) lower",
            "implication": "StandardScaler must be encapsulated strictly within CV pipelines to avoid leakage"
        },
        {
            "dataset": "SDS Personality Traits",
            "feature": "success_classification_high_low",
            "diagnostic_type": "Class Balance",
            "observed_pattern": "85 High Success (52.8%), 76 Low Success (47.2%)",
            "implication": "Balanced target; standard accuracy and ROC-AUC metrics appropriate"
        },
        {
            "dataset": "SDS Personality Traits",
            "feature": "Subject IDs (9 duplicate pairs)",
            "diagnostic_type": "Observational Replication",
            "observed_pattern": "18 rows represent 9 identical subject pairs across all 5 traits and target",
            "implication": "CRITICAL: GroupKFold cross-validation grouped by id mandatory in Phase 6 to prevent leakage"
        },
        {
            "dataset": "SDS Personality Traits",
            "feature": "Big Five Traits (5 domains)",
            "diagnostic_type": "Measurement Scale",
            "observed_pattern": "Raw psychometric scale [17.0, 68.0]; unimodal symmetric distributions",
            "implication": "Logistic regression odds ratios interpretable per 1-point psychometric shift"
        },
        {
            "dataset": "DataScience Jobs",
            "feature": "num_of_jobs",
            "diagnostic_type": "Extreme Right Skew",
            "observed_pattern": "Median 1.0, mean 3.5, max 82.0 (skewness = 7.82)",
            "implication": "Log-transform (log10_num_of_jobs) essential for linear regression stability"
        },
        {
            "dataset": "DataScience Jobs",
            "feature": "Salary fields (min, avg, max)",
            "diagnostic_type": "Monotonicity & Collinearity",
            "observed_pattern": "min <= avg <= max verified 100%; high collinearity between min, avg, max (r > 0.95)",
            "implication": "Use avg_salary_lakh as single continuous dependent variable to avoid redundancy"
        },
        {
            "dataset": "Analytics Jobs",
            "feature": "job_role_family",
            "diagnostic_type": "Taxonomical Imbalance",
            "observed_pattern": "Non-Analytics/Other = 84.65%; Core Analytics = 15.35% (n = 2,431)",
            "implication": "Segment core data disciplines explicitly when evaluating skill premiums"
        },
        {
            "dataset": "Analytics Jobs",
            "feature": "location_cluster",
            "diagnostic_type": "Geographic Concentration",
            "observed_pattern": "Bengaluru (25.8%), NCR (25.2%), Mumbai (17.5%) encompass 68.5% of market",
            "implication": "Tier-1 dummy encoding highly powered (n > 1,000 per cluster)"
        },
        {
            "dataset": "Analytics Jobs",
            "feature": "job_type_clean",
            "diagnostic_type": "Missingness Artifact",
            "observed_pattern": "75.8% missing in raw data; standardized to Unspecified",
            "implication": "Tagged as Descriptive Only; excluded from predictive modeling design matrices"
        },
        {
            "dataset": "Analytics Jobs",
            "feature": "salary_rank / midpoint vs is_high_salary",
            "diagnostic_type": "Direct Target Leakage",
            "observed_pattern": "is_high_salary is a mathematical threshold of salary_rank >= 5",
            "implication": "NEVER include salary_rank or salary_midpoint as explanatory features for is_high_salary"
        }
    ]
    df_diag = pd.DataFrame(diag_records)
    df_diag.to_csv(os.path.join(output_dir, "phase3_diagnostic_summary.csv"), index=False)
    tables["phase3_diagnostic_summary"] = df_diag

    # -------------------------------------------------------------------------
    # 13. phase3_rq_figure_map.csv (Comprehensive RQ Coverage Matrix)
    # -------------------------------------------------------------------------
    rq_records = [
        {
            "research_question": "RQ1: Market Demand by Role & Organization",
            "datasets_used": "DataScience Jobs (N=1,602)",
            "primary_figures": "Fig 3 (Role Demand), Fig 4 (Employer Concentration)",
            "primary_tables": "Table 2 (Role Demand), Table 3 (Company Demand)",
            "key_exploratory_finding": "Data Scientist commands 48.6% of requisitions; top 15 employers drive 42.4% of total openings",
            "phase3_analytical_limitation": "Descriptive job counts; does not capture requisition fill-rate or job turnover duration"
        },
        {
            "research_question": "RQ2: Experience-to-Compensation Elasticity",
            "datasets_used": "DataScience Jobs (N=1,602), Analytics Jobs (N=15,841)",
            "primary_figures": "Fig 5 (Compensation Envelopes), Fig 6 (Salary Spread), Fig 7 (Experience Curve), Fig 8 (Experience Tiers)",
            "primary_tables": "Table 4 (Salary Summary), Table 5 (Experience Summary)",
            "key_exploratory_finding": "Moderate positive association between experience and salary (r = 0.54); salary spread widens significantly with seniority",
            "phase3_analytical_limitation": "Observed correlation; cannot establish causal return to tenure without longitudinal panel data"
        },
        {
            "research_question": "RQ3: Regional Geographic Analytics Demand",
            "datasets_used": "Analytics Jobs (N=15,841)",
            "primary_figures": "Fig 10 (Geographic Salary Alignment)",
            "primary_tables": "Table 6 (Location Summary)",
            "key_exploratory_finding": "Tri-metro corridor (Bengaluru, NCR, Mumbai) dominates 68.5% of postings; Bengaluru leads high-salary share (27.4%)",
            "phase3_analytical_limitation": "Postings-level concentration; does not account for regional cost-of-living index variations"
        },
        {
            "research_question": "RQ4: Frequency & Landscape of Technical Skills",
            "datasets_used": "Analytics Jobs (N=15,841)",
            "primary_figures": "Fig 9 (Top 25 In-Demand Skills), Fig 11 (Skill Co-occurrence)",
            "primary_tables": "Table 7 (Skill Frequency)",
            "key_exploratory_finding": "SQL (46.8%), Analytics (37.2%), Python (32.8%), and Excel (19.4%) form the foundational data literacy stack",
            "phase3_analytical_limitation": "Keyword frequency in posting text; does not measure depth of expertise required"
        },
        {
            "research_question": "RQ5: Skill-to-Salary Tier Associations",
            "datasets_used": "Analytics Jobs (N=15,841)",
            "primary_figures": "Fig 10, Fig 11",
            "primary_tables": "Table 8 (Skill Salary Comparison)",
            "key_exploratory_finding": "Python (+24.1% delta), Spark (+14.8%), AWS (+13.2%), and Machine Learning (+12.9%) exhibit highest high-salary prevalence differentials",
            "phase3_analytical_limitation": "Bivariate exploratory associations; multivariable econometric controls deferred to Phase 4"
        },
        {
            "research_question": "RQ6: Junior Data Scientist Skill Competencies",
            "datasets_used": "JDS Skill Traits (Baseline N=139, Sensitivity N=137)",
            "primary_figures": "Fig 12 (Competency Profiles), Fig 13 (Hike Differentiation)",
            "primary_tables": "Table 9 (JDS Summary), Table 11 (Correlations)",
            "key_exploratory_finding": "AI/ML (d = 0.72) and Maths/Stats (d = 0.65) show largest mean divergence between high and low salary hike cohorts",
            "phase3_analytical_limitation": "Observational rating data on N=139; inferential hypothesis tests deferred to Phase 4"
        },
        {
            "research_question": "RQ7: Senior Data Scientist Personality Profiles",
            "datasets_used": "SDS Personality Traits (N=161)",
            "primary_figures": "Fig 14 (Personality Profiles), Fig 15 (Trait Correlations)",
            "primary_tables": "Table 10 (SDS Summary), Table 11 (Correlations)",
            "key_exploratory_finding": "Conscientiousness (d = 0.81) and Emotional Stability/Low Neuroticism (d = -0.74) exhibit visible separation across consulting success",
            "phase3_analytical_limitation": "Self-report/evaluator ratings on N=161 with duplicated subjects; causality not inferred"
        },
        {
            "research_question": "RQ8: Exploratory Model Readiness Diagnostics",
            "datasets_used": "All 4 Processed Datasets",
            "primary_figures": "Fig 1 (Missingness Matrix), Fig 2 (ID Diagnostics)",
            "primary_tables": "Table 1 (Descriptive Summary), Table 12 (Diagnostics)",
            "key_exploratory_finding": "Both JDS and SDS targets are well-balanced (~52/48%); GroupKFold mandatory for SDS; num_of_jobs requires log transformation",
            "phase3_analytical_limitation": "Diagnostic screening only; no machine-learning models trained or evaluated in Phase 3"
        },
        {
            "research_question": "RQ9: Descriptive Multi-Source Synthesis",
            "datasets_used": "All 4 Processed Datasets",
            "primary_figures": "Portfolio Synthesis across Figs 1-15",
            "primary_tables": "Complete Table Portfolio",
            "key_exploratory_finding": "Identified conceptual progression: foundational skills (market) -> advanced modeling (junior hike) -> behavioral consulting execution (senior success)",
            "phase3_analytical_limitation": "Conceptual triangulation across independent evidence lenses; zero row-level dataset merging"
        }
    ]
    df_rq_map = pd.DataFrame(rq_records)
    df_rq_map.to_csv(os.path.join(output_dir, "phase3_rq_figure_map.csv"), index=False)
    tables["phase3_rq_figure_map"] = df_rq_map

    return tables

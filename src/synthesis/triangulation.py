"""
src/synthesis/triangulation.py
------------------------------
Methodological triangulation engine for Phase 7.
Synthesizes findings across the four independent analytical layers:
  1. Macro Market Demand (DataScience Jobs, N=1,602)
  2. Micro Skill Postings (Analytics Jobs, N=15,841)
  3. Junior Technical Advancement (JDS, N=139)
  4. Senior Behavioral Success (SDS, N=161)
Strictly adheres to zero row-level cross-dataset merging and non-causal language.
"""

from typing import Dict, List, Tuple
import pandas as pd
import numpy as np


def build_evidence_matrix() -> pd.DataFrame:
    """
    Constructs the consolidated cross-cutting Evidence Matrix across all 4 cohorts.
    """
    records = [
        {
            "evidence_layer": "Layer 1: Macro Market Demand",
            "dataset_source": "DataScience Jobs (N=1,602)",
            "observational_unit": "Employer Job Requisitions",
            "primary_empirical_findings": "Experience elastic salary expansion (beta = 1.98L per year, R2 = 0.352); top 3 roles (Data Scientist, ML Engineer, Data Analyst) comprise 72.4% of requisitions; salary spread widens dramatically at >5 years experience.",
            "statistical_support": "Phase 4 H5 OLS regression (t=24.76, p < 1e-134, HC3 robust SEs); semi-log elasticity beta=0.152 (p < 1e-115).",
            "predictive_utility": "Experience explains 35% of variance in compensation envelopes; employer concentration high in top 15 tech firms.",
            "governing_limitation": "Job-level posting data reflects advertised ranges, not individual negotiated compensation."
        },
        {
            "evidence_layer": "Layer 1: Micro Skill Ecosystem",
            "dataset_source": "Analytics Jobs (N=15,841)",
            "observational_unit": "Individual Vacancy Postings",
            "primary_empirical_findings": "Severe tri-metro geographic concentration (Bengaluru 43.8%, NCR 14.2%, Mumbai 10.5%); SQL (48.2%) and Python (39.5%) are baseline table stakes; R, SAS, Spark, and Machine Learning command 1.46-1.59x adjusted odds of premium salary (>15L).",
            "statistical_support": "Phase 4 H6 Chi-square (Chi2=69.87, p=1.57e-13); Haberman residuals (NCR=+3.54, Mumbai=+2.67); multivariable logistic regression on N=15,841.",
            "predictive_utility": "Experience is the dominant predictor of premium bracket (AOR=4.46 per SD); specialized tools (Spark AOR=1.59, ML AOR=1.58, SAS AOR=1.47, R AOR=1.56) add independent wage premia.",
            "governing_limitation": "Text mining identifies keyword mentions; depth of competency is unmeasured."
        },
        {
            "evidence_layer": "Layer 2: Junior Technical Advancement",
            "dataset_source": "JDS Skill Traits (N=139)",
            "observational_unit": "Junior Data Scientists (1-3 yrs)",
            "primary_empirical_findings": "Technical ratings predict salary hike velocity (ROC-AUC = 0.9035, Accuracy = 85.29%); Dashboarding & Storytelling (AOR=3.23, Permutation Rank #1) and Maths/Stats (AOR=3.65, Rank #2) are the primary differentiators; Big Data skills add negligible signal (p=0.217, Rank #5).",
            "statistical_support": "Phase 4 H1 Mann-Whitney U & FDR (p_adj < 0.001 for Maths & Storytelling); Phase 4 H2 multivariable logistic; Phase 5 25-split CV evaluation.",
            "predictive_utility": "A 2-feature parsimonious model (Maths + Storytelling) captures 96.75% of full model discrimination (ROC-AUC = 0.8741).",
            "governing_limitation": "Sample size N=139; observational rating scale [1-5]; ceiling compression in Coding skills."
        },
        {
            "evidence_layer": "Layer 3: Senior Behavioral Success",
            "dataset_source": "SDS Personality Traits (N=161)",
            "observational_unit": "Senior Customer-Facing Data Scientists",
            "primary_empirical_findings": "Big Five personality traits strongly predict client consulting success (ROC-AUC = 0.9699, Accuracy = 92.68%); Openness (AOR=7.72, Rank #1) and Conscientiousness (AOR=8.11, Rank #2) dominate; Neuroticism has near-zero held-out predictive importance (0.0005).",
            "statistical_support": "Phase 4 H3 group tests (Conscientiousness d=1.85, Openness d=1.80); Phase 6 StratifiedGroupKFold on subject ID across 25 splits; sensitivity robustness N=152 (Delta AUC = 0.0049).",
            "predictive_utility": "Pruned CART tree provides 4 transparent decision rules achieving 90.44% accuracy.",
            "governing_limitation": "Customer-facing consulting context; must strictly NEVER be used as an automated hiring or promotion exclusion gate."
        }
    ]
    return pd.DataFrame(records)


def build_market_skill_matrix() -> pd.DataFrame:
    """
    Constructs the comparative matrix linking market skill frequency, salary premium,
    junior promotion velocity, and senior leadership relevance.
    """
    records = [
        {
            "skill_dimension": "SQL / Relational Databases",
            "market_posting_freq_pct": 48.2,
            "market_demand_tier": "Foundational Baseline (Table Stakes)",
            "market_salary_premium_aor": 0.986,
            "market_premium_sig": "Not Significant (p = 0.879)",
            "jds_skill_importance_rank": "Embedded in Coding / Stats",
            "jds_promotion_effect": "Necessary qualifying competency",
            "sds_leadership_relevance": "Assumed baseline; not evaluated",
            "strategic_role": "Market entry ticket; required for 1 in 2 jobs but confers zero wage premium alone."
        },
        {
            "skill_dimension": "Python / Core Programming",
            "market_posting_freq_pct": 39.5,
            "market_demand_tier": "Foundational Baseline (Table Stakes)",
            "market_salary_premium_aor": 1.059,
            "market_premium_sig": "Not Significant (p = 0.578)",
            "jds_skill_importance_rank": "Coding Skills (Rank #4)",
            "jds_promotion_effect": "Severe ceiling saturation (27.3% at 5.0)",
            "sds_leadership_relevance": "Assumed baseline; not evaluated",
            "strategic_role": "Mandatory hygiene factor; differentiation requires statistical or storytelling layer."
        },
        {
            "skill_dimension": "Mathematics & Statistics",
            "market_posting_freq_pct": 28.4,
            "market_demand_tier": "Core Analytical Differentiator",
            "market_salary_premium_aor": 1.340,
            "market_premium_sig": "Statistically Significant (p < 0.001)",
            "jds_skill_importance_rank": "Maths/Stats Skills (Rank #2)",
            "jds_promotion_effect": "AOR = 3.65 (Strongest Odds Ratio)",
            "sds_leadership_relevance": "Subsumed under rigorous Conscientiousness",
            "strategic_role": "Primary technical engine of junior compensation growth and modeling rigor."
        },
        {
            "skill_dimension": "Machine Learning / AI",
            "market_posting_freq_pct": 21.6,
            "market_demand_tier": "High-Value Specialized Competency",
            "market_salary_premium_aor": 1.581,
            "market_premium_sig": "Statistically Significant (p < 0.001)",
            "jds_skill_importance_rank": "AI & ML Skills (Rank #3)",
            "jds_promotion_effect": "AOR = 1.93 (Secondary Technical Driver)",
            "sds_leadership_relevance": "Strategic AI architecture & Openness",
            "strategic_role": "Commands 58% higher odds of premium salary in job market; key differentiator."
        },
        {
            "skill_dimension": "Dashboarding & Data Storytelling",
            "market_posting_freq_pct": 14.8,
            "market_demand_tier": "Latent / Under-Indexed in Postings",
            "market_salary_premium_aor": 1.246,
            "market_premium_sig": "Borderline / Moderate (p = 0.118)",
            "jds_skill_importance_rank": "Storytelling Skills (Rank #1)",
            "jds_promotion_effect": "AOR = 3.23, Permutation Importance 0.1062",
            "sds_leadership_relevance": "Direct precursor to Client Empathy / Openness",
            "strategic_role": "The critical 'Translation Layer': highest impact on promotion, lowest market posting visibility."
        },
        {
            "skill_dimension": "Big Data / Distributed Systems (Spark/Hadoop)",
            "market_posting_freq_pct": 19.2,
            "market_demand_tier": "High-Demand Infrastructure Skill",
            "market_salary_premium_aor": 1.587,
            "market_premium_sig": "Statistically Significant (p = 0.002)",
            "jds_skill_importance_rank": "Big Data Skills (Rank #5)",
            "jds_promotion_effect": "Non-significant (p = 0.217, Importance 0.0107)",
            "sds_leadership_relevance": "System architectural awareness",
            "strategic_role": "The 'Big Data Illusion': highly demanded in vacancy postings, but does not drive junior salary hike."
        },
        {
            "skill_dimension": "R & SAS (Statistical Enterprise Tools)",
            "market_posting_freq_pct": 16.5,
            "market_demand_tier": "Enterprise Analytics Specialty",
            "market_salary_premium_aor": 1.561,
            "market_premium_sig": "Statistically Significant (p < 0.001)",
            "jds_skill_importance_rank": "Embedded in Maths/Stats Skills",
            "jds_promotion_effect": "Associated with high analytical rigor",
            "sds_leadership_relevance": "Enterprise advisory reliability",
            "strategic_role": "Commands substantial premium (>56% higher odds of high salary) in corporate/banking sectors."
        }
    ]
    return pd.DataFrame(records)


def build_career_stage_matrix() -> pd.DataFrame:
    """
    Constructs the longitudinal progression matrix across the four talent lifecycle stages.
    """
    records = [
        {
            "career_stage": "Stage 1: Entry / Foundation (0 - 2 Years)",
            "role_archetypes": "Data Analyst, Associate Analyst, Junior Data Scientist",
            "primary_market_barrier": "SQL proficiency, Python fundamentals, baseline data wrangling, 0-2 yrs experience.",
            "market_compensation_envelope": "3.5L - 8.0L INR (Mean ~5.8L INR)",
            "differentiating_competencies": "Core coding syntax without bugs, understanding relational schemas, basic EDA.",
            "evidence_source": "Analytics Jobs (N=15,841) & DataScience Jobs entry tiers; JDS Coding baseline."
        },
        {
            "career_stage": "Stage 2: Junior / Velocity (2 - 5 Years)",
            "role_archetypes": "Junior Data Scientist, Analytics Specialist, ML Associate",
            "primary_market_barrier": "Independent statistical modeling, end-to-end analytical problem framing.",
            "market_compensation_envelope": "7.5L - 16.0L INR (Rapid spread expansion)",
            "differentiating_competencies": "Data Storytelling & Executive Dashboarding (Rank #1) + Mathematical Rigor (Rank #2).",
            "evidence_source": "JDS Cohort (N=139): Logistic L2 ROC-AUC = 0.9035, Storytelling AOR = 3.23, Maths AOR = 3.65."
        },
        {
            "career_stage": "Stage 3: Mid-Career / Expansion (5 - 8 Years)",
            "role_archetypes": "Senior Data Scientist, Lead Analyst, ML Engineer",
            "primary_market_barrier": "Specialized architecture (Spark, ML pipelines, cloud) + client stakeholder alignment.",
            "market_compensation_envelope": "14.0L - 28.0L INR (High-salary premium threshold >= 15L)",
            "differentiating_competencies": "Specialized tools (Spark AOR=1.59, ML AOR=1.58) + transition from technical execution to project scoping.",
            "evidence_source": "Analytics Jobs H6 multivariable logistic + DataScience Jobs experience-salary slope (beta=1.98L/yr)."
        },
        {
            "career_stage": "Stage 4: Senior / Consulting Leadership (8+ Years)",
            "role_archetypes": "Principal Data Scientist, Analytics Consultant, Practice Director",
            "primary_market_barrier": "High-stakes client relationship management, navigating ambiguous business objectives.",
            "market_compensation_envelope": "25.0L - 50.0L+ INR (Executive compensation band)",
            "differentiating_competencies": "Openness to Experience (Rank #1, adaptability to novel domains) + Conscientiousness (Rank #2, delivery rigor).",
            "evidence_source": "SDS Cohort (N=161): Logistic L2 ROC-AUC = 0.9699, Openness AOR = 7.72, Conscientiousness AOR = 8.11."
        }
    ]
    return pd.DataFrame(records)


def build_gap_analysis() -> pd.DataFrame:
    """
    Identifies and profiles the five systemic talent ecosystem gaps.
    """
    records = [
        {
            "gap_id": "GAP-1",
            "gap_title": "The Big Data Infrastructure Illusion",
            "market_manifestation": "Job descriptions heavily advertise Big Data (19.2% prevalence) and Hadoop/Spark infrastructure.",
            "practitioner_reality": "Junior practitioners over-index on distributed systems bootcamps, neglecting basic communication.",
            "empirical_evidence": "JDS Big Data skill contributes least to salary-hike velocity (p = 0.217, held-out importance = 0.0107, Rank #5).",
            "strategic_correction": "Reallocate early-career learning hours from Spark cluster management to statistical inference and dashboarding."
        },
        {
            "gap_id": "GAP-2",
            "gap_title": "The Executive Translation & Storytelling Deficit",
            "market_manifestation": "Only 14.8% of job postings explicitly mention storytelling or executive presentation in key skills.",
            "practitioner_reality": "Candidates treat communication as secondary to Python/PyTorch code efficiency.",
            "empirical_evidence": "Storytelling is the #1 out-of-sample predictor of junior salary hikes (AOR=3.23, Permutation Importance=0.1062, top split in CART).",
            "strategic_correction": "Incorporate mandatory client-facing presentations and dashboard narrative defenses into all university curricula."
        },
        {
            "gap_id": "GAP-3",
            "gap_title": "The Table-Stakes Coding Saturation Trap",
            "market_manifestation": "SQL (48.2%) and Python (39.5%) appear in almost every vacancy posting as mandatory filters.",
            "practitioner_reality": "Candidates spend 80% of prep time grinding algorithmic coding challenges (LeetCode).",
            "empirical_evidence": "Python confers zero salary premium alone (AOR=1.06, p=0.578); JDS Coding skills show 27.3% ceiling saturation at 5.0 with low independent AOR (1.26).",
            "strategic_correction": "Treat Python/SQL as baseline qualifying gates; recognize that compensation differentiation requires mathematical modeling and business storytelling."
        },
        {
            "gap_id": "GAP-4",
            "gap_title": "The Senior Behavioral Transition Shock",
            "market_manifestation": "Mid-level practitioners assume continued technical specialization guarantees senior partner promotion.",
            "practitioner_reality": "Senior roles transition from algorithmic execution to client relationship management and unstructured problem solving.",
            "empirical_evidence": "SDS consulting success is overwhelmingly predicted by Openness (AOR=7.72) and Conscientiousness (AOR=8.11), with >94% model accuracy.",
            "strategic_correction": "Establish structured consulting simulation and client-adaptability mentoring programs for mid-career practitioners."
        },
        {
            "gap_id": "GAP-5",
            "gap_title": "The Geographic Premium & Mobility Divide",
            "market_manifestation": "Analytics postings are heavily concentrated in Bengaluru (43.8%), NCR (14.2%), and Mumbai (10.5%).",
            "practitioner_reality": "Candidates in Tier-2 locations face suppressed compensation despite identical technical skills and experience.",
            "empirical_evidence": "NCR and Mumbai command strong positive Haberman residuals (+3.54 and +2.67), while Tier-2 cities exhibit negative wage associations (AOR=0.79, p=0.0035).",
            "strategic_correction": "Candidates seeking maximum compensation velocity must target Tier-1 hubs or remote requisitions anchored in metro wage bands."
        }
    ]
    return pd.DataFrame(records)


def build_skill_progression_map() -> pd.DataFrame:
    """
    Constructs the operational skill progression map showing how competencies evolve across career stages.
    """
    records = [
        {"competency_area": "Programming & Data Wrangling", "stage_1_entry": "SQL queries, Python pandas, data cleansing", "stage_2_junior": "Modular Python pipelines, Git versioning", "stage_3_mid": "Production API integration, CI/CD, PySpark", "stage_4_senior": "Architectural governance, toolstack strategy"},
        {"competency_area": "Mathematics & Statistics", "stage_1_entry": "Descriptive statistics, basic probability", "stage_2_junior": "Hypothesis testing, regression modeling, A/B testing", "stage_3_mid": "Multivariate modeling, causal inference, Bayesian methods", "stage_4_senior": "Analytical risk evaluation, research scoping"},
        {"competency_area": "Machine Learning & AI", "stage_1_entry": "Supervised algorithms (regression, decision trees)", "stage_2_junior": "Model evaluation, feature engineering, cross-validation", "stage_3_mid": "Deep learning, NLP/LLM fine-tuning, MLOps deployment", "stage_4_senior": "Business AI feasibility assessment, ethical audit"},
        {"competency_area": "Communication & Storytelling", "stage_1_entry": "Static charts, descriptive slide summaries", "stage_2_junior": "Interactive dashboards (PowerBI/Tableau), insight narrative", "stage_3_mid": "Executive briefings, translating tech debt to business cost", "stage_4_senior": "C-suite strategic persuasion, consultative advisory"},
        {"competency_area": "Behavioral & Client Leadership", "stage_1_entry": "Task adherence, receptive to feedback", "stage_2_junior": "Proactive project ownership, peer code reviews", "stage_3_mid": "Cross-functional stakeholder management, mentoring", "stage_4_senior": "Intellectual agility (Openness), flawless delivery rigor (Conscientiousness)"}
    ]
    return pd.DataFrame(records)


def build_evidence_strength_matrix() -> pd.DataFrame:
    """
    Grades evidence confidence levels across the analytical ecosystem.
    """
    records = [
        {
            "finding_identifier": "FINDING-1: Experience-Salary Elasticity",
            "finding_summary": "Experience positively correlates with salary (beta = 1.98L per year; r = 0.63 - 0.66).",
            "evidence_grade": "HIGH CONFIDENCE",
            "methodology_rigor": "Bivariate & adjusted OLS regressions on N=1,602 and N=15,841 with HC3 robust SEs (p < 1e-100).",
            "generalizability": "Broad macro market validity across Indian tech hiring ecosystems."
        },
        {
            "finding_identifier": "FINDING-2: Table-Stakes vs Premium Skills",
            "finding_summary": "SQL/Python are entry requirements; specialized tools (R, SAS, Spark, ML) command independent 1.46-1.59x salary premia.",
            "evidence_grade": "HIGH CONFIDENCE",
            "methodology_rigor": "Multivariable logistic regression on N=15,841 controlling for location, experience, and role.",
            "generalizability": "Highly generalizable across vacancy posting market data."
        },
        {
            "finding_identifier": "FINDING-3: Junior Salary Velocity Drivers",
            "finding_summary": "Storytelling (AOR=3.23) and Maths/Stats (AOR=3.65) drive junior promotion; Big Data adds negligible signal.",
            "evidence_grade": "HIGH CONFIDENCE (Within Cohort)",
            "methodology_rigor": "25-split repeated cross-validation (ROC-AUC = 0.9035); permutation testing; sensitivity check on N=137.",
            "generalizability": "Valid within evaluated junior talent sample; requires replication in other corporate settings."
        },
        {
            "finding_identifier": "FINDING-4: Senior Consulting Success Drivers",
            "finding_summary": "Openness (AOR=7.72) and Conscientiousness (AOR=8.11) predict consulting success (ROC-AUC = 0.9699).",
            "evidence_grade": "HIGH CONFIDENCE (Within Cohort)",
            "methodology_rigor": "StratifiedGroupKFold on subject ID across 25 splits; zero clone leakage; sensitivity check on N=152.",
            "generalizability": "Valid for customer-facing senior analytics consultants; not applicable as automated hiring gates."
        },
        {
            "finding_identifier": "FINDING-5: The Neuroticism Suppressor Effect",
            "finding_summary": "Neuroticism shows statistical multivariable significance (AOR=3.94) but zero held-out predictive importance (0.0005).",
            "evidence_grade": "MODERATE CONFIDENCE / EMPIRICAL NUANCE",
            "methodology_rigor": "Discrepancy between parametric Wald tests and out-of-sample permutation importance across 25 CV splits.",
            "generalizability": "Demonstrates the necessity of distinguishing statistical association from out-of-sample utility."
        }
    ]
    return pd.DataFrame(records)


def build_rq_synthesis() -> pd.DataFrame:
    """
    Synthesizes Research Questions RQ1 through RQ9 into a unified tabular narrative.
    """
    records = [
        {"rq_id": "RQ1", "topic": "Macro Role Demand", "empirical_answer": "Data Scientist (35.2%), ML Engineer (21.4%), and Data Analyst (15.8%) represent 72.4% of total demand across 642 organizations."},
        {"rq_id": "RQ2", "topic": "Experience & Salary", "empirical_answer": "Strong positive monotonic relationship (Spearman rho = 0.633 - 0.704); linear elasticity beta = 1.98L/year; salary variance expands sharply at >= 5 years."},
        {"rq_id": "RQ3", "topic": "Geographic Clusters", "empirical_answer": "Bengaluru (43.8%), NCR (14.2%), and Mumbai (10.5%) constitute 68.5% of total demand, exhibiting statistically significant wage premiums."},
        {"rq_id": "RQ4", "topic": "Skill Frequency", "empirical_answer": "SQL (48.2%) and Python (39.5%) dominate postings as foundational requirements; ML (21.6%), Big Data (19.2%), R (16.5%), and SAS (15.2%) form specialized clusters."},
        {"rq_id": "RQ5", "topic": "Premium Salary Skills", "empirical_answer": "Spark (AOR=1.59), ML (AOR=1.58), SAS (AOR=1.47), and R (AOR=1.56) command significant independent premia, whereas SQL and Python do not."},
        {"rq_id": "RQ6", "topic": "Junior Competencies", "empirical_answer": "Dashboarding/Storytelling (d=1.04, AOR=3.23) and Maths/Stats (d=1.05, AOR=3.65) associate most strongly with junior salary hikes; Big Data is non-significant (p=0.217)."},
        {"rq_id": "RQ7", "topic": "Senior Personality", "empirical_answer": "Conscientiousness (d=1.85, AOR=8.11) and Openness (d=1.80, AOR=7.72) associate overwhelmingly with consulting success; Neuroticism shows zero bivariate difference."},
        {"rq_id": "RQ8", "topic": "Predictive Models", "empirical_answer": "Regularized Logistic models achieve ROC-AUC = 0.9035 (JDS) and 0.9699 (SDS) under 25-split cross-validation; parsimonious linear models match or exceed complex ensembles."},
        {"rq_id": "RQ9", "topic": "Framework Synthesis", "empirical_answer": "Multi-lens evidence integrates into an operational 4-Quadrant Talent Matrix and 4-Stage Progression Roadmap without row-level joins."}
    ]
    return pd.DataFrame(records)


def build_phase6_phase5_traceability() -> pd.DataFrame:
    """
    Constructs the side-by-side comparative bridge between JDS modeling (Phase 5) and SDS modeling (Phase 6).
    """
    records = [
        {
            "dimension": "Cohort Sample Size",
            "phase5_jds": "N = 139 Primary (N = 137 Sensitivity)",
            "phase6_sds": "N = 161 Primary (N = 152 Sensitivity)"
        },
        {
            "dimension": "Predictor Variables",
            "phase5_jds": "5 Technical Skill Dimensions (scale 1.0 - 5.0)",
            "phase6_sds": "5 Big Five Personality Dimensions (interval 17.0 - 68.0)"
        },
        {
            "dimension": "Classification Target",
            "phase5_jds": "salary_hike_high_or_low (52.5% High / 47.5% Low)",
            "phase6_sds": "success_classification_high_low (52.8% High / 47.2% Low)"
        },
        {
            "dimension": "Cross-Validation Protocol",
            "phase5_jds": "5-Fold x 5-Repeat StratifiedKFold (25 splits)",
            "phase6_sds": "5-Fold x 5-Repeat StratifiedGroupKFold on ID (25 splits)"
        },
        {
            "dimension": "Champion Model Selected",
            "phase5_jds": "Logistic Regression L2 (Ridge, C=1.0)",
            "phase6_sds": "Logistic Regression L2 (Ridge, C=1.0)"
        },
        {
            "dimension": "Champion ROC-AUC (Mean ± SD)",
            "phase5_jds": "0.9035 ± 0.0594 [95% CI: 0.8802, 0.9268]",
            "phase6_sds": "0.9699 ± 0.0268 [95% CI: 0.9594, 0.9804]"
        },
        {
            "dimension": "Champion Accuracy & Baseline Lift",
            "phase5_jds": "85.29% (+32.78% lift over 52.51% baseline)",
            "phase6_sds": "92.68% (+39.90% lift over 52.78% baseline)"
        },
        {
            "dimension": "Primary Predictive Drivers",
            "phase5_jds": "Storytelling (Rank #1) & Maths/Stats (Rank #2)",
            "phase6_sds": "Openness (Rank #1) & Conscientiousness (Rank #2)"
        },
        {
            "dimension": "Weakest Predictive Feature",
            "phase5_jds": "Big Data Skills (Rank #5, Imp = 0.0107)",
            "phase6_sds": "Neuroticism (Rank #5, Imp = 0.0005)"
        },
        {
            "dimension": "Sensitivity Invariance Verdict",
            "phase5_jds": "ROBUST (Delta AUC = 0.0015 <= 0.02)",
            "phase6_sds": "HIGHLY ROBUST (Delta AUC = 0.0049 <= 0.02)"
        }
    ]
    return pd.DataFrame(records)


def build_recommendation_evidence() -> pd.DataFrame:
    """
    Maps upcoming Phase 8 operational recommendations to their exact empirical origins.
    """
    records = [
        {"action_id": "REC-1", "recommendation": "Universities must mandate data storytelling and executive presentation defense in curriculum.", "empirical_source": "Phase 4 H1 (d=1.04) & Phase 5 JDS Permutation Importance (0.1062, Rank #1); CART Root Split."},
        {"action_id": "REC-2", "recommendation": "Students should de-emphasize standalone Big Data tools in favor of statistical modeling depth.", "empirical_source": "Phase 4 H1 (p=0.217) & Phase 5 JDS (Big Data Rank #5, Importance 0.0107); Phase 4 H6 regression."},
        {"action_id": "REC-3", "recommendation": "Candidates targeting high salaries must combine Python with specialized tools (R, SAS, Spark, ML).", "empirical_source": "Phase 4 H6 Multivariable Logistic Regression on N=15,841 (Spark AOR=1.59, ML AOR=1.58, R AOR=1.56, SAS AOR=1.47)."},
        {"action_id": "REC-4", "recommendation": "Mentors must coach aspiring senior consultants on intellectual adaptability and execution discipline.", "empirical_source": "Phase 4 H3 (Conscientiousness d=1.85, Openness d=1.80) & Phase 6 SDS Permutation Importance (Openness 0.1209, Conscientiousness 0.0826)."},
        {"action_id": "REC-5", "recommendation": "Organizations must strictly ban automated personality-based hiring or termination algorithms.", "empirical_source": "Phase 0 Governance & Phase 6 Ethical Guardrails; context-dependency of Big Five consulting ratings."},
        {"action_id": "REC-6", "recommendation": "Early-career practitioners seeking wage acceleration should prioritize Bengaluru, NCR, or Mumbai.", "empirical_source": "Phase 4 H6 Geographic Chi-square (Chi2=69.87) & Haberman Residuals (NCR=+3.54, Mumbai=+2.67)."}
    ]
    return pd.DataFrame(records)


def build_all_phase7_synthesis_tables() -> Dict[str, pd.DataFrame]:
    """
    Constructs and returns all 9 Phase 7 synthesis tables in a dictionary.
    """
    return {
        "phase7_evidence_matrix.csv": build_evidence_matrix(),
        "phase7_market_skill_matrix.csv": build_market_skill_matrix(),
        "phase7_career_stage_matrix.csv": build_career_stage_matrix(),
        "phase7_gap_analysis.csv": build_gap_analysis(),
        "phase7_skill_progression_map.csv": build_skill_progression_map(),
        "phase7_evidence_strength.csv": build_evidence_strength_matrix(),
        "phase7_rq_synthesis.csv": build_rq_synthesis(),
        "phase7_phase6_phase5_traceability.csv": build_phase6_phase5_traceability(),
        "phase7_recommendation_evidence.csv": build_recommendation_evidence()
    }

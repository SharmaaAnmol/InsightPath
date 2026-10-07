"""
src/framework/blueprints.py
---------------------------
Operational stakeholder action blueprints and evidence-to-action mapping for Phase 8.
Covers Students, Universities, Mentors, and Employers with measurable outcomes.
"""

from typing import Dict
import pandas as pd


def build_student_blueprint() -> pd.DataFrame:
    records = [
        {
            "dimension": "Core Challenge",
            "student_context": "Grinding hundreds of algorithmic LeetCode/Python challenges while neglecting communication and statistical inference depth."
        },
        {
            "dimension": "Empirical Evidence",
            "student_context": "Python/SQL have neutral salary odds (AOR ~1.0); Storytelling (AOR=3.23) and Maths/Stats (AOR=3.65) drive 96.7% of junior promotion velocity."
        },
        {
            "dimension": "Action 1: The 'Dual-Artifact' Portfolio",
            "student_context": "For every project, publish both clean modular Python code AND an interactive PowerBI/Tableau executive dashboard with a 2-minute video presentation."
        },
        {
            "dimension": "Action 2: Statistical Rigor Focus",
            "student_context": "Master formal hypothesis testing, regression diagnostics, and A/B test power analysis rather than just calling .fit() on black-box neural nets."
        },
        {
            "dimension": "Action 3: Geographic Targeting",
            "student_context": "Target entry requisitions in Bengaluru, NCR, or Mumbai (68.5% demand), or remote roles anchored in metro wage brackets."
        },
        {
            "dimension": "Measurable Target Indicator",
            "student_context": "Achieve 3 public portfolio projects with deployed dashboards; attain >=80% interview callback rate on storytelling project walkthroughs."
        },
        {
            "dimension": "Key Limitation / Guardrail",
            "student_context": "Do not skip Python/SQL syntax mastery; they remain mandatory gatekeepers to reach the interview stage."
        }
    ]
    return pd.DataFrame(records)


def build_university_blueprint() -> pd.DataFrame:
    records = [
        {
            "dimension": "Core Challenge",
            "university_context": "Curricula overemphasize standalone big data infrastructure (Hadoop/Spark clusters) while under-indexing on data storytelling and business translation."
        },
        {
            "dimension": "Empirical Evidence",
            "university_context": "Big Data skills show zero independent impact on junior salary hikes (p=0.217, Importance 0.0107, Rank #5); Storytelling is Rank #1 driver."
        },
        {
            "dimension": "Action 1: Mandatory Executive Defenses",
            "university_context": "Replace written exam reports with mandatory oral project defenses where students present findings to simulated non-technical business stakeholders."
        },
        {
            "dimension": "Action 2: Reallocate Lab Hours",
            "university_context": "Shift 40% of lab time from distributed system configuration to interactive dashboard design (Tableau/PowerBI) and experimental A/B test design."
        },
        {
            "dimension": "Action 3: Real Messy Industry Data",
            "university_context": "Eliminate synthetic toy datasets (Iris, Titanic); train students on raw, multi-source enterprise data with missingness and conflicting labels."
        },
        {
            "dimension": "Measurable Target Indicator",
            "university_context": "100% of graduating data science capstones include an executive summary and interactive dashboard; graduate median placement salary increases by >=25%."
        },
        {
            "dimension": "Key Limitation / Guardrail",
            "university_context": "Curricular modernization requires retraining academic faculty on modern BI visualization and consultative communication."
        }
    ]
    return pd.DataFrame(records)


def build_mentor_blueprint() -> pd.DataFrame:
    records = [
        {
            "dimension": "Core Challenge",
            "mentor_context": "Mentors focus exclusively on technical upskilling, failing to prepare mentees for the behavioral transition required for senior consulting success."
        },
        {
            "dimension": "Empirical Evidence",
            "mentor_context": "Senior consulting success is predicted with 92.7% accuracy by Openness (AOR=7.72) and Conscientiousness (AOR=8.11); Neuroticism has zero held-out predictive value."
        },
        {
            "dimension": "Action 1: Client Simulation Sessions",
            "mentor_context": "Conduct monthly roleplay simulations where mentees navigate difficult, ambiguous client scenarios, scope changes, and executive pushback."
        },
        {
            "dimension": "Action 2: Cultivate Intellectual Openness",
            "mentor_context": "Encourage mentees to work across unfamiliar business domains (e.g. pivoting from retail churn to manufacturing supply chain) to build cognitive adaptability."
        },
        {
            "dimension": "Action 3: Delivery Conscientiousness Audits",
            "mentor_context": "Instill extreme rigor in documentation, stakeholder follow-up, meeting recaps, and reproducible artifact delivery."
        },
        {
            "dimension": "Measurable Target Indicator",
            "mentor_context": "Mentees achieve >=90% stakeholder approval ratings on complex projects; successful promotion from individual contributor to consulting lead within 24 months."
        },
        {
            "dimension": "Key Limitation / Guardrail",
            "mentor_context": "Strict ethical boundary: Never use Big Five personality scores to judge or categorize a mentee's character; focus on observable communication behaviors."
        }
    ]
    return pd.DataFrame(records)


def build_employer_blueprint() -> pd.DataFrame:
    records = [
        {
            "dimension": "Core Challenge",
            "employer_context": "Job descriptions publish bloated 'wishlists' (asking for 10+ tools), creating high recruiting friction, while internal evaluation relies on subjective bias."
        },
        {
            "dimension": "Empirical Evidence",
            "employer_context": "A 2-feature competency model (Maths + Storytelling) captures 96.75% of junior predictive velocity; experience scales salary linearly at 1.98L/year."
        },
        {
            "dimension": "Action 1: Calibrate Job Descriptions",
            "employer_context": "Remove unrealistic tool requirements (e.g. requiring Spark and Kubernetes for junior roles); explicitly state requirements for data communication and dashboarding."
        },
        {
            "dimension": "Action 2: Standardize Rubrics on Proven Drivers",
            "employer_context": "Evaluate junior candidates on statistical reasoning and business narrative defense rather than LeetCode algorithmic puzzle speed."
        },
        {
            "dimension": "Action 3: Strict Ethical AI Ban on Personality Tools",
            "employer_context": "Prohibit automated personality pre-screening software in recruitment to prevent discrimination and avoid unvalidated exclusion."
        },
        {
            "dimension": "Measurable Target Indicator",
            "employer_context": "Reduction in time-to-hire by >=30%; post-hire 12-month retention rates increase to >=85%; elimination of algorithmic bias liabilities."
        },
        {
            "dimension": "Key Limitation / Guardrail",
            "employer_context": "Requires alignment between HR talent acquisition teams and technical engineering directors."
        }
    ]
    return pd.DataFrame(records)


def build_evidence_to_action() -> pd.DataFrame:
    records = [
        {"action_id": "ACT-1", "recommendation_area": "Portfolio Modernization", "recommended_action": "Mandate interactive dashboard + video presentation alongside Python code.", "supporting_evidence": "Phase 5 JDS: Storytelling Rank #1 Permutation Importance (0.1062), AOR = 3.23.", "target_stakeholder": "Students & Universities", "priority": "Immediate"},
        {"action_id": "ACT-2", "recommendation_area": "Curriculum De-bloating", "recommended_action": "Remove distributed Big Data cluster administration from introductory curricula.", "supporting_evidence": "Phase 4 H1 (p=0.217) & Phase 5 JDS: Big Data Rank #5, Importance 0.0107.", "target_stakeholder": "Universities & Bootcamps", "priority": "High"},
        {"action_id": "ACT-3", "recommendation_area": "Mid-Career Wage Mobility", "recommended_action": "Upskill into specialized stacks (Spark, ML, R, SAS) to cross 15L+ salary bracket.", "supporting_evidence": "Phase 4 H6 Logistic: Spark AOR=1.59, ML AOR=1.58, R AOR=1.56, SAS AOR=1.47.", "target_stakeholder": "Mid-Career Practitioners", "priority": "High"},
        {"action_id": "ACT-4", "recommendation_area": "Consulting Leadership Transition", "recommended_action": "Coach senior candidates on client adaptability (Openness) and execution discipline.", "supporting_evidence": "Phase 6 SDS: Openness AOR=7.72, Conscientiousness AOR=8.11, ROC-AUC=0.9699.", "target_stakeholder": "Mentors & Employers", "priority": "High"},
        {"action_id": "ACT-5", "recommendation_area": "Algorithmic Hiring Ethics", "recommended_action": "Implement policy banning automated psychometric/personality gatekeeping tools.", "supporting_evidence": "Phase 0 Limitations & Phase 6 Ethical Guardrails; context-dependency of Big Five ratings.", "target_stakeholder": "Employers & HR Leadership", "priority": "Mandatory"}
    ]
    return pd.DataFrame(records)


def build_success_indicators() -> pd.DataFrame:
    records = [
        {"indicator_id": "KPI-1", "stakeholder": "Students", "metric_name": "Portfolio Dual-Artifact Ratio", "baseline": "15% of projects have dashboards", "target": "100% of projects have interactive dashboards & video pitches"},
        {"indicator_id": "KPI-2", "stakeholder": "Students", "metric_name": "Junior Salary Hike Velocity", "baseline": "Market median 15-20% hike", "target": "Top-quartile >35% hike via statistical storytelling mastery"},
        {"indicator_id": "KPI-3", "stakeholder": "Universities", "metric_name": "Oral Project Defense Capstones", "baseline": "0% mandatory oral defenses", "target": "100% mandatory presentation to business panels"},
        {"indicator_id": "KPI-4", "stakeholder": "Universities", "metric_name": "Graduate Placement Speed", "baseline": "Median 6.2 months post-grad", "target": "Median <3.5 months post-grad via differentiated portfolios"},
        {"indicator_id": "KPI-5", "stakeholder": "Mentors", "metric_name": "Consulting Transition Velocity", "baseline": "36-48 months IC to Lead", "target": "24 months IC to Lead with structured adaptability coaching"},
        {"indicator_id": "KPI-6", "stakeholder": "Employers", "metric_name": "Candidate Interview-to-Offer Ratio", "baseline": "8:1 ratio due to poor communication", "target": "3:1 ratio using calibrated, storytelling-focused screens"},
        {"indicator_id": "KPI-7", "stakeholder": "Employers", "metric_name": "Ethical Compliance Audit", "baseline": "Unregulated third-party test use", "target": "100% ban on automated personality pre-screening gates"}
    ]
    return pd.DataFrame(records)


def build_framework_traceability() -> pd.DataFrame:
    records = [
        {"framework_element": "4-Quadrant: Advanced Readiness (Q1)", "underlying_data_source": "JDS N=139 & SDS N=161", "phase_traceability": "Phase 5 CART Rule 1 & Phase 6 Tree Leaf 4", "key_metric": "100% High Hike / 94.3% Consulting Success"},
        {"framework_element": "4-Quadrant: Technical Strong (Q2)", "underlying_data_source": "JDS N=139", "phase_traceability": "Phase 5 CART Rules 3 & 4", "key_metric": "Salary velocity drops to 66-82% without storytelling"},
        {"framework_element": "4-Quadrant: Communication Strong (Q3)", "underlying_data_source": "JDS N=139", "phase_traceability": "Phase 5 CART Rule 2", "key_metric": "71.4% High Hike (communication compensates partially)"},
        {"framework_element": "4-Quadrant: Stagnation Trap (Q4)", "underlying_data_source": "JDS N=139 & SDS N=161", "phase_traceability": "Phase 5 CART Rule 6 & Phase 6 Leaf 1", "key_metric": "97.7% Low Hike / 100% Low Consulting Success"},
        {"framework_element": "Stage 1: Entry / Foundation", "underlying_data_source": "Analytics Jobs N=15,841", "phase_traceability": "Phase 3 EDA & Phase 4 H6 Baseline Skills", "key_metric": "SQL (48.2%) & Python (39.5%) Table Stakes"},
        {"framework_element": "Stage 2: Junior / Velocity", "underlying_data_source": "JDS N=139", "phase_traceability": "Phase 4 H1, H2 & Phase 5 ML", "key_metric": "Storytelling AOR=3.23, Maths AOR=3.65 (ROC-AUC=0.9035)"},
        {"framework_element": "Stage 3: Mid-Career / Expansion", "underlying_data_source": "DataScience Jobs & Analytics Jobs", "phase_traceability": "Phase 4 H5, H6 Multivariable Logistic", "key_metric": "Spark AOR=1.59, ML AOR=1.58, Beta=1.98L/year"},
        {"framework_element": "Stage 4: Senior Leadership", "underlying_data_source": "SDS N=161", "phase_traceability": "Phase 4 H3, H4 & Phase 6 ML", "key_metric": "Openness AOR=7.72, Conscientiousness AOR=8.11 (ROC-AUC=0.9699)"}
    ]
    return pd.DataFrame(records)


def build_blueprint_tables() -> Dict[str, pd.DataFrame]:
    return {
        "phase8_student_blueprint.csv": build_student_blueprint(),
        "phase8_university_blueprint.csv": build_university_blueprint(),
        "phase8_mentor_blueprint.csv": build_mentor_blueprint(),
        "phase8_employer_blueprint.csv": build_employer_blueprint(),
        "phase8_evidence_to_action.csv": build_evidence_to_action(),
        "phase8_success_indicators.csv": build_success_indicators(),
        "phase8_framework_traceability.csv": build_framework_traceability()
    }

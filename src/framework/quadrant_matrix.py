"""
src/framework/quadrant_matrix.py
--------------------------------
Core logic for constructing the Four-Quadrant Talent Matrix and Career-Stage Framework.
Maps technical execution against business communication / behavioral execution.
"""

from typing import Dict
import pandas as pd


def build_four_quadrant_matrix() -> pd.DataFrame:
    """
    Constructs the operational Four-Quadrant Talent Matrix table.
    """
    records = [
        {
            "quadrant_id": "Q1",
            "quadrant_name": "Advanced Readiness (Strategic Impact)",
            "technical_execution_level": "High (Maths/Stats >= 3.65, ML/Coding proficient)",
            "communication_behavioral_level": "High (Storytelling >= 4.15, High Openness & Conscientiousness)",
            "observed_cohort_behavior": "JDS CART Rule 1: 100% High Salary Hike (N=45); SDS Leaf 4: 94.3% High Consulting Success (N=88).",
            "market_positioning": "Fast-track talent; commands premium salary envelopes (>15L INR); trusted client advisor.",
            "development_priority": "Strategic leadership, MLOps architecture, business case formulation, cross-functional mentoring.",
            "risk_profile": "Flight risk; high market poaching vulnerability; requires challenging autonomous projects."
        },
        {
            "quadrant_id": "Q2",
            "quadrant_name": "Technically Strong, Communication Gap (The Execution Engine)",
            "technical_execution_level": "High (Maths/Stats >= 3.65, Coding >= 3.85)",
            "communication_behavioral_level": "Low/Moderate (Storytelling <= 4.15, Low Client Openness)",
            "observed_cohort_behavior": "JDS CART Rule 3 & 4: Salary velocity drops from 100% to 66-82%; high technical output unrewarded.",
            "market_positioning": "High individual contributor output; vital for backend modeling, pipeline engineering, and algorithm research.",
            "development_priority": "Mandatory executive dashboard training, business translation workshops, client presentation practice.",
            "risk_profile": "Career plateau; frustration over slower compensation velocity despite technical superiority."
        },
        {
            "quadrant_id": "Q3",
            "quadrant_name": "Communication Strong, Technical Gap (The Business Facilitator)",
            "technical_execution_level": "Low/Moderate (Maths/Stats <= 3.65, AI/ML gaps)",
            "communication_behavioral_level": "High (Storytelling >= 4.15, High Extraversion & Agreeableness)",
            "observed_cohort_behavior": "JDS CART Rule 2: 71.4% High Hike (communication compensates partially for math gaps, but ceiling limits apply).",
            "market_positioning": "Analytics translation, stakeholder bridging, product management, business intelligence reporting.",
            "development_priority": "Formal mathematical foundations, statistical inference rigor, hands-on programming depth.",
            "risk_profile": "Credibility gap with engineering teams; inability to audit model errors or detect statistical leakage."
        },
        {
            "quadrant_id": "Q4",
            "quadrant_name": "Foundational Development (Early Stage / Stagnation Trap)",
            "technical_execution_level": "Low (Maths/Stats <= 3.65, Coding basic)",
            "communication_behavioral_level": "Low (Storytelling <= 4.15, Low Adaptability)",
            "observed_cohort_behavior": "JDS CART Rule 6: 97.7% Low Salary Hike (N=44); SDS Leaf 1 & 2: 100% Low Consulting Success.",
            "market_positioning": "Entry-level operational tasks, routine dashboard maintenance, basic SQL data retrieval.",
            "development_priority": "Structured foundational bootcamps in SQL/Python wrangling followed by statistical inference.",
            "risk_profile": "High automation and redundancy risk; trapped in entry-level salary band (<6L INR)."
        }
    ]
    return pd.DataFrame(records)


def build_career_stage_framework() -> pd.DataFrame:
    """
    Constructs the 4-Stage practical progression framework.
    """
    records = [
        {
            "stage_id": "STAGE-1",
            "stage_name": "Entry / Foundation (0 - 2 Years)",
            "priority_competencies": "SQL, Python, Relational Data Wrangling, Basic Descriptive Analytics",
            "why_it_matters": "Mandatory market table stakes (SQL 48.2%, Python 39.5%); required to pass screening filters.",
            "empirical_evidence_source": "Analytics Jobs (N=15,841) keyword frequency; DataScience Jobs entry salary band (3.5L-8L).",
            "recommended_development_action": "Build 3 end-to-end data cleansing and SQL analysis projects on public messy datasets.",
            "measurable_success_indicator": "Passing technical screen; zero SQL syntax errors; clean GitHub repository with documentation.",
            "primary_stakeholder": "Students & Academic Bootcamps"
        },
        {
            "stage_id": "STAGE-2",
            "stage_name": "Junior / Velocity (2 - 5 Years)",
            "priority_competencies": "Executive Storytelling, Dashboarding (PowerBI/Tableau), Mathematical & Statistical Modeling",
            "why_it_matters": "The primary differentiator of salary hikes (Storytelling AOR=3.23, Maths AOR=3.65; 96.7% power in 2 features).",
            "empirical_evidence_source": "JDS Modeling (N=139): Logistic L2 ROC-AUC = 0.9035, Permutation Importance Rank #1 & #2.",
            "recommended_development_action": "Pair every statistical model with an interactive executive dashboard and a 3-minute executive video walkthrough.",
            "measurable_success_indicator": "Promotion to Senior Analyst / DS; salary hike rating in top quartile; business stakeholder adoption.",
            "primary_stakeholder": "Junior Practitioners & Team Leads"
        },
        {
            "stage_id": "STAGE-3",
            "stage_name": "Mid-Career / Expansion (5 - 8 Years)",
            "priority_competencies": "Specialized Tooling (PySpark, MLOps, ML Algorithms, R/SAS), Project Architecture, Cross-functional Scoping",
            "why_it_matters": "Commands 47-59% independent salary premium (Spark AOR=1.59, ML AOR=1.58); overcomes wage plateau.",
            "empirical_evidence_source": "Analytics Jobs H6 Logistic (N=15,841); DataScience Jobs experience-salary slope (beta=1.98L/yr).",
            "recommended_development_action": "Lead a distributed pipeline migration or deploy an end-to-end ML model into live production.",
            "measurable_success_indicator": "Crossing the 15L+ INR premium compensation threshold; leading complex sprint deliverables.",
            "primary_stakeholder": "Mid-Career Specialists & Engineering Managers"
        },
        {
            "stage_id": "STAGE-4",
            "stage_name": "Senior / Consulting Leadership (8+ Years)",
            "priority_competencies": "Intellectual Adaptability (Openness), Execution Rigor (Conscientiousness), C-suite Advisory, Ethical AI",
            "why_it_matters": "Differentiates senior consulting success with >94% predictive accuracy (Openness AOR=7.72, Conscientiousness AOR=8.11).",
            "empirical_evidence_source": "SDS Modeling (N=161): Logistic L2 ROC-AUC = 0.9699; CART 4-rule decision tree (90.4% accuracy).",
            "recommended_development_action": "Engage in executive shadowing, client empathy coaching, and multi-stakeholder dispute resolution.",
            "measurable_success_indicator": "High client satisfaction index; multi-year enterprise contract renewals; practice leadership.",
            "primary_stakeholder": "Senior Consultants & Practice Directors"
        }
    ]
    return pd.DataFrame(records)


def build_competency_priorities() -> pd.DataFrame:
    """
    Constructs the prioritized competency hierarchy across the talent ecosystem.
    """
    records = [
        {"competency": "Executive Data Storytelling & Dashboarding", "priority_tier": "Tier 1: High Velocity Differentiator", "target_audience": "Junior & Mid-Level Data Scientists", "roi_multiplier": "3.23x Odds of High Promotion", "rationale": "Highest return on career investment; bridges technical output to corporate P&L impact."},
        {"competency": "Mathematical & Statistical Modeling", "priority_tier": "Tier 1: Core Analytical Engine", "target_audience": "Entry & Junior Data Scientists", "roi_multiplier": "3.65x Odds of High Promotion", "rationale": "Ensures model rigor, correct inference, and defensible algorithmic architecture."},
        {"competency": "Client Adaptability & Intellectual Openness", "priority_tier": "Tier 1: Senior Leadership Pillar", "target_audience": "Mid-Career & Senior Consultants", "roi_multiplier": "7.72x Odds of Consulting Success", "rationale": "Critical for navigating ambiguous client requirements and unstandardized domain challenges."},
        {"competency": "Flawless Delivery Conscientiousness", "priority_tier": "Tier 1: Senior Leadership Pillar", "target_audience": "Senior Consultants & Practice Leads", "roi_multiplier": "8.11x Odds of Consulting Success", "rationale": "Execution discipline, quality assurance, and structured follow-through build trusted advisory status."},
        {"competency": "Specialized ML & Distributed Systems (Spark)", "priority_tier": "Tier 2: Premium Wage Accelerator", "target_audience": "Mid-Career Specialists", "roi_multiplier": "1.58x - 1.59x Odds of Premium Salary", "rationale": "Overcomes commodity coding wages; commands significant compensation envelopes in metro tech hubs."},
        {"competency": "SQL & Python Procedural Coding", "priority_tier": "Tier 3: Mandatory Table Stakes", "target_audience": "All Practitioners (Entry Level)", "roi_multiplier": "Baseline (1.0x Wage Multiplier)", "rationale": "Non-negotiable hygiene requirement; necessary for market access but confers zero wage premium alone."}
    ]
    return pd.DataFrame(records)


def build_four_quadrant_tables() -> Dict[str, pd.DataFrame]:
    return {
        "phase8_four_quadrant_matrix.csv": build_four_quadrant_matrix(),
        "phase8_career_stage_framework.csv": build_career_stage_framework(),
        "phase8_competency_priorities.csv": build_competency_priorities()
    }

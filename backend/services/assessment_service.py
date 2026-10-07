"""
backend/services/assessment_service.py
--------------------------------------
Service layer for evaluating career-readiness self-assessments against
the validated Phase 5 JDS champion model, Phase 5 feature importance,
and Phase 8 competency priorities.
Strictly enforces non-deterministic, observed-cohort diagnostic language.
"""

from typing import List, Dict, Any
import logging

from backend.schemas.jds import JDSPredictRequest
from backend.schemas.assessment import (
    AssessmentRequest,
    AssessmentResponse,
    SkillRadarPoint,
    RecommendationItem,
    LearningStage,
    ETHICAL_ASSESSMENT_DISCLAIMER,
)
from backend.services.model_service import model_service
from backend.services.data_service import data_service

logger = logging.getLogger(__name__)

# High-hike group benchmarks derived from data/processed/jds_processed.csv (Class 1 means)
HIGH_HIKE_BENCHMARKS = {
    "maths_stats_skills": {
        "name": "Mathematics & Statistics",
        "benchmark": 4.8,
        "importance_rank": 2,
        "aor": "3.61x",
        "rationale": "High statistical inference and mathematical rigor drive a 3.61x adjusted odds ratio in the observed JDS cohort.",
        "roi": "3.65x Odds Multiplier",
    },
    "dashboard_and_storytelling_skills": {
        "name": "Dashboarding & Storytelling",
        "benchmark": 4.3,
        "importance_rank": 1,
        "aor": "3.06x",
        "rationale": "Executive data narrative and dashboard translation rank #1 in out-of-fold permutation importance (0.1089).",
        "roi": "3.23x Odds Multiplier",
    },
    "ai_and_ml_skills": {
        "name": "AI & Machine Learning",
        "benchmark": 4.8,
        "importance_rank": 3,
        "aor": "2.14x",
        "rationale": "Production modeling pipelines and algorithmic evaluation form the core predictive engine.",
        "roi": "2.14x Odds Multiplier",
    },
    "coding_skills": {
        "name": "Coding (Python/R)",
        "benchmark": 4.5,
        "importance_rank": 4,
        "aor": "1.70x",
        "rationale": "Procedural coding is a non-negotiable table-stakes skill (39.5% market prevalence) required to clear technical screening.",
        "roi": "Baseline Currency",
    },
    "big_data_skills": {
        "name": "Big Data & Cloud",
        "benchmark": 4.1,
        "importance_rank": 5,
        "aor": "1.98x",
        "rationale": "Distributed querying and cloud data platforms accelerate mid-career wage expansion across metro tech clusters.",
        "roi": "1.58x Wage Accelerator",
    },
}


class AssessmentService:
    def evaluate_assessment(self, request: AssessmentRequest) -> AssessmentResponse:
        """
        Executes end-to-end evaluation:
        1. Invokes JDS champion model.
        2. Computes skill radar deltas against high-hike cohort benchmarks.
        3. Assigns career readiness quadrant.
        4. Synthesizes evidence-supported recommendations & learning stages.
        """
        # 1. Run inference through champion model
        jds_req = JDSPredictRequest(
            big_data_skills=request.big_data_skills,
            maths_stats_skills=request.maths_stats_skills,
            coding_skills=request.coding_skills,
            ai_and_ml_skills=request.ai_and_ml_skills,
            dashboard_and_storytelling_skills=request.dashboard_and_storytelling_skills,
        )
        prediction_result = model_service.predict_jds(jds_req)

        # 2. Build Skill Radar Data & identify gaps/strengths
        user_scores = {
            "maths_stats_skills": request.maths_stats_skills,
            "dashboard_and_storytelling_skills": request.dashboard_and_storytelling_skills,
            "ai_and_ml_skills": request.ai_and_ml_skills,
            "coding_skills": request.coding_skills,
            "big_data_skills": request.big_data_skills,
        }

        radar_data: List[SkillRadarPoint] = []
        strengths: List[str] = []
        development_gaps: List[str] = []
        recommendations: List[RecommendationItem] = []

        # Sort features by importance rank (Storytelling #1, Math #2, ML #3, Coding #4, Big Data #5)
        sorted_keys = sorted(
            HIGH_HIKE_BENCHMARKS.keys(),
            key=lambda k: HIGH_HIKE_BENCHMARKS[k]["importance_rank"],
        )

        for key in sorted_keys:
            info = HIGH_HIKE_BENCHMARKS[key]
            user_val = user_scores[key]
            bench = info["benchmark"]
            gap = round(bench - user_val, 2)

            radar_data.append(
                SkillRadarPoint(
                    skill_key=key,
                    skill_name=info["name"],
                    user_score=user_val,
                    cohort_benchmark=bench,
                    importance_rank=info["importance_rank"],
                )
            )

            if gap <= 0.3:
                strengths.append(f"{info['name']} ({user_val}/5.0 - Cohort Benchmark: {bench})")
                priority = "Maintain Strength"
            elif gap <= 0.8:
                development_gaps.append(f"{info['name']} (Delta: -{gap} from high-hike benchmark)")
                priority = "Secondary Focus"
            else:
                development_gaps.append(f"{info['name']} (Significant Delta: -{gap} from high-hike benchmark)")
                priority = "Immediate Priority"

            recommendations.append(
                RecommendationItem(
                    skill_name=info["name"],
                    priority_level=priority,
                    current_score=user_val,
                    target_benchmark=bench,
                    gap_delta=gap,
                    evidence_rationale=info["rationale"],
                    roi_multiplier=info["roi"],
                )
            )

        # 3. Determine Quadrant Assignment
        tech_score = (
            request.maths_stats_skills
            + request.coding_skills
            + request.ai_and_ml_skills
            + request.big_data_skills
        ) / 4.0
        narrative_score = request.dashboard_and_storytelling_skills

        if tech_score >= 3.8 and narrative_score >= 3.8:
            quadrant = "Q1"
            quadrant_title = "Q1: Advanced Career-Ready (Strategic Impact Profile)"
            readiness_summary = (
                f"Based on the observed JDS cohort, your profile demonstrates strong dual-currency alignment. "
                f"Both technical modeling rigor ({tech_score:.1f}/5.0) and executive storytelling ({narrative_score:.1f}/5.0) "
                f"align with the upper-quartile progression tier for a target role of {request.career_goal}."
            )
        elif tech_score >= 3.8 and narrative_score < 3.8:
            quadrant = "Q2"
            quadrant_title = "Q2: Pure Execution Specialist (Communication Development Priority)"
            readiness_summary = (
                f"Based on the observed JDS cohort, your technical foundations ({tech_score:.1f}/5.0) are highly competitive, "
                f"but a development gap in business storytelling ({narrative_score:.1f}/5.0 vs 4.3 benchmark) represents an evidence-supported "
                f"bottleneck for cross-functional impact and senior velocity."
            )
        elif tech_score < 3.8 and narrative_score >= 3.8:
            quadrant = "Q3"
            quadrant_title = "Q3: Strategic Facilitator (Technical Modeling Development Priority)"
            readiness_summary = (
                f"Based on the observed JDS cohort, your narrative and visualization communication ({narrative_score:.1f}/5.0) "
                f"is strong, but deepening applied statistical and machine learning foundations ({tech_score:.1f}/5.0 vs 4.5 benchmark) "
                f"is recommended to reinforce analytical defense with engineering peers."
            )
        else:
            quadrant = "Q4"
            quadrant_title = "Q4: Foundational Development (Foundational Stage)"
            readiness_summary = (
                f"Based on the observed JDS cohort, your self-assessment highlights opportunities across both core table-stakes "
                f"coding/math and storytelling dimensions. Structured, project-based capstone work is recommended to close foundational deltas."
            )

        # 4. Model Signal Language
        prob_pct = round(prediction_result.probability_high * 100, 1)
        if prediction_result.prediction == 1:
            model_signal = f"Observed-model signal: High progression alignment in observed JDS cohort ({prob_pct}% probability)"
            model_class = "High Progression Alignment"
        else:
            model_signal = f"Observed-model signal: Developing foundation alignment in observed JDS cohort ({prob_pct}% probability)"
            model_class = "Developing Foundation Alignment"

        # 5. Extract Priority Skills
        priority_skills = [
            r.skill_name for r in sorted(recommendations, key=lambda x: (-x.gap_delta, x.current_score))
            if r.priority_level in ["Immediate Priority", "Secondary Focus"]
        ]
        if not priority_skills:
            priority_skills = ["Advanced Systems Architecture & Cross-Functional Mentorship"]

        # 6. Suggested Learning Sequence (Phase 8 Framework)
        learning_sequence = [
            LearningStage(
                step=1,
                title="Immediate 30-Day Focus: Close Primary Differentiator Delta",
                timeline="Weeks 1–4",
                milestone=f"Focus on {priority_skills[0] if priority_skills else 'Storytelling'}: build an interactive stakeholder presentation for an existing project.",
                empirical_justification="Phase 5 Permutation Importance demonstrates immediate ROI when closing storytelling and math deltas.",
            ),
            LearningStage(
                step=2,
                title="Mid-Term 60-Day Focus: Dual-Artifact Project Portfolio",
                timeline="Weeks 5–8",
                milestone="Publish an end-to-end repository featuring clean modular Python pipelines, unit tests, and a deployed executive dashboard.",
                empirical_justification="Satisfies Stage-2 Junior Velocity requirements identified in Phase 8 Career Stage Matrix.",
            ),
            LearningStage(
                step=3,
                title="Quarterly Review: Whiteboard Defense & Methodology Re-Assessment",
                timeline="Weeks 9–12",
                milestone="Conduct simulated oral project defense explaining trade-offs, model leakage guards, and P&L business impact.",
                empirical_justification="Prepares candidates for Quadrant Q1 transition as documented in the Phase 8 Student Blueprint.",
            ),
        ]

        return AssessmentResponse(
            career_goal=request.career_goal,
            experience_level=request.experience_level,
            career_readiness_summary=readiness_summary,
            model_signal=model_signal,
            model_probability=prediction_result.probability_high,
            model_classification=model_class,
            quadrant_assigned=quadrant,
            quadrant_title=quadrant_title,
            radar_data=radar_data,
            priority_skills=priority_skills[:3],
            strengths=strengths if strengths else ["Developing core competencies"],
            development_gaps=development_gaps if development_gaps else ["None identified; maintain current proficiency"],
            recommendations=recommendations,
            learning_sequence=learning_sequence,
            methodology_disclaimer=ETHICAL_ASSESSMENT_DISCLAIMER,
        )


assessment_service = AssessmentService()

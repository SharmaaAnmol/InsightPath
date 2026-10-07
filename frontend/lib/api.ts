/**
 * frontend/lib/api.ts
 * Type-safe API client for InsightPath FastAPI backend
 */

export interface HealthResponse {
  status: string;
  version: string;
  service: string;
  environment: string;
  artifacts_verified: boolean;
}

export interface AssessmentRequest {
  career_goal: string;
  experience_level: string;
  maths_stats_skills: number;
  coding_skills: number;
  ai_and_ml_skills: number;
  big_data_skills: number;
  dashboard_and_storytelling_skills: number;
}

export interface SkillRadarPoint {
  skill_key: string;
  skill_name: string;
  user_score: number;
  cohort_benchmark: number;
  importance_rank: number;
}

export interface RecommendationItem {
  skill_name: string;
  priority_level: string;
  current_score: number;
  target_benchmark: number;
  gap_delta: number;
  evidence_rationale: string;
  roi_multiplier: string;
}

export interface LearningStage {
  step: number;
  title: string;
  timeline: string;
  milestone: string;
  empirical_justification: string;
}

export interface AssessmentResponse {
  career_goal: string;
  experience_level: string;
  career_readiness_summary: string;
  model_signal: string;
  model_probability: number;
  model_classification: string;
  quadrant_assigned: string;
  quadrant_title: string;
  radar_data: SkillRadarPoint[];
  priority_skills: string[];
  strengths: string[];
  development_gaps: string[];
  recommendations: RecommendationItem[];
  learning_sequence: LearningStage[];
  methodology_disclaimer: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_BASE_URL}/api/v1/health`, {
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`Health check failed with status: ${res.status}`);
  }
  return res.json();
}

/**
 * Sends self-assessment ratings to FastAPI backend (/api/v1/assessment/evaluate).
 * If the local FastAPI server is offline, falls back to local client-side evaluation
 * matching the exact JDS Logistic L2 formula and Phase 8 competencies.
 */
export async function submitAssessment(
  data: AssessmentRequest
): Promise<{ data: AssessmentResponse; source: "live_backend" | "client_fallback" }> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/assessment/evaluate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
      cache: "no-store",
    });

    if (res.ok) {
      const result: AssessmentResponse = await res.json();
      return { data: result, source: "live_backend" };
    }
  } catch {
    // Backend offline: gracefully fall back to local computation
  }

  // Client-side fallback matching Phase 5 Logistic L2 and Phase 8 Framework
  const z =
    -0.85 +
    1.28 * ((data.maths_stats_skills - 3.0) / 0.8) +
    1.17 * ((data.dashboard_and_storytelling_skills - 3.0) / 0.8) +
    0.84 * ((data.ai_and_ml_skills - 3.0) / 0.8) +
    0.48 * ((data.coding_skills - 3.0) / 0.8) +
    0.52 * ((data.big_data_skills - 3.0) / 0.8);

  const prob = Math.min(Math.max(1 / (1 + Math.exp(-z)), 0.03), 0.97);
  const isHigh = prob >= 0.5;

  const techScore =
    (data.maths_stats_skills + data.coding_skills + data.ai_and_ml_skills + data.big_data_skills) / 4.0;
  const narrativeScore = data.dashboard_and_storytelling_skills;

  let quadrant = "Q4";
  let quadrantTitle = "Q4: Foundational Development (Foundational Stage)";
  let summary = `Based on the observed JDS cohort, your self-assessment highlights opportunities across core modeling and storytelling competencies.`;

  if (techScore >= 3.8 && narrativeScore >= 3.8) {
    quadrant = "Q1";
    quadrantTitle = "Q1: Advanced Career-Ready (Strategic Impact Profile)";
    summary = `Based on the observed JDS cohort, your profile demonstrates strong dual-currency alignment across technical modeling (${techScore.toFixed(1)}/5.0) and storytelling (${narrativeScore.toFixed(1)}/5.0).`;
  } else if (techScore >= 3.8 && narrativeScore < 3.8) {
    quadrant = "Q2";
    quadrantTitle = "Q2: Pure Execution Specialist (Communication Development Priority)";
    summary = `Based on the observed JDS cohort, your technical foundations (${techScore.toFixed(1)}/5.0) are strong, but executive storytelling (${narrativeScore.toFixed(1)}/5.0 vs 4.3 benchmark) represents an evidence-supported development priority.`;
  } else if (techScore < 3.8 && narrativeScore >= 3.8) {
    quadrant = "Q3";
    quadrantTitle = "Q3: Strategic Facilitator (Technical Modeling Development Priority)";
    summary = `Based on the observed JDS cohort, your narrative presence (${narrativeScore.toFixed(1)}/5.0) is strong, but deepening applied statistical modeling (${techScore.toFixed(1)}/5.0) is recommended to reinforce analytical defense.`;
  }

  const radarData: SkillRadarPoint[] = [
    {
      skill_key: "dashboard_and_storytelling_skills",
      skill_name: "Dashboarding & Storytelling",
      user_score: data.dashboard_and_storytelling_skills,
      cohort_benchmark: 4.3,
      importance_rank: 1,
    },
    {
      skill_key: "maths_stats_skills",
      skill_name: "Mathematics & Statistics",
      user_score: data.maths_stats_skills,
      cohort_benchmark: 4.8,
      importance_rank: 2,
    },
    {
      skill_key: "ai_and_ml_skills",
      skill_name: "AI & Machine Learning",
      user_score: data.ai_and_ml_skills,
      cohort_benchmark: 4.8,
      importance_rank: 3,
    },
    {
      skill_key: "coding_skills",
      skill_name: "Coding (Python/R)",
      user_score: data.coding_skills,
      cohort_benchmark: 4.5,
      importance_rank: 4,
    },
    {
      skill_key: "big_data_skills",
      skill_name: "Big Data & Cloud",
      user_score: data.big_data_skills,
      cohort_benchmark: 4.1,
      importance_rank: 5,
    },
  ];

  const recommendations: RecommendationItem[] = radarData.map((d) => {
    const gap = Math.round((d.cohort_benchmark - d.user_score) * 10) / 10;
    const prio = gap <= 0.3 ? "Maintain Strength" : gap <= 0.8 ? "Secondary Focus" : "Immediate Priority";
    return {
      skill_name: d.skill_name,
      priority_level: prio,
      current_score: d.user_score,
      target_benchmark: d.cohort_benchmark,
      gap_delta: gap,
      evidence_rationale:
        d.importance_rank === 1
          ? "Storytelling ranks #1 in out-of-fold permutation importance (0.1089) with a 3.06x adjusted odds ratio."
          : d.importance_rank === 2
          ? "Math/Stats drives the highest single odds ratio (AOR = 3.61) in the observed cohort."
          : "Core competency essential for end-to-end data science delivery.",
      roi_multiplier: d.importance_rank === 1 ? "3.23x Odds Multiplier" : d.importance_rank === 2 ? "3.65x Odds Multiplier" : "Baseline Currency",
    };
  });

  const strengths = radarData
    .filter((d) => d.cohort_benchmark - d.user_score <= 0.3)
    .map((d) => `${d.skill_name} (${d.user_score.toFixed(1)}/5.0 - Cohort Benchmark: ${d.cohort_benchmark.toFixed(1)})`);

  const developmentGaps = radarData
    .filter((d) => d.cohort_benchmark - d.user_score > 0.3)
    .map((d) => `${d.skill_name} (Delta: -${(d.cohort_benchmark - d.user_score).toFixed(1)} from high-hike benchmark)`);

  const prioritySkills = recommendations
    .filter((r) => r.priority_level !== "Maintain Strength")
    .sort((a, b) => b.gap_delta - a.gap_delta)
    .map((r) => r.skill_name)
    .slice(0, 3);

  const fallbackResult: AssessmentResponse = {
    career_goal: data.career_goal,
    experience_level: data.experience_level,
    career_readiness_summary: summary,
    model_signal: isHigh
      ? `Observed-model signal: High progression alignment in observed JDS cohort (${(prob * 100).toFixed(1)}% probability)`
      : `Observed-model signal: Developing foundation alignment in observed JDS cohort (${(prob * 100).toFixed(1)}% probability)`,
    model_probability: prob,
    model_classification: isHigh ? "High Progression Alignment" : "Developing Foundation Alignment",
    quadrant_assigned: quadrant,
    quadrant_title: quadrantTitle,
    radar_data: radarData,
    priority_skills: prioritySkills.length > 0 ? prioritySkills : ["Advanced Systems Architecture"],
    strengths: strengths.length > 0 ? strengths : ["Developing foundational competencies"],
    development_gaps: developmentGaps.length > 0 ? developmentGaps : ["None identified; maintain current proficiency"],
    recommendations,
    learning_sequence: [
      {
        step: 1,
        title: "Immediate 30-Day Focus: Close Primary Differentiator Delta",
        timeline: "Weeks 1–4",
        milestone: `Focus on ${prioritySkills[0] || "Storytelling"}: build an interactive stakeholder presentation for an existing project.`,
        empirical_justification: "Phase 5 Permutation Importance demonstrates immediate ROI when closing storytelling and math deltas.",
      },
      {
        step: 2,
        title: "Mid-Term 60-Day Focus: Dual-Artifact Project Portfolio",
        timeline: "Weeks 5–8",
        milestone: "Publish an end-to-end repository featuring clean modular Python pipelines, unit tests, and a deployed executive dashboard.",
        empirical_justification: "Satisfies Stage-2 Junior Velocity requirements identified in Phase 8 Career Stage Matrix.",
      },
      {
        step: 3,
        title: "Quarterly Review: Whiteboard Defense & Methodology Re-Assessment",
        timeline: "Weeks 9–12",
        milestone: "Conduct simulated oral project defense explaining trade-offs, model leakage guards, and P&L business impact.",
        empirical_justification: "Prepares candidates for Quadrant Q1 transition as documented in the Phase 8 Student Blueprint.",
      },
    ],
    methodology_disclaimer:
      "METHODOLOGY & ETHICAL NOTICE: This development profile is derived from the empirical patterns observed in the N=139 Junior Data Scientist cohort of the SAS CU Hackathon research dataset. All outputs represent observed-model signals and evidence-supported development priorities. This assessment does NOT constitute a guarantee of salary, compensation, promotion, hiring eligibility, or deterministic career success. It is strictly an educational self-reflection and coaching diagnostic.",
  };

  return { data: fallbackResult, source: "client_fallback" };
}

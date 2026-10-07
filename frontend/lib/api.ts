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

export interface JDSPredictRequest {
  big_data_skills: number;
  maths_stats_skills: number;
  coding_skills: number;
  ai_and_ml_skills: number;
  dashboard_and_storytelling_skills: number;
}

export interface SDSPredictRequest {
  neuroticism: number;
  extraversion: number;
  openness_to_experience: number;
  agreeableness: number;
  conscientiousness: number;
}

export interface PredictionResponse {
  prediction: number;
  prediction_label: string;
  probability_high: number;
  probability_low: number;
  model_type: string;
  feature_contributions?: Record<string, number>;
  governance_notice?: string;
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

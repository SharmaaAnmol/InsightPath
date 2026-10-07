/**
 * frontend/lib/supabase/userService.ts
 * ------------------------------------
 * Service layer for interacting with private Supabase user data:
 * - Profiles
 * - Career Goals
 * - Empirical Assessments & Scores
 * - Interactive Career Roadmap Items
 *
 * Strict separation: All ML models and analytical outputs remain public and read-only.
 * User data enforces Row Level Security (RLS) ensuring users only read/write their own records.
 */

import { createClient, isSupabaseConfigured } from "./client.ts";
import type {
  Profile,
  CareerGoal,
  AssessmentRecord,
  AssessmentScoreRecord,
  RoadmapItemRecord,
} from "./types.ts";

const LOCAL_STORAGE_PREFIX = "insightpath_user_data_";

// In-memory backing store for SSR/Node environments
const inMemoryStore = new Map<
  string,
  {
    profile: Profile | null;
    careerGoal: CareerGoal | null;
    assessments: AssessmentRecord[];
    roadmapItems: RoadmapItemRecord[];
  }
>();

// Helper for local mock storage when running offline or without Supabase keys
function getLocalUserData(userId: string) {
  if (typeof window !== "undefined") {
    try {
      const raw = localStorage.getItem(`${LOCAL_STORAGE_PREFIX}${userId}`);
      if (raw) return JSON.parse(raw);
    } catch {
      // ignore json parse error
    }
  }
  if (inMemoryStore.has(userId)) {
    return inMemoryStore.get(userId)!;
  }
  return {
    profile: null,
    careerGoal: null,
    assessments: [] as AssessmentRecord[],
    roadmapItems: [] as RoadmapItemRecord[],
  };
}

function saveLocalUserData(
  userId: string,
  data: {
    profile: Profile | null;
    careerGoal: CareerGoal | null;
    assessments: AssessmentRecord[];
    roadmapItems: RoadmapItemRecord[];
  }
) {
  inMemoryStore.set(userId, data);
  if (typeof window !== "undefined") {
    try {
      localStorage.setItem(`${LOCAL_STORAGE_PREFIX}${userId}`, JSON.stringify(data));
    } catch {
      // ignore storage error
    }
  }
}

// Client accessor with flexible type casting for queries
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const getSupabase = (): any => createClient();

/**
 * Fetch user profile from public.profiles
 */
export async function getProfile(userId: string): Promise<Profile | null> {
  if (!isSupabaseConfigured()) {
    const data = getLocalUserData(userId);
    return data.profile || {
      id: userId,
      email: "user@insightpath.ai",
      full_name: "InsightPath Researcher",
      target_role: "Data Scientist",
      experience_level: "Junior (2-4 years)",
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };
  }

  const supabase = getSupabase();
  const { data, error } = await supabase
    .from("profiles")
    .select("*")
    .eq("id", userId)
    .single();

  if (error) {
    console.warn("Could not fetch profile from Supabase:", error.message);
    return null;
  }
  return data as Profile;
}

/**
 * Fetch career goals for user from public.career_goals
 */
export async function getCareerGoal(userId: string): Promise<CareerGoal | null> {
  if (!isSupabaseConfigured()) {
    const data = getLocalUserData(userId);
    return data.careerGoal || {
      id: "mock-goal-1",
      user_id: userId,
      target_role: "Data Scientist",
      experience_level: "Junior (2-4 years)",
      target_timeline: "6-12 months",
      target_salary_lakh: 18.5,
      key_focus_areas: ["Model Interpretability", "Executive Storytelling"],
      updated_at: new Date().toISOString(),
    };
  }

  const supabase = getSupabase();
  const { data, error } = await supabase
    .from("career_goals")
    .select("*")
    .eq("user_id", userId)
    .maybeSingle();

  if (error) {
    console.warn("Could not fetch career goal:", error.message);
    return null;
  }
  return (data as unknown) as CareerGoal | null;
}

/**
 * Update or create career goal
 */
export async function upsertCareerGoal(
  userId: string,
  goal: Partial<CareerGoal>
): Promise<CareerGoal | null> {
  const updatedPayload = {
    user_id: userId,
    target_role: goal.target_role || "Data Scientist",
    experience_level: goal.experience_level || "Junior (2-4 years)",
    target_timeline: goal.target_timeline || "6-12 months",
    target_salary_lakh: goal.target_salary_lakh || 18.5,
    key_focus_areas: goal.key_focus_areas || ["Model Interpretability", "Executive Storytelling"],
    notes: goal.notes || null,
    updated_at: new Date().toISOString(),
  };

  if (!isSupabaseConfigured()) {
    const data = getLocalUserData(userId);
    const updated = {
      ...(data.careerGoal || { id: "mock-goal-1" }),
      ...updatedPayload,
    };
    data.careerGoal = updated;
    saveLocalUserData(userId, data);
    return updated as CareerGoal;
  }

  const supabase = getSupabase();
  const { data, error } = await supabase
    .from("career_goals")
    .upsert(updatedPayload, { onConflict: "user_id" })
    .select()
    .single();

  if (error) {
    console.error("Failed to upsert career goal:", error.message);
    throw error;
  }
  return data as CareerGoal;
}

/**
 * Fetch all assessment history for user with attached scores
 */
export async function getAssessments(userId: string): Promise<AssessmentRecord[]> {
  if (!isSupabaseConfigured()) {
    const data = getLocalUserData(userId);
    return data.assessments || [];
  }

  const supabase = getSupabase();
  const { data: assessmentsData, error: assessError } = await supabase
    .from("assessments")
    .select("*")
    .eq("user_id", userId)
    .order("created_at", { ascending: false });

  if (assessError) {
    console.error("Error fetching assessments:", assessError.message);
    return [];
  }

  if (!assessmentsData || assessmentsData.length === 0) {
    return [];
  }

  // Fetch scores for all fetched assessments
  const assessmentRecords = assessmentsData as AssessmentRecord[];
  const assessmentIds = assessmentRecords.map((a) => a.id);
  const { data: scoresData, error: scoresError } = await supabase
    .from("assessment_scores")
    .select("*")
    .in("assessment_id", assessmentIds);

  if (scoresError) {
    console.warn("Could not fetch assessment scores:", scoresError.message);
  }

  const scoresRecords = (scoresData || []) as AssessmentScoreRecord[];
  const scoresByAssessmentId = scoresRecords.reduce(
    (acc: Record<string, AssessmentScoreRecord[]>, s) => {
      if (!acc[s.assessment_id]) acc[s.assessment_id] = [];
      acc[s.assessment_id].push(s);
      return acc;
    },
    {}
  );

  return assessmentRecords.map((item) => ({
    ...item,
    scores: scoresByAssessmentId[item.id] || [],
  }));
}

/**
 * Persist assessment result & radar scores
 */
export async function saveAssessmentRecord(
  userId: string,
  assessmentPayload: {
    career_goal: string;
    experience_level: string;
    model_signal: string;
    model_probability: number;
    quadrant_assigned: string;
    quadrant_title: string;
    recommendation_summary?: string;
  },
  scoresPayload: Array<{
    skill_key: string;
    skill_label: string;
    user_score: number;
    cohort_benchmark: number;
    gap: number;
    importance_rank: number;
  }>
): Promise<AssessmentRecord> {
  const newAssessmentId = crypto.randomUUID ? crypto.randomUUID() : `assess-${Date.now()}`;
  const now = new Date().toISOString();

  const assessmentRecord: AssessmentRecord = {
    id: newAssessmentId,
    user_id: userId,
    career_goal: assessmentPayload.career_goal,
    experience_level: assessmentPayload.experience_level,
    model_signal: assessmentPayload.model_signal,
    model_probability: assessmentPayload.model_probability,
    quadrant_assigned: assessmentPayload.quadrant_assigned,
    quadrant_title: assessmentPayload.quadrant_title,
    recommendation_summary: assessmentPayload.recommendation_summary || null,
    created_at: now,
  };

  const scoresRecords: AssessmentScoreRecord[] = scoresPayload.map((s, idx) => ({
    id: `${newAssessmentId}-score-${idx}`,
    assessment_id: newAssessmentId,
    skill_key: s.skill_key,
    skill_label: s.skill_label,
    user_score: s.user_score,
    cohort_benchmark: s.cohort_benchmark,
    gap: s.gap,
    importance_rank: s.importance_rank,
  }));

  if (!isSupabaseConfigured()) {
    const data = getLocalUserData(userId);
    const withScores: AssessmentRecord = {
      ...assessmentRecord,
      scores: scoresRecords,
    };
    data.assessments = [withScores, ...(data.assessments || [])];
    saveLocalUserData(userId, data);
    return withScores;
  }

  const supabase = getSupabase();
  const { data: insertedAssessment, error: assessErr } = await supabase
    .from("assessments")
    .insert({
      id: newAssessmentId,
      user_id: userId,
      career_goal: assessmentPayload.career_goal,
      experience_level: assessmentPayload.experience_level,
      model_signal: assessmentPayload.model_signal,
      model_probability: assessmentPayload.model_probability,
      quadrant_assigned: assessmentPayload.quadrant_assigned,
      quadrant_title: assessmentPayload.quadrant_title,
      recommendation_summary: assessmentPayload.recommendation_summary || null,
    })
    .select()
    .single();

  if (assessErr) {
    console.error("Error creating assessment row:", assessErr.message);
    throw assessErr;
  }

  if (scoresPayload.length > 0) {
    const { error: scoresErr } = await supabase
      .from("assessment_scores")
      .insert(
        scoresPayload.map((s) => ({
          assessment_id: newAssessmentId,
          skill_key: s.skill_key,
          skill_label: s.skill_label,
          user_score: s.user_score,
          cohort_benchmark: s.cohort_benchmark,
          gap: s.gap,
          importance_rank: s.importance_rank,
        }))
      );

    if (scoresErr) {
      console.error("Error creating assessment scores rows:", scoresErr.message);
    }
  }

  return {
    ...(insertedAssessment as AssessmentRecord),
    scores: scoresRecords,
  };
}

/**
 * Fetch user roadmap items
 */
export async function getRoadmapItems(userId: string): Promise<RoadmapItemRecord[]> {
  const defaultRoadmap: RoadmapItemRecord[] = [
    {
      id: "road-1",
      user_id: userId,
      stage_id: "stage-1",
      title: "Python & Pandas Scalability Audits",
      description: "Master vectorization, memory optimization, and unit testing pipelines.",
      milestone_order: 1,
      status: "completed",
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      id: "road-2",
      user_id: userId,
      stage_id: "stage-1",
      title: "Statistical Rigor: Inferential Testing",
      description: "Conduct Mann-Whitney U, Chi-Square, and Cohen's d effect size analyses.",
      milestone_order: 2,
      status: "in_progress",
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      id: "road-3",
      user_id: userId,
      stage_id: "stage-2",
      title: "Interpretable Machine Learning Models",
      description: "Train and evaluate Logistic Regression (L2) with Odds Ratio extraction.",
      milestone_order: 3,
      status: "todo",
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      id: "road-4",
      user_id: userId,
      stage_id: "stage-2",
      title: "Executive Storytelling & Visualization",
      description: "Translate complex ROC-AUC and feature importance into business trade-offs.",
      milestone_order: 4,
      status: "todo",
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      id: "road-5",
      user_id: userId,
      stage_id: "stage-3",
      title: "Cross-Domain Strategic Synthesis",
      description: "Bridge technical analytics with organizational decision-making matrix.",
      milestone_order: 5,
      status: "todo",
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
  ];

  if (!isSupabaseConfigured()) {
    const data = getLocalUserData(userId);
    if (!data.roadmapItems || data.roadmapItems.length === 0) {
      data.roadmapItems = defaultRoadmap;
      saveLocalUserData(userId, data);
    }
    return data.roadmapItems;
  }

  const supabase = getSupabase();
  const { data, error } = await supabase
    .from("roadmap_items")
    .select("*")
    .eq("user_id", userId)
    .order("milestone_order", { ascending: true });

  if (error) {
    console.warn("Could not fetch roadmap items:", error.message);
    return defaultRoadmap;
  }

  if (!data || data.length === 0) {
    // Seed initial roadmap items for new user
    await supabase.from("roadmap_items").insert(
      defaultRoadmap.map((item) => ({
        user_id: userId,
        stage_id: item.stage_id,
        title: item.title,
        description: item.description,
        milestone_order: item.milestone_order,
        status: item.status,
      }))
    );
    return defaultRoadmap;
  }

  return data as RoadmapItemRecord[];
}

/**
 * Toggle roadmap item status (todo, in_progress, completed)
 */
export async function updateRoadmapItemStatus(
  userId: string,
  itemId: string,
  status: "todo" | "in_progress" | "completed"
): Promise<void> {
  if (!isSupabaseConfigured()) {
    const data = getLocalUserData(userId);
    if (data.roadmapItems) {
      data.roadmapItems = data.roadmapItems.map((item: RoadmapItemRecord) =>
        item.id === itemId ? { ...item, status, updated_at: new Date().toISOString() } : item
      );
      saveLocalUserData(userId, data);
    }
    return;
  }

  const supabase = getSupabase();
  const { error } = await supabase
    .from("roadmap_items")
    .update({ status, updated_at: new Date().toISOString() })
    .eq("id", itemId)
    .eq("user_id", userId);

  if (error) {
    console.error("Error updating roadmap item status:", error.message);
    throw error;
  }
}

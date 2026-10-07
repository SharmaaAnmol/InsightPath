/**
 * frontend/lib/supabase/types.ts
 * ------------------------------
 * TypeScript interfaces and Database definitions for Supabase authentication,
 * user profiles, career goals, empirical assessments, and roadmap progress.
 */

export interface Profile {
  id: string;
  email: string;
  full_name: string;
  avatar_url?: string | null;
  target_role: string;
  experience_level: string;
  created_at: string;
  updated_at: string;
}

export interface CareerGoal {
  id: string;
  user_id: string;
  target_role: string;
  experience_level: string;
  target_timeline: string;
  target_salary_lakh: number;
  key_focus_areas: string[];
  notes?: string | null;
  updated_at: string;
}

export interface AssessmentRecord {
  id: string;
  user_id: string;
  career_goal: string;
  experience_level: string;
  model_signal: string;
  model_probability: number;
  quadrant_assigned: string;
  quadrant_title: string;
  recommendation_summary?: string | null;
  created_at: string;
  scores?: AssessmentScoreRecord[];
}

export interface AssessmentScoreRecord {
  id: string;
  assessment_id: string;
  skill_key: string;
  skill_label: string;
  user_score: number;
  cohort_benchmark: number;
  gap: number;
  importance_rank: number;
}

export interface RoadmapItemRecord {
  id: string;
  user_id: string;
  stage_id: string;
  title: string;
  description?: string | null;
  milestone_order: number;
  status: "todo" | "in_progress" | "completed";
  target_date?: string | null;
  created_at: string;
  updated_at: string;
}

export interface Database {
  public: {
    Tables: {
      profiles: {
        Row: Profile;
        Insert: Partial<Profile> & { id: string; email: string };
        Update: Partial<Profile>;
      };
      career_goals: {
        Row: CareerGoal;
        Insert: Partial<CareerGoal> & { user_id: string; target_role: string };
        Update: Partial<CareerGoal>;
      };
      assessments: {
        Row: AssessmentRecord;
        Insert: Omit<AssessmentRecord, "id" | "created_at" | "scores"> & { id?: string };
        Update: Partial<AssessmentRecord>;
      };
      assessment_scores: {
        Row: AssessmentScoreRecord;
        Insert: Omit<AssessmentScoreRecord, "id"> & { id?: string };
        Update: Partial<AssessmentScoreRecord>;
      };
      roadmap_items: {
        Row: RoadmapItemRecord;
        Insert: Omit<RoadmapItemRecord, "id" | "created_at" | "updated_at"> & { id?: string };
        Update: Partial<RoadmapItemRecord>;
      };
    };
  };
}

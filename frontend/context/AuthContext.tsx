"use client";

/**
 * frontend/context/AuthContext.tsx
 * --------------------------------
 * Unified authentication context and career profile state manager.
 * Connects with Supabase Auth (email/password) while gracefully providing
 * local development resilience when credentials are not configured.
 */

import React, { createContext, useContext, useEffect, useState } from "react";
import { User, Session } from "@supabase/supabase-js";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/client";
import type {
  Profile,
  CareerGoal,
  AssessmentRecord,
  RoadmapItemRecord,
} from "@/lib/supabase/types";
import {
  getProfile,
  getCareerGoal,
  getAssessments,
  getRoadmapItems,
  upsertCareerGoal,
  saveAssessmentRecord,
  updateRoadmapItemStatus,
} from "@/lib/supabase/userService";

interface AuthContextType {
  user: User | null;
  session: Session | null;
  profile: Profile | null;
  careerGoal: CareerGoal | null;
  assessments: AssessmentRecord[];
  roadmapItems: RoadmapItemRecord[];
  loading: boolean;
  isConfigured: boolean;
  signIn: (email: string, password: string) => Promise<{ error?: string }>;
  signUp: (
    email: string,
    password: string,
    fullName: string,
    targetRole?: string,
    experienceLevel?: string
  ) => Promise<{ error?: string }>;
  signOut: () => Promise<void>;
  updateCareerGoal: (goal: Partial<CareerGoal>) => Promise<void>;
  saveAssessment: (
    assessment: {
      career_goal: string;
      experience_level: string;
      model_signal: string;
      model_probability: number;
      quadrant_assigned: string;
      quadrant_title: string;
      recommendation_summary?: string;
    },
    scores: Array<{
      skill_key: string;
      skill_label: string;
      user_score: number;
      cohort_benchmark: number;
      gap: number;
      importance_rank: number;
    }>
  ) => Promise<AssessmentRecord>;
  toggleRoadmapItem: (itemId: string, status: "todo" | "in_progress" | "completed") => Promise<void>;
  refreshUserData: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const LOCAL_MOCK_USER_KEY = "insightpath_mock_user";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [careerGoal, setCareerGoal] = useState<CareerGoal | null>(null);
  const [assessments, setAssessments] = useState<AssessmentRecord[]>([]);
  const [roadmapItems, setRoadmapItems] = useState<RoadmapItemRecord[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const configured = isSupabaseConfigured();

  // Load user data based on user id
  const loadUserData = async (userId: string) => {
    try {
      const [userProf, goal, hist, road] = await Promise.all([
        getProfile(userId),
        getCareerGoal(userId),
        getAssessments(userId),
        getRoadmapItems(userId),
      ]);
      setProfile(userProf);
      setCareerGoal(goal);
      setAssessments(hist);
      setRoadmapItems(road);
    } catch (err) {
      console.error("Error loading user data:", err);
    }
  };

  useEffect(() => {
    if (!configured) {
      // Local simulation mode
      if (typeof window !== "undefined") {
        try {
          const raw = localStorage.getItem(LOCAL_MOCK_USER_KEY);
          if (raw) {
            const parsedUser = JSON.parse(raw);
            setUser(parsedUser);
            loadUserData(parsedUser.id);
          }
        } catch {
          // ignore error
        }
      }
      setLoading(false);
      return;
    }

    const supabase = createClient();

    // Check active session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setUser(session?.user ?? null);
      if (session?.user) {
        loadUserData(session.user.id);
      }
      setLoading(false);
    });

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      setUser(session?.user ?? null);
      if (session?.user) {
        loadUserData(session.user.id);
      } else {
        setProfile(null);
        setCareerGoal(null);
        setAssessments([]);
        setRoadmapItems([]);
      }
      setLoading(false);
    });

    return () => {
      subscription.unsubscribe();
    };
  }, [configured]);

  const signIn = async (email: string, password: string): Promise<{ error?: string }> => {
    if (!configured) {
      // Simulation mode
      if (!email.includes("@")) {
        return { error: "Please enter a valid email address." };
      }
      if (password.length < 6) {
        return { error: "Password must be at least 6 characters." };
      }
      const mockUser = {
        id: `mock-user-${btoa(email).slice(0, 8)}`,
        email,
        app_metadata: {},
        user_metadata: { full_name: email.split("@")[0] },
        aud: "authenticated",
        created_at: new Date().toISOString(),
      } as unknown as User;

      if (typeof window !== "undefined") {
        localStorage.setItem(LOCAL_MOCK_USER_KEY, JSON.stringify(mockUser));
      }
      setUser(mockUser);
      await loadUserData(mockUser.id);
      return {};
    }

    const supabase = createClient();
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      return { error: error.message };
    }

    if (data.user) {
      await loadUserData(data.user.id);
    }
    return {};
  };

  const signUp = async (
    email: string,
    password: string,
    fullName: string,
    targetRole: string = "Data Scientist",
    experienceLevel: string = "Junior (2-4 years)"
  ): Promise<{ error?: string }> => {
    if (!configured) {
      // Simulation mode
      if (!email.includes("@")) {
        return { error: "Please enter a valid email address." };
      }
      if (password.length < 6) {
        return { error: "Password must be at least 6 characters." };
      }
      const mockUser = {
        id: `mock-user-${btoa(email).slice(0, 8)}`,
        email,
        app_metadata: {},
        user_metadata: { full_name: fullName },
        aud: "authenticated",
        created_at: new Date().toISOString(),
      } as unknown as User;

      if (typeof window !== "undefined") {
        localStorage.setItem(LOCAL_MOCK_USER_KEY, JSON.stringify(mockUser));
      }
      setUser(mockUser);

      // Seed initial mock profile and goal
      const initialProfile: Profile = {
        id: mockUser.id,
        email,
        full_name: fullName,
        target_role: targetRole,
        experience_level: experienceLevel,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      setProfile(initialProfile);

      await upsertCareerGoal(mockUser.id, {
        target_role: targetRole,
        experience_level: experienceLevel,
      });

      await loadUserData(mockUser.id);
      return {};
    }

    const supabase = createClient();
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          full_name: fullName,
          target_role: targetRole,
          experience_level: experienceLevel,
        },
      },
    });

    if (error) {
      return { error: error.message };
    }

    if (data.user) {
      await loadUserData(data.user.id);
    }
    return {};
  };

  const signOut = async () => {
    if (!configured) {
      if (typeof window !== "undefined") {
        localStorage.removeItem(LOCAL_MOCK_USER_KEY);
      }
      setUser(null);
      setProfile(null);
      setCareerGoal(null);
      setAssessments([]);
      setRoadmapItems([]);
      return;
    }

    const supabase = createClient();
    await supabase.auth.signOut();
    setUser(null);
    setProfile(null);
    setCareerGoal(null);
    setAssessments([]);
    setRoadmapItems([]);
  };

  const handleUpdateCareerGoal = async (goal: Partial<CareerGoal>) => {
    if (!user) throw new Error("Must be logged in to update career goals.");
    const updated = await upsertCareerGoal(user.id, goal);
    setCareerGoal(updated);
  };

  const handleSaveAssessment = async (
    assessment: {
      career_goal: string;
      experience_level: string;
      model_signal: string;
      model_probability: number;
      quadrant_assigned: string;
      quadrant_title: string;
      recommendation_summary?: string;
    },
    scores: Array<{
      skill_key: string;
      skill_label: string;
      user_score: number;
      cohort_benchmark: number;
      gap: number;
      importance_rank: number;
    }>
  ) => {
    if (!user) throw new Error("Must be logged in to persist assessments.");
    const saved = await saveAssessmentRecord(user.id, assessment, scores);
    setAssessments((prev) => [saved, ...prev]);
    return saved;
  };

  const handleToggleRoadmapItem = async (
    itemId: string,
    status: "todo" | "in_progress" | "completed"
  ) => {
    if (!user) throw new Error("Must be logged in to update roadmap items.");
    await updateRoadmapItemStatus(user.id, itemId, status);
    setRoadmapItems((prev) =>
      prev.map((item) => (item.id === itemId ? { ...item, status } : item))
    );
  };

  const refreshUserData = async () => {
    if (user) {
      await loadUserData(user.id);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        session,
        profile,
        careerGoal,
        assessments,
        roadmapItems,
        loading,
        isConfigured: configured,
        signIn,
        signUp,
        signOut,
        updateCareerGoal: handleUpdateCareerGoal,
        saveAssessment: handleSaveAssessment,
        toggleRoadmapItem: handleToggleRoadmapItem,
        refreshUserData,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

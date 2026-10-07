"use client";

/**
 * frontend/app/profile/page.tsx
 * -----------------------------
 * Persistent User Career Profile, Assessment History & Interactive Roadmap
 * Enforces Row Level Security (RLS) data persistence.
 */

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  User,
  Target,
  Calendar,
  CheckCircle2,
  Clock,
  Circle,
  FileCheck2,
  LogOut,
  Sparkles,
  SlidersHorizontal,
  Layers,
  ShieldCheck,
  Check,
} from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { Navbar } from "@/components/Navbar";
import { Sidebar } from "@/components/Sidebar";
import { Footer } from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ProgressBar } from "@/components/ProgressBar";

const CAREER_GOALS = [
  "Data Scientist",
  "Machine Learning Engineer",
  "Analytics Consultant",
  "Data Analyst",
  "Data Architect",
];

const EXPERIENCE_LEVELS = [
  "Entry-Level (0-2 years)",
  "Junior (2-4 years)",
  "Mid-Level (4-6 years)",
  "Senior (6+ years)",
];

const TIMELINES = ["3-6 months", "6-12 months", "1-2 years", "2+ years"];

export default function ProfilePage() {
  const router = useRouter();
  const {
    user,
    profile,
    careerGoal,
    assessments,
    roadmapItems,
    loading,
    signOut,
    updateCareerGoal,
    toggleRoadmapItem,
  } = useAuth();

  const [activeTab, setActiveTab] = useState<"goals" | "history" | "roadmap">("goals");

  // Form states
  const [targetRole, setTargetRole] = useState(careerGoal?.target_role || "Data Scientist");
  const [experienceLevel, setExperienceLevel] = useState(
    careerGoal?.experience_level || "Junior (2-4 years)"
  );
  const [targetTimeline, setTargetTimeline] = useState(
    careerGoal?.target_timeline || "6-12 months"
  );
  const [targetSalary, setTargetSalary] = useState(
    careerGoal?.target_salary_lakh || 18.5
  );
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [savingGoal, setSavingGoal] = useState(false);

  // Sync state if careerGoal updates
  React.useEffect(() => {
    if (careerGoal) {
      setTargetRole(careerGoal.target_role);
      setExperienceLevel(careerGoal.experience_level);
      setTargetTimeline(careerGoal.target_timeline);
      setTargetSalary(careerGoal.target_salary_lakh);
    }
  }, [careerGoal]);

  const handleSaveGoal = async (e: React.FormEvent) => {
    e.preventDefault();
    setSavingGoal(true);
    setSaveSuccess(false);
    try {
      await updateCareerGoal({
        target_role: targetRole,
        experience_level: experienceLevel,
        target_timeline: targetTimeline,
        target_salary_lakh: Number(targetSalary),
      });
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (err) {
      console.error("Failed to save career goals:", err);
    } finally {
      setSavingGoal(false);
    }
  };

  const handleLogout = async () => {
    await signOut();
    router.push("/login");
  };

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--foreground)]">
        <Navbar />
        <main className="flex-1 flex items-center justify-center p-8">
          <div className="flex flex-col items-center gap-3">
            <div className="w-8 h-8 border-2 border-teal-500 border-t-transparent rounded-full animate-spin" />
            <p className="text-xs text-slate-500">Loading career profile...</p>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  // If unauthenticated, prompt to sign in
  if (!user) {
    return (
      <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--foreground)]">
        <Navbar />
        <main className="flex-1 flex items-center justify-center p-8">
          <div className="max-w-md w-full text-center space-y-4 p-8 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-md">
            <div className="w-12 h-12 rounded-xl bg-teal-500/10 text-teal-600 dark:text-teal-400 mx-auto flex items-center justify-center">
              <User className="w-6 h-6" />
            </div>
            <h2 className="text-xl font-bold">Authentication Required</h2>
            <p className="text-xs text-slate-500">
              Please sign in to access your persistent career profile, diagnostic history, and roadmap items.
            </p>
            <div className="pt-2 flex justify-center gap-3">
              <Link href="/login">
                <Button size="sm" className="bg-teal-600 hover:bg-teal-500 text-white text-xs">
                  Sign In
                </Button>
              </Link>
              <Link href="/signup">
                <Button size="sm" variant="outline" className="text-xs">
                  Create Account
                </Button>
              </Link>
            </div>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  const completedRoadmapCount = roadmapItems.filter((i) => i.status === "completed").length;
  const roadmapProgressPct = roadmapItems.length
    ? Math.round((completedRoadmapCount / roadmapItems.length) * 100)
    : 0;

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--foreground)]">
      <Navbar />

      <div className="flex-1 flex w-full">
        <Sidebar className="hidden lg:flex" />

        <main className="flex-1 p-4 md:p-8 max-w-6xl mx-auto w-full space-y-8">
          {/* Profile Header */}
          <div className="p-6 rounded-2xl bg-gradient-to-r from-teal-500/5 via-indigo-500/5 to-transparent border border-slate-200/80 dark:border-slate-800 backdrop-blur-xs flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-teal-500 to-indigo-600 text-white flex items-center justify-center font-bold text-xl shadow-md">
                {(profile?.full_name || user.email || "U").charAt(0).toUpperCase()}
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h1 className="text-xl font-bold text-slate-900 dark:text-slate-100">
                    {profile?.full_name || user.email?.split("@")[0]}
                  </h1>
                  <Badge variant="outline" className="border-teal-500/30 text-teal-600 dark:text-teal-400 text-[10px]">
                    {careerGoal?.target_role || "Data Scientist"}
                  </Badge>
                </div>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                  {user.email} • Member since {new Date(user.created_at || Date.now()).toLocaleDateString()}
                </p>
                <div className="flex items-center gap-2 mt-2">
                  <span className="text-[11px] font-mono text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                    <ShieldCheck className="w-3.5 h-3.5" />
                    RLS Active & Isolated
                  </span>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <Link href="/assessment">
                <Button size="sm" className="h-8 text-xs bg-teal-600 hover:bg-teal-500 text-white gap-1.5">
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Run New Assessment</span>
                </Button>
              </Link>
              <Button
                variant="outline"
                size="sm"
                onClick={handleLogout}
                className="h-8 text-xs text-rose-600 hover:text-rose-700 hover:bg-rose-50 dark:hover:bg-rose-950/20 border-rose-200 dark:border-rose-900/40 gap-1.5"
              >
                <LogOut className="w-3.5 h-3.5" />
                <span>Log Out</span>
              </Button>
            </div>
          </div>

          {/* Quick Metrics Bar */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 shadow-xs">
              <span className="text-[11px] text-slate-500 font-medium uppercase tracking-wider">
                Assessments Recorded
              </span>
              <p className="text-2xl font-bold mt-1 text-slate-900 dark:text-slate-100">
                {assessments.length}
              </p>
              <span className="text-[11px] text-teal-600 dark:text-teal-400 mt-1 block">
                {assessments.length > 0 ? "Latest: " + assessments[0].quadrant_assigned : "No runs yet"}
              </span>
            </div>

            <div className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 shadow-xs">
              <span className="text-[11px] text-slate-500 font-medium uppercase tracking-wider">
                Roadmap Milestones
              </span>
              <p className="text-2xl font-bold mt-1 text-slate-900 dark:text-slate-100">
                {completedRoadmapCount} / {roadmapItems.length}
              </p>
              <div className="mt-2">
                <ProgressBar value={roadmapProgressPct} size="sm" showPercent={false} />
              </div>
            </div>

            <div className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 shadow-xs">
              <span className="text-[11px] text-slate-500 font-medium uppercase tracking-wider">
                Target Timeline
              </span>
              <p className="text-2xl font-bold mt-1 text-slate-900 dark:text-slate-100">
                {careerGoal?.target_timeline || "6-12 months"}
              </p>
              <span className="text-[11px] text-slate-500 mt-1 block">
                Tier: {careerGoal?.experience_level || "Junior (2-4 years)"}
              </span>
            </div>
          </div>

          {/* Tab Navigation */}
          <div className="flex border-b border-slate-200 dark:border-slate-800 space-x-6">
            <button
              onClick={() => setActiveTab("goals")}
              className={`pb-3 text-xs font-semibold tracking-wide transition-colors relative flex items-center gap-2 ${
                activeTab === "goals"
                  ? "text-teal-600 dark:text-teal-400 border-b-2 border-teal-500"
                  : "text-slate-500 hover:text-slate-900 dark:hover:text-slate-300"
              }`}
            >
              <Target className="w-3.5 h-3.5" />
              <span>Career Trajectory & Goals</span>
            </button>

            <button
              onClick={() => setActiveTab("history")}
              className={`pb-3 text-xs font-semibold tracking-wide transition-colors relative flex items-center gap-2 ${
                activeTab === "history"
                  ? "text-teal-600 dark:text-teal-400 border-b-2 border-teal-500"
                  : "text-slate-500 hover:text-slate-900 dark:hover:text-slate-300"
              }`}
            >
              <FileCheck2 className="w-3.5 h-3.5" />
              <span>Assessment History ({assessments.length})</span>
            </button>

            <button
              onClick={() => setActiveTab("roadmap")}
              className={`pb-3 text-xs font-semibold tracking-wide transition-colors relative flex items-center gap-2 ${
                activeTab === "roadmap"
                  ? "text-teal-600 dark:text-teal-400 border-b-2 border-teal-500"
                  : "text-slate-500 hover:text-slate-900 dark:hover:text-slate-300"
              }`}
            >
              <Layers className="w-3.5 h-3.5" />
              <span>Interactive Roadmap State</span>
            </button>
          </div>

          {/* TAB 1: GOALS */}
          {activeTab === "goals" && (
            <div className="space-y-6">
              <div className="p-6 rounded-2xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 shadow-xs">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h2 className="text-sm font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
                      <Target className="w-4 h-4 text-teal-500" />
                      Configure Career Trajectory
                    </h2>
                    <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                      Updates saved here calibrate the benchmarks shown across your diagnostic reports.
                    </p>
                  </div>
                  {saveSuccess && (
                    <div className="flex items-center gap-1.5 text-xs text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-md border border-emerald-500/20">
                      <Check className="w-3.5 h-3.5" />
                      <span>Saved successfully!</span>
                    </div>
                  )}
                </div>

                <form onSubmit={handleSaveGoal} className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-1.5">
                      <label className="text-xs font-medium text-slate-700 dark:text-slate-300">
                        Target Role in Market
                      </label>
                      <select
                        value={targetRole}
                        onChange={(e) => setTargetRole(e.target.value)}
                        className="w-full h-9 rounded-md border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/60 px-3 text-xs text-slate-900 dark:text-slate-100 focus:outline-hidden focus:ring-2 focus:ring-teal-500"
                      >
                        {CAREER_GOALS.map((r) => (
                          <option key={r} value={r}>
                            {r}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="space-y-1.5">
                      <label className="text-xs font-medium text-slate-700 dark:text-slate-300">
                        Experience Tier
                      </label>
                      <select
                        value={experienceLevel}
                        onChange={(e) => setExperienceLevel(e.target.value)}
                        className="w-full h-9 rounded-md border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/60 px-3 text-xs text-slate-900 dark:text-slate-100 focus:outline-hidden focus:ring-2 focus:ring-teal-500"
                      >
                        {EXPERIENCE_LEVELS.map((exp) => (
                          <option key={exp} value={exp}>
                            {exp}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="space-y-1.5">
                      <label className="text-xs font-medium text-slate-700 dark:text-slate-300">
                        Target Transition Timeline
                      </label>
                      <select
                        value={targetTimeline}
                        onChange={(e) => setTargetTimeline(e.target.value)}
                        className="w-full h-9 rounded-md border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/60 px-3 text-xs text-slate-900 dark:text-slate-100 focus:outline-hidden focus:ring-2 focus:ring-teal-500"
                      >
                        {TIMELINES.map((t) => (
                          <option key={t} value={t}>
                            {t}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="space-y-1.5">
                      <label className="text-xs font-medium text-slate-700 dark:text-slate-300">
                        Target Annual Compensation (Lakh INR)
                      </label>
                      <input
                        type="number"
                        step="0.5"
                        min="5"
                        max="80"
                        value={targetSalary}
                        onChange={(e) => setTargetSalary(Number(e.target.value))}
                        className="w-full h-9 rounded-md border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/60 px-3 text-xs text-slate-900 dark:text-slate-100 focus:outline-hidden focus:ring-2 focus:ring-teal-500"
                      />
                    </div>
                  </div>

                  <div className="pt-2 flex justify-end">
                    <Button
                      type="submit"
                      disabled={savingGoal}
                      className="text-xs h-9 bg-slate-900 hover:bg-slate-800 dark:bg-teal-500 dark:hover:bg-teal-400 dark:text-slate-950 text-white font-medium shadow-xs"
                    >
                      {savingGoal ? "Saving..." : "Save Goal Calibration"}
                    </Button>
                  </div>
                </form>
              </div>
            </div>
          )}

          {/* TAB 2: ASSESSMENT HISTORY */}
          {activeTab === "history" && (
            <div className="space-y-4">
              {assessments.length === 0 ? (
                <div className="p-8 text-center rounded-2xl border border-dashed border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/30 space-y-3">
                  <div className="w-12 h-12 rounded-xl bg-teal-500/10 text-teal-600 dark:text-teal-400 mx-auto flex items-center justify-center">
                    <SlidersHorizontal className="w-6 h-6" />
                  </div>
                  <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                    No Diagnostic Runs Recorded Yet
                  </h3>
                  <p className="text-xs text-slate-500 max-w-sm mx-auto">
                    Take the empirical career-readiness assessment to calculate your model signal and persist your skill breakdown.
                  </p>
                  <Link href="/assessment">
                    <Button size="sm" className="text-xs bg-teal-600 hover:bg-teal-500 text-white mt-2">
                      Start Diagnostic
                    </Button>
                  </Link>
                </div>
              ) : (
                assessments.map((a) => (
                  <div
                    key={a.id}
                    className="p-5 rounded-2xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 shadow-xs space-y-4"
                  >
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 dark:border-slate-800/80 pb-3">
                      <div className="flex items-center gap-3">
                        <Badge
                          variant="outline"
                          className={`text-xs font-mono font-bold px-2 py-0.5 ${
                            a.quadrant_assigned === "Q1"
                              ? "bg-emerald-500/10 text-emerald-600 border-emerald-500/30"
                              : a.quadrant_assigned === "Q2"
                              ? "bg-indigo-500/10 text-indigo-600 border-indigo-500/30"
                              : a.quadrant_assigned === "Q3"
                              ? "bg-amber-500/10 text-amber-600 border-amber-500/30"
                              : "bg-slate-500/10 text-slate-600 border-slate-500/30"
                          }`}
                        >
                          {a.quadrant_assigned} • {a.quadrant_title}
                        </Badge>
                        <span className="text-xs text-slate-500">
                          {a.career_goal} ({a.experience_level})
                        </span>
                      </div>
                      <div className="flex items-center gap-2 text-xs text-slate-400 font-mono">
                        <Calendar className="w-3.5 h-3.5" />
                        <span>{new Date(a.created_at).toLocaleDateString()}</span>
                      </div>
                    </div>

                    <div className="text-xs text-slate-600 dark:text-slate-300">
                      <strong className="font-semibold text-slate-900 dark:text-slate-100">
                        {a.model_signal}
                      </strong>{" "}
                      (Observed probability: {((a.model_probability || 0) * 100).toFixed(1)}%)
                    </div>

                    {a.scores && a.scores.length > 0 && (
                      <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 pt-2">
                        {a.scores.map((sc) => (
                          <div
                            key={sc.id}
                            className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800/40 border border-slate-100 dark:border-slate-800 text-center"
                          >
                            <span className="text-[10px] text-slate-500 block truncate">
                              {sc.skill_label}
                            </span>
                            <span className="text-sm font-bold text-slate-900 dark:text-slate-100">
                              {sc.user_score.toFixed(1)} / 5.0
                            </span>
                            <span className="text-[10px] text-teal-600 dark:text-teal-400 block mt-0.5">
                              Bench: {sc.cohort_benchmark.toFixed(1)}
                            </span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          )}

          {/* TAB 3: INTERACTIVE ROADMAP STATE */}
          {activeTab === "roadmap" && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-sm font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
                    <Layers className="w-4 h-4 text-teal-500" />
                    Personal Milestone Tracker
                  </h2>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                    Click status badges to advance your progression across curriculum stages.
                  </p>
                </div>
                <div className="text-xs font-mono text-teal-600 dark:text-teal-400 font-semibold">
                  {completedRoadmapCount} of {roadmapItems.length} Complete ({roadmapProgressPct}%)
                </div>
              </div>

              <div className="space-y-3">
                {roadmapItems.map((item) => (
                  <div
                    key={item.id}
                    className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4 transition-colors"
                  >
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] font-mono uppercase px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-500">
                          {item.stage_id}
                        </span>
                        <h4 className="text-xs font-semibold text-slate-900 dark:text-slate-100">
                          {item.title}
                        </h4>
                      </div>
                      <p className="text-xs text-slate-500 dark:text-slate-400">
                        {item.description}
                      </p>
                    </div>

                    <div className="flex items-center gap-2 shrink-0">
                      <button
                        onClick={() =>
                          toggleRoadmapItem(
                            item.id,
                            item.status === "completed"
                              ? "todo"
                              : item.status === "in_progress"
                              ? "completed"
                              : "in_progress"
                          )
                        }
                        className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-colors ${
                          item.status === "completed"
                            ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20"
                            : item.status === "in_progress"
                            ? "bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20"
                            : "bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700"
                        }`}
                      >
                        {item.status === "completed" ? (
                          <>
                            <CheckCircle2 className="w-3.5 h-3.5" />
                            <span>Completed</span>
                          </>
                        ) : item.status === "in_progress" ? (
                          <>
                            <Clock className="w-3.5 h-3.5" />
                            <span>In Progress</span>
                          </>
                        ) : (
                          <>
                            <Circle className="w-3.5 h-3.5" />
                            <span>To Do</span>
                          </>
                        )}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </main>
      </div>

      <Footer />
    </div>
  );
}

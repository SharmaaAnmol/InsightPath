"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  SlidersHorizontal,
  Sparkles,
  ShieldAlert,
  ArrowRight,
  RotateCcw,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  FileCheck2,
  Target,
  Clock,
  Printer,
  Compass,
} from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Sidebar } from "@/components/Sidebar";
import { Footer } from "@/components/Footer";
import { RadarChart } from "@/components/RadarChart";
import { ProgressBar } from "@/components/ProgressBar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  submitAssessment,
  AssessmentRequest,
  AssessmentResponse,
} from "@/lib/api";
import { useAuth } from "@/context/AuthContext";

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

const PRESETS = [
  {
    name: "Pure Coder (Q2 Archetype)",
    tag: "Technical Heavy / Communication Gap",
    goal: "Machine Learning Engineer",
    exp: "Junior (2-4 years)",
    scores: {
      maths_stats: 4.6,
      coding: 4.8,
      ai_ml: 4.5,
      big_data: 4.0,
      storytelling: 2.2,
    },
  },
  {
    name: "Business Facilitator (Q3 Archetype)",
    tag: "High Narrative / Technical Depth Need",
    goal: "Analytics Consultant",
    exp: "Junior (2-4 years)",
    scores: {
      maths_stats: 2.6,
      coding: 2.8,
      ai_ml: 2.5,
      big_data: 2.4,
      storytelling: 4.7,
    },
  },
  {
    name: "Executive Ready (Q1 Archetype)",
    tag: "High Dual-Currency Mastery",
    goal: "Data Scientist",
    exp: "Mid-Level (4-6 years)",
    scores: {
      maths_stats: 4.7,
      coding: 4.5,
      ai_ml: 4.6,
      big_data: 4.2,
      storytelling: 4.5,
    },
  },
  {
    name: "Fresh Graduate (Q4 Archetype)",
    tag: "Foundational Development Need",
    goal: "Data Analyst",
    exp: "Entry-Level (0-2 years)",
    scores: {
      maths_stats: 2.8,
      coding: 3.0,
      ai_ml: 2.5,
      big_data: 2.2,
      storytelling: 2.5,
    },
  },
];

export default function AssessmentPage() {
  // Form State
  const [careerGoal, setCareerGoal] = useState<string>("Data Scientist");
  const [experienceLevel, setExperienceLevel] = useState<string>("Junior (2-4 years)");
  const [scores, setScores] = useState({
    maths_stats_skills: 3.8,
    coding_skills: 4.0,
    ai_and_ml_skills: 3.6,
    big_data_skills: 3.2,
    dashboard_and_storytelling_skills: 3.0,
  });

  // Submission & Result State
  const { user, saveAssessment } = useAuth();
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AssessmentResponse | null>(null);
  const [resultSource, setResultSource] = useState<"live_backend" | "client_fallback" | null>(null);
  const [savedToProfile, setSavedToProfile] = useState<boolean>(false);

  const applyPreset = (preset: (typeof PRESETS)[0]) => {
    setCareerGoal(preset.goal);
    setExperienceLevel(preset.exp);
    setScores({
      maths_stats_skills: preset.scores.maths_stats,
      coding_skills: preset.scores.coding,
      ai_and_ml_skills: preset.scores.ai_ml,
      big_data_skills: preset.scores.big_data,
      dashboard_and_storytelling_skills: preset.scores.storytelling,
    });
  };

  const resetForm = () => {
    setScores({
      maths_stats_skills: 3.8,
      coding_skills: 4.0,
      ai_and_ml_skills: 3.6,
      big_data_skills: 3.2,
      dashboard_and_storytelling_skills: 3.0,
    });
    setResult(null);
    setError(null);
    setSavedToProfile(false);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSavedToProfile(false);

    // Validate bounds
    const vals = Object.values(scores);
    if (vals.some((v) => v < 1.0 || v > 5.0 || isNaN(v))) {
      setError("Please ensure all skill scores are between 1.0 and 5.0.");
      setLoading(false);
      return;
    }

    const payload: AssessmentRequest = {
      career_goal: careerGoal,
      experience_level: experienceLevel,
      maths_stats_skills: scores.maths_stats_skills,
      coding_skills: scores.coding_skills,
      ai_and_ml_skills: scores.ai_and_ml_skills,
      big_data_skills: scores.big_data_skills,
      dashboard_and_storytelling_skills: scores.dashboard_and_storytelling_skills,
    };

    try {
      const { data, source } = await submitAssessment(payload);
      setResult(data);
      setResultSource(source);

      // Auto-save to Supabase if authenticated
      if (user) {
        try {
          const scoresPayload = (data.radar_data || []).map((r) => ({
            skill_key: r.skill_key,
            skill_label: r.skill_name,
            user_score: Number(r.user_score),
            cohort_benchmark: Number(r.cohort_benchmark),
            gap: Number((r.user_score - r.cohort_benchmark).toFixed(2)),
            importance_rank: Number(r.importance_rank),
          }));

          await saveAssessment(
            {
              career_goal: data.career_goal,
              experience_level: data.experience_level,
              model_signal: data.model_signal,
              model_probability: data.model_probability,
              quadrant_assigned: data.quadrant_assigned,
              quadrant_title: data.quadrant_title,
              recommendation_summary: data.career_readiness_summary,
            },
            scoresPayload
          );
          setSavedToProfile(true);
        } catch (saveErr) {
          console.warn("Could not auto-save to user profile:", saveErr);
        }
      }

      // Scroll to top of results smoothly
      window.scrollTo({ top: 120, behavior: "smooth" });
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to evaluate assessment.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--foreground)]">
      <Navbar />

      <div className="flex-1 flex w-full">
        <Sidebar className="hidden lg:flex" />

        <main className="flex-1 p-4 md:p-8 max-w-6xl mx-auto w-full space-y-8">
          {/* Header */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-200/80 dark:border-slate-800">
            <div>
              <div className="flex items-center space-x-2 text-xs font-semibold uppercase tracking-wider text-teal-600 dark:text-teal-400 mb-1.5">
                <SlidersHorizontal className="w-3.5 h-3.5" />
                <span>Empirical Development Diagnostic</span>
              </div>
              <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
                Interactive Career-Readiness Assessment
              </h1>
              <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                Evaluate your technical modeling and storytelling competencies against the observed N=139 Junior Data Scientist cohort.
              </p>
            </div>

            <div className="flex items-center space-x-2">
              {result && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setResult(null)}
                  className="text-xs h-9 flex items-center space-x-1.5"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                  <span>Modify Scores</span>
                </Button>
              )}
              <Link href="/methodology">
                <Button variant="ghost" size="sm" className="text-xs h-9 text-slate-500 hover:text-slate-900 dark:hover:text-slate-100">
                  <FileCheck2 className="w-3.5 h-3.5 mr-1" />
                  Audit Methodology
                </Button>
              </Link>
            </div>
          </div>

          {/* Mandatory Ethical Notice Banner */}
          <div className="p-4 rounded-xl border border-amber-500/30 bg-amber-500/10 dark:bg-amber-500/5 text-amber-900 dark:text-amber-200 text-xs flex items-start space-x-3">
            <ShieldAlert className="w-5 h-5 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
            <div className="space-y-1">
              <div className="font-semibold text-xs tracking-wide uppercase text-amber-800 dark:text-amber-300">
                Methodology & Ethical Safeguard Commitment
              </div>
              <p className="text-[11px] text-amber-700 dark:text-amber-300/80 leading-relaxed">
                This diagnostic simulator is strictly an educational self-reflection and mentoring instrument based on patterns observed in the research cohort. Under project ethical governance, all outputs represent <strong>observed-model signals</strong> and <strong>development priorities</strong>. This model does NOT provide any guarantee of salary, compensation, promotion, hiring eligibility, or deterministic career progression.
              </p>
            </div>
          </div>

          {/* LOADING STATE */}
          {loading && (
            <div className="p-12 rounded-xl border border-teal-500/30 bg-white dark:bg-slate-900/80 flex flex-col items-center justify-center space-y-4 text-center">
              <div className="w-10 h-10 rounded-full border-3 border-teal-500/20 border-t-teal-500 animate-spin" />
              <div className="space-y-1">
                <h3 className="text-base font-bold text-slate-900 dark:text-slate-100">
                  Evaluating Profile Against Serialized JDS Champion Model...
                </h3>
                <p className="text-xs text-slate-500 dark:text-slate-400 max-w-md">
                  Processing input scores through the validated Logistic Regression L2 pipeline and synthesizing Phase 8 competency priorities.
                </p>
              </div>
            </div>
          )}

          {/* ERROR STATE */}
          {error && !loading && (
            <div className="p-4 rounded-xl border border-rose-500/30 bg-rose-500/10 text-rose-800 dark:text-rose-300 text-xs flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <AlertCircle className="w-4 h-4 text-rose-500 shrink-0" />
                <span>{error}</span>
              </div>
              <Button size="sm" variant="outline" onClick={() => setError(null)} className="h-7 text-xs">
                Dismiss
              </Button>
            </div>
          )}

          {/* ========================================================================= */}
          {/* ASSESSMENT FORM VIEW (When no result is active) */}
          {/* ========================================================================= */}
          {!result && !loading && (
            <div className="space-y-8">
              {/* Presets */}
              <div className="space-y-2">
                <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                  Quick Benchmark Archetypes
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                  {PRESETS.map((p) => (
                    <button
                      key={p.name}
                      type="button"
                      onClick={() => applyPreset(p)}
                      className="p-3.5 text-left rounded-lg border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 hover:border-teal-500/50 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-all text-xs group"
                    >
                      <div className="font-semibold text-slate-800 dark:text-slate-200 group-hover:text-teal-600 dark:group-hover:text-teal-400">
                        {p.name}
                      </div>
                      <div className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">{p.tag}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Form Card */}
              <form onSubmit={handleSubmit} className="p-6 md:p-8 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-8">
                {/* Context Selectors */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 pb-6 border-b border-slate-100 dark:border-slate-800/80">
                  <div className="space-y-2">
                    <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                      Target Career Goal
                    </label>
                    <select
                      value={careerGoal}
                      onChange={(e) => setCareerGoal(e.target.value)}
                      className="w-full h-9 rounded-md border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950 px-3 text-xs focus:outline-none focus:ring-1 focus:ring-teal-500"
                    >
                      {CAREER_GOALS.map((g) => (
                        <option key={g} value={g}>
                          {g}
                        </option>
                      ))}
                    </select>
                    <p className="text-[11px] text-slate-400">
                      Evaluates required competency envelopes against market demand.
                    </p>
                  </div>

                  <div className="space-y-2">
                    <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                      Current Experience Level
                    </label>
                    <select
                      value={experienceLevel}
                      onChange={(e) => setExperienceLevel(e.target.value)}
                      className="w-full h-9 rounded-md border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950 px-3 text-xs focus:outline-none focus:ring-1 focus:ring-teal-500"
                    >
                      {EXPERIENCE_LEVELS.map((exp) => (
                        <option key={exp} value={exp}>
                          {exp}
                        </option>
                      ))}
                    </select>
                    <p className="text-[11px] text-slate-400">
                      Calibrates milestone horizons in the learning sequence.
                    </p>
                  </div>
                </div>

                {/* Core Competency Sliders */}
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100">
                        Technical & Storytelling Skill Ratings
                      </h3>
                      <p className="text-xs text-slate-500 dark:text-slate-400">
                        Input ratings on the standardized 1.0 to 5.0 scale documented in the JDS analytical dataset.
                      </p>
                    </div>
                    <span className="text-xs font-mono text-teal-600 dark:text-teal-400 font-semibold">
                      Scale: 1.0 (Basic) → 5.0 (Advanced)
                    </span>
                  </div>

                  <div className="space-y-6 pt-2">
                    {/* Mathematics & Statistics */}
                    <div className="p-4 rounded-lg bg-slate-50/70 dark:bg-slate-950/40 border border-slate-200/60 dark:border-slate-800/80 space-y-2">
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 text-xs">
                        <div>
                          <span className="font-semibold text-slate-900 dark:text-slate-100">
                            1. Mathematics & Statistics Skills
                          </span>
                          <span className="ml-2 text-[10px] font-mono text-teal-600 dark:text-teal-400 font-semibold">
                            β = +1.28 • AOR = 3.61x • Highest Odds Ratio Lever
                          </span>
                        </div>
                        <span className="font-mono font-bold text-sm text-teal-600 dark:text-teal-400">
                          {scores.maths_stats_skills.toFixed(1)} / 5.0
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-500 dark:text-slate-400">
                        Hypothesis testing, probability distributions, regression assumptions, and statistical inference depth.
                      </p>
                      <input
                        type="range"
                        min="1.0"
                        max="5.0"
                        step="0.1"
                        value={scores.maths_stats_skills}
                        onChange={(e) =>
                          setScores({ ...scores, maths_stats_skills: parseFloat(e.target.value) })
                        }
                        className="w-full accent-teal-500 cursor-pointer h-2 bg-slate-200 dark:bg-slate-800 rounded-lg"
                      />
                    </div>

                    {/* Dashboarding & Storytelling */}
                    <div className="p-4 rounded-lg bg-slate-50/70 dark:bg-slate-950/40 border border-slate-200/60 dark:border-slate-800/80 space-y-2">
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 text-xs">
                        <div>
                          <span className="font-semibold text-slate-900 dark:text-slate-100">
                            2. Dashboarding & Storytelling Skills
                          </span>
                          <span className="ml-2 text-[10px] font-mono text-indigo-500 font-semibold">
                            Rank #1 Permutation Importance (0.1089) • AOR = 3.06x
                          </span>
                        </div>
                        <span className="font-mono font-bold text-sm text-indigo-500">
                          {scores.dashboard_and_storytelling_skills.toFixed(1)} / 5.0
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-500 dark:text-slate-400">
                        Translating models into executive P&L insights, interactive PowerBI/Tableau dashboards, and oral stakeholder presentations.
                      </p>
                      <input
                        type="range"
                        min="1.0"
                        max="5.0"
                        step="0.1"
                        value={scores.dashboard_and_storytelling_skills}
                        onChange={(e) =>
                          setScores({
                            ...scores,
                            dashboard_and_storytelling_skills: parseFloat(e.target.value),
                          })
                        }
                        className="w-full accent-indigo-500 cursor-pointer h-2 bg-slate-200 dark:bg-slate-800 rounded-lg"
                      />
                    </div>

                    {/* AI & Machine Learning */}
                    <div className="p-4 rounded-lg bg-slate-50/70 dark:bg-slate-950/40 border border-slate-200/60 dark:border-slate-800/80 space-y-2">
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 text-xs">
                        <div>
                          <span className="font-semibold text-slate-900 dark:text-slate-100">
                            3. AI & Machine Learning Skills
                          </span>
                          <span className="ml-2 text-[10px] font-mono text-cyan-500 font-semibold">
                            β = +0.76 • AOR = 2.14x • Core Modeling Competency
                          </span>
                        </div>
                        <span className="font-mono font-bold text-sm text-cyan-500">
                          {scores.ai_and_ml_skills.toFixed(1)} / 5.0
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-500 dark:text-slate-400">
                        Supervised & unsupervised learning, scikit-learn cross-validation pipelines, feature selection, and leakage prevention.
                      </p>
                      <input
                        type="range"
                        min="1.0"
                        max="5.0"
                        step="0.1"
                        value={scores.ai_and_ml_skills}
                        onChange={(e) =>
                          setScores({ ...scores, ai_and_ml_skills: parseFloat(e.target.value) })
                        }
                        className="w-full accent-cyan-500 cursor-pointer h-2 bg-slate-200 dark:bg-slate-800 rounded-lg"
                      />
                    </div>

                    {/* Coding Skills */}
                    <div className="p-4 rounded-lg bg-slate-50/70 dark:bg-slate-950/40 border border-slate-200/60 dark:border-slate-800/80 space-y-2">
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 text-xs">
                        <div>
                          <span className="font-semibold text-slate-900 dark:text-slate-100">
                            4. Coding Skills (Python / R)
                          </span>
                          <span className="ml-2 text-[10px] font-mono text-slate-400 font-semibold">
                            Table-Stakes Currency • 39.5% Prevalence Requirement
                          </span>
                        </div>
                        <span className="font-mono font-bold text-sm text-slate-700 dark:text-slate-300">
                          {scores.coding_skills.toFixed(1)} / 5.0
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-500 dark:text-slate-400">
                        Clean modular Python code, unit testing, vectorization (pandas/numpy), and Git version control workflows.
                      </p>
                      <input
                        type="range"
                        min="1.0"
                        max="5.0"
                        step="0.1"
                        value={scores.coding_skills}
                        onChange={(e) =>
                          setScores({ ...scores, coding_skills: parseFloat(e.target.value) })
                        }
                        className="w-full accent-slate-500 cursor-pointer h-2 bg-slate-200 dark:bg-slate-800 rounded-lg"
                      />
                    </div>

                    {/* Big Data & Cloud */}
                    <div className="p-4 rounded-lg bg-slate-50/70 dark:bg-slate-950/40 border border-slate-200/60 dark:border-slate-800/80 space-y-2">
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 text-xs">
                        <div>
                          <span className="font-semibold text-slate-900 dark:text-slate-100">
                            5. Big Data & Cloud Skills
                          </span>
                          <span className="ml-2 text-[10px] font-mono text-slate-400 font-semibold">
                            Wage Expansion Currency • AOR = 1.98x
                          </span>
                        </div>
                        <span className="font-mono font-bold text-sm text-slate-700 dark:text-slate-300">
                          {scores.big_data_skills.toFixed(1)} / 5.0
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-500 dark:text-slate-400">
                        Distributed processing (Spark/PySpark), SQL query plan optimization, and cloud storage paradigms.
                      </p>
                      <input
                        type="range"
                        min="1.0"
                        max="5.0"
                        step="0.1"
                        value={scores.big_data_skills}
                        onChange={(e) =>
                          setScores({ ...scores, big_data_skills: parseFloat(e.target.value) })
                        }
                        className="w-full accent-slate-500 cursor-pointer h-2 bg-slate-200 dark:bg-slate-800 rounded-lg"
                      />
                    </div>
                  </div>
                </div>

                {/* Form Submit Footer */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-4 border-t border-slate-100 dark:border-slate-800/80">
                  <Button
                    type="button"
                    variant="ghost"
                    onClick={resetForm}
                    className="text-xs text-slate-500 hover:text-slate-900 dark:hover:text-slate-100"
                  >
                    Reset to Defaults
                  </Button>

                  <Button
                    type="submit"
                    className="bg-teal-600 hover:bg-teal-500 text-white font-medium text-xs h-10 px-6 shadow-sm flex items-center space-x-2"
                  >
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>Generate Evidence-Based Profile</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Button>
                </div>
              </form>
            </div>
          )}

          {/* ========================================================================= */}
          {/* RESULT PROFILE VIEW (Rendered after submission) */}
          {/* ========================================================================= */}
          {result && !loading && (
            <div className="space-y-8 animate-in fade-in-50 duration-300">
              {/* Result Meta Bar */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60">
                <div className="flex items-center space-x-3 text-xs">
                  <Badge variant="outline" className="font-mono text-teal-600 dark:text-teal-400 border-teal-500/30">
                    Goal: {result.career_goal}
                  </Badge>
                  <span className="text-slate-400">•</span>
                  <span className="text-slate-600 dark:text-slate-300">{result.experience_level}</span>
                  <span className="text-slate-400">•</span>
                  <span className="text-slate-500 dark:text-slate-400">
                    Source: {resultSource === "live_backend" ? "FastAPI Live Endpoint" : "Client Engine Fallback"}
                  </span>
                </div>

                <div className="flex items-center space-x-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => window.print()}
                    className="h-8 text-xs flex items-center space-x-1.5"
                  >
                    <Printer className="w-3 h-3" />
                    <span>Print / Save</span>
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setResult(null)}
                    className="h-8 text-xs text-teal-600 dark:text-teal-400"
                  >
                    <RotateCcw className="w-3 h-3 mr-1" />
                    Retake
                  </Button>
                </div>
              </div>

              {/* Profile Persistence Status */}
              {savedToProfile ? (
                <div className="p-3.5 rounded-xl border border-emerald-500/30 bg-emerald-500/10 dark:bg-emerald-500/5 text-emerald-800 dark:text-emerald-300 text-xs flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0" />
                    <span>
                      Diagnostic scores successfully saved to your persistent profile &amp; roadmap history.
                    </span>
                  </div>
                  <Link
                    href="/profile"
                    className="text-xs font-semibold underline text-emerald-700 dark:text-emerald-300 hover:text-emerald-900"
                  >
                    View in Profile →
                  </Link>
                </div>
              ) : !user ? (
                <div className="p-3.5 rounded-xl border border-indigo-500/20 bg-indigo-500/5 text-slate-700 dark:text-slate-300 text-xs flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div className="flex items-center space-x-2">
                    <Sparkles className="w-4 h-4 text-indigo-500 shrink-0" />
                    <span>
                      Viewing evaluation in guest mode. Create a profile to save diagnostic history and calibrate roadmap milestones.
                    </span>
                  </div>
                  <Link
                    href="/signup"
                    className="text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:underline shrink-0"
                  >
                    Create Profile & Save →
                  </Link>
                </div>
              ) : null}

              {/* 1. Career Readiness Summary & Model Signal */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="md:col-span-2 p-6 rounded-xl border border-teal-500/30 bg-teal-500/5 dark:bg-teal-950/20 space-y-4">
                  <div className="flex items-center space-x-2 text-xs font-semibold uppercase tracking-wider text-teal-700 dark:text-teal-400">
                    <Compass className="w-4 h-4 text-teal-500" />
                    <span>Career Readiness Summary</span>
                  </div>
                  <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100">
                    {result.quadrant_title}
                  </h2>
                  <p className="text-xs text-slate-700 dark:text-slate-300 leading-relaxed">
                    {result.career_readiness_summary}
                  </p>
                  <div className="pt-2 flex items-center space-x-3 text-xs">
                    <span className="font-semibold text-slate-800 dark:text-slate-200">Matrix Position:</span>
                    <Badge variant="default" className="bg-teal-600 text-white font-mono text-xs">
                      Quadrant {result.quadrant_assigned}
                    </Badge>
                  </div>
                </div>

                {/* Model Signal Card */}
                <div className="p-6 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-4 flex flex-col justify-between">
                  <div className="space-y-2">
                    <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">
                      Observed-Model Signal
                    </span>
                    <div className="text-2xl font-bold font-mono text-teal-600 dark:text-teal-400">
                      {(result.model_probability * 100).toFixed(1)}%
                    </div>
                    <p className="text-xs text-slate-500 dark:text-slate-400 leading-snug">
                      {result.model_signal}
                    </p>
                  </div>

                  <div className="space-y-1.5 pt-2">
                    <ProgressBar
                      value={result.model_probability * 100}
                      color={result.model_probability >= 0.5 ? "teal" : "amber"}
                    />
                    <div className="flex justify-between text-[10px] text-slate-400 font-mono">
                      <span>Threshold: 50.0%</span>
                      <span>Phase 5 Champion ROC-AUC: 0.9035</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* 2. Skill Radar Chart & Breakdown Table */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-center p-6 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60">
                <div className="space-y-3">
                  <div className="space-y-1">
                    <h3 className="text-base font-bold text-slate-900 dark:text-slate-100">
                      Competency Radar vs. High-Hike Cohort
                    </h3>
                    <p className="text-xs text-slate-500 dark:text-slate-400">
                      Visualizing your self-assessment against the empirical Class-1 mean scores of the observed JDS cohort.
                    </p>
                  </div>
                  <RadarChart data={result.radar_data} size={320} />
                </div>

                {/* Breakdown List */}
                <div className="space-y-3">
                  <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                    Dimension Score Breakdown
                  </div>
                  <div className="space-y-2.5">
                    {result.radar_data.map((r) => {
                      const delta = Math.round((r.cohort_benchmark - r.user_score) * 10) / 10;
                      return (
                        <div
                          key={r.skill_key}
                          className="p-3 rounded-lg border border-slate-200/60 dark:border-slate-800/80 bg-slate-50/50 dark:bg-slate-950/40 text-xs flex items-center justify-between"
                        >
                          <div>
                            <span className="font-semibold text-slate-800 dark:text-slate-200 block">
                              {r.skill_name}
                            </span>
                            <span className="text-[10px] text-slate-500">
                              Cohort Benchmark: {r.cohort_benchmark.toFixed(1)} / 5.0
                            </span>
                          </div>
                          <div className="text-right">
                            <span className="font-mono font-bold text-slate-900 dark:text-slate-100">
                              {r.user_score.toFixed(1)}
                            </span>
                            <span
                              className={`block text-[10px] font-mono font-semibold ${
                                delta <= 0.3 ? "text-emerald-500" : "text-amber-500"
                              }`}
                            >
                              {delta <= 0 ? "Above Benchmark" : `-${delta.toFixed(1)} Delta`}
                            </span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>

              {/* 3. Strengths & Development Gaps */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Strengths */}
                <div className="p-6 rounded-xl border border-emerald-500/20 bg-emerald-500/5 dark:bg-emerald-950/10 space-y-3">
                  <div className="flex items-center space-x-2 text-emerald-600 dark:text-emerald-400 font-semibold text-xs uppercase tracking-wider">
                    <CheckCircle2 className="w-4 h-4" />
                    <span>Identified Strengths</span>
                  </div>
                  <ul className="space-y-2 text-xs text-slate-700 dark:text-slate-300">
                    {result.strengths.map((str, idx) => (
                      <li key={idx} className="flex items-start space-x-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-1.5 shrink-0" />
                        <span>{str}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Development Gaps */}
                <div className="p-6 rounded-xl border border-amber-500/20 bg-amber-500/5 dark:bg-amber-950/10 space-y-3">
                  <div className="flex items-center space-x-2 text-amber-600 dark:text-amber-400 font-semibold text-xs uppercase tracking-wider">
                    <Target className="w-4 h-4" />
                    <span>Development Priorities & Gaps</span>
                  </div>
                  <ul className="space-y-2 text-xs text-slate-700 dark:text-slate-300">
                    {result.development_gaps.map((gap, idx) => (
                      <li key={idx} className="flex items-start space-x-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-1.5 shrink-0" />
                        <span>{gap}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* 4. Evidence Behind Each Recommendation */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                    Evidence Behind Recommendations
                  </h3>
                  <span className="text-xs font-mono text-slate-400">Phase 5 Odds Ratios & Permutation Ranks</span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {result.recommendations.map((rec) => (
                    <div
                      key={rec.skill_name}
                      className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-2.5 transition-all"
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-xs text-slate-900 dark:text-slate-100">
                          {rec.skill_name}
                        </span>
                        <Badge
                          variant={
                            rec.priority_level === "Immediate Priority"
                              ? "destructive"
                              : rec.priority_level === "Secondary Focus"
                              ? "secondary"
                              : "outline"
                          }
                          className="text-[10px] px-1.5 py-0"
                        >
                          {rec.priority_level}
                        </Badge>
                      </div>

                      <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                        {rec.evidence_rationale}
                      </p>

                      <div className="pt-2 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between text-[11px] font-mono">
                        <span className="text-teal-600 dark:text-teal-400 font-semibold">
                          {rec.roi_multiplier}
                        </span>
                        <span className="text-slate-400">
                          Score: {rec.current_score.toFixed(1)} / {rec.target_benchmark.toFixed(1)}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* 5. Suggested Learning Sequence */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                    Suggested Learning Sequence
                  </h3>
                  <span className="text-xs font-mono text-slate-400">Phase 8 Career Stage Progression</span>
                </div>

                <div className="space-y-3">
                  {result.learning_sequence.map((stage) => (
                    <div
                      key={stage.step}
                      className="p-5 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-2.5"
                    >
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 pb-2 border-b border-slate-100 dark:border-slate-800/80">
                        <div className="flex items-center space-x-2">
                          <span className="w-6 h-6 rounded-full bg-teal-500/10 text-teal-600 dark:text-teal-400 text-xs font-bold font-mono flex items-center justify-center shrink-0 border border-teal-500/20">
                            {stage.step}
                          </span>
                          <h4 className="text-xs font-bold text-slate-900 dark:text-slate-100">
                            {stage.title}
                          </h4>
                        </div>
                        <span className="text-[11px] font-mono text-slate-500 flex items-center space-x-1">
                          <Clock className="w-3 h-3 text-slate-400 inline" />
                          <span>{stage.timeline}</span>
                        </span>
                      </div>

                      <p className="text-xs text-slate-700 dark:text-slate-300 font-medium">
                        {stage.milestone}
                      </p>

                      <p className="text-[11px] text-slate-500 dark:text-slate-400 italic">
                        Basis: {stage.empirical_justification}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              {/* 6. Methodology Disclaimer Banner */}
              <div className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/40 text-slate-600 dark:text-slate-400 text-[11px] leading-relaxed flex items-start space-x-3">
                <HelpCircle className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
                <span>{result.methodology_disclaimer}</span>
              </div>

              {/* Bottom Actions */}
              <div className="pt-4 flex flex-col sm:flex-row items-center justify-between gap-4 border-t border-slate-200/80 dark:border-slate-800">
                <Button
                  variant="outline"
                  onClick={() => setResult(null)}
                  className="text-xs h-9 w-full sm:w-auto"
                >
                  <RotateCcw className="w-3.5 h-3.5 mr-1.5" />
                  Adjust Ratings & Re-evaluate
                </Button>

                <div className="flex items-center space-x-3 w-full sm:w-auto">
                  <Link href="/roadmap" className="w-full sm:w-auto">
                    <Button variant="default" className="bg-teal-600 hover:bg-teal-500 text-white text-xs h-9 w-full sm:w-auto">
                      <span>Explore Stakeholder Roadmaps</span>
                      <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
                    </Button>
                  </Link>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>

      <Footer />
    </div>
  );
}

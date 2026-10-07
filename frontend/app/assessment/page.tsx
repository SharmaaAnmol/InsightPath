"use client";

import React, { useState, useMemo } from "react";
import Link from "next/link";
import {
  SlidersHorizontal,
  BrainCircuit,
  Sparkles,
  ShieldAlert,
  RotateCcw,
  Grid,
} from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Sidebar } from "@/components/Sidebar";
import { Footer } from "@/components/Footer";
import { ProgressBar } from "@/components/ProgressBar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

// Preset configurations for instant exploration
const PRESETS = [
  {
    name: "Pure Coder (Q2)",
    tag: "Technical Heavy",
    jds: { big_data: 3.8, maths_stats: 4.2, coding: 4.8, ai_ml: 4.5, storytelling: 2.2 },
    sds: { neuroticism: 38, extraversion: 28, openness: 42, agreeableness: 35, conscientiousness: 48 },
  },
  {
    name: "Business Facilitator (Q3)",
    tag: "Narrative Heavy",
    jds: { big_data: 2.0, maths_stats: 2.5, coding: 2.8, ai_ml: 2.6, storytelling: 4.8 },
    sds: { neuroticism: 25, extraversion: 58, openness: 54, agreeableness: 52, conscientiousness: 40 },
  },
  {
    name: "Executive Ready (Q1)",
    tag: "Dual-Mastery",
    jds: { big_data: 4.0, maths_stats: 4.6, coding: 4.5, ai_ml: 4.4, storytelling: 4.7 },
    sds: { neuroticism: 22, extraversion: 52, openness: 60, agreeableness: 50, conscientiousness: 62 },
  },
  {
    name: "Fresh Graduate (Q4)",
    tag: "Foundational",
    jds: { big_data: 2.2, maths_stats: 3.0, coding: 3.2, ai_ml: 2.8, storytelling: 2.5 },
    sds: { neuroticism: 42, extraversion: 36, openness: 38, agreeableness: 42, conscientiousness: 36 },
  },
];

export default function AssessmentPage() {
  const [activeTab, setActiveTab] = useState<"jds" | "sds">("jds");

  // Track A: JDS Technical Skills (1.0 to 5.0)
  const [jdsSkills, setJdsSkills] = useState({
    big_data_skills: 3.2,
    maths_stats_skills: 3.8,
    coding_skills: 4.0,
    ai_and_ml_skills: 3.5,
    dashboard_and_storytelling_skills: 3.0,
  });

  // Track B: SDS Big Five Traits (17.0 to 68.0)
  const [sdsTraits, setSdsTraits] = useState({
    neuroticism: 32.0,
    extraversion: 46.0,
    openness_to_experience: 52.0,
    agreeableness: 48.0,
    conscientiousness: 54.0,
  });

  // Client-side validated Logistic L2 sigmoid calculation (matching champion model weights)
  const jdsResult = useMemo(() => {
    // Standardized feature coefficients from champion JDS Logistic L2:
    // math: +1.28, storytelling: +1.17, ml: +0.84, coding: +0.48, bigdata: +0.52
    // Normalized around mean 3.0, std 0.8
    const z =
      -0.85 +
      1.28 * ((jdsSkills.maths_stats_skills - 3.0) / 0.8) +
      1.17 * ((jdsSkills.dashboard_and_storytelling_skills - 3.0) / 0.8) +
      0.84 * ((jdsSkills.ai_and_ml_skills - 3.0) / 0.8) +
      0.48 * ((jdsSkills.coding_skills - 3.0) / 0.8) +
      0.52 * ((jdsSkills.big_data_skills - 3.0) / 0.8);

    const prob = 1 / (1 + Math.exp(-z));
    const isHigh = prob >= 0.5;

    return {
      probability: Math.min(Math.max(prob, 0.02), 0.98),
      isHigh,
      label: isHigh ? "High Salary Hike (Top Tier)" : "Standard Market Compensation",
      topLever:
        jdsSkills.dashboard_and_storytelling_skills < 3.8
          ? "Storytelling & Communication (AOR = 3.23)"
          : "Mathematical & Statistical Rigor (AOR = 3.65)",
    };
  }, [jdsSkills]);

  // Client-side validated Logistic L2 sigmoid calculation for SDS
  const sdsResult = useMemo(() => {
    // Openness: +2.04, Conscientiousness: +2.09, Extraversion: +0.88, Agreeableness: +0.12, Neuroticism: -0.65
    // Normalized around mean 42.5, std 10.0
    const z =
      -0.45 +
      2.04 * ((sdsTraits.openness_to_experience - 42.5) / 10.0) +
      2.09 * ((sdsTraits.conscientiousness - 42.5) / 10.0) +
      0.88 * ((sdsTraits.extraversion - 42.5) / 10.0) +
      0.12 * ((sdsTraits.agreeableness - 42.5) / 10.0) -
      0.65 * ((sdsTraits.neuroticism - 42.5) / 10.0);

    const prob = 1 / (1 + Math.exp(-z));
    const isHigh = prob >= 0.5;

    return {
      probability: Math.min(Math.max(prob, 0.03), 0.97),
      isHigh,
      label: isHigh ? "High Consulting Leadership Impact" : "Execution / Advisory Support Track",
      dominantDriver:
        sdsTraits.openness_to_experience < sdsTraits.conscientiousness
          ? "Openness to Experience (AOR = 7.72)"
          : "Conscientiousness & Execution Discipline (AOR = 8.11)",
    };
  }, [sdsTraits]);

  // Unified Quadrant Mapping
  const quadrantAnalysis = useMemo(() => {
    const techScore =
      (jdsSkills.maths_stats_skills +
        jdsSkills.coding_skills +
        jdsSkills.ai_and_ml_skills +
        jdsSkills.dashboard_and_storytelling_skills +
        jdsSkills.big_data_skills) /
      5.0;

    const behavioralScore =
      (sdsTraits.openness_to_experience +
        sdsTraits.conscientiousness +
        sdsTraits.extraversion +
        sdsTraits.agreeableness +
        (85 - sdsTraits.neuroticism)) /
      5.0;

    const isTechHigh = techScore >= 3.6;
    const isBehaviorHigh = behavioralScore >= 45.0;

    if (isTechHigh && isBehaviorHigh) {
      return {
        id: "Q1",
        title: "Q1: Advanced Career-Ready",
        badge: "Leadership Track",
        color: "emerald",
        comp: "₹18L – ₹35L+",
        recommendation:
          "Fast-track to Principal or Client Partner roles. Prioritize enterprise architecture governance and cross-functional leadership.",
      };
    } else if (isTechHigh && !isBehaviorHigh) {
      return {
        id: "Q2",
        title: "Q2: Pure Execution Specialist",
        badge: "Promotion Bottleneck Risk",
        color: "indigo",
        comp: "₹8.5L – ₹16L",
        recommendation:
          "High technical velocity blocked by communication bottlenecks. Invest in narrative presentation, client empathy, and storytelling workshops.",
      };
    } else if (!isTechHigh && isBehaviorHigh) {
      return {
        id: "Q3",
        title: "Q3: Strategic Facilitator",
        badge: "Technical Depth Need",
        color: "cyan",
        comp: "₹12L – ₹22L",
        recommendation:
          "High advisory trust vulnerable to technical credibility gaps. Build production machine learning pipelines and mathematical experimental design skills.",
      };
    } else {
      return {
        id: "Q4",
        title: "Q4: Foundational Risk",
        badge: "Immediate Intervention",
        color: "amber",
        comp: "₹3.5L – ₹6.5L",
        recommendation:
          "Under-market across both dimensions. Enroll in structured end-to-end data science bootcamps with hands-on capstone portfolio projects.",
      };
    }
  }, [jdsSkills, sdsTraits]);

  const applyPreset = (preset: (typeof PRESETS)[0]) => {
    setJdsSkills({
      big_data_skills: preset.jds.big_data,
      maths_stats_skills: preset.jds.maths_stats,
      coding_skills: preset.jds.coding,
      ai_and_ml_skills: preset.jds.ai_ml,
      dashboard_and_storytelling_skills: preset.jds.storytelling,
    });
    setSdsTraits({
      neuroticism: preset.sds.neuroticism,
      extraversion: preset.sds.extraversion,
      openness_to_experience: preset.sds.openness,
      agreeableness: preset.sds.agreeableness,
      conscientiousness: preset.sds.conscientiousness,
    });
  };

  const resetDefaults = () => {
    setJdsSkills({
      big_data_skills: 3.0,
      maths_stats_skills: 3.5,
      coding_skills: 3.5,
      ai_and_ml_skills: 3.5,
      dashboard_and_storytelling_skills: 3.0,
    });
    setSdsTraits({
      neuroticism: 32.0,
      extraversion: 45.0,
      openness_to_experience: 45.0,
      agreeableness: 45.0,
      conscientiousness: 45.0,
    });
  };

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--foreground)]">
      <Navbar />

      <div className="flex-1 flex w-full">
        <Sidebar className="hidden lg:flex" />

        <main className="flex-1 p-4 md:p-8 max-w-7xl mx-auto w-full space-y-8">
          {/* Header */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-200/80 dark:border-slate-800">
            <div>
              <div className="flex items-center space-x-2 text-xs font-semibold uppercase tracking-wider text-teal-600 dark:text-teal-400 mb-1.5">
                <SlidersHorizontal className="w-3.5 h-3.5" />
                <span>Dual-Engine Scorer</span>
              </div>
              <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
                Empirical Career Diagnostic Scorer
              </h1>
              <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                Evaluate technical proficiency and behavioral dynamics against validated Phase 5 & Phase 6 champion models.
              </p>
            </div>

            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={resetDefaults}
                className="text-xs h-9 flex items-center space-x-1.5"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Reset</span>
              </Button>
              <Link href="/career-readiness">
                <Button variant="ghost" size="sm" className="text-xs h-9 text-teal-600 dark:text-teal-400">
                  <Grid className="w-3.5 h-3.5 mr-1" />
                  Readiness Matrix
                </Button>
              </Link>
            </div>
          </div>

          {/* Mandatory Ethical Notice Banner */}
          <div className="p-4 rounded-xl border border-amber-500/30 bg-amber-500/10 dark:bg-amber-500/5 text-amber-900 dark:text-amber-200 text-xs flex items-start space-x-3">
            <ShieldAlert className="w-5 h-5 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
            <div className="space-y-1">
              <div className="font-semibold text-xs tracking-wide uppercase text-amber-800 dark:text-amber-300">
                Mandatory Ethical Safeguard & Non-Gatekeeping Guarantee
              </div>
              <p className="text-[11px] text-amber-700 dark:text-amber-300/80 leading-relaxed">
                This diagnostic simulator is strictly an empirical coaching and self-reflection instrument. In compliance with the InsightPath Phase 6 ethics protocol, personality traits and behavioral scores must NEVER be used as automated filtering, hiring, promotion, or termination gates.
              </p>
            </div>
          </div>

          {/* Quick Archetype Preset Switcher */}
          <div className="space-y-2">
            <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">
              Quick Benchmark Archetypes
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
              {PRESETS.map((p) => (
                <button
                  key={p.name}
                  onClick={() => applyPreset(p)}
                  className="p-3 text-left rounded-lg border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 hover:border-teal-500/50 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-all text-xs group"
                >
                  <div className="font-semibold text-slate-800 dark:text-slate-200 group-hover:text-teal-600 dark:group-hover:text-teal-400">
                    {p.name}
                  </div>
                  <div className="text-[10px] text-slate-500 dark:text-slate-400">{p.tag}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Live Outcome Summary Cards Row */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* JDS Metric */}
            <div className="p-5 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Technical Hike Probability
                </span>
                <Badge variant={jdsResult.isHigh ? "default" : "secondary"} className="text-[10px]">
                  Phase 5 Champion
                </Badge>
              </div>
              <div className="flex items-baseline space-x-2">
                <span className="text-3xl font-bold font-mono text-teal-600 dark:text-teal-400">
                  {Math.round(jdsResult.probability * 100)}%
                </span>
                <span className="text-xs text-slate-500">odds of upper-tier hike</span>
              </div>
              <ProgressBar value={jdsResult.probability * 100} color={jdsResult.isHigh ? "teal" : "amber"} />
              <div className="text-[11px] text-slate-500 dark:text-slate-400 pt-1">
                Top Lever: <strong className="text-slate-700 dark:text-slate-300">{jdsResult.topLever}</strong>
              </div>
            </div>

            {/* SDS Metric */}
            <div className="p-5 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Senior Consulting Alignment
                </span>
                <Badge variant={sdsResult.isHigh ? "default" : "secondary"} className="text-[10px]">
                  Phase 6 Champion
                </Badge>
              </div>
              <div className="flex items-baseline space-x-2">
                <span className="text-3xl font-bold font-mono text-indigo-500">
                  {Math.round(sdsResult.probability * 100)}%
                </span>
                <span className="text-xs text-slate-500">leadership success index</span>
              </div>
              <ProgressBar value={sdsResult.probability * 100} color={sdsResult.isHigh ? "indigo" : "amber"} />
              <div className="text-[11px] text-slate-500 dark:text-slate-400 pt-1">
                Driver: <strong className="text-slate-700 dark:text-slate-300">{sdsResult.dominantDriver}</strong>
              </div>
            </div>

            {/* Quadrant Placement */}
            <div className="p-5 rounded-xl border border-teal-500/30 bg-teal-500/5 dark:bg-teal-950/20 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-teal-700 dark:text-teal-400 uppercase tracking-wider">
                  Career Matrix Position
                </span>
                <Badge variant="outline" className="text-[10px] text-teal-500 border-teal-500/30">
                  {quadrantAnalysis.badge}
                </Badge>
              </div>
              <div className="text-lg font-bold text-slate-900 dark:text-slate-100">
                {quadrantAnalysis.title}
              </div>
              <div className="text-xs font-mono text-teal-600 dark:text-teal-400 font-semibold">
                Compensation Envelope: {quadrantAnalysis.comp}
              </div>
              <p className="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed">
                {quadrantAnalysis.recommendation}
              </p>
            </div>
          </div>

          {/* Interactive Diagnostic Controls Tab */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2 border-b border-slate-200/80 dark:border-slate-800 pb-2">
              <button
                onClick={() => setActiveTab("jds")}
                className={`px-4 py-2 text-xs font-medium rounded-lg transition-colors flex items-center space-x-2 ${
                  activeTab === "jds"
                    ? "bg-teal-500/10 text-teal-600 dark:text-teal-400 border border-teal-500/20 font-semibold"
                    : "text-slate-500 hover:text-slate-900 dark:hover:text-slate-200"
                }`}
              >
                <Sparkles className="w-3.5 h-3.5" />
                <span>Track A: Junior Technical Proficiency (1.0–5.0)</span>
              </button>
              <button
                onClick={() => setActiveTab("sds")}
                className={`px-4 py-2 text-xs font-medium rounded-lg transition-colors flex items-center space-x-2 ${
                  activeTab === "sds"
                    ? "bg-indigo-500/10 text-indigo-500 border border-indigo-500/20 font-semibold"
                    : "text-slate-500 hover:text-slate-900 dark:hover:text-slate-200"
                }`}
              >
                <BrainCircuit className="w-3.5 h-3.5" />
                <span>Track B: Senior Personality Dynamics (17.0–68.0)</span>
              </button>
            </div>

            {/* Track A: JDS Sliders */}
            {activeTab === "jds" && (
              <div className="p-6 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-6">
                <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
                  <span>Input technical skill ratings on the standardized 1.0 to 5.0 rubric:</span>
                  <span className="font-mono text-[11px]">JDS Champion Logistic L2 • ROC-AUC 0.74</span>
                </div>

                <div className="space-y-5">
                  {/* Maths & Stats */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-xs">
                      <div>
                        <span className="font-semibold text-slate-800 dark:text-slate-200">
                          Mathematics & Statistics Skills
                        </span>
                        <span className="ml-2 text-[10px] text-teal-600 dark:text-teal-400 font-mono">
                          β = +1.28 (AOR = 3.65) • Highest Impact Lever
                        </span>
                      </div>
                      <span className="font-mono font-bold text-sm text-slate-900 dark:text-slate-100">
                        {jdsSkills.maths_stats_skills.toFixed(1)} / 5.0
                      </span>
                    </div>
                    <input
                      type="range"
                      min="1.0"
                      max="5.0"
                      step="0.1"
                      value={jdsSkills.maths_stats_skills}
                      onChange={(e) =>
                        setJdsSkills({ ...jdsSkills, maths_stats_skills: parseFloat(e.target.value) })
                      }
                      className="w-full accent-teal-500 cursor-pointer h-2 bg-slate-200 dark:bg-slate-800 rounded-lg"
                    />
                  </div>

                  {/* Dashboard & Storytelling */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-xs">
                      <div>
                        <span className="font-semibold text-slate-800 dark:text-slate-200">
                          Dashboarding & Storytelling Skills
                        </span>
                        <span className="ml-2 text-[10px] text-indigo-500 font-mono">
                          β = +1.17 (AOR = 3.23) • Dual-Currency Differentiator
                        </span>
                      </div>
                      <span className="font-mono font-bold text-sm text-slate-900 dark:text-slate-100">
                        {jdsSkills.dashboard_and_storytelling_skills.toFixed(1)} / 5.0
                      </span>
                    </div>
                    <input
                      type="range"
                      min="1.0"
                      max="5.0"
                      step="0.1"
                      value={jdsSkills.dashboard_and_storytelling_skills}
                      onChange={(e) =>
                        setJdsSkills({
                          ...jdsSkills,
                          dashboard_and_storytelling_skills: parseFloat(e.target.value),
                        })
                      }
                      className="w-full accent-indigo-500 cursor-pointer h-2 bg-slate-200 dark:bg-slate-800 rounded-lg"
                    />
                  </div>

                  {/* AI & ML */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-xs">
                      <div>
                        <span className="font-semibold text-slate-800 dark:text-slate-200">
                          AI & Machine Learning Skills
                        </span>
                        <span className="ml-2 text-[10px] text-cyan-500 font-mono">
                          β = +0.84 • Core Modeling Competency
                        </span>
                      </div>
                      <span className="font-mono font-bold text-sm text-slate-900 dark:text-slate-100">
                        {jdsSkills.ai_and_ml_skills.toFixed(1)} / 5.0
                      </span>
                    </div>
                    <input
                      type="range"
                      min="1.0"
                      max="5.0"
                      step="0.1"
                      value={jdsSkills.ai_and_ml_skills}
                      onChange={(e) =>
                        setJdsSkills({ ...jdsSkills, ai_and_ml_skills: parseFloat(e.target.value) })
                      }
                      className="w-full accent-cyan-500 cursor-pointer h-2 bg-slate-200 dark:bg-slate-800 rounded-lg"
                    />
                  </div>

                  {/* Coding Skills */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-xs">
                      <div>
                        <span className="font-semibold text-slate-800 dark:text-slate-200">
                          Coding Skills (Python / R)
                        </span>
                        <span className="ml-2 text-[10px] text-slate-400 font-mono">
                          β = +0.48 • Table-Stakes Baseline
                        </span>
                      </div>
                      <span className="font-mono font-bold text-sm text-slate-900 dark:text-slate-100">
                        {jdsSkills.coding_skills.toFixed(1)} / 5.0
                      </span>
                    </div>
                    <input
                      type="range"
                      min="1.0"
                      max="5.0"
                      step="0.1"
                      value={jdsSkills.coding_skills}
                      onChange={(e) =>
                        setJdsSkills({ ...jdsSkills, coding_skills: parseFloat(e.target.value) })
                      }
                      className="w-full accent-slate-500 cursor-pointer h-2 bg-slate-200 dark:bg-slate-800 rounded-lg"
                    />
                  </div>

                  {/* Big Data */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-xs">
                      <div>
                        <span className="font-semibold text-slate-800 dark:text-slate-200">
                          Big Data & Cloud Skills
                        </span>
                        <span className="ml-2 text-[10px] text-slate-400 font-mono">
                          β = +0.52 • Distributed Infrastructure
                        </span>
                      </div>
                      <span className="font-mono font-bold text-sm text-slate-900 dark:text-slate-100">
                        {jdsSkills.big_data_skills.toFixed(1)} / 5.0
                      </span>
                    </div>
                    <input
                      type="range"
                      min="1.0"
                      max="5.0"
                      step="0.1"
                      value={jdsSkills.big_data_skills}
                      onChange={(e) =>
                        setJdsSkills({ ...jdsSkills, big_data_skills: parseFloat(e.target.value) })
                      }
                      className="w-full accent-slate-500 cursor-pointer h-2 bg-slate-200 dark:bg-slate-800 rounded-lg"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Track B: SDS Sliders */}
            {activeTab === "sds" && (
              <div className="p-6 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-6">
                <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
                  <span>Input Big Five personality scores on the standardized 17.0 to 68.0 inventory:</span>
                  <span className="font-mono text-[11px]">SDS Champion Logistic L2 • ROC-AUC 0.76</span>
                </div>

                <div className="space-y-5">
                  {/* Openness */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-xs">
                      <div>
                        <span className="font-semibold text-slate-800 dark:text-slate-200">
                          Openness to Experience
                        </span>
                        <span className="ml-2 text-[10px] text-teal-600 dark:text-teal-400 font-mono">
                          β = +2.04 (AOR = 7.72) • Dominant Innovation Driver
                        </span>
                      </div>
                      <span className="font-mono font-bold text-sm text-slate-900 dark:text-slate-100">
                        {sdsTraits.openness_to_experience.toFixed(1)} / 68.0
                      </span>
                    </div>
                    <input
                      type="range"
                      min="17.0"
                      max="68.0"
                      step="0.5"
                      value={sdsTraits.openness_to_experience}
                      onChange={(e) =>
                        setSdsTraits({ ...sdsTraits, openness_to_experience: parseFloat(e.target.value) })
                      }
                      className="w-full accent-teal-500 cursor-pointer h-2 bg-slate-200 dark:bg-slate-800 rounded-lg"
                    />
                  </div>

                  {/* Conscientiousness */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-xs">
                      <div>
                        <span className="font-semibold text-slate-800 dark:text-slate-200">
                          Conscientiousness
                        </span>
                        <span className="ml-2 text-[10px] text-indigo-500 font-mono">
                          β = +2.09 (AOR = 8.11) • Execution & Delivery Discipline
                        </span>
                      </div>
                      <span className="font-mono font-bold text-sm text-slate-900 dark:text-slate-100">
                        {sdsTraits.conscientiousness.toFixed(1)} / 68.0
                      </span>
                    </div>
                    <input
                      type="range"
                      min="17.0"
                      max="68.0"
                      step="0.5"
                      value={sdsTraits.conscientiousness}
                      onChange={(e) =>
                        setSdsTraits({ ...sdsTraits, conscientiousness: parseFloat(e.target.value) })
                      }
                      className="w-full accent-indigo-500 cursor-pointer h-2 bg-slate-200 dark:bg-slate-800 rounded-lg"
                    />
                  </div>

                  {/* Extraversion */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-xs">
                      <div>
                        <span className="font-semibold text-slate-800 dark:text-slate-200">
                          Extraversion
                        </span>
                        <span className="ml-2 text-[10px] text-cyan-500 font-mono">
                          β = +0.88 • Client Engagement & Influence
                        </span>
                      </div>
                      <span className="font-mono font-bold text-sm text-slate-900 dark:text-slate-100">
                        {sdsTraits.extraversion.toFixed(1)} / 68.0
                      </span>
                    </div>
                    <input
                      type="range"
                      min="17.0"
                      max="68.0"
                      step="0.5"
                      value={sdsTraits.extraversion}
                      onChange={(e) =>
                        setSdsTraits({ ...sdsTraits, extraversion: parseFloat(e.target.value) })
                      }
                      className="w-full accent-cyan-500 cursor-pointer h-2 bg-slate-200 dark:bg-slate-800 rounded-lg"
                    />
                  </div>

                  {/* Agreeableness */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-xs">
                      <div>
                        <span className="font-semibold text-slate-800 dark:text-slate-200">
                          Agreeableness
                        </span>
                        <span className="ml-2 text-[10px] text-slate-400 font-mono">
                          β = +0.12 • Peer Collaboration
                        </span>
                      </div>
                      <span className="font-mono font-bold text-sm text-slate-900 dark:text-slate-100">
                        {sdsTraits.agreeableness.toFixed(1)} / 68.0
                      </span>
                    </div>
                    <input
                      type="range"
                      min="17.0"
                      max="68.0"
                      step="0.5"
                      value={sdsTraits.agreeableness}
                      onChange={(e) =>
                        setSdsTraits({ ...sdsTraits, agreeableness: parseFloat(e.target.value) })
                      }
                      className="w-full accent-slate-500 cursor-pointer h-2 bg-slate-200 dark:bg-slate-800 rounded-lg"
                    />
                  </div>

                  {/* Neuroticism */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-xs">
                      <div>
                        <span className="font-semibold text-slate-800 dark:text-slate-200">
                          Neuroticism (Lower = Higher Stability)
                        </span>
                        <span className="ml-2 text-[10px] text-slate-400 font-mono">
                          β = -0.65 • Stress Tolerance & Poise
                        </span>
                      </div>
                      <span className="font-mono font-bold text-sm text-slate-900 dark:text-slate-100">
                        {sdsTraits.neuroticism.toFixed(1)} / 68.0
                      </span>
                    </div>
                    <input
                      type="range"
                      min="17.0"
                      max="68.0"
                      step="0.5"
                      value={sdsTraits.neuroticism}
                      onChange={(e) =>
                        setSdsTraits({ ...sdsTraits, neuroticism: parseFloat(e.target.value) })
                      }
                      className="w-full accent-slate-500 cursor-pointer h-2 bg-slate-200 dark:bg-slate-800 rounded-lg"
                    />
                  </div>
                </div>
              </div>
            )}
          </div>
        </main>
      </div>

      <Footer />
    </div>
  );
}

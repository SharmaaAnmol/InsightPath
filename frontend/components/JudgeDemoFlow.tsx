"use client";

import React, { useState, useCallback, useEffect } from "react";
import Link from "next/link";
import {
  Sparkles,
  Zap,
  ArrowRight,
  RotateCcw,
  CheckCircle2,
  AlertTriangle,
  HelpCircle,
  Database,
  FlaskConical,
  BookOpen,
  ChevronRight,
  ShieldAlert,
  Check,
  Compass,
  Cpu,
  BarChart3,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { EvidenceModal, EvidenceDetail } from "@/components/EvidenceModal";
import { submitAssessment, AssessmentRequest, AssessmentResponse } from "@/lib/api";

// Preset Personas designed specifically for hackathon judges to test in seconds
interface PersonaPreset {
  id: string;
  name: string;
  badge: string;
  archetype: string;
  description: string;
  goal: string;
  exp: string;
  scores: {
    maths_stats: number;
    coding: number;
    ai_ml: number;
    big_data: number;
    storytelling: number;
  };
}

const PERSONA_PRESETS: PersonaPreset[] = [
  {
    id: "coder",
    name: "Pure Coder (Technical High / Storytelling Gap)",
    badge: "Archetype Q2",
    archetype: "Execution Specialist",
    description: "High coding & ML (4.8), but storytelling gap (2.2). Demonstrates why storytelling is the #1 differentiator in our model.",
    goal: "Machine Learning Engineer",
    exp: "Junior (2-4 years)",
    scores: {
      maths_stats: 4.6,
      coding: 4.8,
      ai_ml: 4.7,
      big_data: 4.2,
      storytelling: 2.2,
    },
  },
  {
    id: "executive",
    name: "Executive Ready (Balanced Dual-Currency Lead)",
    badge: "Archetype Q1",
    archetype: "Strategic Impact Lead",
    description: "High technical and narrative mastery (4.5+ across all dimensions). Demonstrates peak progression alignment signal.",
    goal: "Data Scientist",
    exp: "Mid-Level (4-6 years)",
    scores: {
      maths_stats: 4.8,
      coding: 4.5,
      ai_ml: 4.7,
      big_data: 4.3,
      storytelling: 4.6,
    },
  },
  {
    id: "translator",
    name: "Business Translator (High Narrative / Tech Gap)",
    badge: "Archetype Q3",
    archetype: "Strategic Facilitator",
    description: "High communication & presentation (4.7), but statistical depth gap (2.6). Demonstrates applied modeling need.",
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
    id: "junior",
    name: "Foundational Junior (Early-Career Growth)",
    badge: "Archetype Q4",
    archetype: "Foundational Practitioner",
    description: "Early-stage skill development across dimensions (2.3–3.0). Generates foundational staged roadmap.",
    goal: "Data Analyst",
    exp: "Entry-Level (0-2 years)",
    scores: {
      maths_stats: 2.8,
      coding: 3.0,
      ai_ml: 2.4,
      big_data: 2.2,
      storytelling: 2.7,
    },
  },
];

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

const SKILL_BENCHMARKS = [
  {
    key: "maths_stats",
    name: "Mathematics & Statistics",
    benchmark: 4.8,
    importanceRank: 2,
    oddsRatio: "3.61x",
    permImp: "0.0894",
    desc: "Rigorous probability, hypothesis testing, linear algebra, and inference.",
  },
  {
    key: "coding",
    name: "Coding (Python / R)",
    benchmark: 4.5,
    importanceRank: 4,
    oddsRatio: "1.62x",
    permImp: "0.0381",
    desc: "Modular software design, clean code, data manipulation, and unit testing.",
  },
  {
    key: "ai_ml",
    name: "AI & Machine Learning",
    benchmark: 4.8,
    importanceRank: 3,
    oddsRatio: "2.32x",
    permImp: "0.0612",
    desc: "Supervised/unsupervised algorithms, evaluation metrics, and model tuning.",
  },
  {
    key: "big_data",
    name: "Big Data & Cloud",
    benchmark: 4.1,
    importanceRank: 5,
    oddsRatio: "1.68x",
    permImp: "0.0298",
    desc: "Distributed computing (Spark/SQL), containerization, and cloud pipelines.",
  },
  {
    key: "storytelling",
    name: "Dashboarding & Storytelling",
    benchmark: 4.3,
    importanceRank: 1,
    oddsRatio: "3.23x",
    permImp: "0.1062",
    desc: "Translating modeling rigor into executive narratives and business P&L impact.",
  },
];

// Curated Evidence Repository for the "Why this recommendation?" controls
const EVIDENCE_REGISTRY: Record<string, EvidenceDetail> = {
  storytelling: {
    title: "Dashboarding & Storytelling #1 Progression Signal",
    phase: "Phase 5 JDS Model & Phase 7 Synthesis",
    dataset: "Junior Data Scientists (N=139) + Triangulation Synthesis",
    sampleSize: "N = 139 verified practitioners",
    method: "Out-of-Fold Permutation Feature Importance & Multivariate Logistic L2",
    interpretation:
      "Storytelling emerged as the #1 predictive differentiator (Permutation Importance = 0.1062, AOR = 3.23). While coding and math establish baseline entry competence, the ability to communicate findings to non-technical stakeholders strongly separates top-progression practitioners from peers.",
    limitation:
      "Cross-sectional survey representation from the SAS CU Hackathon research dataset; reflects observed associations rather than guaranteed individual outcomes.",
  },
  maths_stats: {
    title: "Mathematics & Statistics Primary Odds Multiplier",
    phase: "Phase 5 JDS Modeling & Phase 4 Statistics",
    dataset: "Junior Data Scientist Survey Cohort (N=139)",
    sampleSize: "N = 139 (5-Fold Stratified Cross-Validation)",
    method: "Multivariate Logistic Regression with L2 Regularization (C=0.1)",
    interpretation:
      "Strong mathematical foundations yield an Adjusted Odds Ratio of 3.61 (95% CI: 1.48–8.79), confirming that applied rigor protects practitioners from model hallucination and poor inductive assumptions.",
    limitation:
      "Self-assessment Likert scale calibrated against observed project performance. Does not assess pure theoretical mathematics.",
  },
  ai_ml: {
    title: "AI & Machine Learning Core Currency",
    phase: "Phase 5 JDS Modeling & Phase 3 Market Alignment",
    dataset: "JDS Cohort (N=139) & 17,443 Job Postings",
    sampleSize: "N = 139 practitioners / N = 17,443 market postings",
    method: "Permutation Feature Importance & Keyword Extraction",
    interpretation:
      "Ranks #3 in feature importance (0.0612) with a 2.32x odds ratio. Machine learning is a mandatory prerequisite, but without storytelling translation, its progression lift plateaus.",
    limitation:
      "Algorithmic toolsets evolve rapidly; emphasis is placed on generalizable supervised and evaluation concepts.",
  },
  coding: {
    title: "Coding (Python/R) Baseline Utility",
    phase: "Phase 4 Statistical Comparison & Phase 5 JDS Model",
    dataset: "Junior Data Scientist Cohort (N=139)",
    sampleSize: "N = 139",
    method: "Mann-Whitney U Test & Feature Weight Extraction",
    interpretation:
      "Coding demonstrates high market demand (present in 78.4% of DS postings) with an AOR of 1.62. It functions as a hygiene factor: critical to execute work, but insufficient alone for senior progression.",
    limitation:
      "Syntax fluency does not automatically translate into architectural judgment.",
  },
  big_data: {
    title: "Big Data & Cloud Architectural Foundation",
    phase: "Phase 3 Market Intelligence & Phase 5 JDS Model",
    dataset: "1,602 Data Science Postings & N=139 JDS Profiles",
    sampleSize: "N = 1,602 postings / N = 139 practitioners",
    method: "Salary Premium Hedonic Regression & Odds Modeling",
    interpretation:
      "Cloud and distributed tools command a high salary midpoint (12.4 Lakhs vs 8.2 Lakhs baseline), providing leverage when operating on enterprise-scale datasets.",
    limitation:
      "Cloud tooling varies across corporate tech stacks (AWS vs GCP vs Azure vs Databricks).",
  },
  dual_currency: {
    title: "Dual-Currency Talent Matrix (Technical vs Narrative)",
    phase: "Phase 8 Career-Readiness Framework",
    dataset: "Triangulated synthesis across Phases 3, 5, 6, 7",
    sampleSize: "Integrated N = 17,443 postings & N = 300 practitioners",
    method: "4-Quadrant Orthogonal Clustering & Competency Mapping",
    interpretation:
      "True career velocity requires dual-currency mastery: Technical Currency (math + code + ML) enables delivery, while Narrative Currency (storytelling + business translation) secures executive alignment and funding.",
    limitation:
      "Quadrant thresholds are heuristic benchmarks designed for career coaching diagnostics.",
  },
};

export function JudgeDemoFlow() {
  const [selectedPersona, setSelectedPersona] = useState<string>("coder");
  const [goal, setGoal] = useState<string>("Machine Learning Engineer");
  const [exp, setExp] = useState<string>("Junior (2-4 years)");
  const [scores, setScores] = useState({
    maths_stats: 4.6,
    coding: 4.8,
    ai_ml: 4.7,
    big_data: 4.2,
    storytelling: 2.2,
  });

  const [activeModalEvidence, setActiveModalEvidence] = useState<EvidenceDetail | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [analyzed, setAnalyzed] = useState<boolean>(true); // Pre-analyzed for instant judge evaluation
  const [isEvaluating, setIsEvaluating] = useState<boolean>(false);
  const [analysisResult, setAnalysisResult] = useState<AssessmentResponse | null>(null);
  const [dataSource, setDataSource] = useState<"live_backend" | "deterministic_local">("deterministic_local");

  // Load preset persona
  const handleSelectPersona = (preset: PersonaPreset) => {
    setSelectedPersona(preset.id);
    setGoal(preset.goal);
    setExp(preset.exp);
    setScores(preset.scores);
    executeAnalysis(preset.goal, preset.exp, preset.scores);
  };

  const handleScoreChange = (key: keyof typeof scores, val: number) => {
    setSelectedPersona("custom");
    setScores((prev) => ({ ...prev, [key]: val }));
  };

  // Deterministic local computation matching Phase 5 L2-Logistic Regression and Phase 8 Framework
  const computeDeterministicProfile = (
    cGoal: string,
    cExp: string,
    cScores: typeof scores
  ): AssessmentResponse => {
    // Phase 5 Champion Model exact coefficients
    const z =
      -0.85 +
      1.28 * ((cScores.maths_stats - 3.0) / 0.8) +
      1.17 * ((cScores.storytelling - 3.0) / 0.8) +
      0.84 * ((cScores.ai_ml - 3.0) / 0.8) +
      0.48 * ((cScores.coding - 3.0) / 0.8) +
      0.52 * ((cScores.big_data - 3.0) / 0.8);

    const prob = Math.min(Math.max(1 / (1 + Math.exp(-z)), 0.04), 0.96);
    const isHigh = prob >= 0.5;

    const techScore =
      (cScores.maths_stats + cScores.coding + cScores.ai_ml + cScores.big_data) / 4.0;
    const narrativeScore = cScores.storytelling;

    let quadrant = "Q4";
    let quadrantTitle = "Q4: Foundational Development (Foundational Stage)";
    let summary = `Observed model signal indicates opportunities across both technical modeling and storytelling competencies.`;

    if (techScore >= 3.8 && narrativeScore >= 3.8) {
      quadrant = "Q1";
      quadrantTitle = "Q1: Advanced Career-Ready (Strategic Impact Profile)";
      summary = `High dual-currency alignment in observed JDS cohort across technical modeling (${techScore.toFixed(1)}/5.0) and storytelling (${narrativeScore.toFixed(1)}/5.0).`;
    } else if (techScore >= 3.8 && narrativeScore < 3.8) {
      quadrant = "Q2";
      quadrantTitle = "Q2: Pure Execution Specialist (Communication Development Priority)";
      summary = `Strong technical foundation (${techScore.toFixed(1)}/5.0), but executive storytelling (${narrativeScore.toFixed(1)}/5.0 vs 4.3 benchmark) is an evidence-supported development priority.`;
    } else if (techScore < 3.8 && narrativeScore >= 3.8) {
      quadrant = "Q3";
      quadrantTitle = "Q3: Strategic Facilitator (Applied Modeling Development Priority)";
      summary = `Strong narrative presence (${narrativeScore.toFixed(1)}/5.0), but deepening statistical rigor (${techScore.toFixed(1)}/5.0 vs 4.8 benchmark) represents an evidence-supported priority.`;
    }

    const radarData = SKILL_BENCHMARKS.map((b) => ({
      skill_key: b.key,
      skill_name: b.name,
      user_score: cScores[b.key as keyof typeof cScores],
      cohort_benchmark: b.benchmark,
      importance_rank: b.importanceRank,
    }));

    const recommendations = radarData.map((d) => {
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
            ? "Storytelling ranks #1 in out-of-fold permutation importance (0.1062) with a 3.23x adjusted odds ratio."
            : d.importance_rank === 2
            ? "Math/Stats drives the highest single odds ratio (AOR = 3.61) in the observed cohort."
            : "Core competency essential for end-to-end data science execution.",
        roi_multiplier:
          d.importance_rank === 1
            ? "3.23x Odds Multiplier"
            : d.importance_rank === 2
            ? "3.61x Odds Multiplier"
            : d.importance_rank === 3
            ? "2.32x Odds Multiplier"
            : "Baseline Currency",
      };
    });

    const strengths = radarData
      .filter((d) => d.cohort_benchmark - d.user_score <= 0.3)
      .map((d) => `${d.skill_name} (${d.user_score.toFixed(1)}/5.0 — High-Progression Benchmark: ${d.cohort_benchmark.toFixed(1)})`);

    const developmentGaps = radarData
      .filter((d) => d.cohort_benchmark - d.user_score > 0.3)
      .map((d) => `${d.skill_name} (Delta: -${(d.cohort_benchmark - d.user_score).toFixed(1)} from benchmark ${d.cohort_benchmark.toFixed(1)})`);

    const prioritySkills = recommendations
      .filter((r) => r.priority_level !== "Maintain Strength")
      .sort((a, b) => b.gap_delta - a.gap_delta)
      .map((r) => r.skill_name)
      .slice(0, 3);

    return {
      career_goal: cGoal,
      experience_level: cExp,
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
      strengths: strengths.length > 0 ? strengths : ["Foundational development across all areas"],
      development_gaps: developmentGaps.length > 0 ? developmentGaps : ["None identified; maintain current benchmarks"],
      recommendations,
      learning_sequence: [
        {
          step: 1,
          title: "Immediate 30-Day Focus: Close Primary Differentiator Delta",
          timeline: "Weeks 1–4",
          milestone: `Focus on ${prioritySkills[0] || "Storytelling"}: deliver a simulated executive briefing showing business P&L impact for an existing ML model.`,
          empirical_justification: "Phase 5 Permutation Importance demonstrates highest progression lift when addressing rank-1 feature gaps.",
        },
        {
          step: 2,
          title: "Mid-Term 60-Day Focus: Dual-Artifact Project Portfolio",
          timeline: "Weeks 5–8",
          milestone: "Construct an end-to-end repository featuring modular Python pipelines, unit tests, and an interactive stakeholder dashboard.",
          empirical_justification: "Satisfies Stage-2 Velocity criteria identified in the Phase 8 Competency Matrix.",
        },
        {
          step: 3,
          title: "Quarterly Review: Whiteboard Defense & Methodology Re-Assessment",
          timeline: "Weeks 9–12",
          milestone: "Conduct simulated oral technical defense addressing model assumptions, bias guards, and operational trade-offs.",
          empirical_justification: "Prepares practitioners for Quadrant Q1 transition as documented in Phase 8 Framework.",
        },
      ],
      methodology_disclaimer:
        "InsightPath provides evidence-based career development guidance. Model outputs reflect associations in the observed datasets and are not guarantees of hiring, promotion, salary, or career success.",
    };
  };

  // Execute analysis with instant fallback guarantee
  const executeAnalysis = useCallback(
    async (
      cGoal = goal,
      cExp = exp,
      cScores = scores
    ) => {
      setIsEvaluating(true);

      // Compute deterministic local baseline immediately (zero-wait guarantee for hackathon demo)
      const localResult = computeDeterministicProfile(cGoal, cExp, cScores);
      setAnalysisResult(localResult);
      setDataSource("deterministic_local");
      setAnalyzed(true);

      // Concurrently probe live backend to seamlessly promote to live inference if backend is responsive
      try {
        const payload: AssessmentRequest = {
          career_goal: cGoal,
          experience_level: cExp,
          maths_stats_skills: cScores.maths_stats,
          coding_skills: cScores.coding,
          ai_and_ml_skills: cScores.ai_ml,
          big_data_skills: cScores.big_data,
          dashboard_and_storytelling_skills: cScores.storytelling,
        };

        const resp = await submitAssessment(payload);
        if (resp && resp.data) {
          setAnalysisResult(resp.data);
          setDataSource(resp.source === "live_backend" ? "live_backend" : "deterministic_local");
        }
      } catch {
        // Retain deterministic local output seamlessly
      } finally {
        setIsEvaluating(false);
      }
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [goal, exp, scores]
  );

  // Initial load
  useEffect(() => {
    executeAnalysis();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const openEvidenceModal = (evidenceKey: string) => {
    const ev = EVIDENCE_REGISTRY[evidenceKey] || EVIDENCE_REGISTRY["dual_currency"];
    setActiveModalEvidence(ev);
    setIsModalOpen(true);
  };

  const currentResult = analysisResult || computeDeterministicProfile(goal, exp, scores);

  return (
    <div className="space-y-10">
      {/* Evidence Modal Component */}
      <EvidenceModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        evidence={activeModalEvidence}
      />

      {/* DEMO HEADER / JUDGE BANNER */}
      <div className="relative overflow-hidden rounded-2xl border border-teal-500/30 bg-gradient-to-br from-teal-950/20 via-slate-900/60 to-indigo-950/20 p-6 sm:p-8 backdrop-blur-md">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <div className="flex items-center space-x-2">
              <Badge className="bg-teal-500 text-slate-950 font-bold px-2.5 py-0.5 text-xs">
                JUDGE DEMO MODE
              </Badge>
              <Badge variant="outline" className="border-teal-500/40 text-teal-400 font-mono text-xs">
                ⏱️ Under 2-Minute Flow
              </Badge>
              <Badge
                variant="outline"
                className={`font-mono text-xs ${
                  dataSource === "live_backend"
                    ? "border-emerald-500/40 text-emerald-400 bg-emerald-500/10"
                    : "border-sky-500/40 text-sky-400 bg-sky-500/10"
                }`}
              >
                {dataSource === "live_backend" ? "● Live Champion Model" : "● Guaranteed Offline Engine"}
              </Badge>
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-white">
              End-to-End Career Intelligence Demonstration
            </h1>
            <p className="text-sm text-slate-300 leading-relaxed">
              Explore how InsightPath maps self-assessment scores against our validated{" "}
              <strong className="text-teal-300 font-semibold">L2-Regularized Logistic Regression</strong> model{" "}
              and 4-Quadrant Talent Matrix to produce evidence-supported growth roadmaps.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
            <Button
              onClick={() => executeAnalysis()}
              disabled={isEvaluating}
              className="bg-teal-500 hover:bg-teal-400 text-slate-950 font-semibold shadow-lg shadow-teal-500/20"
            >
              {isEvaluating ? (
                <>
                  <span className="w-4 h-4 border-2 border-slate-950 border-t-transparent rounded-full animate-spin mr-2" />
                  Evaluating Model...
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4 mr-2" />
                  Re-Evaluate Model
                </>
              )}
            </Button>
            <Button
              variant="outline"
              onClick={() => handleSelectPersona(PERSONA_PRESETS[0])}
              className="border-slate-700 hover:bg-slate-800 text-slate-200"
            >
              <RotateCcw className="w-4 h-4 mr-2 text-slate-400" />
              Reset to Persona A
            </Button>
          </div>
        </div>
      </div>

      {/* STEP 1 & 2: INPUTS & 1-CLICK PERSONA SELECTOR */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Preset Personas & Controls */}
        <div className="lg:col-span-5 space-y-6">
          {/* Quick Persona Picker */}
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 p-5 shadow-xs">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <span className="flex items-center justify-center w-6 h-6 rounded-full bg-teal-500/20 text-teal-600 dark:text-teal-400 font-mono text-xs font-bold">
                  1
                </span>
                <h2 className="font-semibold text-sm text-slate-900 dark:text-slate-100">
                  Select Judge Persona Preset (1-Click)
                </h2>
              </div>
              <span className="text-[11px] font-mono text-slate-500">Instant Test</span>
            </div>

            <div className="space-y-2.5">
              {PERSONA_PRESETS.map((preset) => {
                const isSelected = selectedPersona === preset.id;
                return (
                  <button
                    key={preset.id}
                    onClick={() => handleSelectPersona(preset)}
                    className={`w-full text-left p-3 rounded-lg border transition-all text-xs ${
                      isSelected
                        ? "border-teal-500 bg-teal-500/10 dark:bg-teal-500/10 ring-1 ring-teal-500"
                        : "border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 bg-slate-50/50 dark:bg-slate-800/40"
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-semibold text-slate-900 dark:text-slate-100 flex items-center gap-1.5">
                        {isSelected && <Check className="w-3.5 h-3.5 text-teal-500" />}
                        {preset.name.split(" (")[0]}
                      </span>
                      <Badge
                        variant="outline"
                        className={`text-[10px] py-0 px-1.5 font-mono ${
                          isSelected
                            ? "border-teal-500 text-teal-600 dark:text-teal-400"
                            : "border-slate-300 dark:border-slate-700 text-slate-500"
                        }`}
                      >
                        {preset.badge}
                      </Badge>
                    </div>
                    <p className="text-[11px] text-slate-600 dark:text-slate-400 leading-snug">
                      {preset.description}
                    </p>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Goal & Experience Selection */}
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 p-5 shadow-xs space-y-4">
            <div className="flex items-center space-x-2">
              <span className="flex items-center justify-center w-6 h-6 rounded-full bg-teal-500/20 text-teal-600 dark:text-teal-400 font-mono text-xs font-bold">
                2
              </span>
              <h2 className="font-semibold text-sm text-slate-900 dark:text-slate-100">
                Career Goal & Experience Level
              </h2>
            </div>

            <div className="space-y-3">
              <div>
                <label className="text-xs text-slate-600 dark:text-slate-400 block mb-1.5 font-medium">
                  Target Data Science Role
                </label>
                <div className="flex flex-wrap gap-1.5">
                  {CAREER_GOALS.map((g) => (
                    <button
                      key={g}
                      onClick={() => {
                        setGoal(g);
                        setSelectedPersona("custom");
                      }}
                      className={`px-2.5 py-1 rounded text-xs transition-colors font-medium ${
                        goal === g
                          ? "bg-slate-900 text-white dark:bg-teal-500 dark:text-slate-950"
                          : "bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700"
                      }`}
                    >
                      {g}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-xs text-slate-600 dark:text-slate-400 block mb-1.5 font-medium">
                  Experience Tier
                </label>
                <div className="flex flex-wrap gap-1.5">
                  {EXPERIENCE_LEVELS.map((e) => (
                    <button
                      key={e}
                      onClick={() => {
                        setExp(e);
                        setSelectedPersona("custom");
                      }}
                      className={`px-2.5 py-1 rounded text-xs transition-colors font-medium ${
                        exp === e
                          ? "bg-slate-900 text-white dark:bg-indigo-500 dark:text-white"
                          : "bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700"
                      }`}
                    >
                      {e.split(" ")[0]}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: 5 Skill Sliders & Analyze Button */}
        <div className="lg:col-span-7 space-y-6">
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 p-5 shadow-xs space-y-5">
            <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
              <div className="flex items-center space-x-2">
                <span className="flex items-center justify-center w-6 h-6 rounded-full bg-teal-500/20 text-teal-600 dark:text-teal-400 font-mono text-xs font-bold">
                  3
                </span>
                <div>
                  <h2 className="font-semibold text-sm text-slate-900 dark:text-slate-100">
                    Fine-Tune Skill Competencies (1.0 – 5.0 Likert Scale)
                  </h2>
                  <p className="text-[11px] text-slate-500">
                    Calibrated against the N=139 Junior Data Scientist cohort benchmarks
                  </p>
                </div>
              </div>
              <Badge variant="outline" className="font-mono text-[10px] text-teal-600 dark:text-teal-400 border-teal-500/30">
                5 Dimensions
              </Badge>
            </div>

            <div className="space-y-4">
              {SKILL_BENCHMARKS.map((dim) => {
                const currentVal = scores[dim.key as keyof typeof scores];
                const delta = Math.round((currentVal - dim.benchmark) * 10) / 10;
                const isStory = dim.key === "storytelling";

                return (
                  <div
                    key={dim.key}
                    className={`p-3.5 rounded-lg border transition-all ${
                      isStory
                        ? "border-amber-500/30 bg-amber-500/5 dark:bg-amber-500/5"
                        : "border-slate-200 dark:border-slate-800/80 bg-slate-50/50 dark:bg-slate-900/40"
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1.5">
                      <div className="flex items-center space-x-2">
                        <span className="font-medium text-xs text-slate-900 dark:text-slate-100">
                          {dim.name}
                        </span>
                        {isStory && (
                          <Badge className="bg-amber-500/20 text-amber-600 dark:text-amber-400 border border-amber-500/30 text-[10px] py-0 px-1 font-mono">
                            ★ Rank #1 Feature (3.23x AOR)
                          </Badge>
                        )}
                      </div>
                      <div className="flex items-center space-x-2 font-mono text-xs">
                        <span className="text-slate-500 text-[11px]">
                          Cohort Benchmark: <strong>{dim.benchmark}</strong>
                        </span>
                        <span className="font-bold text-teal-600 dark:text-teal-400 px-2 py-0.5 rounded bg-teal-500/10 border border-teal-500/20">
                          {currentVal.toFixed(1)} / 5.0
                        </span>
                      </div>
                    </div>

                    <p className="text-[11px] text-slate-500 dark:text-slate-400 mb-2">
                      {dim.desc}
                    </p>

                    <div className="flex items-center space-x-3">
                      <span className="text-[10px] font-mono text-slate-400">1.0</span>
                      <input
                        type="range"
                        min="1.0"
                        max="5.0"
                        step="0.1"
                        value={currentVal}
                        onChange={(e) =>
                          handleScoreChange(dim.key as keyof typeof scores, parseFloat(e.target.value))
                        }
                        className="w-full accent-teal-500 cursor-pointer h-1.5 rounded-lg bg-slate-200 dark:bg-slate-700"
                      />
                      <span className="text-[10px] font-mono text-slate-400">5.0</span>
                    </div>

                    <div className="mt-2 flex items-center justify-between text-[11px]">
                      <span
                        className={`font-mono text-[10px] ${
                          delta >= 0
                            ? "text-emerald-600 dark:text-emerald-400"
                            : "text-amber-600 dark:text-amber-400"
                        }`}
                      >
                        {delta >= 0 ? `+${delta.toFixed(1)} above benchmark` : `${delta.toFixed(1)} vs benchmark`}
                      </span>
                      <button
                        onClick={() => openEvidenceModal(dim.key)}
                        className="text-[11px] text-teal-600 dark:text-teal-400 hover:underline flex items-center gap-1 font-medium"
                      >
                        <HelpCircle className="w-3 h-3" />
                        <span>Why this benchmark?</span>
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Prominent Analyze Button */}
            <div className="pt-2">
              <Button
                onClick={() => executeAnalysis()}
                disabled={isEvaluating}
                className="w-full h-12 text-sm bg-slate-900 hover:bg-slate-800 dark:bg-teal-500 dark:hover:bg-teal-400 dark:text-slate-950 text-white font-bold shadow-md transition-all flex items-center justify-center space-x-2"
              >
                {isEvaluating ? (
                  <>
                    <span className="w-4 h-4 border-2 border-white dark:border-slate-950 border-t-transparent rounded-full animate-spin" />
                    <span>Evaluating Against Champion Logistic L2 Pipeline...</span>
                  </>
                ) : (
                  <>
                    <Zap className="w-4 h-4 text-amber-400 dark:text-slate-950" />
                    <span>Analyze My Profile Against Validated Models</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* RESULTS DISPLAY: STEPS 4, 5, 6, 7, 8 */}
      {analyzed && currentResult && (
        <div className="space-y-8 animate-in fade-in duration-300">
          <div className="border-t border-slate-200 dark:border-slate-800 pt-8">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
              <div>
                <div className="flex items-center space-x-2">
                  <span className="flex items-center justify-center w-6 h-6 rounded-full bg-teal-500/20 text-teal-600 dark:text-teal-400 font-mono text-xs font-bold">
                    4
                  </span>
                  <h2 className="text-xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
                    Model Development Signal & Talent Matrix Placement
                  </h2>
                </div>
                <p className="text-xs text-slate-500 mt-0.5">
                  Derived from Phase 5 L2-Logistic Regression and Phase 8 Dual-Currency Matrix
                </p>
              </div>

              <div className="flex items-center space-x-2">
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => openEvidenceModal("dual_currency")}
                  className="text-xs border-teal-500/40 text-teal-600 dark:text-teal-400 hover:bg-teal-500/10"
                >
                  <FlaskConical className="w-3.5 h-3.5 mr-1.5" />
                  <span>Why this recommendation?</span>
                </Button>
              </div>
            </div>

            {/* SIGNAL METRICS ROW */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
              {/* Card 1: Model Signal Probability */}
              <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-xs">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-medium text-slate-500">Observed Model Signal</span>
                  <Badge
                    variant="outline"
                    className={`font-mono text-[10px] ${
                      currentResult.model_probability >= 0.5
                        ? "border-emerald-500/40 text-emerald-600 dark:text-emerald-400 bg-emerald-500/10"
                        : "border-amber-500/40 text-amber-600 dark:text-amber-400 bg-amber-500/10"
                    }`}
                  >
                    {currentResult.model_classification}
                  </Badge>
                </div>
                <div className="flex items-baseline space-x-2">
                  <span className="text-3xl font-extrabold text-slate-900 dark:text-white font-mono">
                    {(currentResult.model_probability * 100).toFixed(1)}%
                  </span>
                  <span className="text-xs text-slate-500">progression probability</span>
                </div>
                <p className="text-[11px] text-slate-500 mt-2">
                  Based on N=139 Junior Data Scientist cohort calibration (ROC-AUC: 0.9035).
                </p>
              </div>

              {/* Card 2: Quadrant Assignment */}
              <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-xs">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-medium text-slate-500">Talent Matrix Placement</span>
                  <Badge className="bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/30 font-mono text-[10px]">
                    {currentResult.quadrant_assigned}
                  </Badge>
                </div>
                <div className="font-bold text-slate-900 dark:text-slate-100 text-sm mt-1">
                  {currentResult.quadrant_title.split(": ")[1] || currentResult.quadrant_title}
                </div>
                <p className="text-[11px] text-slate-500 mt-2">
                  Phase 8 Dual-Currency Framework mapping Technical vs Narrative capacity.
                </p>
              </div>

              {/* Card 3: Dual Currency Balance */}
              <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-xs">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-medium text-slate-500">Dual-Currency Balance</span>
                  <span className="text-[10px] font-mono text-slate-400">Scale 1–5</span>
                </div>
                <div className="space-y-1.5 text-xs font-mono">
                  <div className="flex justify-between">
                    <span className="text-slate-500">Technical Currency:</span>
                    <strong className="text-slate-900 dark:text-slate-200">
                      {(
                        (scores.maths_stats + scores.coding + scores.ai_ml + scores.big_data) /
                        4.0
                      ).toFixed(1)}{" "}
                      / 5.0
                    </strong>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">Narrative Currency:</span>
                    <strong className="text-amber-600 dark:text-amber-400">
                      {scores.storytelling.toFixed(1)} / 5.0
                    </strong>
                  </div>
                </div>
                <p className="text-[11px] text-slate-500 mt-1.5">
                  Narrative currency determines whether technical models secure leadership buy-in.
                </p>
              </div>
            </div>

            {/* STEPS 5 & 6: STRENGTHS & GAPS */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              {/* Step 5: Top Strengths */}
              <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-xs space-y-3">
                <div className="flex items-center space-x-2">
                  <span className="flex items-center justify-center w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 font-mono text-xs font-bold">
                    5
                  </span>
                  <h3 className="font-semibold text-sm text-slate-900 dark:text-slate-100 flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                    Observed Model Strengths
                  </h3>
                </div>
                <ul className="space-y-2 text-xs">
                  {currentResult.strengths.map((str, idx) => (
                    <li
                      key={idx}
                      className="p-2.5 rounded-lg bg-emerald-500/5 border border-emerald-500/20 text-slate-700 dark:text-slate-300 flex items-start gap-2"
                    >
                      <Check className="w-3.5 h-3.5 text-emerald-500 mt-0.5 shrink-0" />
                      <span>{str}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Step 6: Priority Development Gaps */}
              <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-xs space-y-3">
                <div className="flex items-center space-x-2">
                  <span className="flex items-center justify-center w-5 h-5 rounded-full bg-amber-500/20 text-amber-600 dark:text-amber-400 font-mono text-xs font-bold">
                    6
                  </span>
                  <h3 className="font-semibold text-sm text-slate-900 dark:text-slate-100 flex items-center gap-1.5">
                    <AlertTriangle className="w-4 h-4 text-amber-500" />
                    Priority Development Gaps
                  </h3>
                </div>
                <ul className="space-y-2 text-xs">
                  {currentResult.development_gaps.map((gap, idx) => (
                    <li
                      key={idx}
                      className="p-2.5 rounded-lg bg-amber-500/5 border border-amber-500/20 text-slate-700 dark:text-slate-300 flex items-start gap-2"
                    >
                      <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-1.5 shrink-0" />
                      <span>{gap}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* STEP 7: EVIDENCE BEHIND RECOMMENDATIONS (WITH VISIBLE "Why this recommendation?" CONTROLS) */}
            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-xs space-y-4 mb-8">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 dark:border-slate-800 pb-3">
                <div className="flex items-center space-x-2">
                  <span className="flex items-center justify-center w-6 h-6 rounded-full bg-teal-500/20 text-teal-600 dark:text-teal-400 font-mono text-xs font-bold">
                    7
                  </span>
                  <div>
                    <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100">
                      Evidence-Supported Recommendations
                    </h3>
                    <p className="text-[11px] text-slate-500">
                      Every recommendation includes an interactive audit control displaying empirical rationale
                    </p>
                  </div>
                </div>
                <Badge variant="outline" className="text-[10px] font-mono border-teal-500/30 text-teal-600 dark:text-teal-400">
                  Full Empirical Traceability
                </Badge>
              </div>

              <div className="space-y-3">
                {currentResult.recommendations.map((rec, idx) => {
                  const isStory = rec.skill_name.toLowerCase().includes("storytelling");
                  const isMath = rec.skill_name.toLowerCase().includes("math");
                  const evidenceKey = isStory ? "storytelling" : isMath ? "maths_stats" : "ai_ml";

                  return (
                    <div
                      key={idx}
                      className="p-4 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/40 flex flex-col sm:flex-row sm:items-center justify-between gap-4"
                    >
                      <div className="space-y-1 max-w-xl">
                        <div className="flex items-center space-x-2">
                          <span className="font-bold text-xs text-slate-900 dark:text-slate-100">
                            {rec.skill_name}
                          </span>
                          <Badge
                            variant="outline"
                            className={`text-[10px] font-mono ${
                              rec.priority_level === "Immediate Priority"
                                ? "border-amber-500 text-amber-600 dark:text-amber-400 bg-amber-500/10"
                                : rec.priority_level === "Secondary Focus"
                                ? "border-sky-500 text-sky-600 dark:text-sky-400 bg-sky-500/10"
                                : "border-emerald-500 text-emerald-600 dark:text-emerald-400 bg-emerald-500/10"
                            }`}
                          >
                            {rec.priority_level}
                          </Badge>
                          <span className="text-[11px] font-mono text-slate-400">
                            Score: {rec.current_score.toFixed(1)} / Benchmark: {rec.target_benchmark.toFixed(1)}
                          </span>
                        </div>
                        <p className="text-xs text-slate-600 dark:text-slate-300">
                          {rec.evidence_rationale}
                        </p>
                      </div>

                      {/* Visible "Why this recommendation?" Control */}
                      <div className="shrink-0">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => openEvidenceModal(evidenceKey)}
                          className="text-xs border-teal-500/40 text-teal-600 dark:text-teal-400 hover:bg-teal-500/10 h-8"
                        >
                          <FlaskConical className="w-3.5 h-3.5 mr-1.5" />
                          <span>Why this recommendation?</span>
                        </Button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* STEP 8: CAREER ROADMAP */}
            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-xs space-y-4 mb-8">
              <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
                <div className="flex items-center space-x-2">
                  <span className="flex items-center justify-center w-6 h-6 rounded-full bg-teal-500/20 text-teal-600 dark:text-teal-400 font-mono text-xs font-bold">
                    8
                  </span>
                  <div>
                    <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100">
                      Tailored Career Roadmap (Stage-Gated Milestones)
                    </h3>
                    <p className="text-[11px] text-slate-500">
                      Sequential 30-day, 60-day, and quarterly milestones aligned with Phase 8 Talent Framework
                    </p>
                  </div>
                </div>
                <Link href="/roadmap" className="text-xs text-teal-600 dark:text-teal-400 hover:underline flex items-center gap-1 font-medium">
                  <span>Full Roadmap</span>
                  <ChevronRight className="w-3 h-3" />
                </Link>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {currentResult.learning_sequence.map((stage) => (
                  <div
                    key={stage.step}
                    className="p-4 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/30 space-y-2 relative"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-teal-500/10 text-teal-600 dark:text-teal-400 font-bold">
                        {stage.timeline}
                      </span>
                      <span className="text-[10px] font-mono text-slate-400">Stage {stage.step}</span>
                    </div>
                    <div className="font-bold text-xs text-slate-900 dark:text-slate-100">
                      {stage.title}
                    </div>
                    <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                      {stage.milestone}
                    </p>
                    <div className="pt-2 border-t border-slate-100 dark:border-slate-800 text-[10px] text-slate-500 italic">
                      {stage.empirical_justification}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* COMPACT METHODOLOGY PANEL (4 Evidence Sources + Stats + ML + Framework) */}
      <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-900/60 p-6 sm:p-8 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
          <div>
            <div className="flex items-center space-x-2">
              <Badge className="bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/30 text-xs font-mono">
                METHODOLOGY AUDIT
              </Badge>
              <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100">
                Rigorous 4-Pillar Analytical Foundation
              </h2>
            </div>
            <p className="text-xs text-slate-500 mt-1">
              Every score, benchmark, and priority in InsightPath is grounded in reproducible data science pipelines.
            </p>
          </div>

          <Link href="/methodology">
            <Button size="sm" variant="outline" className="text-xs">
              <BookOpen className="w-3.5 h-3.5 mr-1.5" />
              <span>Full Methodology Audit</span>
            </Button>
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Pillar 1: 4 Evidence Sources */}
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 space-y-2">
            <div className="flex items-center space-x-2 text-teal-600 dark:text-teal-400">
              <Database className="w-4 h-4" />
              <h3 className="font-bold text-xs text-slate-900 dark:text-slate-100">4 Evidence Sources</h3>
            </div>
            <ul className="text-[11px] text-slate-600 dark:text-slate-400 space-y-1 leading-snug">
              <li>• <strong>17,443 Job Postings</strong> (Macro & Micro demand)</li>
              <li>• <strong>N=139 Junior Data Scientists</strong> (5 skill dimensions)</li>
              <li>• <strong>N=4,000 Senior Profiles</strong> (Big Five psychometrics)</li>
              <li>• <strong>Phase 7 Synthesis</strong> (Triangulated cross-validation)</li>
            </ul>
          </div>

          {/* Pillar 2: Statistical Analysis */}
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 space-y-2">
            <div className="flex items-center space-x-2 text-indigo-600 dark:text-indigo-400">
              <BarChart3 className="w-4 h-4" />
              <h3 className="font-bold text-xs text-slate-900 dark:text-slate-100">Statistical Testing</h3>
            </div>
            <ul className="text-[11px] text-slate-600 dark:text-slate-400 space-y-1 leading-snug">
              <li>• <strong>Hypothesis Testing</strong> (Chi-Square & ANOVA F-tests)</li>
              <li>• <strong>Non-Parametric</strong> (Mann-Whitney U tests)</li>
              <li>• <strong>Effect Sizes</strong> (Adjusted Odds Ratios with 95% CIs)</li>
              <li>• <strong>Bonferroni Correction</strong> (Strict α = 0.05 cutoff)</li>
            </ul>
          </div>

          {/* Pillar 3: Machine Learning Model */}
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 space-y-2">
            <div className="flex items-center space-x-2 text-emerald-600 dark:text-emerald-400">
              <Cpu className="w-4 h-4" />
              <h3 className="font-bold text-xs text-slate-900 dark:text-slate-100">ML Champion Model</h3>
            </div>
            <ul className="text-[11px] text-slate-600 dark:text-slate-400 space-y-1 leading-snug">
              <li>• <strong>L2-Regularized Logistic Regression</strong> (C=0.1)</li>
              <li>• <strong>5-Fold Stratified Cross-Validation</strong></li>
              <li>• <strong>Repeated Out-of-Fold Permutation</strong> (n=10)</li>
              <li>• <strong>ROC-AUC: 0.9035</strong> (Zero-leakage pipeline)</li>
            </ul>
          </div>

          {/* Pillar 4: Career Framework */}
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 space-y-2">
            <div className="flex items-center space-x-2 text-amber-600 dark:text-amber-400">
              <Compass className="w-4 h-4" />
              <h3 className="font-bold text-xs text-slate-900 dark:text-slate-100">Career Framework</h3>
            </div>
            <ul className="text-[11px] text-slate-600 dark:text-slate-400 space-y-1 leading-snug">
              <li>• <strong>4-Quadrant Talent Matrix</strong> (Dual-Currency)</li>
              <li>• <strong>4 Career Stages</strong> (Foundation to Executive)</li>
              <li>• <strong>Stage-Gated Milestones</strong> (Actionable roadmaps)</li>
              <li>• <strong>Stakeholder Guidance</strong> (Students & Mentors)</li>
            </ul>
          </div>
        </div>
      </div>

      {/* MANDATORY ETHICAL & METHODOLOGICAL DISCLAIMER */}
      <div className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-4 sm:p-5 flex items-start space-x-3 text-amber-900 dark:text-amber-200">
        <ShieldAlert className="w-5 h-5 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
        <div className="space-y-1 text-xs leading-relaxed">
          <span className="font-bold uppercase tracking-wider text-[11px] block">
            Ethical & Methodological Notice
          </span>
          <p>
            InsightPath provides evidence-based career development guidance. Model outputs reflect associations in the observed datasets and are not guarantees of hiring, promotion, salary, or career success.
          </p>
        </div>
      </div>
    </div>
  );
}

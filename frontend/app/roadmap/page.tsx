"use client";

import React, { useState, useEffect } from "react";
import {
  GraduationCap,
  Building2,
  Users,
  CheckCircle2,
  Sparkles,
  BookOpen,
} from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Sidebar } from "@/components/Sidebar";
import { Footer } from "@/components/Footer";
import { Badge } from "@/components/ui/badge";
import { ChartCard } from "@/components/ChartCard";
import { CareerRoadmapVisual } from "@/components/CareerRoadmapVisual";
import { EvidenceModal, EvidenceDetail } from "@/components/EvidenceModal";

import {
  fetchCareerStages,
  CareerStageItem,
} from "@/lib/api";

const BLUEPRINTS = {
  student: {
    title: "Student & Job-Seeker Roadmap",
    roleDescription: "Engineered transition pathway for aspiring and early-career data scientists to reach top-tier readiness.",
    icon: GraduationCap,
    badge: "Candidate Track",
    kpis: [
      { label: "Target Readiness", value: "Quadrant Q1" },
      { label: "Expected Timeframe", value: "6–12 Months" },
      { label: "Salary Target", value: "₹14L – ₹22L+" },
    ],
    phases: [
      {
        phase: "Phase 1: Table-Stakes Foundations (Months 1–3)",
        focus: "SQL & Python Engineering Rigor",
        evidence: "SQL requested in 5.78% and Python in 5.30% of audited requisitions (Baseline Currency).",
        milestones: [
          "Master complex SQL: CTEs, window functions, query plan optimization, and relational schema design.",
          "Write production Python: clean modular code, unit tests, typing, and Git workflows.",
          "Avoid toy datasets; build ingestion pipelines on raw, messy public APIs and databases.",
        ],
      },
      {
        phase: "Phase 2: Mathematical Modeling & Rigor (Months 4–6)",
        focus: "Applied Statistics, Inference & Machine Learning",
        evidence: "Math/Stats drives the highest single promotional odds (AOR = 3.61, β = +1.28).",
        milestones: [
          "Study classical experimental design: A/B testing power analysis, p-value adjustments, bootstrap CI.",
          "Implement Scikit-Learn pipelines with leakage prevention, cross-validation, and ROC-AUC analysis.",
          "Defend model assumptions: collinearity, residuals, and interpretability (permutation importance).",
        ],
      },
      {
        phase: "Phase 3: The Differentiator Currency (Months 7–9)",
        focus: "Business Storytelling & Executive Dashboards",
        evidence: "High storytelling aptitude yields a 3.23x adjusted odds ratio for top compensation.",
        milestones: [
          "Translate technical outputs into P&L and ROI business cases for non-technical stakeholders.",
          "Build production executive dashboards (Tableau / PowerBI) emphasizing metric hierarchies.",
          "Conduct oral project defenses: practice answering 'So what?' in 90-second executive summaries.",
        ],
      },
      {
        phase: "Phase 4: Senior Readiness & Adaptive Mindset (Months 10–12)",
        focus: "Intellectual Openness & Consulting Adaptability",
        evidence: "Openness (AOR = 7.72) and Conscientiousness (AOR = 8.11) dominate senior consulting success.",
        milestones: [
          "Lead cross-functional projects with ambiguous requirements and uncertain data inputs.",
          "Engage in structured peer code reviews and client expectation management exercises.",
          "Publish complete portfolio repositories featuring documentation, dashboard links, and video walkthroughs.",
        ],
      },
    ],
  },
  university: {
    title: "University & Academic Curriculum Blueprint",
    roleDescription: "Curricular restructuring blueprint for universities and coding bootcamps based on empirical labor market demand.",
    icon: BookOpen,
    badge: "Educator Track",
    kpis: [
      { label: "Placement Rate Target", value: ">85% in Tier-1/2" },
      { label: "Curriculum Shift", value: "Dual-Currency Model" },
      { label: "Key Addition", value: "Storytelling Practicum" },
    ],
    phases: [
      {
        phase: "Recommendation 1: De-emphasize Premature Big Data Infrastructure",
        focus: "Reallocate Credits to Applied Inferential Statistics",
        evidence: "Distributed Big Data shows Rank #5 permutation importance (0.0107) and neutral hike odds (AOR = 0.94).",
        milestones: [
          "Eliminate distributed Hadoop/Spark cluster administration from introductory core curricula.",
          "Replace low-retention infrastructure modules with rigorous applied hypothesis testing.",
          "Mandate coverage of p-value adjustments, effect sizes, power calculations, and collinearity diagnostics.",
        ],
      },
      {
        phase: "Recommendation 2: Institutionalize Mandatory Storytelling Practicums",
        focus: "Executive Communication & Stakeholder Defense",
        evidence: "Storytelling is the #1 out-of-fold permutation importance driver (0.1062) for junior promotion velocity.",
        milestones: [
          "Require 30% of capstone project grades to be based on oral presentation to non-technical evaluators.",
          "Teach dashboard design principles: visual hierarchy, cognitive load, and decision architecture.",
          "Train students to draft 1-page executive memos summarizing technical machine-learning models.",
        ],
      },
      {
        phase: "Recommendation 3: Mandate End-to-End Messy Data Engineering",
        focus: "From Raw Requisitions to Validated Schemas",
        evidence: "Audited market datasets required extensive standardization across 642 unique employers.",
        milestones: [
          "Ban pre-cleaned Kaggle CSVs in intermediate and advanced coursework.",
          "Assign assignments requiring web scraping, regex parsing, handling missingness, and outlier winsorization.",
          "Incorporate automated data quality scorecards and schema assertion tests into automated grading.",
        ],
      },
    ],
  },
  mentor: {
    title: "Mentor & Practitioner Coaching Guide",
    roleDescription: "Targeted mentoring protocols to diagnose and transition talent across the Four-Quadrant matrix.",
    icon: Users,
    badge: "Mentorship Track",
    kpis: [
      { label: "Diagnostic Engine", value: "4-Quadrant Mapping" },
      { label: "Primary Intervention", value: "Executive Presence" },
      { label: "Assessment Cycle", value: "Quarterly Review" },
    ],
    phases: [
      {
        phase: "Protocol 1: Diagnosing Q2 (Execution Heavy, Communication Gap)",
        focus: "The Execution Engine Trapped at Mid-Tier Compensation",
        evidence: "Q2 salary velocity drops from 100% to 66-82% despite technical superiority (JDS CART Rules 3 & 4).",
        milestones: [
          "Assign simulated executive stakeholder roleplay sessions to build business translation capability.",
          "Guide candidate to build interactive dashboards for existing models rather than learning more algorithms.",
          "Coach on verbal conciseness: structuring answers with the Pyramid Principle and executive summaries.",
        ],
      },
      {
        phase: "Protocol 2: Diagnosing Q3 (Communication Strong, Technical Gap)",
        focus: "The Strategic Facilitator Needing Modeling Rigor",
        evidence: "Communication partially compensates for math gaps (71.4% hike rate), but wage ceilings apply.",
        milestones: [
          "Assign targeted drills in mathematical modeling, cross-validation protocols, and regularization trade-offs.",
          "Require candidate to audit existing models for data leakage, multicollinearity, and overfitting.",
          "Pair candidate with senior technical architects on production code reviews.",
        ],
      },
      {
        phase: "Protocol 3: Preparing Senior Talent for Leadership",
        focus: "Fostering Intellectual Adaptability and Conscientiousness",
        evidence: "Openness (AOR = 7.72) and Conscientiousness (AOR = 8.11) separate senior consulting advisory success.",
        milestones: [
          "Transition mentoring from technical debugging to ambiguous problem scoping and client empathy.",
          "Encourage exposure to cross-industry client cases and strategic advisory roadmaps.",
          "Reinforce ethical AI principles and responsible model deployment standards.",
        ],
      },
    ],
  },
  employer: {
    title: "Enterprise Employer Talent Strategy",
    roleDescription: "Evidence-based hiring rubric and talent progression policy for engineering leaders and HR executives.",
    icon: Building2,
    badge: "Employer Track",
    kpis: [
      { label: "Hiring Signal", value: "Dual-Currency Rubric" },
      { label: "Ethical Compliance", value: "Zero Psychometric Gating" },
      { label: "Retention Impact", value: "+30% Promotion Velocity" },
    ],
    phases: [
      {
        phase: "Policy 1: Modernize Screening Filters Beyond LeetCode",
        focus: "Dual-Currency Candidate Evaluation",
        evidence: "Procedural coding shows near-zero promotional lift (AOR = 1.04), while storytelling drives 3.23x lift.",
        milestones: [
          "Replace purely algorithmic syntax quizzes with business problem scoping and data interpretation exercises.",
          "Evaluate candidates on their ability to explain statistical trade-offs and communicate findings to executives.",
          "Score portfolios for interactive dashboards, clean documentation, and end-to-end delivery.",
        ],
      },
      {
        phase: "Policy 2: Enforce Strict Ethical Safeguards on Psychometrics",
        focus: "Ban Automated Gatekeeping via Personality Assessments",
        evidence: "Phase 6 Ethical Guardrail: Personality reflects coaching diagnostics, never employment gatekeeping.",
        milestones: [
          "Explicitly prohibit automated filtering, rejection, or promotion decisions based on Big Five assessments.",
          "Use psychometric frameworks strictly for voluntary leadership coaching, onboarding, and self-reflection.",
          "Audit internal hiring algorithms annually for disparate impact and demographic fairness.",
        ],
      },
      {
        phase: "Policy 3: Establish Clear Progression Tracks for Q1-Q4",
        focus: "Clear Promotion Rubrics and Individual Contributor Ladders",
        evidence: "Q2 practitioners hit career plateaus, creating flight risk and loss of top technical talent.",
        milestones: [
          "Create dual advancement tracks: Principal Individual Contributor (Technical) and Advisory / Leadership.",
          "Fund executive communication coaching programs for high-performing technical specialists (Q2).",
          "Tie promotion criteria to documented business impact rather than tenure alone.",
        ],
      },
    ],
  },
};

export default function RoadmapPage() {
  const [activeBlueprintKey, setActiveBlueprintKey] = useState<keyof typeof BLUEPRINTS>("student");
  const [careerStages, setCareerStages] = useState<CareerStageItem[]>([]);

  const [selectedEvidence, setSelectedEvidence] = useState<EvidenceDetail | null>(null);
  const [isEvidenceOpen, setIsEvidenceOpen] = useState(false);

  useEffect(() => {
    fetchCareerStages().then((stageRes) => {
      setCareerStages(stageRes.records);
    });
  }, []);

  const activeBlueprint = BLUEPRINTS[activeBlueprintKey];
  const Icon = activeBlueprint.icon;

  const openEvidence = (detail: EvidenceDetail) => {
    setSelectedEvidence(detail);
    setIsEvidenceOpen(true);
  };

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--foreground)]">
      <Navbar />

      <div className="flex-1 flex w-full">
        <Sidebar className="hidden lg:flex" />

        <main className="flex-1 p-4 md:p-8 max-w-7xl mx-auto w-full space-y-10">
          {/* Header */}
          <div className="space-y-3 pb-6 border-b border-slate-200/80 dark:border-slate-800">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-mono font-medium border border-teal-500/30 bg-teal-500/10 text-teal-600 dark:text-teal-400">
              <Sparkles className="w-3.5 h-3.5 mr-1" />
              <span>Phase 8 Career-Readiness & Action Blueprints</span>
            </div>
            <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight text-slate-900 dark:text-slate-100">
              Evidence-Based Implementation Blueprints
            </h1>
            <p className="text-sm text-slate-500 dark:text-slate-400 max-w-3xl leading-relaxed">
              Operational blueprints translating empirical findings from 17,443 requisitions and 300 practitioners into structured roadmaps for students, academic departments, mentors, and hiring organizations.
            </p>
          </div>

          {/* Interactive Career Progression Roadmap */}
          <ChartCard
            title="Four-Tier Empirical Progression Framework"
            subtitle="Explore stage-specific competencies, empirical rationales, recommended development milestones, and measurable KPIs"
            badge={<Badge variant="outline" className="text-[10px]">Phase 8 Framework</Badge>}
          >
            <CareerRoadmapVisual
              stages={careerStages}
              onOpenEvidence={() =>
                openEvidence({
                  title: "Four-Tier Career Progression Framework",
                  phase: "Phase 8: Career-Readiness Framework",
                  dataset: "Cross-dataset synthesis across all 4 datasets",
                  sampleSize: "N = 17,443 postings & 300 practitioners",
                  method: "Multi-cohort evidence synthesis establishing required competencies and KPIs by career stage.",
                  interpretation: "Documents how career value creation shifts systematically from syntactic entry compliance (Stage 1) to salary hike velocity via storytelling and statistical modeling (Stage 2), premium stack differentiation (Stage 3), and advisory leadership adaptability (Stage 4).",
                  limitation: "Progression velocity varies by organization size, industry vertical, and geography.",
                })
              }
            />
          </ChartCard>

          {/* Track Selector Tabs */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100">
                Stakeholder-Specific Roadmaps
              </h2>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {(Object.keys(BLUEPRINTS) as (keyof typeof BLUEPRINTS)[]).map((key) => {
                const bp = BLUEPRINTS[key];
                const BpIcon = bp.icon;
                const isSelected = activeBlueprintKey === key;
                return (
                  <button
                    key={key}
                    type="button"
                    onClick={() => setActiveBlueprintKey(key)}
                    className={`p-3.5 rounded-xl border text-left transition-all flex flex-col justify-between space-y-2 ${
                      isSelected
                        ? "border-teal-500 bg-teal-50/60 dark:bg-teal-950/30 ring-1 ring-teal-500 shadow-xs"
                        : "border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 hover:bg-slate-50 dark:hover:bg-slate-800/40"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <BpIcon className={`w-4 h-4 ${isSelected ? "text-teal-600 dark:text-teal-400" : "text-slate-400"}`} />
                      <Badge variant="outline" className="text-[10px] font-mono py-0 px-1.5">
                        {bp.badge}
                      </Badge>
                    </div>
                    <span className="text-xs font-bold text-slate-800 dark:text-slate-200 truncate block">
                      {bp.title.split("&")[0].split("Blueprint")[0].split("Roadmap")[0].trim()}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Active Blueprint View */}
          <div className="p-6 rounded-2xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/80 space-y-6 shadow-xs">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-100 dark:border-slate-800">
              <div className="space-y-1">
                <div className="flex items-center space-x-2">
                  <Icon className="w-5 h-5 text-teal-600 dark:text-teal-400" />
                  <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">
                    {activeBlueprint.title}
                  </h3>
                </div>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  {activeBlueprint.roleDescription}
                </p>
              </div>

              <div className="flex items-center gap-3">
                {activeBlueprint.kpis.map((kpi, i) => (
                  <div key={i} className="text-right">
                    <span className="text-[10px] font-mono text-slate-400 uppercase block">
                      {kpi.label}
                    </span>
                    <span className="text-xs font-bold font-mono text-teal-600 dark:text-teal-400">
                      {kpi.value}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Phases timeline */}
            <div className="space-y-4">
              {activeBlueprint.phases.map((p, idx) => (
                <div
                  key={idx}
                  className="p-4 rounded-xl border border-slate-200/60 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/30 space-y-3"
                >
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <h4 className="text-xs sm:text-sm font-bold text-slate-900 dark:text-slate-100">
                      {p.phase}
                    </h4>
                    <span className="text-[11px] font-mono text-indigo-600 dark:text-indigo-400 font-semibold">
                      Focus: {p.focus}
                    </span>
                  </div>

                  <div className="p-2.5 rounded-lg bg-teal-500/10 border border-teal-500/20 text-[11px] text-teal-800 dark:text-teal-300 font-mono">
                    <strong>Evidence Anchor: </strong>{p.evidence}
                  </div>

                  <div className="space-y-1.5 pt-1">
                    {p.milestones.map((m, mIdx) => (
                      <div key={mIdx} className="flex items-start space-x-2 text-xs text-slate-700 dark:text-slate-300">
                        <CheckCircle2 className="w-3.5 h-3.5 text-teal-500 shrink-0 mt-0.5" />
                        <span>{m}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </main>
      </div>

      <EvidenceModal
        isOpen={isEvidenceOpen}
        onClose={() => setIsEvidenceOpen(false)}
        evidence={selectedEvidence}
      />

      <Footer />
    </div>
  );
}

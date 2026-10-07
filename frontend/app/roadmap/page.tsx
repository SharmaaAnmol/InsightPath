"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  MapPin,
  GraduationCap,
  Building2,
  Users,
  CheckCircle2,
  ArrowRight,
  Sparkles,
  BookOpen,
  SlidersHorizontal,
} from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Sidebar } from "@/components/Sidebar";
import { Footer } from "@/components/Footer";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

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
        evidence: "SQL requested in 48.2% and Python in 39.5% of all 17,443 requisitions.",
        milestones: [
          "Master complex SQL: CTEs, window functions, query plan optimization, and schema design.",
          "Write production Python: clean modular code, unit tests, typing, and Git workflows.",
          "Avoid toy datasets; build ingestion pipelines on raw, messy public APIs and databases.",
        ],
      },
      {
        phase: "Phase 2: Mathematical Modeling & Rigor (Months 4–6)",
        focus: "Applied Statistics, Inference & Machine Learning",
        evidence: "Math/Stats is the highest predictive driver of salary hike (AOR = 3.65, β = +1.28).",
        milestones: [
          "Study classical experimental design: A/B testing power analysis, p-value adjustments, bootstrap CI.",
          "Implement Scikit-Learn pipelines with leakage prevention, cross-validation, and ROC-AUC analysis.",
          "Defend model assumptions: collinearity, residuals, and interpretability (SHAP / permutation).",
        ],
      },
      {
        phase: "Phase 3: The Differentiator Currency (Months 7–9)",
        focus: "Business Storytelling & Executive Dashboards",
        evidence: "High storytelling aptitude yields a 3.23x adjusted odds ratio for top compensation.",
        milestones: [
          "Translate technical outputs into P&L and ROI business cases for non-technical stakeholders.",
          "Build production executive dashboards (Tableau / PowerBI / Streamlit) emphasizing metric hierarchies.",
          "Publish 2 end-to-end case studies detailing problem statement, methodology, trade-offs, and impact.",
        ],
      },
      {
        phase: "Phase 4: Market Positioning & Portfolio Defense (Months 10–12)",
        focus: "Domain Contextualization & Technical Interview Mastery",
        evidence: "7 geo-clusters exhibit distinct compensation envelopes; Bengaluru commands 1.42x odds.",
        milestones: [
          "Conduct simulated whiteboard defenses of your architecture and analytical decisions.",
          "Tailor application strategy to target geo-clusters and industry verticals (Fintech, SaaS, E-commerce).",
          "Complete diagnostic benchmark on InsightPath to verify Q1 readiness profile.",
        ],
      },
    ],
  },
  university: {
    title: "University & Academic Curriculum Blueprint",
    roleDescription: "Strategic modernization guide for computer science and data science academic departments.",
    icon: BookOpen,
    badge: "Higher Education",
    kpis: [
      { label: "Curriculum Shift", value: "End-to-End Systems" },
      { label: "Project Alignment", value: "Industry Messy Data" },
      { label: "Employability Uplift", value: "+45% Placement Rate" },
    ],
    phases: [
      {
        phase: "Intervention 1: Retire Toy Datasets & Synthetic Assumptions",
        focus: "Messy, Real-World Data Ingestion",
        evidence: "Phase 1 data audit identified severe anomalies, schema drift, and missingness in live industry data.",
        milestones: [
          "Replace standard Kaggle toy datasets (Titanic, Iris, Boston) with uncurated multi-table relational databases.",
          "Incorporate mandatory data profiling, validation gates, and quality scorecards into grading criteria.",
          "Teach data cleaning and anomaly detection as first-class statistical disciplines.",
        ],
      },
      {
        phase: "Intervention 2: Mandatory Business Translation & Storytelling",
        focus: "Oral Defense & Stakeholder Communication",
        evidence: "Storytelling aptitude (AOR = 3.23) is severely underrepresented in fresh graduate cohorts (Gap #2).",
        milestones: [
          "Require oral capstone defenses before a non-technical executive jury for all final-year projects.",
          "Grade students on their ability to articulate ROI, opportunity costs, and strategic implications.",
          "Incorporate executive memo writing into machine learning and statistics course syllabi.",
        ],
      },
      {
        phase: "Intervention 3: Enterprise Capstone Partnerships",
        focus: "Industry Co-op & Real Client Engagements",
        evidence: "Postgraduate and industry-coached students achieve +2.8L starting salary shifts (H6 confirmed).",
        milestones: [
          "Establish semester-long industry project partnerships with local enterprise employers.",
          "Deploy dual-evaluator rubrics: academic professor evaluates rigor; industry mentor evaluates utility.",
          "Mandate Git version control, CI/CD automated test suites, and containerized deployment in course work.",
        ],
      },
    ],
  },
  mentor: {
    title: "Mentorship & Professional Coaching Guide",
    roleDescription: "Evidence-based framework for senior data leaders coaching junior and mid-level practitioners.",
    icon: Users,
    badge: "Leadership & Coaching",
    kpis: [
      { label: "Primary Role", value: "Diagnostic Coaching" },
      { label: "Ethical Safeguard", value: "Non-Gatekeeping Only" },
      { label: "Focus Quadrant", value: "Q2 → Q1 Transition" },
    ],
    phases: [
      {
        phase: "Pillar 1: Diagnostic Assessment & Quadrant Mapping",
        focus: "Objective Self-Awareness & Baseline",
        evidence: "38% of practitioners reside in Quadrant Q2 (Pure Execution), hitting promotion plateaus.",
        milestones: [
          "Use the InsightPath diagnostic scorer to benchmark technical vs behavioral strengths.",
          "Examine if the mentee is over-indexing on technical depth while neglecting business narrative.",
          "Reassure mentees that behavioral scores are reflective instruments for personal growth.",
        ],
      },
      {
        phase: "Pillar 2: Bridging the Q2 to Q1 Promotion Plateau",
        focus: "From Coder to Strategic Partner",
        evidence: "Moving from Q2 to Q1 unlocks senior consulting and principal salary bands (₹18L–₹35L+).",
        milestones: [
          "Coach the mentee through live stakeholder meetings: how to frame trade-offs and dissent constructively.",
          "Facilitate opportunities for the mentee to present findings directly to VP-level stakeholders.",
          "Nurture intellectual curiosity and openness to cross-functional methodologies (H4 confirmed).",
        ],
      },
      {
        phase: "Pillar 3: Ethical Guardrail Maintenance",
        focus: "Protecting Candidates from Unfair Stereotyping",
        evidence: "Phase 6 ethical directive explicitly prohibits using personality models as employment filters.",
        milestones: [
          "Ensure personality data is kept confidential between mentor and mentee.",
          "Refocus conversations on observable behavioral skills and communication habits.",
          "Celebrate improvements in storytelling confidence and cross-team empathy.",
        ],
      },
    ],
  },
  employer: {
    title: "Enterprise Talent Acquisition & Hiring Blueprint",
    roleDescription: "Modernizing job requisitions, compensation benchmarking, and candidate evaluation.",
    icon: Building2,
    badge: "Enterprise Talent",
    kpis: [
      { label: "Requisitions Audited", value: "17,443 Postings" },
      { label: "Firms Represented", value: "642 Enterprises" },
      { label: "Hiring Efficiency", value: "+30% Quality of Hire" },
    ],
    phases: [
      {
        phase: "Recommendation 1: Eliminate Skill Inflation in Job Descriptions",
        focus: "De-escalate Unrealistic Junior Postings",
        evidence: "Market requisitions frequently demand 5+ years of experience for entry-level analyst postings.",
        milestones: [
          "Separate non-negotiable Table-Stakes (SQL, Python) from nice-to-have specialized tooling.",
          "Calibrate experience requirements against the empirical salary gradient (₹1.34L/yr baseline).",
          "Publish explicit compensation ranges to attract high-caliber qualified applicants.",
        ],
      },
      {
        phase: "Recommendation 2: Dual-Currency Interview Design",
        focus: "Evaluating Both Code and Narrative",
        evidence: "Technical proficiency alone does not predict strategic project success (ROC-AUC 0.74 vs 0.76).",
        milestones: [
          "Replace abstract LeetCode algorithms with practical, contextual data analysis challenges.",
          "Include a mandatory 15-minute presentation where the candidate explains findings to a mock client.",
          "Score candidates on clarity, assumption justification, and business impact translation.",
        ],
      },
      {
        phase: "Recommendation 3: Geographic Wage Harmonization",
        focus: "Fair Compensation Across Clusters",
        evidence: "Bengaluru commands 1.42x odds premium, while Delhi-NCR and Mumbai form strong tier-2 hubs.",
        milestones: [
          "Align compensation bands to verified regional cost-of-living and talent competition indices.",
          "Offer competitive remote allowances for distributed talent pools in Pune, Hyderabad, and Chennai.",
          "Provide continuous internal upskilling paths to transition internal Q2 analysts into Q1 leaders.",
        ],
      },
    ],
  },
};

export default function RoadmapPage() {
  const [activeStakeholder, setActiveStakeholder] = useState<keyof typeof BLUEPRINTS>("student");
  const blueprint = BLUEPRINTS[activeStakeholder];
  const Icon = blueprint.icon;

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
                <MapPin className="w-3.5 h-3.5" />
                <span>Phase 8 Career-Readiness Framework</span>
              </div>
              <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
                Stakeholder Execution Blueprints
              </h1>
              <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                Actionable, empirically grounded transformation roadmaps for Candidates, Universities, Mentors, and Enterprise Hiring.
              </p>
            </div>

            <div className="flex items-center space-x-2">
              <Link href="/assessment">
                <Button className="bg-teal-600 hover:bg-teal-500 text-white font-medium text-xs h-9 shadow-sm flex items-center space-x-1.5">
                  <SlidersHorizontal className="w-3.5 h-3.5" />
                  <span>Test Your Baseline</span>
                </Button>
              </Link>
            </div>
          </div>

          {/* Stakeholder Selector Tabs */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {(
              [
                { key: "student", label: "Student & Candidate", icon: GraduationCap, sub: "Personal Progression" },
                { key: "university", label: "University & Academia", icon: BookOpen, sub: "Curriculum Redesign" },
                { key: "mentor", label: "Mentors & Leaders", icon: Users, sub: "Coaching Playbook" },
                { key: "employer", label: "Enterprise Hiring", icon: Building2, sub: "Requisition & Talent" },
              ] as const
            ).map((s) => {
              const isSelected = activeStakeholder === s.key;
              const TabIcon = s.icon;
              return (
                <button
                  key={s.key}
                  onClick={() => setActiveStakeholder(s.key)}
                  className={`p-4 rounded-xl border text-left transition-all ${
                    isSelected
                      ? "border-teal-500/70 bg-teal-50/50 dark:bg-teal-950/20 shadow-xs ring-1 ring-teal-500/30"
                      : "border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 hover:border-slate-300 dark:hover:border-slate-700"
                  }`}
                >
                  <div className="flex items-center space-x-2.5 mb-1.5">
                    <div
                      className={`p-2 rounded-lg border ${
                        isSelected
                          ? "bg-teal-500/10 border-teal-500/30 text-teal-600 dark:text-teal-400"
                          : "bg-slate-100 dark:bg-slate-800 border-slate-200 dark:border-slate-700 text-slate-500"
                      }`}
                    >
                      <TabIcon className="w-4 h-4" />
                    </div>
                    <span
                      className={`text-xs font-bold ${
                        isSelected ? "text-teal-700 dark:text-teal-300" : "text-slate-800 dark:text-slate-200"
                      }`}
                    >
                      {s.label}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-500 dark:text-slate-400 pl-1">{s.sub}</p>
                </button>
              );
            })}
          </div>

          {/* Active Blueprint Overview Banner */}
          <div className="p-6 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div className="flex items-center space-x-3">
                <div className="p-2.5 rounded-lg bg-teal-500/10 text-teal-600 dark:text-teal-400 border border-teal-500/20">
                  <Icon className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100">
                    {blueprint.title}
                  </h2>
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    {blueprint.roleDescription}
                  </p>
                </div>
              </div>
              <Badge variant="outline" className="text-xs font-mono self-start sm:self-auto text-teal-600 dark:text-teal-400 border-teal-500/30">
                {blueprint.badge}
              </Badge>
            </div>

            {/* Blueprint Targets Row */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-3 border-t border-slate-100 dark:border-slate-800/80">
              {blueprint.kpis.map((k, i) => (
                <div key={i} className="p-3 rounded-lg bg-slate-50 dark:bg-slate-950/40 border border-slate-200/60 dark:border-slate-800/60">
                  <div className="text-[10px] uppercase font-semibold text-slate-400 tracking-wider">
                    {k.label}
                  </div>
                  <div className="text-sm font-bold font-mono text-slate-900 dark:text-slate-100 mt-0.5">
                    {k.value}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Chronological Action Milestones */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                Actionable Transformation Stages
              </h3>
              <span className="text-xs text-slate-400 font-mono">Synthesized from Phase 8 Framework</span>
            </div>

            <div className="space-y-4">
              {blueprint.phases.map((item, idx) => (
                <div
                  key={idx}
                  className="p-6 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-4 transition-all hover:border-slate-300 dark:hover:border-slate-700"
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-100 dark:border-slate-800/80">
                    <div className="flex items-center space-x-2.5">
                      <span className="w-6 h-6 rounded-full bg-teal-500/10 text-teal-600 dark:text-teal-400 text-xs font-bold font-mono flex items-center justify-center shrink-0 border border-teal-500/20">
                        {idx + 1}
                      </span>
                      <h4 className="text-sm font-bold text-slate-900 dark:text-slate-100">
                        {item.phase}
                      </h4>
                    </div>
                    <Badge variant="secondary" className="text-[11px] self-start sm:self-auto">
                      Focus: {item.focus}
                    </Badge>
                  </div>

                  {/* Empirical Evidence Pill */}
                  <div className="p-3 rounded-lg bg-teal-500/5 dark:bg-teal-950/20 border border-teal-500/20 text-xs text-teal-800 dark:text-teal-300 flex items-start space-x-2">
                    <Sparkles className="w-3.5 h-3.5 text-teal-500 shrink-0 mt-0.5" />
                    <span className="leading-relaxed">
                      <strong>Empirical Rationale:</strong> {item.evidence}
                    </span>
                  </div>

                  {/* Concrete Checklist Items */}
                  <div className="space-y-2 pt-1">
                    <div className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                      Concrete Implementation Deliverables:
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-2.5">
                      {item.milestones.map((m, mIdx) => (
                        <div
                          key={mIdx}
                          className="p-3 rounded-lg border border-slate-200/60 dark:border-slate-800/80 bg-slate-50/50 dark:bg-slate-950/30 text-xs text-slate-600 dark:text-slate-400 flex items-start space-x-2"
                        >
                          <CheckCircle2 className="w-3.5 h-3.5 text-teal-500 shrink-0 mt-0.5" />
                          <span className="leading-snug">{m}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Quick CTA Card */}
          <div className="p-6 rounded-xl border border-teal-500/30 bg-linear-to-r from-teal-500/10 via-indigo-500/5 to-transparent flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="space-y-1">
              <h3 className="text-base font-bold text-slate-900 dark:text-slate-100">
                Ready to Benchmark Your Current Quadrant?
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Run your self-assessment through our dual-track ML model to obtain personalized gap closures.
              </p>
            </div>
            <Link href="/assessment">
              <Button className="bg-teal-600 hover:bg-teal-500 text-white font-medium text-xs h-9 shadow-sm shrink-0 flex items-center space-x-2">
                <span>Open Diagnostic Tool</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Button>
            </Link>
          </div>
        </main>
      </div>

      <Footer />
    </div>
  );
}

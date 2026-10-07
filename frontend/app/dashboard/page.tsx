"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  BarChart3,
  Sparkles,
  Grid,
  MapPin,
  FileCheck2,
  SlidersHorizontal,
  ArrowRight,
  TrendingUp,
  BrainCircuit,
  Database,
  CheckCircle2,
  ShieldCheck,
  ChevronRight,
  Activity,
} from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Sidebar } from "@/components/Sidebar";
import { Footer } from "@/components/Footer";
import { StatCard } from "@/components/StatCard";
import { ChartCard } from "@/components/ChartCard";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

const HYPOTHESES_STATUS = [
  {
    code: "H1",
    label: "Experience vs Salary Gradient",
    result: "CONFIRMED",
    metric: "β = +1.34L / year",
    pVal: "p < 0.001",
    detail: "Linear regression confirms monotonic increase across all experience tiers with R² = 0.58.",
  },
  {
    code: "H2",
    label: "Big Tech vs Non-Tech Pay Gap",
    result: "CONFIRMED",
    metric: "Cohen's d = 0.84",
    pVal: "p < 0.001",
    detail: "Statistically significant Tier-1 tech premium with median differential of +6.8L/year.",
  },
  {
    code: "H3",
    label: "Storytelling vs Pure Math Premium",
    result: "CONFIRMED",
    metric: "AOR = 3.23 (Storytelling)",
    pVal: "p = 0.002",
    detail: "High storytelling aptitude yields a 3.23x adjusted odds ratio for top-bracket compensation.",
  },
  {
    code: "H4",
    label: "Personality in Senior Consulting",
    result: "CONFIRMED",
    metric: "AOR = 7.72 (Openness)",
    pVal: "p < 0.001",
    detail: "Openness and Conscientiousness heavily differentiate Tier-1 strategic advisory success.",
  },
  {
    code: "H5",
    label: "Bengaluru Geographic Premium",
    result: "CONFIRMED",
    metric: "1.42x Premium Odds",
    pVal: "p < 0.001",
    detail: "38.6% of national hiring demand concentrated with significant upper-tier salary density.",
  },
  {
    code: "H6",
    label: "Postgraduate Qualification Premium",
    result: "CONFIRMED",
    metric: "+2.8L Median Shift",
    pVal: "p = 0.014",
    detail: "Master's & PhD credentials unlock upper-quartile starting roles in core research requisitions.",
  },
];

const QUADRANTS = [
  {
    id: "Q1",
    name: "Advanced Career-Ready",
    share: "22%",
    description: "High Technical (≥3.8) & High Behavioral (≥45.0)",
    color: "emerald",
    action: "Fast-track to Principal / Consulting partner tracks.",
  },
  {
    id: "Q2",
    name: "Pure Execution Specialist",
    share: "38%",
    description: "High Technical (≥3.8) & Developing Behavioral (<45.0)",
    color: "indigo",
    action: "Target business narrative and executive presentation skills.",
  },
  {
    id: "Q3",
    name: "Strategic Facilitator",
    share: "18%",
    description: "Developing Technical (<3.8) & High Behavioral (≥45.0)",
    color: "cyan",
    action: "Deepen applied statistical modeling and data systems rigor.",
  },
  {
    id: "Q4",
    name: "Foundational Risk",
    share: "22%",
    description: "Developing Technical (<3.8) & Developing Behavioral (<45.0)",
    color: "amber",
    action: "Structured end-to-end technical bootcamp and mentorship.",
  },
];

export default function DashboardPage() {
  const [selectedQuadrant, setSelectedQuadrant] = useState("Q1");

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--foreground)]">
      <Navbar />

      <div className="flex-1 flex w-full">
        {/* Collapsible/Responsive Sidebar */}
        <Sidebar className="hidden lg:flex" />

        {/* Main Content Area */}
        <main className="flex-1 p-4 md:p-8 max-w-7xl mx-auto w-full space-y-8">
          {/* Header Bar */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-200/80 dark:border-slate-800">
            <div>
              <div className="flex items-center space-x-2 text-xs font-semibold uppercase tracking-wider text-teal-600 dark:text-teal-400 mb-1.5">
                <Activity className="w-3.5 h-3.5" />
                <span>Executive Command Center</span>
              </div>
              <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
                Talent Intelligence Dashboard
              </h1>
              <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                Unified empirical evidence synthesized across 17,443 jobs, 300 practitioners, and dual ML engines.
              </p>
            </div>

            <div className="flex items-center space-x-3">
              <Link href="/assessment">
                <Button className="bg-teal-600 hover:bg-teal-500 text-white font-medium shadow-sm flex items-center space-x-2 text-xs h-9">
                  <SlidersHorizontal className="w-3.5 h-3.5" />
                  <span>Launch Diagnostic Scorer</span>
                </Button>
              </Link>
              <Link href="/methodology">
                <Button variant="outline" className="text-xs h-9">
                  <FileCheck2 className="w-3.5 h-3.5 mr-1.5" />
                  Audit Trail
                </Button>
              </Link>
            </div>
          </div>

          {/* Top Macro Metrics Row */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard
              label="Audited Market Requisitions"
              value="17,443"
              subvalue="15.8k macro + 1.6k JDS"
              badgeText="100% Validated"
              badgeVariant="secondary"
              icon={Database}
              color="teal"
              trend={{ value: "4 Distinct Datasets", direction: "up" }}
            />
            <StatCard
              label="Practitioner Profiles"
              value="300"
              subvalue="200 JDS + 100 SDS"
              badgeText="Dual Analytical Lens"
              badgeVariant="secondary"
              icon={BrainCircuit}
              color="indigo"
              trend={{ value: "Technical & Personality", direction: "neutral" }}
            />
            <StatCard
              label="Experience Salary Beta"
              value="+₹1.34L"
              subvalue="per year of experience"
              badgeText="p < 0.001 (R²=0.58)"
              badgeVariant="default"
              icon={TrendingUp}
              color="emerald"
              trend={{ value: "Monotonic Growth", direction: "up" }}
            />
            <StatCard
              label="Champion ML Engines"
              value="2 Models"
              subvalue="JDS (0.74) & SDS (0.76)"
              badgeText="Logistic L2 Penalized"
              badgeVariant="secondary"
              icon={ShieldCheck}
              color="amber"
              trend={{ value: "Strict Small-Sample Guardrails", direction: "up" }}
            />
          </div>

          {/* Dual Main Cards Row */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Quick Diagnostic Launcher Card */}
            <div className="lg:col-span-1 rounded-xl p-6 border border-teal-500/20 bg-linear-to-br from-teal-500/5 via-teal-500/10 to-transparent dark:from-teal-500/10 dark:via-teal-500/5 dark:to-transparent flex flex-col justify-between space-y-5">
              <div className="space-y-3">
                <div className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-[11px] font-semibold bg-teal-500/15 text-teal-700 dark:text-teal-300 border border-teal-500/30">
                  <Sparkles className="w-3 h-3 text-teal-500" />
                  <span>Self-Assessment Simulator</span>
                </div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">
                  Calculate Your Empirical Hike & Placement Odds
                </h3>
                <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                  Enter your technical ratings (Python, Math, Storytelling) and Big Five behavioral scores to evaluate placement into the 4-Quadrant readiness matrix.
                </p>
                <div className="pt-2 space-y-2 text-xs text-slate-600 dark:text-slate-400">
                  <div className="flex items-center space-x-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-teal-500 shrink-0" />
                    <span>Real-time logistic probability engine</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-teal-500 shrink-0" />
                    <span>Calculates Quadrant tier & compensation bracket</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-teal-500 shrink-0" />
                    <span>Instant personalized gap closing roadmap</span>
                  </div>
                </div>
              </div>

              <div className="pt-4 border-t border-teal-500/20">
                <Link href="/assessment">
                  <Button className="w-full bg-teal-600 hover:bg-teal-500 text-white font-medium shadow-sm flex items-center justify-center space-x-2 text-xs h-10">
                    <span>Open Interactive Scorer</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Button>
                </Link>
              </div>
            </div>

            {/* 4-Quadrant Breakdown Card */}
            <div className="lg:col-span-2">
              <ChartCard
                title="Four-Quadrant Career-Readiness Distribution"
                subtitle="Cross-dataset classification based on Technical Execution and Behavioral Maturity"
                infoTooltip="Q1 to Q4 mapping synthesized in Phase 8 from JDS skill performance and SDS behavioral profiles."
                badge={
                  <Badge variant="outline" className="text-[10px] text-teal-500 border-teal-500/30">
                    Phase 8 Synthesis
                  </Badge>
                }
                action={
                  <Link href="/career-readiness" className="text-xs text-teal-600 dark:text-teal-400 hover:underline flex items-center space-x-1">
                    <span>Full Matrix</span>
                    <ChevronRight className="w-3 h-3" />
                  </Link>
                }
              >
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-6">
                  {QUADRANTS.map((q) => {
                    const isSelected = selectedQuadrant === q.id;
                    return (
                      <div
                        key={q.id}
                        onClick={() => setSelectedQuadrant(q.id)}
                        className={`p-3.5 rounded-lg border cursor-pointer transition-all ${
                          isSelected
                            ? "border-teal-500/60 bg-teal-50/50 dark:bg-teal-950/20 shadow-xs ring-1 ring-teal-500/30"
                            : "border-slate-200/80 dark:border-slate-800 bg-slate-50/30 dark:bg-slate-900/40 hover:border-slate-300 dark:hover:border-slate-700"
                        }`}
                      >
                        <div className="flex items-center justify-between mb-1.5">
                          <div className="flex items-center space-x-2">
                            <span className="text-xs font-mono font-bold text-teal-600 dark:text-teal-400">
                              {q.id}
                            </span>
                            <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">
                              {q.name}
                            </span>
                          </div>
                          <span className="text-xs font-bold font-mono text-slate-600 dark:text-slate-400">
                            {q.share}
                          </span>
                        </div>
                        <p className="text-[11px] text-slate-500 dark:text-slate-400 mb-2">
                          {q.description}
                        </p>
                        <p className="text-[11px] text-teal-700 dark:text-teal-300 font-medium">
                          {q.action}
                        </p>
                      </div>
                    );
                  })}
                </div>

                <div className="p-3 bg-slate-50 dark:bg-slate-950/50 rounded-lg border border-slate-200/60 dark:border-slate-800/80 flex items-center justify-between text-xs">
                  <div className="flex items-center space-x-2 text-slate-600 dark:text-slate-400">
                    <Grid className="w-4 h-4 text-teal-500" />
                    <span>
                      Selected: <strong>{selectedQuadrant}</strong> — Detailed transition plans available in the Readiness module.
                    </span>
                  </div>
                  <Link href="/career-readiness">
                    <Button variant="ghost" size="sm" className="h-7 text-xs text-teal-600 dark:text-teal-400">
                      Explore Blueprint
                    </Button>
                  </Link>
                </div>
              </ChartCard>
            </div>
          </div>

          {/* Empirical Hypothesis Scorecard (H1–H6) */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100 flex items-center space-x-2">
                  <FileCheck2 className="w-4 h-4 text-teal-500" />
                  <span>Hypothesis Verification Matrix (H1–H6)</span>
                </h2>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  Statistical test results confirmed via OLS regression, Mann-Whitney U, and Logistic AOR odds ratios.
                </p>
              </div>
              <Link href="/methodology" className="text-xs text-teal-600 dark:text-teal-400 hover:underline flex items-center space-x-1">
                <span>View Full Test Stats</span>
                <ArrowRight className="w-3 h-3" />
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {HYPOTHESES_STATUS.map((h) => (
                <div
                  key={h.code}
                  className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-2.5 transition-all hover:border-slate-300 dark:hover:border-slate-700"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <span className="text-xs font-mono font-bold px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                        {h.code}
                      </span>
                      <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">
                        {h.label}
                      </span>
                    </div>
                    <Badge variant="default" className="bg-emerald-600 text-white text-[10px] px-2 py-0">
                      {h.result}
                    </Badge>
                  </div>

                  <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                    {h.detail}
                  </p>

                  <div className="pt-2 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between text-[11px] font-mono">
                    <span className="text-teal-600 dark:text-teal-400 font-semibold">{h.metric}</span>
                    <span className="text-slate-400 dark:text-slate-500">{h.pVal}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Quick Analytical Deep-Dive Navigation */}
          <div className="pt-6 border-t border-slate-200/80 dark:border-slate-800 space-y-4">
            <h2 className="text-sm font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">
              Analytical Deep-Dives & Tooling
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <Link
                href="/market"
                className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/40 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors group"
              >
                <div className="flex items-center space-x-2 text-teal-600 dark:text-teal-400 mb-1">
                  <BarChart3 className="w-4 h-4" />
                  <span className="text-xs font-semibold">Market Intelligence</span>
                </div>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  Inspect salary distributions across 7 geo-clusters and top-50 requested technical skills.
                </p>
              </Link>

              <Link
                href="/skills"
                className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/40 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors group"
              >
                <div className="flex items-center space-x-2 text-indigo-500 mb-1">
                  <Sparkles className="w-4 h-4" />
                  <span className="text-xs font-semibold">Skills Dual-Currency</span>
                </div>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  Table-Stakes vs Differentiators model detailing the 5 systemic talent gaps.
                </p>
              </Link>

              <Link
                href="/career-readiness"
                className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/40 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors group"
              >
                <div className="flex items-center space-x-2 text-cyan-500 mb-1">
                  <Grid className="w-4 h-4" />
                  <span className="text-xs font-semibold">4-Quadrant Framework</span>
                </div>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  Four career-readiness profiles with compensation envelopes and transition curricula.
                </p>
              </Link>

              <Link
                href="/roadmap"
                className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/40 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors group"
              >
                <div className="flex items-center space-x-2 text-amber-500 mb-1">
                  <MapPin className="w-4 h-4" />
                  <span className="text-xs font-semibold">Stakeholder Blueprints</span>
                </div>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  Tailored execution roadmaps for Students, Universities, Mentors, and Enterprise Hiring.
                </p>
              </Link>
            </div>
          </div>
        </main>
      </div>

      <Footer />
    </div>
  );
}

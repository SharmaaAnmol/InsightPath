"use client";

import React, { useState, useEffect } from "react";
import { Sparkles } from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { ChartCard } from "@/components/ChartCard";
import { Badge } from "@/components/ui/badge";
import { BarChartVisual } from "@/components/BarChartVisual";
import { EvidenceModal, EvidenceDetail } from "@/components/EvidenceModal";

import {
  fetchSkillFrequency,
  fetchPremiumSkills,
  SkillFrequencyItem,
  PremiumSkillItem,
} from "@/lib/api";

const TALENT_GAPS = [
  {
    gapNumber: "01",
    name: "The Big Data Illusion",
    prevalenceInJobs: "Rank #5 in JDS (0.0107)",
    promotionalLift: "AOR = 0.94 (p = 0.866)",
    summary: "Massive market posting prevalence creates the illusion of mandatory expertise, yet distributed infrastructure skills yield near-zero promotion lift for early practitioners.",
    action: "Master query optimization and modeling intuition before deploying multi-node Spark clusters.",
  },
  {
    gapNumber: "02",
    name: "The Storytelling Deficit",
    prevalenceInJobs: "Rank #1 Permutation Importance",
    promotionalLift: "AOR = 3.23 (p = 0.002)",
    summary: "Rarely specified in job descriptions as a mandatory technical keyword, yet empirical modeling reveals it is the single strongest differentiator of junior salary hikes.",
    action: "Pair analytical models with clear executive narratives, decision impact bridges, and business metrics.",
  },
  {
    gapNumber: "03",
    name: "The Coding Saturation Trap",
    prevalenceInJobs: "Rank #3 in JDS (0.0245)",
    promotionalLift: "AOR = 1.04 (p = 0.925)",
    summary: "Coding competency is saturated across both high and low performers (mean score 4.1 vs 4.0). Writing code is a ticket to enter, not a differentiator for promotion.",
    action: "Avoid spending 100% of study time on algorithmic syntax puzzles once baseline competence is reached.",
  },
  {
    gapNumber: "04",
    name: "The Senior Behavioral Shock",
    prevalenceInJobs: "Senior Consulting (N=161)",
    promotionalLift: "Openness AOR = 7.72",
    summary: "Transitioning to senior client-facing roles requires an abrupt pivot: technical tools decline in importance while intellectual adaptability and conscientious rigor govern 96.99% of success variance.",
    action: "Cultivate client empathy, ambiguous problem scoping, and structured executive communication.",
  },
  {
    gapNumber: "05",
    name: "The Geographic Mobility Divide",
    prevalenceInJobs: "68.5% in Tri-Metros",
    promotionalLift: "Premium Odds = 1.42x",
    summary: "Elite compensation envelopes (>₹15L) are geographically locked into Bengaluru, NCR, and Mumbai. Candidates without geographic flexibility face an artificial wage ceiling.",
    action: "Target remote global engineering teams or plan strategic metro rotations for velocity tiers.",
  },
];

export default function SkillsIntelligencePage() {
  const [skills, setSkills] = useState<SkillFrequencyItem[]>([]);
  const [premiums, setPremiums] = useState<PremiumSkillItem[]>([]);

  const [selectedEvidence, setSelectedEvidence] = useState<EvidenceDetail | null>(null);
  const [isEvidenceOpen, setIsEvidenceOpen] = useState(false);

  useEffect(() => {
    Promise.all([
      fetchSkillFrequency(),
      fetchPremiumSkills(),
    ]).then(([skillRes, premRes]) => {
      setSkills(skillRes.records);
      setPremiums(premRes.records);
    });
  }, []);

  const openEvidence = (detail: EvidenceDetail) => {
    setSelectedEvidence(detail);
    setIsEvidenceOpen(true);
  };

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--foreground)]">
      <Navbar />

      <main className="flex-1 py-12 md:py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
          {/* Header */}
          <div className="space-y-3">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-mono font-medium border border-teal-500/30 bg-teal-500/10 text-teal-600 dark:text-teal-400">
              <Sparkles className="w-3.5 h-3.5 mr-1" />
              <span>Phase 7 Cross-Dataset Triangulation</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900 dark:text-slate-50">
              The Asymmetric Dual-Currency Skill Model
            </h1>
            <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400 leading-relaxed max-w-3xl">
              Job postings and promotional velocity measure entirely different things. Market access requires foundational syntax, while salary multipliers and leadership promotions require narrative synthesis and intellectual agility.
            </p>
          </div>

          {/* Dual Currency Framework Highlight */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-6 rounded-xl border border-indigo-200/80 dark:border-indigo-900/40 bg-indigo-50/40 dark:bg-indigo-950/20 space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
                  Currency 1
                </span>
                <Badge variant="outline" className="border-indigo-500/30 text-indigo-600 dark:text-indigo-400">
                  Market Access Currency
                </Badge>
              </div>
              <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">
                Baseline Table-Stakes Skills
              </h3>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                Skills heavily screened by automated ATS filters and recruiter keyword rubrics. Required to secure entry-level interviews, but offering near-zero marginal promotional elasticity.
              </p>
              <div className="space-y-2 pt-2 text-xs font-mono">
                <div className="flex justify-between border-b border-indigo-200/60 dark:border-indigo-800/60 pb-1">
                  <span>SQL Querying:</span>
                  <span className="font-semibold">915 Postings (5.78%) • Relative Ratio 0.96x</span>
                </div>
                <div className="flex justify-between border-b border-indigo-200/60 dark:border-indigo-800/60 pb-1">
                  <span>Python Syntax:</span>
                  <span className="font-semibold">840 Postings (5.30%) • Relative Ratio 1.30x</span>
                </div>
                <div className="flex justify-between pb-1">
                  <span>Excel / Spreadsheet:</span>
                  <span className="font-semibold">393 Postings (2.48%) • Relative Ratio 0.81x</span>
                </div>
              </div>
            </div>

            <div className="p-6 rounded-xl border border-teal-200/80 dark:border-teal-900/40 bg-teal-50/40 dark:bg-teal-950/20 space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-teal-600 dark:text-teal-400">
                  Currency 2
                </span>
                <Badge variant="outline" className="border-teal-500/30 text-teal-600 dark:text-teal-400">
                  Career Velocity Currency
                </Badge>
              </div>
              <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">
                Promotional & Wage Multipliers
              </h3>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                Capabilities that translate computational findings into executive business decisions, unlocking upper-quartile salary hikes and partner-track consulting leadership.
              </p>
              <div className="space-y-2 pt-2 text-xs font-mono">
                <div className="flex justify-between border-b border-teal-200/60 dark:border-teal-800/60 pb-1">
                  <span>Executive Storytelling:</span>
                  <span className="font-semibold text-teal-600 dark:text-teal-400">3.23x Adjusted Odds (Rank #1)</span>
                </div>
                <div className="flex justify-between border-b border-teal-200/60 dark:border-teal-800/60 pb-1">
                  <span>Mathematical Modeling:</span>
                  <span className="font-semibold text-teal-600 dark:text-teal-400">3.61x Adjusted Odds (Rank #2)</span>
                </div>
                <div className="flex justify-between pb-1">
                  <span>Client Adaptability (Openness):</span>
                  <span className="font-semibold text-teal-600 dark:text-teal-400">7.72x Senior Consulting AOR</span>
                </div>
              </div>
            </div>
          </div>

          {/* Visualizations Section */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* 1. Skill Frequency */}
            <ChartCard
              title="Technical Skill Prevalence Across 15,841 Requisitions"
              subtitle="Empirical frequency and percentage prevalence of audited technical keywords"
              badge={<Badge variant="outline" className="text-[10px]">Phase 3 EDA</Badge>}
            >
              <BarChartVisual
                unitLabel="Demand Prevalence (%)"
                maxValue={8.0}
                items={skills.slice(0, 10).map((s) => ({
                  label: s.skill_name,
                  value: s.prevalence_pct,
                  secondaryValue: `${s.frequency_count.toLocaleString()} jobs`,
                  unit: "%",
                  category: s.domain_category.split("/")[0],
                  color: s.domain_category.includes("SQL") || s.domain_category.includes("Programming") ? "indigo" : "teal",
                }))}
                meaning="SQL (5.78%), Analytics (5.71%), and Python (5.30%) form the foundational tripartite baseline required for job entry."
                onOpenEvidence={() =>
                  openEvidence({
                    title: "Technical Skill Frequency Analysis",
                    phase: "Phase 3: Exploratory Data Analysis",
                    dataset: "Analytics Jobs (N=15,841)",
                    sampleSize: "N = 15,841 postings",
                    method: "Dictionary-matched token extraction and frequency profiling across audited job postings.",
                    interpretation: "Confirms that procedural programming syntax is the dominant gate for interview eligibility.",
                    limitation: "Does not evaluate the code quality or depth expected by the employer.",
                  })
                }
              />
            </ChartCard>

            {/* 2. Premium Salary Skill Signals */}
            <ChartCard
              title="Specialized Skill Wage Multipliers (Prevalence Ratios)"
              subtitle="Relative prevalence ratio in upper-bracket salaries (>₹15L) vs baseline postings"
              badge={<Badge variant="outline" className="text-[10px]">Phase 3 / H6</Badge>}
            >
              <BarChartVisual
                unitLabel="Prevalence Ratio"
                items={premiums.map((s) => ({
                  label: s.skill_name,
                  value: s.relative_prevalence_ratio,
                  secondaryValue: `High: ${s.prevalence_in_high_salary_pct}% vs Low: ${s.prevalence_in_non_high_salary_pct}%`,
                  unit: "x ratio",
                  highlight: s.relative_prevalence_ratio > 2.0,
                  color: s.relative_prevalence_ratio > 2.0 ? "teal" : s.relative_prevalence_ratio > 1.2 ? "indigo" : "amber",
                }))}
                meaning="Data Science (2.75x), R (2.56x), Spark (2.18x), and Machine Learning (2.15x) are true premium wage multipliers, while SQL (0.96x) and Excel (0.81x) are table-stakes."
                onOpenEvidence={() =>
                  openEvidence({
                    title: "Premium Salary Differentiation Ratios",
                    phase: "Phase 3 EDA & Phase 4 H6",
                    dataset: "Analytics Jobs (N=15,841)",
                    sampleSize: "N = 15,841 postings",
                    method: "Prevalence ratio calculation between upper-tier salary bracket and baseline bracket.",
                    interpretation: "Empirical proof of the dual-currency skill model: table-stakes skills do not generate wage premiums.",
                    limitation: "Skills inferred via keyword matching in job descriptions.",
                  })
                }
              />
            </ChartCard>
          </div>

          {/* 5 Structural Talent Gaps */}
          <div className="space-y-6">
            <div className="space-y-2">
              <h2 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
                The 5 Structural Talent Gaps
              </h2>
              <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400">
                Systematic market blind spots identified through Phase 7 cross-dataset synthesis.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {TALENT_GAPS.map((gap) => (
                <div
                  key={gap.gapNumber}
                  className="p-5 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-3 flex flex-col justify-between"
                >
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-mono font-bold text-teal-600 dark:text-teal-400">
                        GAP {gap.gapNumber}
                      </span>
                      <Badge variant="outline" className="text-[10px] font-mono">
                        {gap.promotionalLift}
                      </Badge>
                    </div>
                    <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100">
                      {gap.name}
                    </h3>
                    <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                      {gap.summary}
                    </p>
                  </div>
                  <div className="pt-2 border-t border-slate-100 dark:border-slate-800/80 text-[11px] text-teal-700 dark:text-teal-300">
                    <strong>Action: </strong>{gap.action}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>

      <EvidenceModal
        isOpen={isEvidenceOpen}
        onClose={() => setIsEvidenceOpen(false)}
        evidence={selectedEvidence}
      />

      <Footer />
    </div>
  );
}

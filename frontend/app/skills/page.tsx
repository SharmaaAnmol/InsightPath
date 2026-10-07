"use client";

import React from "react";
import Link from "next/link";
import { Sparkles, SlidersHorizontal } from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { SkillCard } from "@/components/SkillCard";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

const TALENT_GAPS = [
  {
    gapNumber: "01",
    name: "The Big Data Illusion",
    prevalenceInJobs: "44.9% of Vacancies",
    promotionalLift: "AOR = 0.94 (p = 0.866)",
    summary: "Massive market posting prevalence creates the illusion of mandatory expertise, yet distributed infrastructure skills yield near-zero promotion lift for early practitioners.",
    action: "Master query optimization and modeling intuition before deploying multi-node Spark clusters.",
  },
  {
    gapNumber: "02",
    name: "The Storytelling Deficit",
    prevalenceInJobs: "21.9% of Vacancies",
    promotionalLift: "AOR = 3.23 (p = 0.003)",
    summary: "Rarely specified in job descriptions as a mandatory technical keyword, yet empirical modeling reveals it is the single strongest differentiator of junior salary hikes (d = 1.32).",
    action: "Pair analytical models with clear executive narratives, decision impact bridges, and business metrics.",
  },
  {
    gapNumber: "03",
    name: "The Coding Saturation Trap",
    prevalenceInJobs: "82.4% of Postings",
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
    summary: "Elite compensation envelopes (>15L) are geographically locked into Bengaluru, NCR, and Mumbai. Candidates without geographic flexibility face an artificial wage ceiling.",
    action: "Target remote global engineering teams or plan strategic metro rotations for velocity tiers.",
  },
];

export default function SkillsIntelligencePage() {
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
                Skills heavily screened by automated ATS filters and recruiter keyword rubrics. Required to secure entry-level interviews, but offer near-zero marginal promotional elasticity.
              </p>
              <div className="space-y-2 pt-2 text-xs font-mono">
                <div className="flex justify-between border-b border-indigo-200/60 dark:border-indigo-800/60 pb-1">
                  <span>SQL Querying:</span>
                  <span className="font-semibold">48.2% Prevalence • AOR ≈ 1.0</span>
                </div>
                <div className="flex justify-between border-b border-indigo-200/60 dark:border-indigo-800/60 pb-1">
                  <span>Python Syntax:</span>
                  <span className="font-semibold">39.5% Prevalence • AOR ≈ 1.0</span>
                </div>
                <div className="flex justify-between pb-1">
                  <span>Excel / Spreadsheet Modeling:</span>
                  <span className="font-semibold">34.1% Prevalence • AOR ≈ 1.0</span>
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
                Competencies rarely advertised as discrete keyword requirements, yet statistically explain over 90% of observed salary hike variance and consulting excellence.
              </p>
              <div className="space-y-2 pt-2 text-xs font-mono">
                <div className="flex justify-between border-b border-teal-200/60 dark:border-teal-800/60 pb-1">
                  <span>Dashboarding & Storytelling:</span>
                  <span className="font-semibold text-teal-600 dark:text-teal-400">AOR = 3.23x • d = 1.32</span>
                </div>
                <div className="flex justify-between border-b border-teal-200/60 dark:border-teal-800/60 pb-1">
                  <span>Mathematical & Statistical Rigor:</span>
                  <span className="font-semibold text-teal-600 dark:text-teal-400">AOR = 3.65x • d = 1.22</span>
                </div>
                <div className="flex justify-between pb-1">
                  <span>Openness to Experience (Senior):</span>
                  <span className="font-semibold text-teal-600 dark:text-teal-400">AOR = 7.72x • Imp = 0.121</span>
                </div>
              </div>
            </div>
          </div>

          {/* Detailed Skill Cards */}
          <div className="space-y-4">
            <h2 className="text-xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
              Evaluated Competency Dimensions
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
              <SkillCard
                name="Dashboarding & Storytelling"
                category="Communication & Story"
                currencyType="Career Velocity"
                prevalencePercent={21.9}
                oddsRatio={3.23}
                effectSize="d = 1.32"
                description="The ability to translate model weights, residuals, and predictions into executive business decisions that non-technical leaders can act upon."
                stageRelevance="Velocity (3-5y)"
              />

              <SkillCard
                name="Mathematical & Stats Foundations"
                category="Mathematical Rigor"
                currencyType="Career Velocity"
                prevalencePercent={22.3}
                oddsRatio={3.65}
                effectSize="d = 1.22"
                description="Understanding probability distributions, hypothesis testing assumptions, and optimization mechanics beneath API wrappers."
                stageRelevance="Velocity (3-5y)"
              />

              <SkillCard
                name="Openness to Experience"
                category="Executive Behavior"
                currencyType="Career Velocity"
                prevalencePercent={16.5}
                oddsRatio={7.72}
                effectSize="d = 1.80"
                description="Intellectual curiosity and willingness to navigate ambiguous, unstructured customer business problems without preconceived technical dogmas."
                stageRelevance="Leadership (10+y)"
              />

              <SkillCard
                name="SQL & Data Warehousing"
                category="Technical Tool"
                currencyType="Market Access"
                prevalencePercent={48.2}
                oddsRatio={1.0}
                effectSize="d = 0.35"
                description="Standard query extraction, joins, aggregations, and window functions. Mandatory for early screenings across nearly half of all vacancies."
                stageRelevance="Entry (0-2y)"
              />

              <SkillCard
                name="Coding / Software Syntax"
                category="Technical Tool"
                currencyType="Saturated Foundation"
                prevalencePercent={39.5}
                oddsRatio={1.04}
                effectSize="d = 0.21"
                description="Scripting in Python or R. Uniformly proficient across both high and low salary hike cohorts, providing zero marginal promotional lift."
                stageRelevance="Entry (0-2y)"
              />

              <SkillCard
                name="Conscientiousness & Execution"
                category="Executive Behavior"
                currencyType="Career Velocity"
                prevalencePercent={18.0}
                oddsRatio={8.11}
                effectSize="d = 1.85"
                description="Methodical rigor, systematic validation, and reliable project execution under demanding senior consulting timelines."
                stageRelevance="Leadership (10+y)"
              />
            </div>
          </div>

          {/* The Five Systemic Talent Gaps */}
          <div className="space-y-4">
            <div>
              <h2 className="text-xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
                The Five Systemic Labor Market Talent Gaps
              </h2>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Identified through Phase 7 Methodological Triangulation comparing employer requisitions against actual practitioner performance.
              </p>
            </div>

            <div className="space-y-3">
              {TALENT_GAPS.map((gap) => (
                <div
                  key={gap.gapNumber}
                  className="p-5 rounded-xl border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-900/80 space-y-2.5"
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <div className="flex items-center space-x-2.5">
                      <span className="w-6 h-6 rounded-md bg-slate-100 dark:bg-slate-800 flex items-center justify-center font-mono font-bold text-xs text-teal-600 dark:text-teal-400">
                        {gap.gapNumber}
                      </span>
                      <h4 className="text-sm font-bold text-slate-900 dark:text-slate-100">
                        {gap.name}
                      </h4>
                    </div>
                    <div className="flex items-center space-x-3 text-xs font-mono">
                      <span className="text-slate-400">Postings: {gap.prevalenceInJobs}</span>
                      <span className="text-teal-600 dark:text-teal-400 font-semibold">{gap.promotionalLift}</span>
                    </div>
                  </div>

                  <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                    {gap.summary}
                  </p>

                  <div className="pt-2 border-t border-slate-100 dark:border-slate-800/80 text-xs text-teal-700 dark:text-teal-300">
                    <strong>Recommended Strategic Action:</strong> {gap.action}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Link to Diagnostic Scorer */}
          <div className="p-6 rounded-2xl border border-slate-200 dark:border-slate-800 bg-gradient-to-r from-slate-900 to-slate-800 dark:from-slate-900 dark:to-slate-950 text-white flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="space-y-1">
              <h3 className="text-base font-bold">Assess Your Dual-Currency Skill Profile</h3>
              <p className="text-xs text-slate-300">
                Input your technical ratings to calculate your estimated salary hike probability using our validated Logistic L2 model.
              </p>
            </div>
            <Link href="/assessment">
              <Button size="sm" className="bg-teal-500 hover:bg-teal-400 text-slate-950 font-semibold text-xs shrink-0">
                <SlidersHorizontal className="w-3.5 h-3.5 mr-1.5" />
                <span>Launch Assessment</span>
              </Button>
            </Link>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}

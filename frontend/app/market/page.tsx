"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  BarChart3,
  MapPin,
  Sparkles,
  ArrowRight,
} from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { StatCard } from "@/components/StatCard";
import { ChartCard } from "@/components/ChartCard";
import { ProgressBar } from "@/components/ProgressBar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

const ROLES_DEMAND = [
  { role: "Data Scientist", percentage: 43.1, count: 690, avgExp: 4.8, avgSalary: "14.2L" },
  { role: "Machine Learning Engineer", percentage: 18.2, count: 292, avgExp: 5.2, avgSalary: "17.6L" },
  { role: "Analytics Consultant", percentage: 12.5, count: 200, avgExp: 6.1, avgSalary: "18.9L" },
  { role: "Data Analyst", percentage: 11.4, count: 183, avgExp: 2.8, avgSalary: "8.5L" },
  { role: "Business Intelligence Specialist", percentage: 5.8, count: 93, avgExp: 4.1, avgSalary: "11.8L" },
  { role: "AI Research Scientist", percentage: 4.2, count: 67, avgExp: 6.8, avgSalary: "24.5L" },
  { role: "Data Architect", percentage: 4.8, count: 77, avgExp: 8.5, avgSalary: "26.8L" },
];

const GEO_CLUSTERS = [
  { city: "Bengaluru (Silicon Plateau)", percentage: 38.6, count: 6115, avgSalaryBracket: "15to25 / 25to50", premiumOdds: "1.42x" },
  { city: "Delhi-NCR (Gurugram / Noida)", percentage: 17.8, count: 2820, avgSalaryBracket: "10to15 / 15to25", premiumOdds: "1.18x" },
  { city: "Mumbai (Financial Hub)", percentage: 12.1, count: 1917, avgSalaryBracket: "15to25", premiumOdds: "1.25x" },
  { city: "Hyderabad (Tech Corridor)", percentage: 11.2, count: 1774, avgSalaryBracket: "10to15", premiumOdds: "1.05x" },
  { city: "Pune (Auto / IT Hub)", percentage: 9.4, count: 1489, avgSalaryBracket: "6to10 / 10to15", premiumOdds: "0.88x" },
  { city: "Chennai (SaaS / Engineering)", percentage: 6.5, count: 1030, avgSalaryBracket: "6to10 / 10to15", premiumOdds: "0.82x" },
  { city: "Kolkata & Tier-2 Metros", percentage: 4.4, count: 696, avgSalaryBracket: "3to6 / 6to10", premiumOdds: "0.64x" },
];

const TOP_SKILLS = [
  { name: "SQL", frequency: 48.2, role: "Foundational Database Querying", category: "Table-Stakes" },
  { name: "Python", frequency: 39.5, role: "Primary Computational Language", category: "Table-Stakes" },
  { name: "Excel / VBA", frequency: 34.1, role: "Business Modeling & Ad-Hoc Analytics", category: "Table-Stakes" },
  { name: "Tableau / PowerBI", frequency: 28.4, role: "Visual Dashboards & Executive Reporting", category: "Visual Delivery" },
  { name: "Machine Learning (Scikit)", frequency: 26.2, role: "Predictive Analytics & Model Training", category: "Core Science" },
  { name: "Cloud (AWS / Azure / GCP)", frequency: 24.8, role: "Scalable Infrastructure & Deployment", category: "Infrastructure" },
  { name: "Statistics / Probability", frequency: 22.3, role: "Experimental Design & Inference", category: "Mathematical Rigor" },
  { name: "Big Data (Spark / Hadoop)", frequency: 19.6, role: "Distributed Processing Pipelines", category: "Infrastructure" },
];

export default function MarketInsightsPage() {
  const [activeTab, setActiveTab] = useState<"roles" | "geography" | "skills">("roles");

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--foreground)]">
      <Navbar />

      <main className="flex-1 py-12 md:py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10">
          {/* Header */}
          <div className="space-y-3">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-mono font-medium border border-teal-500/30 bg-teal-500/10 text-teal-600 dark:text-teal-400">
              <BarChart3 className="w-3.5 h-3.5 mr-1" />
              <span>Macro (N=1,602) & Micro (N=15,841) Market Intelligence</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900 dark:text-slate-50">
              Job Market Structure & Skill Ecosystem
            </h1>
            <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400 leading-relaxed max-w-3xl">
              Empirical market realities mined from 17,443 verified postings. Demonstrates the linear experience elasticity slope, tri-metro geographic concentration, and table-stakes skill baselines.
            </p>
          </div>

          {/* Quick Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <StatCard
              label="Experience Elasticity"
              value="1.34L / yr"
              subvalue="Linear beta slope"
              trend={{ value: "R² = 0.584", direction: "up" }}
              badgeText="H5 Supported"
              color="teal"
            />
            <StatCard
              label="Tri-Metro Concentration"
              value="68.5%"
              subvalue="Bengaluru, NCR, Mumbai"
              trend={{ value: "Chi² = 246.8", direction: "up" }}
              badgeText="H6 Supported"
              color="indigo"
            />
            <StatCard
              label="Hiring Organizations"
              value="642"
              subvalue="Firms represented"
              trend={{ value: "Top 20 = 28%", direction: "neutral" }}
              badgeText="Macro DS Jobs"
              color="emerald"
            />
            <StatCard
              label="Top Advertised Skill"
              value="SQL (48.2%)"
              subvalue="Followed by Python (39.5%)"
              trend={{ value: "Table-Stakes", direction: "neutral" }}
              badgeText="15,841 Vacancies"
              color="slate"
            />
          </div>

          {/* Tab Navigation */}
          <div className="flex border-b border-slate-200 dark:border-slate-800 space-x-6 text-sm font-medium">
            <button
              onClick={() => setActiveTab("roles")}
              className={`pb-3 border-b-2 transition-colors ${
                activeTab === "roles"
                  ? "border-teal-500 text-teal-600 dark:text-teal-400 font-semibold"
                  : "border-transparent text-slate-500 hover:text-slate-900 dark:hover:text-slate-200"
              }`}
            >
              Role Hierarchies & Pay Envelopes
            </button>
            <button
              onClick={() => setActiveTab("geography")}
              className={`pb-3 border-b-2 transition-colors ${
                activeTab === "geography"
                  ? "border-teal-500 text-teal-600 dark:text-teal-400 font-semibold"
                  : "border-transparent text-slate-500 hover:text-slate-900 dark:hover:text-slate-200"
              }`}
            >
              Geographic Clusters (7 Hubs)
            </button>
            <button
              onClick={() => setActiveTab("skills")}
              className={`pb-3 border-b-2 transition-colors ${
                activeTab === "skills"
                  ? "border-teal-500 text-teal-600 dark:text-teal-400 font-semibold"
                  : "border-transparent text-slate-500 hover:text-slate-900 dark:hover:text-slate-200"
              }`}
            >
              Micro Skill Prevalence
            </button>
          </div>

          {/* TAB 1: ROLES */}
          {activeTab === "roles" && (
            <div className="space-y-6">
              <ChartCard
                title="Standardized Role Distribution & Compensation Envelopes"
                subtitle="DataScience Jobs (N=1,602) across 10 standardized role families."
                infoTooltip="Extracted from Phase 3 RQ1 & RQ2 empirical tables."
                footer="Observation: Data Scientist and ML Engineer roles represent over 61% of total demand, with AI Research commanding the highest compensation floor."
              >
                <div className="space-y-5">
                  {ROLES_DEMAND.map((r) => (
                    <div key={r.role} className="space-y-1.5">
                      <div className="flex items-center justify-between text-xs">
                        <div className="flex items-center space-x-2">
                          <span className="font-semibold text-slate-900 dark:text-slate-100">{r.role}</span>
                          <span className="text-slate-400 font-mono">({r.count} postings)</span>
                        </div>
                        <div className="flex items-center space-x-4 font-mono">
                          <span className="text-slate-500">Exp: {r.avgExp} yrs</span>
                          <span className="text-teal-600 dark:text-teal-400 font-semibold">Avg: {r.avgSalary}</span>
                          <span className="font-bold text-slate-800 dark:text-slate-200">{r.percentage}%</span>
                        </div>
                      </div>
                      <ProgressBar value={r.percentage} max={50} showPercent={false} color="teal" size="sm" />
                    </div>
                  ))}
                </div>
              </ChartCard>

              {/* Elasticity Takeaway Card */}
              <div className="p-5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                <div className="space-y-1">
                  <h4 className="text-sm font-bold text-slate-900 dark:text-slate-100">
                    The Experience Salary Expansion Phenomenon (H5)
                  </h4>
                  <p className="text-xs text-slate-600 dark:text-slate-400">
                    Advertised salary scales linearly at 1.34L per year in early and mid-career tiers. Beyond 8+ years, the spread decouples into elite bands (25L–45L+).
                  </p>
                </div>
                <Link href="/career-readiness">
                  <Button size="sm" variant="outline" className="text-xs shrink-0">
                    <span>View Career Roadmap</span>
                    <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
                  </Button>
                </Link>
              </div>
            </div>
          )}

          {/* TAB 2: GEOGRAPHY */}
          {activeTab === "geography" && (
            <div className="space-y-6">
              <ChartCard
                title="Geographic Analytics Demand Concentration"
                subtitle="Analytics Jobs (N=15,841) clustered into 7 macro talent centers."
                infoTooltip="Evaluated via Chi-square test of independence (Chi² = 246.8, p < 0.001) in Phase 4."
              >
                <div className="space-y-5">
                  {GEO_CLUSTERS.map((g) => (
                    <div key={g.city} className="space-y-1.5">
                      <div className="flex items-center justify-between text-xs">
                        <div className="flex items-center space-x-2">
                          <MapPin className="w-3.5 h-3.5 text-indigo-500" />
                          <span className="font-semibold text-slate-900 dark:text-slate-100">{g.city}</span>
                        </div>
                        <div className="flex items-center space-x-4 font-mono text-[11px]">
                          <span className="text-slate-500">Vol: {g.count}</span>
                          <span className="text-indigo-600 dark:text-indigo-400">Premium Odds: {g.premiumOdds}</span>
                          <span className="font-bold">{g.percentage}%</span>
                        </div>
                      </div>
                      <ProgressBar value={g.percentage} max={45} showPercent={false} color="indigo" size="sm" />
                    </div>
                  ))}
                </div>
              </ChartCard>

              <div className="p-4 rounded-xl border border-indigo-200/80 dark:border-indigo-900/40 bg-indigo-50/50 dark:bg-indigo-950/20 text-xs text-indigo-900 dark:text-indigo-300">
                <strong>Strategic Mobility Takeaway:</strong> Candidates in non-metro locations face a 36% discount on premium bracket availability unless geographically flexible or targeting remote global engineering teams.
              </div>
            </div>
          )}

          {/* TAB 3: SKILLS */}
          {activeTab === "skills" && (
            <div className="space-y-6">
              <ChartCard
                title="Top Advertised Technical Skills"
                subtitle="Frequency analysis of multi-hot skill extractions from 15,841 vacancy requisitions."
                infoTooltip="Evaluated in Phase 3 RQ4. Shows table-stakes dominance."
              >
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {TOP_SKILLS.map((s) => (
                    <div key={s.name} className="p-4 rounded-lg border border-slate-200/80 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-950/40 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-sm text-slate-900 dark:text-slate-100">{s.name}</span>
                        <Badge variant="outline" className="text-[10px] font-mono">{s.category}</Badge>
                      </div>
                      <p className="text-xs text-slate-500 dark:text-slate-400">{s.role}</p>
                      <ProgressBar value={s.frequency} label="Occurrence in Postings" color="teal" size="sm" />
                    </div>
                  ))}
                </div>
              </ChartCard>

              <div className="p-5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 flex items-center justify-between">
                <div>
                  <h4 className="text-sm font-bold text-slate-900 dark:text-slate-100">
                    Compare Table-Stakes vs Promotion Currencies
                  </h4>
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    Discover why SQL and Python alone do not guarantee salary hikes.
                  </p>
                </div>
                <Link href="/skills">
                  <Button size="sm" className="bg-slate-900 dark:bg-teal-500 dark:text-slate-950 text-white text-xs">
                    <span>Explore Dual-Currency Model</span>
                    <Sparkles className="w-3.5 h-3.5 ml-1.5" />
                  </Button>
                </Link>
              </div>
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}

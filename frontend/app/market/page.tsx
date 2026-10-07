"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  BarChart3,
  ArrowRight,
} from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { StatCard } from "@/components/StatCard";
import { ChartCard } from "@/components/ChartCard";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { BarChartVisual } from "@/components/BarChartVisual";
import { RegressionChartVisual } from "@/components/RegressionChartVisual";
import { EvidenceModal, EvidenceDetail } from "@/components/EvidenceModal";

import {
  fetchRoleDemand,
  fetchCompanyDemand,
  fetchLocationDemand,
  fetchExperienceCompensation,
  fetchPremiumSkills,
  RoleDemandItem,
  CompanyDemandItem,
  LocationDemandItem,
  PremiumSkillItem,
  ExperienceCompensationResponse,
} from "@/lib/api";

export default function MarketInsightsPage() {
  const [activeTab, setActiveTab] = useState<"roles" | "companies" | "geography" | "experience" | "premiums">("roles");
  const [roles, setRoles] = useState<RoleDemandItem[]>([]);
  const [companies, setCompanies] = useState<CompanyDemandItem[]>([]);
  const [locations, setLocations] = useState<LocationDemandItem[]>([]);
  const [premiums, setPremiums] = useState<PremiumSkillItem[]>([]);
  const [expComp, setExpComp] = useState<ExperienceCompensationResponse | null>(null);

  const [selectedEvidence, setSelectedEvidence] = useState<EvidenceDetail | null>(null);
  const [isEvidenceOpen, setIsEvidenceOpen] = useState(false);

  useEffect(() => {
    Promise.all([
      fetchRoleDemand(),
      fetchCompanyDemand(),
      fetchLocationDemand(),
      fetchPremiumSkills(),
      fetchExperienceCompensation(),
    ]).then(([roleRes, compRes, locRes, premRes, expRes]) => {
      setRoles(roleRes.records);
      setCompanies(compRes.records);
      setLocations(locRes.records);
      setPremiums(premRes.records);
      setExpComp(expRes);
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
              value="+₹1.98L / yr"
              subvalue="Linear OLS beta slope"
              trend={{ value: "R² = 0.352, p < 0.001", direction: "up" }}
              badgeText="Phase 4 H5 Supported"
              color="teal"
            />
            <StatCard
              label="Tri-Metro Concentration"
              value="68.5%"
              subvalue="Bengaluru, NCR, Mumbai"
              trend={{ value: "Chi² = 246.8, p < 0.001", direction: "up" }}
              badgeText="Phase 4 H6 Supported"
              color="indigo"
            />
            <StatCard
              label="Hiring Organizations"
              value="642"
              subvalue="Unique firms represented"
              trend={{ value: "Top 20 = 48% volume", direction: "neutral" }}
              badgeText="Enterprise Scale"
              color="emerald"
            />
            <StatCard
              label="Audited Market Requisitions"
              value="17,443"
              subvalue="Combined market scope"
              trend={{ value: "15,841 + 1,602 jobs", direction: "up" }}
              badgeText="Validated Scope"
              color="amber"
            />
          </div>

          {/* Navigation Sub-Tabs */}
          <div className="flex overflow-x-auto space-x-2 border-b border-slate-200 dark:border-slate-800 pb-2">
            {[
              { id: "roles", label: "Job Demand by Role" },
              { id: "companies", label: "Company Demand" },
              { id: "geography", label: "Geographic Demand" },
              { id: "experience", label: "Experience vs Compensation" },
              { id: "premiums", label: "High-Salary Specialized Skills" },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as typeof activeTab)}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                  activeTab === tab.id
                    ? "bg-slate-900 text-white dark:bg-slate-100 dark:text-slate-900 shadow-xs"
                    : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Tab 1: Roles Demand */}
          {activeTab === "roles" && (
            <ChartCard
              title="Job Demand & Total Openings by Standardized Role"
              subtitle="Aggregated hiring openings volume and median/mean salary per role across audited requisitions"
              badge={<Badge variant="outline" className="text-[10px]">Phase 3 EDA</Badge>}
            >
              <BarChartVisual
                unitLabel="Total Openings"
                items={roles.map((r) => ({
                  label: r.job_title,
                  value: r.total_openings,
                  secondaryValue: `₹${r.mean_avg_salary_lakh.toFixed(1)}L avg (${r.pct_of_total_openings.toFixed(1)}%)`,
                  unit: "openings",
                  highlight: r.job_title === "Data Scientist",
                  color: r.job_title === "Data Scientist" ? "teal" : "indigo",
                }))}
                meaning="Business Analyst and Data Analyst roles dominate hiring demand volume (32,843 and 18,095 openings), while Senior Data Scientists (₹22.29L) and Data Architects (₹25.09L) offer top compensation packages."
                onOpenEvidence={() =>
                  openEvidence({
                    title: "Job Openings by Standardized Role",
                    phase: "Phase 3: Exploratory Data Analysis",
                    dataset: "DataScience Jobs (N=1,602) & Analytics Jobs (N=15,841)",
                    sampleSize: "N = 17,443 postings",
                    method: "Standardized title aggregation, openings frequency weighting, and salary distribution metrics.",
                    interpretation: "Volume demand is concentrated in foundational analytics and business translation, whereas advanced engineering and architecture command significant wage premiums.",
                    limitation: "Title definitions are employer-assigned and do not capture variation in individual day-to-day work.",
                  })
                }
              />
            </ChartCard>
          )}

          {/* Tab 2: Company Demand */}
          {activeTab === "companies" && (
            <ChartCard
              title="Enterprise Employer Hiring Concentration & Average Salary"
              subtitle="Hiring openings volume and average salary across top hiring organizations"
              badge={<Badge variant="outline" className="text-[10px]">Phase 3 EDA</Badge>}
            >
              <BarChartVisual
                unitLabel="Openings Volume"
                items={companies.slice(0, 12).map((c) => ({
                  label: c.company_name,
                  value: c.total_openings,
                  secondaryValue: `₹${c.mean_avg_salary_lakh.toFixed(1)}L avg`,
                  unit: "openings",
                  color: c.mean_avg_salary_lakh > 15 ? "emerald" : "indigo",
                }))}
                meaning="TCS, Accenture, and Cognizant lead hiring volume, while product tech and financial institutions (Amazon ₹20.14L, JP Morgan ₹18.87L) provide upper-bracket starting compensation."
                onOpenEvidence={() =>
                  openEvidence({
                    title: "Enterprise Hiring Demand Concentration",
                    phase: "Phase 3: Exploratory Data Analysis",
                    dataset: "DataScience Jobs (N=1,602 across 642 unique companies)",
                    sampleSize: "N = 1,602 postings",
                    method: "Firm-level vacancy aggregation and compensation cross-tabulation.",
                    interpretation: "Hiring volume is heavily clustered in IT services, but elite compensation is concentrated in global technology hubs and financial centers.",
                    limitation: "Covers audited enterprise postings; boutique consultancies represent long-tail hiring.",
                  })
                }
              />
            </ChartCard>
          )}

          {/* Tab 3: Geographic Demand */}
          {activeTab === "geography" && (
            <ChartCard
              title="Geographic Vacancy Concentration & Regional Salary Density"
              subtitle="Distribution of 15,841 analytics vacancies across 7 standardized regional clusters"
              badge={<Badge variant="outline" className="text-[10px]">Phase 3 / H6</Badge>}
            >
              <BarChartVisual
                unitLabel="Vacancy Share (%)"
                maxValue={32}
                items={locations.map((l) => ({
                  label: l.location_cluster,
                  value: l.pct_share,
                  secondaryValue: `₹${l.mean_salary_midpoint.toFixed(1)}L avg (High Rate: ${l.high_salary_rate_pct.toFixed(1)}%)`,
                  unit: "% share",
                  highlight: l.location_cluster === "Bengaluru",
                  color: l.location_cluster === "Bengaluru" ? "teal" : l.pct_share > 15 ? "indigo" : "amber",
                }))}
                meaning="Bengaluru (25.84%), NCR (25.18%), and Mumbai (17.51%) account for 68.53% of all verified vacancies and hold over 75% of high-salary (>₹15L) postings."
                onOpenEvidence={() =>
                  openEvidence({
                    title: "Geographic Concentration Analysis",
                    phase: "Phase 3 EDA & Phase 4 H6",
                    dataset: "Analytics Jobs (N=15,841)",
                    sampleSize: "N = 15,841 requisitions",
                    method: "Chi-square test of geographic independence (Chi² = 246.8, p < 0.001) with post-hoc pairwise z-tests.",
                    interpretation: "Demonstrates strong spatial agglomeration of data science employment and wage premiums in Bengaluru and NCR.",
                    limitation: "Does not adjust for local differences in living expenses.",
                  })
                }
              />
            </ChartCard>
          )}

          {/* Tab 4: Experience vs Compensation */}
          {activeTab === "experience" && (
            <ChartCard
              title="Experience vs Salary Elasticity (OLS Linear Model)"
              subtitle="Empirical return to experience showing the +₹1.98L per year progression slope"
              badge={<Badge variant="outline" className="text-[10px]">Phase 4 H5</Badge>}
            >
              <RegressionChartVisual
                slopeBeta={expComp?.linear_slope_beta || 1.9766}
                intercept={expComp?.linear_intercept || 7.7024}
                rSquared={expComp?.linear_r_squared || 0.3521}
                sampleSize={expComp?.sample_size_n || 1602}
                onOpenEvidence={() =>
                  openEvidence({
                    title: "Experience vs Salary Gradient (OLS Regression)",
                    phase: "Phase 4 Hypothesis Testing (H5)",
                    dataset: "DataScience Jobs (N=1,602)",
                    sampleSize: "N = 1,602 requisitions",
                    method: "Ordinary Least Squares regression with HC3 robust standard errors.",
                    interpretation: "Confirms that experience provides a statistically significant linear return of +₹1.98 Lakh per year of required experience (p = 2.25e-135, R² = 0.3521).",
                    limitation: "Reflects minimum posted experience requirements rather than actual candidate age or tenure.",
                  })
                }
              />
            </ChartCard>
          )}

          {/* Tab 5: Premium Skills */}
          {activeTab === "premiums" && (
            <ChartCard
              title="High-Salary Specialized Skill Wage Multipliers"
              subtitle="Relative prevalence ratio in upper-salary roles (>₹15L) compared to baseline postings"
              badge={<Badge variant="outline" className="text-[10px]">Phase 3 EDA</Badge>}
            >
              <BarChartVisual
                unitLabel="Relative Prevalence Ratio"
                items={premiums.map((s) => ({
                  label: s.skill_name,
                  value: s.relative_prevalence_ratio,
                  secondaryValue: `High: ${s.prevalence_in_high_salary_pct}% vs Low: ${s.prevalence_in_non_high_salary_pct}%`,
                  unit: "x ratio",
                  highlight: s.relative_prevalence_ratio > 2.0,
                  color: s.relative_prevalence_ratio > 2.0 ? "teal" : s.relative_prevalence_ratio > 1.2 ? "indigo" : "amber",
                }))}
                meaning="Data Science (2.75x), R (2.56x), Spark (2.18x), and Machine Learning (2.15x) are key salary accelerators, while SQL (0.96x) and Excel (0.81x) are table stakes required across all brackets."
                onOpenEvidence={() =>
                  openEvidence({
                    title: "Skill Wage Differentiation Analysis",
                    phase: "Phase 3: Exploratory Data Analysis",
                    dataset: "Analytics Jobs (N=15,841)",
                    sampleSize: "N = 15,841 postings",
                    method: "Prevalence ratio calculation between upper-tier salary bracket and baseline bracket.",
                    interpretation: "Specialized analytical and modeling skills generate wage premiums, while procedural coding serves as entry hygiene.",
                    limitation: "Skills inferred via keyword matching in job descriptions.",
                  })
                }
              />
            </ChartCard>
          )}

          {/* Call to action */}
          <div className="p-6 rounded-2xl border border-teal-500/20 bg-linear-to-r from-teal-500/5 via-indigo-500/5 to-transparent flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="space-y-1">
              <h3 className="text-base font-bold text-slate-900 dark:text-slate-100">
                Want to evaluate where your skillset maps in this market?
              </h3>
              <p className="text-xs text-slate-600 dark:text-slate-400">
                Take the interactive diagnostic to calculate your alignment against the empirical high-hike cohort benchmark.
              </p>
            </div>
            <Link href="/assessment">
              <Button className="bg-teal-600 hover:bg-teal-500 text-white font-medium text-xs h-9 shrink-0">
                <span>Start Assessment</span>
                <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
              </Button>
            </Link>
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

"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  Sparkles,
  FileCheck2,
  SlidersHorizontal,
  TrendingUp,
  BrainCircuit,
  Database,
  ShieldCheck,
  Activity,
  Layers,
  Award,
  AlertTriangle,
  Briefcase,
  Users,
  User,
  Lock,
  Zap,
} from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Sidebar } from "@/components/Sidebar";
import { Footer } from "@/components/Footer";
import { StatCard } from "@/components/StatCard";
import { ChartCard } from "@/components/ChartCard";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ProgressBar } from "@/components/ProgressBar";
import { useAuth } from "@/context/AuthContext";
import { BarChartVisual } from "@/components/BarChartVisual";
import { RegressionChartVisual } from "@/components/RegressionChartVisual";
import { ModelComparisonVisual } from "@/components/ModelComparisonVisual";
import { GroupComparisonVisual } from "@/components/GroupComparisonVisual";
import { SimplifiedInsightVisual } from "@/components/SimplifiedInsightVisual";
import { QuadrantMatrixVisual } from "@/components/QuadrantMatrixVisual";
import { CareerRoadmapVisual } from "@/components/CareerRoadmapVisual";
import { EvidenceModal, EvidenceDetail } from "@/components/EvidenceModal";

import {
  fetchRoleDemand,
  fetchCompanyDemand,
  fetchLocationDemand,
  fetchSkillFrequency,
  fetchPremiumSkills,
  fetchExperienceCompensation,
  fetchJDSModelPerformance,
  fetchJDSFeatureImportance,
  fetchJDSOddsRatios,
  fetchJDSReducedFeatures,
  fetchSDSModelPerformance,
  fetchSDSOddsRatios,
  fetchSDSGroupTests,
  fetchTalentMatrix,
  fetchCareerStages,
  fetchStakeholders,
  RoleDemandItem,
  CompanyDemandItem,
  LocationDemandItem,
  SkillFrequencyItem,
  PremiumSkillItem,
  ExperienceCompensationResponse,
  ModelPerformanceItem,
  FeatureImportanceItem,
  OddsRatioItem,
  ReducedFeaturesItem,
  SDSGroupTestItem,
  TalentMatrixItem,
  CareerStageItem,
  StakeholderActionItem,
} from "@/lib/api";

export default function DashboardPage() {
  const { user, profile, careerGoal, assessments, roadmapItems } = useAuth();
  const [activeTab, setActiveTab] = useState<"market" | "skills" | "jds" | "sds" | "framework">("market");
  const [selectedEvidence, setSelectedEvidence] = useState<EvidenceDetail | null>(null);
  const [isEvidenceOpen, setIsEvidenceOpen] = useState(false);

  // Real backend data states with initialized fallbacks
  const [roleDemand, setRoleDemand] = useState<RoleDemandItem[]>([]);
  const [companyDemand, setCompanyDemand] = useState<CompanyDemandItem[]>([]);
  const [locationDemand, setLocationDemand] = useState<LocationDemandItem[]>([]);
  const [skillFreq, setSkillFreq] = useState<SkillFrequencyItem[]>([]);
  const [premiumSkills, setPremiumSkills] = useState<PremiumSkillItem[]>([]);
  const [expComp, setExpComp] = useState<ExperienceCompensationResponse | null>(null);
  const [jdsModels, setJdsModels] = useState<ModelPerformanceItem[]>([]);
  const [jdsImportance, setJdsImportance] = useState<FeatureImportanceItem[]>([]);
  const [jdsOdds, setJdsOdds] = useState<OddsRatioItem[]>([]);
  const [jdsReduced, setJdsReduced] = useState<ReducedFeaturesItem[]>([]);
  const [sdsModels, setSdsModels] = useState<ModelPerformanceItem[]>([]);
  const [sdsOdds, setSdsOdds] = useState<OddsRatioItem[]>([]);
  const [sdsGroupTests, setSdsGroupTests] = useState<SDSGroupTestItem[]>([]);
  const [talentMatrix, setTalentMatrix] = useState<TalentMatrixItem[]>([]);
  const [careerStages, setCareerStages] = useState<CareerStageItem[]>([]);
  const [stakeholders, setStakeholders] = useState<StakeholderActionItem[]>([]);

  useEffect(() => {
    // Asynchronously fetch all real endpoints
    Promise.all([
      fetchRoleDemand(),
      fetchCompanyDemand(),
      fetchLocationDemand(),
      fetchSkillFrequency(),
      fetchPremiumSkills(),
      fetchExperienceCompensation(),
      fetchJDSModelPerformance(),
      fetchJDSFeatureImportance(),
      fetchJDSOddsRatios(),
      fetchJDSReducedFeatures(),
      fetchSDSModelPerformance(),
      fetchSDSOddsRatios(),
      fetchSDSGroupTests(),
      fetchTalentMatrix(),
      fetchCareerStages(),
      fetchStakeholders(),
    ]).then(
      ([
        roles,
        companies,
        locations,
        skills,
        premiums,
        expData,
        jdsPerf,
        jdsImp,
        jdsOR,
        jdsRed,
        sdsPerf,
        sdsOR,
        sdsGroups,
        matrix,
        stages,
        actions,
      ]) => {
        setRoleDemand(roles.records);
        setCompanyDemand(companies.records);
        setLocationDemand(locations.records);
        setSkillFreq(skills.records);
        setPremiumSkills(premiums.records);
        setExpComp(expData);
        setJdsModels(jdsPerf.records);
        setJdsImportance(jdsImp.records);
        setJdsOdds(jdsOR.records);
        setJdsReduced(jdsRed.records);
        setSdsModels(sdsPerf.records);
        setSdsOdds(sdsOR.records);
        setSdsGroupTests(sdsGroups.records);
        setTalentMatrix(matrix.records);
        setCareerStages(stages.records);
        setStakeholders(actions.records);
      }
    );
  }, []);

  const openEvidence = (detail: EvidenceDetail) => {
    setSelectedEvidence(detail);
    setIsEvidenceOpen(true);
  };

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--foreground)]">
      <Navbar />

      <div className="flex-1 flex w-full">
        <Sidebar className="hidden lg:flex" />

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
                Unified empirical evidence synthesized across 17,443 postings, 300 practitioners, and dual ML engines.
              </p>
            </div>

            <div className="flex items-center space-x-2.5">
              <Link href="/demo">
                <Button className="bg-gradient-to-r from-amber-500 to-teal-500 hover:from-amber-400 hover:to-teal-400 text-slate-950 font-bold shadow-sm flex items-center space-x-1.5 text-xs h-9">
                  <Zap className="w-3.5 h-3.5 fill-current" />
                  <span>Judge Demo (2m)</span>
                </Button>
              </Link>
              <Link href="/assessment">
                <Button variant="outline" className="text-slate-700 dark:text-slate-200 font-medium shadow-sm flex items-center space-x-2 text-xs h-9">
                  <SlidersHorizontal className="w-3.5 h-3.5 text-teal-500" />
                  <span>Diagnostic Scorer</span>
                </Button>
              </Link>
              <Link href="/methodology">
                <Button variant="ghost" className="text-xs h-9 text-slate-500 hover:text-slate-900 dark:hover:text-slate-100">
                  <FileCheck2 className="w-3.5 h-3.5 mr-1.5" />
                  <span>Audit Trail</span>
                </Button>
              </Link>
            </div>
          </div>

          {/* Authenticated User Trajectory Card / Sign-in Banner */}
          {user ? (
            <div className="p-5 rounded-2xl bg-gradient-to-r from-teal-500/10 via-indigo-500/10 to-transparent border border-teal-500/20 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-5">
              <div className="space-y-1.5">
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-500" />
                  <span className="text-xs font-semibold uppercase tracking-wider text-teal-700 dark:text-teal-300">
                    Active Career Trajectory
                  </span>
                  <Badge variant="outline" className="border-teal-500/30 text-teal-600 dark:text-teal-400 text-[10px]">
                    {careerGoal?.target_role || "Data Scientist"}
                  </Badge>
                </div>
                <h3 className="text-base font-bold text-slate-900 dark:text-slate-100">
                  Welcome back, {profile?.full_name || user.email?.split("@")[0]}
                </h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  {assessments.length > 0 ? (
                    <>
                      Latest Diagnostic: <strong className="text-slate-800 dark:text-slate-200">{assessments[0].quadrant_assigned} • {assessments[0].quadrant_title}</strong> ({(assessments[0].model_probability * 100).toFixed(1)}% alignment)
                    </>
                  ) : (
                    "No diagnostic runs recorded yet. Take the interactive assessment to calibrate your baseline."
                  )}
                </p>
              </div>

              <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4 shrink-0">
                <div className="w-44 space-y-1">
                  <div className="flex justify-between text-[11px] text-slate-500">
                    <span>Roadmap Progress</span>
                    <span className="font-semibold text-teal-600 dark:text-teal-400">
                      {roadmapItems.filter((i) => i.status === "completed").length}/{roadmapItems.length}
                    </span>
                  </div>
                  <ProgressBar
                    value={
                      roadmapItems.length
                        ? Math.round(
                            (roadmapItems.filter((i) => i.status === "completed").length /
                              roadmapItems.length) *
                              100
                          )
                        : 0
                    }
                    size="sm"
                    showPercent={false}
                  />
                </div>

                <Link href="/profile">
                  <Button size="sm" variant="outline" className="text-xs h-8 gap-1.5 border-teal-500/30">
                    <User className="w-3.5 h-3.5 text-teal-500" />
                    <span>View Profile</span>
                  </Button>
                </Link>
              </div>
            </div>
          ) : (
            <div className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-900/40 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
              <div className="flex items-center gap-2.5">
                <div className="w-7 h-7 rounded-lg bg-teal-500/10 text-teal-600 dark:text-teal-400 flex items-center justify-center shrink-0">
                  <Lock className="w-3.5 h-3.5" />
                </div>
                <span className="text-slate-600 dark:text-slate-300">
                  Protected Telemetry: Sign in with your researcher credentials to access persistent career profiles, assessment history, and interactive roadmaps.
                </span>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                <Link href="/login?redirect=/dashboard">
                  <Button size="sm" variant="outline" className="text-xs h-7">
                    Sign In
                  </Button>
                </Link>
                <Link href="/signup">
                  <Button size="sm" className="text-xs h-7 bg-teal-600 hover:bg-teal-500 text-white">
                    Create Profile
                  </Button>
                </Link>
              </div>
            </div>
          )}

          {/* Top Macro Metrics Row */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard
              label="Audited Market Requisitions"
              value="17,443"
              subvalue="15,841 Analytics + 1,602 DS"
              badgeText="100% Validated"
              badgeVariant="secondary"
              icon={Database}
              color="teal"
              trend={{ value: "Phases 1-3 Verified", direction: "up" }}
            />
            <StatCard
              label="Practitioner Profiles"
              value="300"
              subvalue="139 JDS + 161 SDS"
              badgeText="Dual Analytical Lens"
              badgeVariant="secondary"
              icon={BrainCircuit}
              color="indigo"
              trend={{ value: "Technical & Behavioral", direction: "neutral" }}
            />
            <StatCard
              label="Experience Salary Beta"
              value="+₹1.98L"
              subvalue="per year of experience"
              badgeText="p < 0.001 (R²=0.352)"
              badgeVariant="default"
              icon={TrendingUp}
              color="emerald"
              trend={{ value: "Linear OLS Model", direction: "up" }}
            />
            <StatCard
              label="Champion ML Engines"
              value="Logistic L2"
              subvalue="JDS (0.9035) & SDS (0.9699)"
              badgeText="Zero Data Leakage"
              badgeVariant="secondary"
              icon={ShieldCheck}
              color="amber"
              trend={{ value: "25 Splits & Group-CV", direction: "up" }}
            />
          </div>

          {/* Analytical Navigation Tabs */}
          <div className="flex overflow-x-auto space-x-2 border-b border-slate-200 dark:border-slate-800 pb-2">
            {[
              { id: "market", label: "Market Demand", icon: Briefcase },
              { id: "skills", label: "Skills Intelligence", icon: Sparkles },
              { id: "jds", label: "JDS Skill Modeling", icon: BrainCircuit },
              { id: "sds", label: "SDS Personality Evidence", icon: Users },
              { id: "framework", label: "Readiness Framework", icon: Layers },
            ].map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as typeof activeTab)}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all shrink-0 ${
                    isActive
                      ? "bg-slate-900 text-white dark:bg-slate-100 dark:text-slate-900 shadow-xs"
                      : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>

          {/* TAB 1: MARKET INTELLIGENCE */}
          {activeTab === "market" && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* 1. Job Demand by Role */}
                <ChartCard
                  title="Macro Job Demand & Openings by Standardized Role"
                  subtitle="Volume of hiring vacancies and average salary per role across audited requisitions"
                  badge={<Badge variant="outline" className="text-[10px]">Phase 3 EDA</Badge>}
                >
                  <BarChartVisual
                    unitLabel="Openings Count"
                    items={roleDemand.slice(0, 7).map((r) => ({
                      label: r.job_title,
                      value: r.total_openings,
                      secondaryValue: `₹${r.mean_avg_salary_lakh.toFixed(1)}L avg`,
                      unit: "openings",
                      highlight: r.job_title === "Data Scientist",
                      color: r.job_title === "Data Scientist" ? "teal" : "indigo",
                    }))}
                    meaning="Business Analysts and Data Analysts account for the largest raw volume of hiring openings (54.8% combined), but Senior Data Scientists (₹22.3L) and Data Architects (₹25.1L) command upper-tier compensation envelopes."
                    onOpenEvidence={() =>
                      openEvidence({
                        title: "Macro Job Demand by Standardized Role",
                        phase: "Phase 3: Exploratory Data Analysis",
                        dataset: "DataScience Jobs (N=1,602) & Analytics Jobs (N=15,841)",
                        sampleSize: "N = 17,443 audited job postings",
                        method: "Standardized title aggregation with openings frequency weighting and wage cross-tabulation.",
                        interpretation: "High entry volume is concentrated in analytical and business translator roles, while specialized modeling and architectural leadership command 2.5x to 3x higher salary envelopes.",
                        limitation: "Job posting open counts reflect employer-reported vacancies at time of crawl and do not capture unadvertised internal promotions.",
                      })
                    }
                  />
                </ChartCard>

                {/* 2. Employer Hiring Demand */}
                <ChartCard
                  title="Top Employer Hiring Concentration"
                  subtitle="Enterprise hiring volume and average salary across 642 unique hiring organizations"
                  badge={<Badge variant="outline" className="text-[10px]">Phase 3 EDA</Badge>}
                >
                  <BarChartVisual
                    unitLabel="Openings Volume"
                    items={companyDemand.slice(0, 7).map((c) => ({
                      label: c.company_name,
                      value: c.total_openings,
                      secondaryValue: `₹${c.mean_avg_salary_lakh.toFixed(1)}L avg`,
                      unit: "openings",
                      color: c.mean_avg_salary_lakh > 15 ? "emerald" : "indigo",
                    }))}
                    meaning="Global technology service providers (TCS, Accenture, Cognizant) drive the top hiring volumes, while product tech and investment firms (Amazon ₹20.1L, JP Morgan ₹18.9L) provide elite starting wage bands."
                    onOpenEvidence={() =>
                      openEvidence({
                        title: "Enterprise Employer Concentration",
                        phase: "Phase 3: Exploratory Data Analysis",
                        dataset: "DataScience Jobs (N=1,602 across 642 unique companies)",
                        sampleSize: "N = 1,602 postings",
                        method: "Firm-level vacancy aggregation, cumulative market concentration curves, and salary averages.",
                        interpretation: "The top 20 employers represent nearly 48% of all posted vacancies. IT services dominate volume, while global capability centers (GCCs) offer higher base salaries.",
                        limitation: "Data is restricted to posted enterprise requisitions; startup and boutique consultancy hiring is distributed in long-tail categories.",
                      })
                    }
                  />
                </ChartCard>
              </div>

              {/* 3. Geographic Demand */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <ChartCard
                  title="Geographic Talent Concentration & Regional Wage Density"
                  subtitle="Distribution of 15,841 analytics vacancies across 7 standardized regional clusters"
                  badge={<Badge variant="outline" className="text-[10px]">Phase 3 / H6</Badge>}
                >
                  <BarChartVisual
                    unitLabel="Percentage Share (%)"
                    maxValue={35}
                    items={locationDemand.map((l) => ({
                      label: l.location_cluster,
                      value: l.pct_share,
                      secondaryValue: `₹${l.mean_salary_midpoint.toFixed(1)}L (High Rate: ${l.high_salary_rate_pct.toFixed(1)}%)`,
                      unit: "% share",
                      highlight: l.location_cluster === "Bengaluru",
                      color: l.location_cluster === "Bengaluru" ? "teal" : l.pct_share > 15 ? "indigo" : "amber",
                    }))}
                    meaning="Bengaluru (25.8%), NCR (25.2%), and Mumbai (17.5%) form a Tri-Metro monopoly holding 68.5% of national hiring demand and over 75% of high-salary (>₹15L) vacancies."
                    onOpenEvidence={() =>
                      openEvidence({
                        title: "Geographic Concentration & Chi-Square Test",
                        phase: "Phase 3 EDA & Phase 4 H6",
                        dataset: "Analytics Jobs (N=15,841)",
                        sampleSize: "N = 15,841 requisitions",
                        method: "Chi-square test of independence (Chi² = 246.8, p < 0.001) and post-hoc pairwise z-tests with FDR correction.",
                        interpretation: "Geographic location strongly predicts salary tier. Candidates outside the top-3 metro clusters face a significant wage penalty unless targeting remote positions.",
                        limitation: "Cross-sectional data does not normalize for regional cost-of-living differences (e.g. Bengaluru housing costs vs Tier-2 cities).",
                      })
                    }
                  />
                </ChartCard>

                {/* 4. Experience vs Compensation OLS */}
                <ChartCard
                  title="Experience Elasticity vs Salary Gradient (OLS Regression)"
                  subtitle="Fitted linear slope demonstrating empirical salary gains per year of professional experience"
                  badge={<Badge variant="outline" className="text-[10px]">Phase 4 H5</Badge>}
                >
                  <RegressionChartVisual
                    slopeBeta={expComp?.linear_slope_beta || 1.9766}
                    intercept={expComp?.linear_intercept || 7.7024}
                    rSquared={expComp?.linear_r_squared || 0.3521}
                    sampleSize={expComp?.sample_size_n || 1602}
                    onOpenEvidence={() =>
                      openEvidence({
                        title: "Experience vs Salary Elasticity (H5 Regression)",
                        phase: "Phase 4: Hypothesis Testing (H5)",
                        dataset: "DataScience Jobs (N=1,602)",
                        sampleSize: "N = 1,602 audited requisitions",
                        method: "Ordinary Least Squares (OLS) with HC3 heteroskedasticity-consistent robust standard errors.",
                        interpretation: "Experience yields a statistically significant linear return of +₹1.98 Lakh per year (beta=1.9766, t=24.76, p=2.25e-135, R²=0.3521). Starting salary intercept is ₹7.70L.",
                        limitation: "OLS assumes linear relationship; exponential acceleration observed beyond 10+ years is better modeled by polynomial or segmented specifications.",
                      })
                    }
                  />
                </ChartCard>
              </div>

              {/* 5. High-Salary Specialized Skills */}
              <ChartCard
                title="Specialized Skill Wage Multipliers: Premium vs Table-Stakes Ratio"
                subtitle="Relative prevalence ratio in upper-bracket salaries (>₹15L) compared to baseline postings"
                badge={<Badge variant="outline" className="text-[10px]">Phase 3 EDA</Badge>}
              >
                <BarChartVisual
                  unitLabel="Relative Prevalence Ratio"
                  items={premiumSkills.map((s) => ({
                    label: s.skill_name,
                    value: s.relative_prevalence_ratio,
                    secondaryValue: `High: ${s.prevalence_in_high_salary_pct}% vs Low: ${s.prevalence_in_non_high_salary_pct}%`,
                    unit: "x ratio",
                    highlight: s.relative_prevalence_ratio > 2.0,
                    color: s.relative_prevalence_ratio > 2.0 ? "teal" : s.relative_prevalence_ratio > 1.2 ? "indigo" : "amber",
                  }))}
                  meaning="Data Science (2.75x), R (2.56x), Spark (2.18x), and Machine Learning (2.15x) are massive premium wage multipliers. Conversely, SQL (0.96x) and Excel (0.81x) are table-stakes: universally required, but conferring zero wage premium alone."
                  onOpenEvidence={() =>
                    openEvidence({
                      title: "Skill Salary Wage Differentiation Ratios",
                      phase: "Phase 3: Exploratory Data Analysis",
                      dataset: "Analytics Jobs (N=15,841)",
                      sampleSize: "N = 15,841 postings",
                      method: "Relative prevalence ratio computed as % prevalence in high-salary band (>₹15L) divided by % prevalence in baseline band (<₹15L).",
                      interpretation: "Reveals the Asymmetric Dual-Currency talent paradox: procedural skills grant market entry, while specialized and modeling skills unlock upper-quartile salary bands.",
                      limitation: "Prevalence based on keyword mentions; does not measure depth of expertise or portfolio quality.",
                    })
                  }
                />
              </ChartCard>
            </div>
          )}

          {/* TAB 2: SKILLS INTELLIGENCE */}
          {activeTab === "skills" && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Skill Frequency */}
                <ChartCard
                  title="Empirical Skill Frequency Across 15,841 Requisitions"
                  subtitle="Absolute count and percentage prevalence of technical skills demanded by employers"
                  badge={<Badge variant="outline" className="text-[10px]">Phase 3 EDA</Badge>}
                >
                  <BarChartVisual
                    unitLabel="Demand Prevalence (%)"
                    maxValue={8.0}
                    items={skillFreq.slice(0, 10).map((s) => ({
                      label: s.skill_name,
                      value: s.prevalence_pct,
                      secondaryValue: `${s.frequency_count.toLocaleString()} postings`,
                      unit: "%",
                      category: s.domain_category.split("/")[0],
                      color: s.domain_category.includes("SQL") || s.domain_category.includes("Programming") ? "indigo" : "teal",
                    }))}
                    meaning="SQL (5.78%), Analytics (5.71%), and Python (5.30%) represent the non-negotiable tripartite baseline of the Indian analytics labor market."
                    onOpenEvidence={() =>
                      openEvidence({
                        title: "Macro Technical Skill Frequency Distribution",
                        phase: "Phase 3: Exploratory Data Analysis",
                        dataset: "Analytics Jobs (N=15,841)",
                        sampleSize: "N = 15,841 postings",
                        method: "Tokenized keyword matching against audited domain dictionary with deduplication.",
                        interpretation: "SQL and Python are ubiquitous table stakes required by nearly all employers regardless of sector.",
                        limitation: "Does not capture newer niche frameworks not represented in the audited dictionary.",
                      })
                    }
                  />
                </ChartCard>

                {/* Skill Ranking by Category */}
                <ChartCard
                  title="Domain Category Prevalence Breakdown"
                  subtitle="Relative distribution of required skills grouped by functional technical discipline"
                  badge={<Badge variant="outline" className="text-[10px]">Phase 3 Synthesis</Badge>}
                >
                  <BarChartVisual
                    unitLabel="Keyword Frequency"
                    items={[
                      { label: "Programming & Languages (Python, R, Java)", value: 2221, unit: "mentions", color: "teal" },
                      { label: "Foundational Analytics (Data & Business Analysis)", value: 2155, unit: "mentions", color: "indigo" },
                      { label: "Business & Domain (Finance, Sales, Marketing)", value: 2110, unit: "mentions", color: "amber" },
                      { label: "Database / SQL", value: 915, unit: "mentions", color: "emerald" },
                      { label: "Cloud & Distributed Big Data (Spark, Hadoop)", value: 584, unit: "mentions", color: "indigo" },
                      { label: "BI & Visualization (Excel, Dashboards)", value: 393, unit: "mentions", color: "rose" },
                    ]}
                    meaning="Core programming and analytical problem-solving dominate hiring requirements, exceeding distributed big data infrastructure by nearly 4 to 1 in entry and mid-tier roles."
                    onOpenEvidence={() =>
                      openEvidence({
                        title: "Functional Skill Domain Distribution",
                        phase: "Phase 3: Exploratory Data Analysis",
                        dataset: "Analytics Jobs (N=15,841)",
                        sampleSize: "N = 15,841 requisitions",
                        method: "Functional taxonomic aggregation across 50 audited skill keys.",
                        interpretation: "Confirms that introductory bootcamps over-emphasizing Hadoop/Spark cluster administration are misaligned with foundational market demand.",
                        limitation: "Category boundaries are defined analytically and some skills span multiple disciplines.",
                      })
                    }
                  />
                </ChartCard>
              </div>

              {/* Premium Salary Signals Comparison */}
              <ChartCard
                title="Premium Salary Signal: Differential Prevalence Analysis"
                subtitle="Absolute percentage point difference in prevalence between top-tier (>₹15L) and entry salary brackets"
                badge={<Badge variant="outline" className="text-[10px]">Phase 3 / H6</Badge>}
              >
                <BarChartVisual
                  unitLabel="Percentage Points Lift (%)"
                  items={premiumSkills.map((s) => ({
                    label: s.skill_name,
                    value: Math.max(s.absolute_difference_pct, 0),
                    secondaryValue: s.absolute_difference_pct < 0 ? `${s.absolute_difference_pct.toFixed(2)}% (Negative Lift)` : `+${s.absolute_difference_pct.toFixed(2)}% lift`,
                    unit: "pts",
                    color: s.absolute_difference_pct > 2.0 ? "teal" : s.absolute_difference_pct > 0.5 ? "indigo" : "amber",
                  }))}
                  meaning="R (+4.45 pts), Machine Learning (+3.44 pts), and SAS (+3.00 pts) show the largest positive prevalence differences in upper-salary roles, while SQL and Excel show negative lift, confirming their status as hygiene factors rather than differentiators."
                  onOpenEvidence={() =>
                    openEvidence({
                      title: "Salary Tier Differential Prevalence Analysis",
                      phase: "Phase 3 EDA & Phase 4 H6",
                      dataset: "Analytics Jobs (N=15,841)",
                      sampleSize: "N = 15,841 postings",
                      method: "Two-sample proportion comparisons between upper-quartile salary (>₹15L) and baseline postings with Benjamini-Hochberg FDR correction.",
                      interpretation: "Empirical proof of the dual-currency skill model: table-stakes skills do not generate wage premiums.",
                      limitation: "Salary bands reflect requisition ranges rather than individual negotiation outcomes.",
                    })
                  }
                />
              </ChartCard>
            </div>
          )}

          {/* TAB 3: JDS MODELING */}
          {activeTab === "jds" && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Model Comparison */}
                <ChartCard
                  title="Phase 5 Benchmark Model Comparison (25 CV Splits)"
                  subtitle="Out-of-sample performance across algorithms with strict small-sample validation (N=139)"
                  badge={<Badge variant="outline" className="text-[10px]">Phase 5 ML</Badge>}
                >
                  <ModelComparisonVisual
                    models={jdsModels}
                    championName="Logistic_Regression_L2"
                    cohortTitle="JDS Phase 5"
                    onOpenEvidence={() =>
                      openEvidence({
                        title: "JDS Cross-Validated Algorithm Benchmarks",
                        phase: "Phase 5: Junior Data Scientist Skill Modeling",
                        dataset: "JDS Primary Cohort (N=139)",
                        sampleSize: "N = 139 junior practitioners across 5 skills",
                        method: "Repeated Stratified 5-Fold Cross-Validation repeated 5 times (25 independent validation splits) with fixed seeds.",
                        interpretation: "Logistic Regression L2 achieved champion performance (ROC-AUC = 0.9035, Macro F1 = 0.8506). Regularization prevented overfitting that degraded tree-based models.",
                        limitation: "Sample size of 139 limits the parameter complexity that can be learned without severe variance.",
                      })
                    }
                  />
                </ChartCard>

                {/* Permutation Feature Importance */}
                <ChartCard
                  title="Out-of-Fold Permutation Feature Importance (Skill Drivers)"
                  subtitle="Empirical AUC degradation when feature values are permuted on held-out validation folds"
                  badge={<Badge variant="outline" className="text-[10px]">Phase 5 ML</Badge>}
                >
                  <BarChartVisual
                    unitLabel="AUC Drop (Importance)"
                    items={jdsImportance.map((f) => ({
                      label: (f.feature || "").replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()),
                      value: f.mean_permutation_importance,
                      unit: "drop",
                      highlight: f.importance_rank <= 2,
                      color: f.importance_rank === 1 ? "teal" : f.importance_rank === 2 ? "emerald" : "indigo",
                    }))}
                    meaning="Dashboarding & Storytelling (0.1062) and Mathematics & Statistics (0.0633) are the decisive drivers of promotional salary velocity, far exceeding generic coding (0.0245) and big data (0.0107)."
                    onOpenEvidence={() =>
                      openEvidence({
                        title: "Out-of-Fold Permutation Feature Importance",
                        phase: "Phase 5: Junior Data Scientist Skill Modeling",
                        dataset: "JDS Primary Cohort (N=139)",
                        sampleSize: "N = 139 practitioners",
                        method: "Permutation feature importance computed across 25 cross-validation splits with 10 random shuffles per fold.",
                        interpretation: "Executive storytelling aptitude is the single highest predictor of salary promotion velocity.",
                        limitation: "Measures predictive contribution within the trained pipeline rather than direct experimental intervention.",
                      })
                    }
                  />
                </ChartCard>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Standardized Odds Ratios */}
                <ChartCard
                  title="Champion Logistic L2 Adjusted Odds Ratios"
                  subtitle="Standardized promotional hike odds per 1-standard-deviation increase in skill proficiency"
                  badge={<Badge variant="outline" className="text-[10px]">Phase 5 / H2</Badge>}
                >
                  <BarChartVisual
                    unitLabel="Adjusted Odds Ratio (AOR)"
                    items={jdsOdds.map((o) => ({
                      label: (o.feature || "").replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()),
                      value: o.odds_ratio || 1.0,
                      secondaryValue: `beta = +${(o.standardized_coef_beta || 0).toFixed(2)}`,
                      unit: "x odds",
                      highlight: (o.odds_ratio || 0) > 3.0,
                      color: (o.odds_ratio || 0) > 3.0 ? "teal" : "indigo",
                    }))}
                    meaning="A 1-SD increase in Mathematics & Statistics proficiency multiplies promotion odds by 3.61x; Dashboarding & Storytelling multiplies odds by 3.23x. Coding confers near-neutral odds (1.04x)."
                    onOpenEvidence={() =>
                      openEvidence({
                        title: "Standardized Logistic Odds Ratios (Phase 5 / H2)",
                        phase: "Phase 5 Modeling & Phase 4 H2",
                        dataset: "JDS Primary Cohort (N=139)",
                        sampleSize: "N = 139 practitioners",
                        method: "L2-penalized logistic regression with standardized feature scaling and HC3 standard error estimation.",
                        interpretation: "Demonstrates that promotion decisions in junior roles reward analytical rigor and business communication, treating coding as a baseline commodity.",
                        limitation: "Observational data reflects promotion decisions in a single enterprise talent pool.",
                      })
                    }
                  />
                </ChartCard>

                {/* Simplified 2-Feature Insight */}
                <ChartCard
                  title="Parsimonious 2-Feature Core Model"
                  subtitle="Retaining 96.75% of full discrimination power with a 60% reduction in skill complexity"
                  badge={<Badge variant="outline" className="text-[10px]">Phase 5 Parsimony</Badge>}
                >
                  <SimplifiedInsightVisual
                    reducedData={jdsReduced}
                    pctRetained={96.75}
                    fullAuc={0.9035}
                    reducedAuc={0.8741}
                    onOpenEvidence={() =>
                      openEvidence({
                        title: "Parsimonious 2-Feature Model Evaluation",
                        phase: "Phase 5: Junior Data Scientist Skill Modeling",
                        dataset: "JDS Primary Cohort (N=139)",
                        sampleSize: "N = 139 practitioners",
                        method: "Greedy backward feature selection and parsimony audit comparing 5-feature baseline against reduced 2-feature subset.",
                        interpretation: "Evaluating candidates on Mathematics and Storytelling alone captures 96.75% of total predictive power (ROC-AUC 0.8741 vs 0.9035).",
                        limitation: "Feature reduction is valid for screening prioritization but comprehensive development still benefits from all 5 skills.",
                      })
                    }
                  />
                </ChartCard>
              </div>
            </div>
          )}

          {/* TAB 4: SDS PERSONALITY EVIDENCE */}
          {activeTab === "sds" && (
            <div className="space-y-6">
              {/* Mandatory Ethical Notice Banner */}
              <div className="p-4 rounded-xl border border-amber-300 dark:border-amber-900 bg-amber-50/50 dark:bg-amber-950/20 text-amber-900 dark:text-amber-200 flex items-start space-x-3 text-xs leading-relaxed">
                <AlertTriangle className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" />
                <div>
                  <strong className="font-bold uppercase tracking-wider block mb-0.5">
                    MANDATORY ETHICAL & METHODOLOGICAL GOVERNANCE WARNING:
                  </strong>
                  The personality evidence below represents observational statistical correlations within a senior consulting cohort. Personality traits serve exclusively as diagnostic frameworks for self-reflection and professional mentoring. In strict adherence to InsightPath ethical guidelines, psychometric traits must <span className="underline font-bold">NEVER</span> be used as automated hiring, screening, promotion, or termination filters.
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Big Five Group Differences */}
                <ChartCard
                  title="Big Five Trait Comparisons (High vs Low Success Cohorts)"
                  subtitle="Empirical separation across 85 High Success vs 76 Low Success senior practitioners (Phase 4 H3)"
                  badge={<Badge variant="outline" className="text-[10px]">Phase 4 H3 / SDS</Badge>}
                >
                  <GroupComparisonVisual
                    tests={sdsGroupTests}
                    highSuccessCount={85}
                    lowSuccessCount={76}
                    onOpenEvidence={() =>
                      openEvidence({
                        title: "Big Five Personality Differences (Phase 4 H3)",
                        phase: "Phase 4 Hypothesis Testing & Phase 6 Modeling",
                        dataset: "SDS Cohort (N=161, 152 unique subjects)",
                        sampleSize: "N = 161 (85 High Success, 76 Low Success)",
                        method: "Welch's two-sample t-test, Mann-Whitney U test, Cohen's d effect sizes, and Benjamini-Hochberg FDR control.",
                        interpretation: "Conscientiousness (+17.95 pts, d=1.85, p<0.001) and Openness (+15.18 pts, d=1.80, p<0.001) exhibit large separations. Neuroticism shows zero significant difference (d=-0.01, p=0.941).",
                        limitation: "Observational evidence from a senior advisory setting; must never be applied deterministically to individuals.",
                      })
                    }
                  />
                </ChartCard>

                {/* SDS Model Performance */}
                <ChartCard
                  title="Phase 6 Model Benchmarks (Stratified Group K-Fold)"
                  subtitle="Cross-validated performance guarding against duplicate subject leakage across 152 unique subjects"
                  badge={<Badge variant="outline" className="text-[10px]">Phase 6 ML</Badge>}
                >
                  <ModelComparisonVisual
                    models={sdsModels}
                    championName="Logistic_Regression_L2"
                    cohortTitle="SDS Phase 6"
                    onOpenEvidence={() =>
                      openEvidence({
                        title: "SDS Group-Aware Model Validation",
                        phase: "Phase 6: Senior Data Scientist Personality Modeling",
                        dataset: "SDS Cohort (N=161, 152 unique subjects)",
                        sampleSize: "N = 161 observations across 152 subjects",
                        method: "StratifiedGroupKFold on Subject ID ensuring zero cross-fold subject leakage.",
                        interpretation: "Logistic Regression L2 achieved 0.9699 ROC-AUC and 92.68% accuracy, demonstrating that delivery rigor and intellectual adaptability separate advisory success.",
                        limitation: "Diagnostic framework for mentoring only; hiring gatekeeping strictly prohibited.",
                      })
                    }
                  />
                </ChartCard>
              </div>

              {/* Personality Odds Ratios */}
              <ChartCard
                title="Champion Logistic L2 Personality Adjusted Odds Ratios"
                subtitle="Standardized odds of top consulting performance per 1-SD increase in Big Five traits"
                badge={<Badge variant="outline" className="text-[10px]">Phase 6 / H4</Badge>}
              >
                <BarChartVisual
                  unitLabel="Adjusted Odds Ratio (AOR)"
                  items={sdsOdds.map((o) => ({
                    label: (o.trait_dimension || "").replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()),
                    value: o.adjusted_odds_ratio || 1.0,
                    secondaryValue: `95% CI: [${(o.or_ci_lower_95 || 0).toFixed(1)}, ${(o.or_ci_upper_95 || 0).toFixed(1)}]`,
                    unit: "x odds",
                    highlight: (o.adjusted_odds_ratio || 0) > 7.0,
                    color: (o.adjusted_odds_ratio || 0) > 7.0 ? "teal" : "indigo",
                  }))}
                  meaning="Conscientiousness (AOR = 8.11, 95% CI [6.23, 10.58]) and Openness to Experience (AOR = 7.72, 95% CI [5.58, 10.67]) strongly dominate senior consulting advisory success, underscoring execution discipline and client adaptability."
                  onOpenEvidence={() =>
                    openEvidence({
                      title: "Senior Consulting Adjusted Odds Ratios",
                      phase: "Phase 6 Modeling & Phase 4 H4",
                      dataset: "SDS Cohort (N=161)",
                      sampleSize: "N = 161 practitioners",
                      method: "Standardized L2-regularized logistic regression with Group K-Fold cross-validation.",
                      interpretation: "Reveals that senior consulting leadership requires an abrupt pivot from pure code to delivery rigor and client empathy.",
                      limitation: "Personality scores reflect self-assessment inventories in professional coaching contexts.",
                    })
                  }
                />
              </ChartCard>
            </div>
          )}

          {/* TAB 5: FRAMEWORK & ACTIONS */}
          {activeTab === "framework" && (
            <div className="space-y-6">
              {/* Four Quadrant Matrix */}
              <ChartCard
                title="Four-Quadrant Career-Readiness Talent Matrix"
                subtitle="Cross-dataset classification synthesized from JDS skill rules and SDS behavioral leaves"
                badge={<Badge variant="outline" className="text-[10px]">Phase 8 Framework</Badge>}
              >
                <QuadrantMatrixVisual
                  quadrants={talentMatrix}
                  onOpenEvidence={() =>
                    openEvidence({
                      title: "Four-Quadrant Talent Matrix Synthesis",
                      phase: "Phase 8: Career-Readiness Framework",
                      dataset: "Synthesized from JDS (N=139) & SDS (N=161)",
                      sampleSize: "N = 300 total practitioners",
                      method: "CART decision rule mapping intersecting technical execution thresholds with behavioral agility.",
                      interpretation: "Explains the career stagnation risk of pure execution specialists (Q2) and outlines concrete transition paths toward strategic impact (Q1).",
                      limitation: "Quadrants are conceptual diagnostic archetypes; candidates exhibit continuous profiles.",
                    })
                  }
                />
              </ChartCard>

              {/* Career Progression Stages */}
              <ChartCard
                title="Four-Tier Empirical Career Progression Roadmap"
                subtitle="Stage-specific competency priorities, why they matter, actions, and measurable success KPIs"
                badge={<Badge variant="outline" className="text-[10px]">Phase 8 Framework</Badge>}
              >
                <CareerRoadmapVisual
                  stages={careerStages}
                  onOpenEvidence={() =>
                    openEvidence({
                      title: "Empirical Career Stage Framework",
                      phase: "Phase 8: Career-Readiness Framework",
                      dataset: "Cross-dataset synthesis across all 4 datasets",
                      sampleSize: "N = 17,443 postings & 300 practitioners",
                      method: "Multi-cohort evidence synthesis establishing required competencies and KPIs by career stage.",
                      interpretation: "Defines actionable development milestones from early syntactic mastery through executive advisory leadership.",
                      limitation: "Progression velocity varies by organization size, industry vertical, and geography.",
                    })
                  }
                />
              </ChartCard>

              {/* Stakeholder Action Blueprints */}
              <ChartCard
                title="Synthesized Stakeholder Action Blueprints (ACT-1 to ACT-5)"
                subtitle="Evidence-based policy and curriculum recommendations for students, universities, mentors, and employers"
                badge={<Badge variant="outline" className="text-[10px]">Phase 8 Actions</Badge>}
              >
                <div className="space-y-3">
                  {stakeholders.map((act) => (
                    <div
                      key={act.action_id}
                      className="p-4 rounded-xl border border-slate-200/70 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-2 hover:border-slate-300 dark:hover:border-slate-700 transition-all"
                    >
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <div className="flex items-center space-x-2">
                          <Badge className="bg-teal-500/10 text-teal-600 dark:text-teal-400 border-teal-500/20 font-mono text-xs">
                            {act.action_id}
                          </Badge>
                          <h4 className="text-xs sm:text-sm font-bold text-slate-900 dark:text-slate-100">
                            {act.recommendation_area}
                          </h4>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Badge variant="outline" className="text-[11px] font-mono text-indigo-600 dark:text-indigo-400 border-indigo-500/30">
                            {act.target_stakeholder}
                          </Badge>
                          <Badge
                            className={`text-[10px] font-mono ${
                              act.priority === "Immediate" || act.priority === "Mandatory"
                                ? "bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/20"
                                : "bg-teal-500/10 text-teal-600 dark:text-teal-400 border-teal-500/20"
                            }`}
                          >
                            {act.priority}
                          </Badge>
                        </div>
                      </div>

                      <p className="text-xs text-slate-700 dark:text-slate-300 font-medium leading-relaxed">
                        <strong>Action: </strong>{act.recommended_action}
                      </p>

                      <div className="pt-2 border-t border-slate-100 dark:border-slate-800/80 text-[11px] text-slate-500 dark:text-slate-400 flex items-center space-x-1.5 font-mono">
                        <Award className="w-3.5 h-3.5 text-teal-500 shrink-0" />
                        <span>Supporting Evidence: {act.supporting_evidence}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </ChartCard>
            </div>
          )}
        </main>
      </div>

      {/* Universal Evidence Drawer / Modal */}
      <EvidenceModal
        isOpen={isEvidenceOpen}
        onClose={() => setIsEvidenceOpen(false)}
        evidence={selectedEvidence}
      />

      <Footer />
    </div>
  );
}

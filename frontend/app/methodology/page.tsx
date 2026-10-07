"use client";

import React, { useState } from "react";
import {
  FileCheck2,
  ShieldCheck,
  Search,
  Sparkles,
  Terminal,
} from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const HYPOTHESES_DECISIONS = [
  {
    id: "H1",
    hypothesis: "Technical skill ratings are significantly higher for Junior Data Scientists with high salary hikes.",
    tests: "Mann-Whitney U, t-test, Benjamini-Hochberg FDR",
    sample: "N = 139 (Primary), N = 137 (Sensitivity)",
    empiricalResult: "Storytelling (d = 1.32, p < 0.001) and Maths/Stats (d = 1.22, p < 0.001) strongly differentiate hike outcomes. Coding (d = 0.21) shows negligible difference.",
    decision: "Supported (Storytelling & Math)",
    verdictType: "supported",
  },
  {
    id: "H2",
    hypothesis: "Technical skill dimensions have unequal independent associations with salary hike in multivariable models.",
    tests: "Multivariable Logistic Regression (L2), VIF diagnostics",
    sample: "N = 139 (Primary)",
    empiricalResult: "Storytelling (AOR = 3.23, p = 0.003) and Maths/Stats (AOR = 3.65, p = 0.001) dominate. Big Data (AOR = 0.94, p = 0.866) and Coding (AOR = 1.04, p = 0.925) have no marginal lift.",
    decision: "Supported (Unequal Weights)",
    verdictType: "supported",
  },
  {
    id: "H3",
    hypothesis: "Big Five personality traits differ significantly between high and low success Senior Data Scientists.",
    tests: "Mann-Whitney U, Benjamini-Hochberg FDR",
    sample: "N = 161 (Primary), N = 152 (Deduplicated)",
    empiricalResult: "Conscientiousness (d = 1.85, p < 0.001), Openness (d = 1.80, p < 0.001), and Extraversion (d = 1.13, p < 0.001) are dramatically elevated in high performers.",
    decision: "Supported (3 Dimensions)",
    verdictType: "supported",
  },
  {
    id: "H4",
    hypothesis: "Conscientiousness/Extraversion positively associate, and Neuroticism negatively associates, with senior success.",
    tests: "Multivariable Logistic Regression (L2), Permutation Importance",
    sample: "N = 161, 25 Group-KFold splits",
    empiricalResult: "Openness (AOR = 7.72) and Conscientiousness (AOR = 8.11) drive out-of-sample accuracy. Neuroticism exhibits suppressor collinearity with zero out-of-sample predictive importance (0.0005).",
    decision: "Partially Supported / Refined",
    verdictType: "refined",
  },
  {
    id: "H5",
    hypothesis: "Required minimum experience is positively correlated with advertised average salary in job postings.",
    tests: "Spearman rank, Pearson correlation, OLS with HC3 SEs",
    sample: "N = 1,602 (DataScience Jobs)",
    empiricalResult: "Robust positive relationship (r = 0.764, p < 0.001). Salary expands by 1.34L per year of experience (R² = 0.584). Variance widens significantly at senior tiers.",
    decision: "Supported (beta = 1.34L)",
    verdictType: "supported",
  },
  {
    id: "H6",
    hypothesis: "Representation in high-salary brackets is statistically dependent on geographic tech hub and specialized skills.",
    tests: "Chi-square of Independence, Haberman residuals",
    sample: "N = 15,841 (Analytics Jobs)",
    empiricalResult: "Significant dependence on geography (Chi² = 246.8, p < 0.001). Bengaluru, NCR, and Mumbai show high-salary concentrations. Cloud, PyTorch, and NLP command premium odds ratios (> 1.8x).",
    decision: "Supported (Geo + Tech)",
    verdictType: "supported",
  },
];

const PHASE_ROADMAP = [
  { phase: "Phase 0", title: "Analytical Foundation & Architecture", status: "Complete", items: "19 foundation architecture documents, pre-registered hypotheses H1–H6, zero data merge strategy." },
  { phase: "Phase 1", title: "Data Audit & Quality Profiling", status: "Complete", items: "13 tabular profile audits, Tukey IQR outlier checks, duplicate ID audits, missingness scans." },
  { phase: "Phase 2", title: "Data Cleaning & Transformation", status: "Complete", items: "Cryptographic SHA-256 checks, currency string parsers, top-50 multi-hot skills, zero raw modification." },
  { phase: "Phase 3", title: "Purpose-Driven Exploratory Data Analysis", status: "Complete", items: "15 publication figures (300 DPI PNG/SVG), 13 summary tables, empirical elasticity slopes." },
  { phase: "Phase 4", title: "Statistical Analysis & Hypothesis Testing", status: "Complete", items: "Formal hypothesis testing, Benjamini-Hochberg FDR correction, effect size calculations." },
  { phase: "Phase 5", title: "Junior Data Scientist Skill Modeling", status: "Complete", items: "5x5 repeated stratified CV (25 splits), Logistic L2 champion (ROC-AUC 0.9035), odds ratios." },
  { phase: "Phase 6", title: "Senior Data Scientist Personality Modeling", status: "Complete", items: "StratifiedGroupKFold on subject ID (25 splits), Logistic L2 champion (ROC-AUC 0.9699), ethical directive." },
  { phase: "Phase 7", title: "Cross-Dataset Analytical Synthesis", status: "Complete", items: "Methodological Triangulation without row merges, Asymmetric Dual-Currency model, 5 talent gaps." },
  { phase: "Phase 8", title: "Career-Readiness Framework Construction", status: "Complete", items: "Four-Quadrant Talent Matrix (Q1–Q4), 4 stakeholder blueprints (Student, Univ, Mentor, Employer)." },
  { phase: "Phase 9", title: "Final Report & Presentation Assembly", status: "Complete", items: "25-page Round 2 master report (DOCX/MD), 15 widescreen executive presentation slides (PPTX)." },
];

export default function MethodologyPage() {
  const [searchTerm, setSearchTerm] = useState("");

  const filteredHypotheses = HYPOTHESES_DECISIONS.filter(
    (h) =>
      h.hypothesis.toLowerCase().includes(searchTerm.toLowerCase()) ||
      h.empiricalResult.toLowerCase().includes(searchTerm.toLowerCase()) ||
      h.id.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--foreground)]">
      <Navbar />

      <main className="flex-1 py-12 md:py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
          {/* Header */}
          <div className="space-y-3">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-mono font-medium border border-teal-500/30 bg-teal-500/10 text-teal-600 dark:text-teal-400">
              <FileCheck2 className="w-3.5 h-3.5 mr-1" />
              <span>Scientific Governance & Audit Trail</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900 dark:text-slate-50">
              Methodology & Empirical Verification
            </h1>
            <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400 leading-relaxed max-w-3xl">
              InsightPath adheres to strict experimental standards: pre-registered hypotheses, repeated stratified cross-validation, clone-leakage prevention, and multi-lens conceptual synthesis without synthetic merges.
            </p>
          </div>

          {/* Machine Learning Validation Standards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-900/80 p-6 space-y-3">
              <div className="flex items-center space-x-2 text-teal-600 dark:text-teal-400 font-semibold text-xs font-mono uppercase">
                <Terminal className="w-4 h-4" />
                <span>Small-Sample Discipline</span>
              </div>
              <h3 className="text-base font-bold text-slate-900 dark:text-slate-100">
                Parsimony Over Overfitting
              </h3>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                With N = 139 (JDS) and N = 161 (SDS), complex deep networks risk extreme memorization. We deploy regularized Logistic Regression (L2) and constrained decision trees, validating every result over 25 out-of-sample splits.
              </p>
            </Card>

            <Card className="border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-900/80 p-6 space-y-3">
              <div className="flex items-center space-x-2 text-indigo-600 dark:text-indigo-400 font-semibold text-xs font-mono uppercase">
                <ShieldCheck className="w-4 h-4" />
                <span>Clone-Leakage Protection</span>
              </div>
              <h3 className="text-base font-bold text-slate-900 dark:text-slate-100">
                StratifiedGroupKFold on ID
              </h3>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                9 subjects in SDS appear with duplicate rows. Standard CV would allow twin profiles to bleed between train and test. We strictly group splits by subject ID across 5 folds and 5 seeds.
              </p>
            </Card>

            <Card className="border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-900/80 p-6 space-y-3">
              <div className="flex items-center space-x-2 text-emerald-600 dark:text-emerald-400 font-semibold text-xs font-mono uppercase">
                <Sparkles className="w-4 h-4" />
                <span>Multiple Testing Control</span>
              </div>
              <h3 className="text-base font-bold text-slate-900 dark:text-slate-100">
                Benjamini-Hochberg FDR
              </h3>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                To prevent false discovery inflation from multiple pairwise hypothesis comparisons, every p-value was adjusted using the Benjamini-Hochberg False Discovery Rate at alpha = 0.05.
              </p>
            </Card>
          </div>

          {/* Hypotheses Matrix */}
          <div className="space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h2 className="text-xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
                  Pre-Registered Hypotheses Decision Matrix (H1 – H6)
                </h2>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  All 6 hypotheses were pre-registered in Phase 0 before testing in Phase 4 and modeling in Phases 5 & 6.
                </p>
              </div>

              <div className="relative w-full sm:w-64">
                <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  placeholder="Filter hypotheses..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-1 focus:ring-teal-500"
                />
              </div>
            </div>

            <div className="space-y-3">
              {filteredHypotheses.map((h) => (
                <div
                  key={h.id}
                  className="p-5 rounded-xl border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-900/80 space-y-3 hover:border-slate-300 dark:hover:border-slate-700 transition-colors"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex items-center space-x-2">
                      <Badge variant="outline" className="font-mono text-xs font-bold text-teal-600 dark:text-teal-400">
                        {h.id}
                      </Badge>
                      <span className="text-xs font-mono text-slate-500 dark:text-slate-400">
                        {h.sample}
                      </span>
                    </div>
                    <Badge
                      variant={h.verdictType === "supported" ? "default" : "secondary"}
                      className={
                        h.verdictType === "supported"
                          ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 text-xs"
                          : "bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/20 text-xs"
                      }
                    >
                      {h.decision}
                    </Badge>
                  </div>

                  <div>
                    <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-1">
                      {h.hypothesis}
                    </h4>
                    <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                      {h.empiricalResult}
                    </p>
                  </div>

                  <div className="pt-2 border-t border-slate-100 dark:border-slate-800/80 text-[11px] font-mono text-slate-500 dark:text-slate-400">
                    <strong>Statistical Evaluation Method:</strong> {h.tests}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Phase 0 to Phase 9 Roadmap Progress */}
          <div className="space-y-4">
            <div>
              <h2 className="text-xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
                Phases 0–9 Pipeline Architecture
              </h2>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                10-phase sequential execution roadmap completed with zero skips and full reproducibility.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
              {PHASE_ROADMAP.map((p) => (
                <div
                  key={p.phase}
                  className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-1.5"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono font-bold text-teal-600 dark:text-teal-400 text-[11px]">
                      {p.phase}
                    </span>
                    <Badge variant="outline" className="text-[10px] text-emerald-600 dark:text-emerald-400 border-emerald-500/20 bg-emerald-500/10">
                      {p.status}
                    </Badge>
                  </div>
                  <h4 className="font-semibold text-slate-900 dark:text-slate-100 text-xs">
                    {p.title}
                  </h4>
                  <p className="text-slate-500 dark:text-slate-400 text-[11px] leading-relaxed">
                    {p.items}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}

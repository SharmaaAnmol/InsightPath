"use client";

import React from "react";
import { Award, ShieldCheck, Database } from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function AboutPage() {
  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--foreground)]">
      <Navbar />

      <main className="flex-1 py-12 md:py-16">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
          {/* Header */}
          <div className="space-y-3">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-mono font-medium border border-teal-500/30 bg-teal-500/10 text-teal-600 dark:text-teal-400">
              <span>Team RUSTY WOLVES • Project InsightPath</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900 dark:text-slate-50">
              About InsightPath & The SAS CU Hackathon
            </h1>
            <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400 leading-relaxed max-w-3xl">
              InsightPath was created for Round 2 of the SAS CU Hackathon. Our analytical mission is to replace fragmented intuition in data science talent strategy with verified statistical evidence.
            </p>
          </div>

          {/* Evaluation Pillars Rubric */}
          <Card className="border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-900/80 shadow-xs">
            <CardHeader className="border-b border-slate-100 dark:border-slate-800/80 pb-4">
              <div className="flex items-center space-x-2">
                <Award className="w-5 h-5 text-teal-500" />
                <CardTitle className="text-lg">SAS Round 2 Official Evaluation Criteria (100 Marks)</CardTitle>
              </div>
              <CardDescription className="text-xs">
                How our analytical pipeline directly satisfies the hackathon judging rubric.
              </CardDescription>
            </CardHeader>
            <CardContent className="p-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 text-xs">
                <div className="p-3.5 rounded-lg bg-slate-50 dark:bg-slate-950/60 border border-slate-200/60 dark:border-slate-800 space-y-1">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-slate-900 dark:text-slate-100">Problem Definition</span>
                    <Badge variant="outline" className="font-mono text-[10px]">10 Marks</Badge>
                  </div>
                  <p className="text-slate-500 dark:text-slate-400">
                    Pre-registered in Phase 0 across 19 architecture docs and 9 formal Research Questions.
                  </p>
                </div>

                <div className="p-3.5 rounded-lg bg-slate-50 dark:bg-slate-950/60 border border-slate-200/60 dark:border-slate-800 space-y-1">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-slate-900 dark:text-slate-100">Approach Description</span>
                    <Badge variant="outline" className="font-mono text-[10px]">15 Marks</Badge>
                  </div>
                  <p className="text-slate-500 dark:text-slate-400">
                    Methodological Triangulation without row-level joins; strict population boundary governance.
                  </p>
                </div>

                <div className="p-3.5 rounded-lg bg-slate-50 dark:bg-slate-950/60 border border-slate-200/60 dark:border-slate-800 space-y-1">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-slate-900 dark:text-slate-100">Data Exploration</span>
                    <Badge variant="outline" className="font-mono text-[10px]">25 Marks</Badge>
                  </div>
                  <p className="text-slate-500 dark:text-slate-400">
                    Phases 1–3: 13 audit profiles, 15 publication figures (PNG/SVG), 13 tabular matrices.
                  </p>
                </div>

                <div className="p-3.5 rounded-lg bg-slate-50 dark:bg-slate-950/60 border border-slate-200/60 dark:border-slate-800 space-y-1">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-slate-900 dark:text-slate-100">Data Analysis & ML</span>
                    <Badge variant="outline" className="font-mono text-[10px]">30 Marks</Badge>
                  </div>
                  <p className="text-slate-500 dark:text-slate-400">
                    H1–H6 tests with FDR control; 2 champion Logistic L2 pipelines with 25-split repeated CV.
                  </p>
                </div>

                <div className="p-3.5 rounded-lg bg-slate-50 dark:bg-slate-950/60 border border-slate-200/60 dark:border-slate-800 space-y-1">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-slate-900 dark:text-slate-100">Results & Conclusions</span>
                    <Badge variant="outline" className="font-mono text-[10px]">10 Marks</Badge>
                  </div>
                  <p className="text-slate-500 dark:text-slate-400">
                    Asymmetric Dual-Currency model, 5 systemic talent gaps, and 4-tier career stage roadmap.
                  </p>
                </div>

                <div className="p-3.5 rounded-lg bg-slate-50 dark:bg-slate-950/60 border border-slate-200/60 dark:border-slate-800 space-y-1">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-slate-900 dark:text-slate-100">Business Implications</span>
                    <Badge variant="outline" className="font-mono text-[10px]">10 Marks</Badge>
                  </div>
                  <p className="text-slate-500 dark:text-slate-400">
                    Four-Quadrant Talent Matrix and 4 tailored stakeholder blueprints with quantitative KPIs.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Dataset Provenance */}
          <div className="space-y-4">
            <h2 className="text-xl font-bold tracking-tight text-slate-900 dark:text-slate-100 flex items-center space-x-2">
              <Database className="w-5 h-5 text-teal-500" />
              <span>Dataset Provenance & Cryptographic Immutability</span>
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-2">
                <span className="font-semibold text-slate-900 dark:text-slate-100 block">Analytics Jobs (`Analytics Jobs.csv`)</span>
                <p className="text-slate-500 dark:text-slate-400 leading-relaxed">
                  15,841 individual job vacancies across India. Verified SHA-256: <code className="font-mono text-[10px]">c0bfd52e06...</code>
                </p>
              </div>

              <div className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-2">
                <span className="font-semibold text-slate-900 dark:text-slate-100 block">Data Science Jobs (`DataScience Jobs.csv`)</span>
                <p className="text-slate-500 dark:text-slate-400 leading-relaxed">
                  1,602 employer job requisitions. Verified SHA-256: <code className="font-mono text-[10px]">24658523ee...</code>
                </p>
              </div>

              <div className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-2">
                <span className="font-semibold text-slate-900 dark:text-slate-100 block">JDS Skill Traits (`JDS Skill Traits.xlsx`)</span>
                <p className="text-slate-500 dark:text-slate-400 leading-relaxed">
                  139 valid junior data scientists evaluated across 5 dimensions. Verified SHA-256: <code className="font-mono text-[10px]">2dc0a3f070...</code>
                </p>
              </div>

              <div className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-2">
                <span className="font-semibold text-slate-900 dark:text-slate-100 block">SDS Personality Traits (`SDS Personality Traits.xlsx`)</span>
                <p className="text-slate-500 dark:text-slate-400 leading-relaxed">
                  161 senior consultants evaluated across Big Five traits. Verified SHA-256: <code className="font-mono text-[10px]">112a08e50c...</code>
                </p>
              </div>
            </div>
          </div>

          {/* Ethical Directive */}
          <div className="p-6 rounded-xl border border-amber-200/80 dark:border-amber-900/40 bg-amber-50/50 dark:bg-amber-950/20 space-y-2">
            <div className="flex items-center space-x-2 text-amber-700 dark:text-amber-400 font-semibold text-sm">
              <ShieldCheck className="w-4 h-4 text-amber-500" />
              <span>Ethical AI & Psychometric Guardrail Commitment</span>
            </div>
            <p className="text-xs text-amber-800 dark:text-amber-300/80 leading-relaxed">
              In accordance with pre-registered ethical standards (docs/phase0/LIMITATIONS.md and Phase 6 SDS report), personality models reflect behavioral self-awareness and executive presence. They are strictly prohibited from use as automated employment gates, candidate screening filters, or performance termination mechanisms.
            </p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}

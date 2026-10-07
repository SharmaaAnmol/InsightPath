"use client";

import React from "react";
import Link from "next/link";
import {
  ArrowRight,
  Database,
  BarChart3,
  CheckCircle2,
  Cpu,
  BrainCircuit,
  ShieldCheck,
  ChevronRight,
  ExternalLink,
} from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { StatCard } from "@/components/StatCard";
import { EvidenceCard } from "@/components/EvidenceCard";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--foreground)] selection:bg-teal-500/20 selection:text-teal-400">
      <Navbar />

      <main className="flex-1">
        {/* HERO SECTION */}
        <section className="relative pt-20 pb-24 md:pt-28 md:pb-32 overflow-hidden border-b border-slate-200/80 dark:border-slate-800/80">
          <div className="absolute inset-0 bg-grid-pattern opacity-60 pointer-events-none" />
          <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] glow-teal blur-3xl opacity-30 pointer-events-none" />
          <div className="absolute top-1/3 left-1/3 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[300px] glow-indigo blur-3xl opacity-20 pointer-events-none" />

          <div className="relative max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-mono font-medium border border-teal-500/30 bg-teal-500/10 text-teal-600 dark:text-teal-400 backdrop-blur-xs">
              <span className="w-1.5 h-1.5 rounded-full bg-teal-500 animate-pulse" />
              <span>SAS CU Hackathon Round 2 • Team RUSTY WOLVES</span>
            </div>

            <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight text-slate-900 dark:text-white max-w-4xl mx-auto leading-[1.12]">
              Evidence-Based Career Intelligence for{" "}
              <span className="bg-gradient-to-r from-teal-500 via-cyan-400 to-indigo-500 bg-clip-text text-transparent">
                Data Science
              </span>
            </h1>

            <p className="text-base sm:text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto leading-relaxed">
              Moving beyond intuition with 4 triangulated evidence lenses. Analyzing 17,443 job postings, 300 practitioner profiles, and 2 validated machine learning pipelines.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-4">
              <Link href="/dashboard">
                <Button size="lg" className="h-11 px-6 text-sm bg-slate-900 hover:bg-slate-800 dark:bg-teal-500 dark:hover:bg-teal-400 dark:text-slate-950 text-white font-semibold shadow-md group">
                  <span>Explore Dashboard</span>
                  <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Link>
              <Link href="/assessment">
                <Button size="lg" variant="outline" className="h-11 px-6 text-sm border-slate-300 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800/80 font-medium">
                  <Cpu className="w-4 h-4 mr-2 text-teal-500" />
                  <span>Run Career Assessment</span>
                </Button>
              </Link>
              <Link href="/methodology">
                <Button size="lg" variant="ghost" className="h-11 px-4 text-sm text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white">
                  <span>Audit Methodology</span>
                  <ExternalLink className="w-3.5 h-3.5 ml-1.5 text-slate-400" />
                </Button>
              </Link>
            </div>

            {/* KEY PROJECT STATISTICS */}
            <div className="pt-14 grid grid-cols-2 md:grid-cols-4 gap-4 text-left max-w-4xl mx-auto">
              <StatCard
                label="Job Postings Analyzed"
                value="17,443"
                subvalue="15,841 AJ + 1,602 DS"
                trend={{ value: "100% Verified", direction: "up" }}
                badgeText="Macro + Micro"
                color="teal"
              />
              <StatCard
                label="Practitioner Profiles"
                value="300"
                subvalue="139 JDS + 161 SDS"
                trend={{ value: "Valid Samples", direction: "up" }}
                badgeText="Empirical Cohort"
                color="indigo"
              />
              <StatCard
                label="JDS Model ROC-AUC"
                value="0.9035"
                subvalue="Logistic L2 Champion"
                trend={{ value: "+32.8% Lift", direction: "up" }}
                badgeText="25 Repeated Splits"
                color="emerald"
              />
              <StatCard
                label="SDS Model ROC-AUC"
                value="0.9699"
                subvalue="Group-Aware Champion"
                trend={{ value: "+39.9% Lift", direction: "up" }}
                badgeText="Clone-Protected"
                color="teal"
              />
            </div>
          </div>
        </section>

        {/* PROBLEM STATEMENT */}
        <section className="py-20 border-b border-slate-200/80 dark:border-slate-800/80 bg-slate-50/40 dark:bg-slate-950/30">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
            <div className="max-w-3xl space-y-3">
              <div className="inline-flex items-center space-x-1.5 text-xs font-mono uppercase tracking-wider text-teal-600 dark:text-teal-400 font-semibold">
                <span>The Core Dilemma</span>
              </div>
              <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
                Why Data Science Careers Suffer from Fragmented Decisions
              </h2>
              <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
                Aspiring professionals face conflicting signals: employers advertise tool syntax, early promotions reward storytelling and mathematics, and senior consulting success hinges on psychological adaptability.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card className="border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-900/70 p-6 space-y-3">
                <div className="w-8 h-8 rounded-lg bg-rose-500/10 text-rose-500 border border-rose-500/20 flex items-center justify-center font-mono font-bold text-sm">
                  01
                </div>
                <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100">
                  The Coding Saturation Trap
                </h3>
                <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                  Coding skills are universally high across junior practitioners (Cohen&apos;s d = 0.21, AOR = 1.04). Code fluency gets candidates through the door, but provides zero marginal promotion advantage.
                </p>
              </Card>

              <Card className="border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-900/70 p-6 space-y-3">
                <div className="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-500 border border-amber-500/20 flex items-center justify-center font-mono font-bold text-sm">
                  02
                </div>
                <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100">
                  The Big Data Illusion
                </h3>
                <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                  Big Data keywords appear in 44.9% of postings, yet show zero predictive association with early-career salary hikes (AOR = 0.94, p = 0.866). Candidates over-invest in infrastructure rather than narrative impact.
                </p>
              </Card>

              <Card className="border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-900/70 p-6 space-y-3">
                <div className="w-8 h-8 rounded-lg bg-teal-500/10 text-teal-500 border border-teal-500/20 flex items-center justify-center font-mono font-bold text-sm">
                  03
                </div>
                <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100">
                  The Senior Behavioral Shock
                </h3>
                <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                  Senior customer-facing success shifts completely away from syntax to Openness to Experience (AOR = 7.72) and Conscientiousness (AOR = 8.11). Technical experts without coaching hit an executive plateau.
                </p>
              </Card>
            </div>
          </div>
        </section>

        {/* HOW INSIGHTPATH WORKS (THE 4 LENSES) */}
        <section className="py-20 border-b border-slate-200/80 dark:border-slate-800/80">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
            <div className="text-center max-w-2xl mx-auto space-y-2">
              <span className="text-xs font-mono uppercase tracking-wider text-teal-600 dark:text-teal-400 font-semibold">
                Methodological Triangulation
              </span>
              <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
                Four Complementary Evidence Layers
              </h2>
              <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400">
                Zero row-level joins. Zero synthetic leakage. We integrate distinct populations conceptually through structured synthesis matrices.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="p-5 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-3">
                <div className="flex items-center justify-between">
                  <Badge variant="outline" className="text-[10px] font-mono">Layer 1 • Macro</Badge>
                  <Database className="w-4 h-4 text-teal-500" />
                </div>
                <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100">DataScience Jobs</h3>
                <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                  1,602 employer requisitions across 642 organizations. Maps role hierarchies, experience thresholds, and compensation envelopes (beta = 1.34L/yr).
                </p>
              </div>

              <div className="p-5 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-3">
                <div className="flex items-center justify-between">
                  <Badge variant="outline" className="text-[10px] font-mono">Layer 2 • Micro</Badge>
                  <BarChart3 className="w-4 h-4 text-indigo-500" />
                </div>
                <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100">Analytics Jobs</h3>
                <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                  15,841 individual vacancies. Mines top-50 skills, regional talent hubs (Bengaluru, NCR, Mumbai = 68.5%), and categorical salary brackets.
                </p>
              </div>

              <div className="p-5 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-3">
                <div className="flex items-center justify-between">
                  <Badge variant="outline" className="text-[10px] font-mono">Layer 3 • Junior</Badge>
                  <Cpu className="w-4 h-4 text-cyan-500" />
                </div>
                <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100">JDS Skill Traits</h3>
                <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                  139 junior practitioners. Evaluates 5 technical dimensions against salary-hike classification. Storytelling (AOR = 3.23) and Math (AOR = 3.65) dominate.
                </p>
              </div>

              <div className="p-5 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-3">
                <div className="flex items-center justify-between">
                  <Badge variant="outline" className="text-[10px] font-mono">Layer 4 • Senior</Badge>
                  <BrainCircuit className="w-4 h-4 text-amber-500" />
                </div>
                <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100">SDS Personality Traits</h3>
                <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                  161 senior consultants. Models Big Five traits against consulting success. Group-aware CV proves Openness and Conscientiousness drive out-of-sample accuracy.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* EVIDENCE CARDS PREVIEW */}
        <section className="py-20 border-b border-slate-200/80 dark:border-slate-800/80 bg-slate-50/40 dark:bg-slate-950/30">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
            <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
              <div className="space-y-1">
                <span className="text-xs font-mono uppercase tracking-wider text-teal-600 dark:text-teal-400 font-semibold">
                  Pre-Registered Empirical Proof
                </span>
                <h2 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
                  Key Statistical Findings
                </h2>
              </div>
              <Link href="/methodology" className="text-xs font-semibold text-teal-600 dark:text-teal-400 hover:underline flex items-center">
                <span>View All Pre-Registered Hypotheses</span>
                <ChevronRight className="w-3.5 h-3.5 ml-1" />
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <EvidenceCard
                hypothesisId="H1 / H2"
                claim="Storytelling is the #1 Early-Career Differentiator"
                finding="Junior Data Scientists with high salary hikes scored significantly higher in Storytelling (Cohen's d = 1.32, p < 0.001) and Mathematics (d = 1.22)."
                datasetName="JDS Skill Traits"
                sampleSize="N = 139"
                metric="AOR = 3.23 (p = 0.003)"
                verdict="Supported"
                implication="Narrative framing out-earns raw syntax."
              />

              <EvidenceCard
                hypothesisId="H3 / H4"
                claim="Openness & Conscientiousness Drive Senior Leadership"
                finding="Senior consulting success is strongly predicted by Openness to Experience (AOR = 7.72) and Conscientiousness (AOR = 8.11) with 96.99% ROC-AUC."
                datasetName="SDS Personality Traits"
                sampleSize="N = 161"
                metric="ROC-AUC = 0.9699"
                verdict="Supported"
                implication="Intellectual agility creates executive presence."
              />

              <EvidenceCard
                hypothesisId="H5 / H6"
                claim="Experience Elasticity Expands Salary Variance"
                finding="Advertised average salary increases linearly by 1.34L per year of experience (R² = 0.584), but salary spread widens substantially beyond 8 years."
                datasetName="DataScience Jobs"
                sampleSize="N = 1,602"
                metric="beta = 1.34L (p < 0.001)"
                verdict="Supported"
                implication="Senior compensation decouples into elite bands."
              />
            </div>
          </div>
        </section>

        {/* METHODOLOGY CREDIBILITY SECTION */}
        <section className="py-20 border-b border-slate-200/80 dark:border-slate-800/80">
          <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="p-8 sm:p-10 rounded-2xl border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-900/80 shadow-xs space-y-6">
              <div className="flex items-center space-x-2 text-xs font-mono text-teal-600 dark:text-teal-400 font-semibold uppercase">
                <ShieldCheck className="w-4 h-4 text-teal-500" />
                <span>Analytical Rigor & Ethical Standards</span>
              </div>
              <h3 className="text-xl sm:text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
                Built on Verified Scientific Governance, Not Black-Box Guesswork
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                <div className="flex items-start space-x-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span><strong>Cryptographic Immutability:</strong> Raw datasets preserved byte-for-byte; verified via SHA-256 before and after pipeline execution.</span>
                </div>
                <div className="flex items-start space-x-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span><strong>Clone-Leakage Mitigation:</strong> SDS model uses 25 Group-KFold splits grouped by subject ID to prevent identical subject bleed.</span>
                </div>
                <div className="flex items-start space-x-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span><strong>Multiple Testing Control:</strong> Benjamini-Hochberg FDR applied across all p-value sets to prevent false discovery inflation.</span>
                </div>
                <div className="flex items-start space-x-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span><strong>Mandatory Ethical Guardrail:</strong> Big Five personality models prohibited from automated hiring, termination, or screening gates.</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA SECTION */}
        <section className="py-24 text-center">
          <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
            <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900 dark:text-white">
              Ready to Explore Market-Calibrated Career Intelligence?
            </h2>
            <p className="text-sm text-slate-600 dark:text-slate-400 max-w-xl mx-auto leading-relaxed">
              Access the interactive dashboard, explore the 4-Quadrant Talent Matrix, and run diagnostic assessments calibrated against validated hackathon benchmarks.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
              <Link href="/dashboard">
                <Button size="lg" className="h-11 px-8 text-sm bg-slate-900 hover:bg-slate-800 dark:bg-teal-500 dark:hover:bg-teal-400 dark:text-slate-950 text-white font-semibold shadow-md">
                  Launch Platform Dashboard
                </Button>
              </Link>
              <Link href="/roadmap">
                <Button size="lg" variant="outline" className="h-11 px-6 text-sm border-slate-300 dark:border-slate-700">
                  Inspect Stakeholder Blueprints
                </Button>
              </Link>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}

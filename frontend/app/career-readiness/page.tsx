"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Grid, ArrowRight } from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

const QUADRANTS = [
  {
    id: "Q1",
    name: "Advanced Career-Ready",
    technicalCriteria: "Technical Execution ≥ 3.8 / 5.0",
    behavioralCriteria: "Business / Adaptive ≥ 45.0 / 68.0",
    profile: "Balanced high performer combining mathematical execution with narrative clarity and intellectual adaptability.",
    compensationTier: "Velocity to Leadership (18L - 35L+)",
    transitionIntervention: "Executive presence coaching, enterprise system architecture, client portfolio ownership.",
    risk: "Burnout or retention competition.",
    color: "emerald",
  },
  {
    id: "Q2",
    name: "Pure Execution Specialist",
    technicalCriteria: "Technical Execution ≥ 3.8 / 5.0",
    behavioralCriteria: "Business / Adaptive < 45.0 / 68.0",
    profile: "Strong code and pipeline builder vulnerable to promotion plateaus due to storytelling and stakeholder communication deficits.",
    compensationTier: "Standard Market Floor (8.5L - 16L)",
    transitionIntervention: "Storytelling immersion, executive presentation rehearsals, client shadowing.",
    risk: "Stagnation at mid-career tiers due to inability to defend analytical decisions.",
    color: "indigo",
  },
  {
    id: "Q3",
    name: "Strategic Facilitator",
    technicalCriteria: "Technical Execution < 3.8 / 5.0",
    behavioralCriteria: "Business / Adaptive ≥ 45.0 / 68.0",
    profile: "Exceptional stakeholder empathy and presentation presence requiring technical and mathematical foundations to evaluate complex models.",
    compensationTier: "Consulting & Product Track (12L - 22L)",
    transitionIntervention: "Applied mathematical modeling bootcamps, SQL query optimization, experimental design.",
    risk: "Vulnerable to technical credibility loss with engineering teams.",
    color: "cyan",
  },
  {
    id: "Q4",
    name: "Foundational Risk",
    technicalCriteria: "Technical Execution < 3.8 / 5.0",
    behavioralCriteria: "Business / Adaptive < 45.0 / 68.0",
    profile: "Early-stage candidate requiring structured interventions across both technical execution and business narrative framing.",
    compensationTier: "Entry Tier (4.5L - 8.5L)",
    transitionIntervention: "Dual-currency foundation plan: SQL/Python mastery alongside structured project defense presentations.",
    risk: "High ATS filtering attrition and low initial interview conversion.",
    color: "amber",
  },
];

const CAREER_STAGES = [
  {
    stage: "Stage 1: Entry Tier",
    experienceRange: "0 – 2 Years",
    salaryBand: "4.5L – 8.5L",
    coreDeliverable: "Data Extraction & Script Execution",
    dominantCurrencies: "SQL, Python, Excel, Basic Visualization",
    keyTransitionBarrier: "Breaking out of passive coding tickets into business problem formulation.",
  },
  {
    stage: "Stage 2: Velocity Tier",
    experienceRange: "3 – 5 Years",
    salaryBand: "8.5L – 16.0L",
    coreDeliverable: "Narrative Analytics & Applied Modeling",
    dominantCurrencies: "Storytelling (AOR=3.23), Maths/Stats (AOR=3.65), Cloud ML",
    keyTransitionBarrier: "The Coding Saturation Trap: realizing code alone no longer wins promotion.",
  },
  {
    stage: "Stage 3: Expansion Tier",
    experienceRange: "6 – 9 Years",
    salaryBand: "16.0L – 28.0L",
    coreDeliverable: "End-to-End System Scoping & Cross-Functional Translation",
    dominantCurrencies: "System Design, Stakeholder Persuasion, Conscientiousness",
    keyTransitionBarrier: "Managing ambiguity and framing ROI for executive sponsors.",
  },
  {
    stage: "Stage 4: Leadership Tier",
    experienceRange: "10+ Years",
    salaryBand: "28.0L – 45.0L+",
    coreDeliverable: "Organizational AI Strategy & Client Trust",
    dominantCurrencies: "Openness to Experience (AOR=7.72), Conscientiousness (AOR=8.11)",
    keyTransitionBarrier: "Technical dogma: letting go of tool preferences to solve high-stakes business needs.",
  },
];

export default function CareerReadinessPage() {
  const [selectedQuadrant, setSelectedQuadrant] = useState("Q1");

  const currentQ = QUADRANTS.find((q) => q.id === selectedQuadrant) || QUADRANTS[0];

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--foreground)]">
      <Navbar />

      <main className="flex-1 py-12 md:py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
          {/* Header */}
          <div className="space-y-3">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-mono font-medium border border-teal-500/30 bg-teal-500/10 text-teal-600 dark:text-teal-400">
              <Grid className="w-3.5 h-3.5 mr-1" />
              <span>Phase 8 Career-Readiness Framework</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900 dark:text-slate-50">
              Four-Quadrant Talent Matrix & Progression Roadmap
            </h1>
            <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400 leading-relaxed max-w-3xl">
              An operational diagnostic mapping technical execution against business narrative & adaptive consulting presence. Enables personalized intervention strategies across all 4 career stages.
            </p>
          </div>

          {/* Quadrant Interactive Explorer */}
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h2 className="text-xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
                  The Four-Quadrant Talent Matrix
                </h2>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  Select a quadrant to inspect empirical thresholds, compensation envelopes, and transition pathways.
                </p>
              </div>

              <div className="flex space-x-2">
                {QUADRANTS.map((q) => (
                  <button
                    key={q.id}
                    onClick={() => setSelectedQuadrant(q.id)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-bold font-mono transition-all border ${
                      selectedQuadrant === q.id
                        ? "bg-teal-500 text-slate-950 border-teal-500 shadow-xs"
                        : "bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-400 border-slate-200 dark:border-slate-800 hover:border-slate-400"
                    }`}
                  >
                    {q.id}
                  </button>
                ))}
              </div>
            </div>

            {/* Matrix Visual Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {QUADRANTS.map((q) => {
                const isSelected = selectedQuadrant === q.id;
                return (
                  <div
                    key={q.id}
                    onClick={() => setSelectedQuadrant(q.id)}
                    className={`cursor-pointer p-5 rounded-xl border transition-all duration-200 space-y-3 ${
                      isSelected
                        ? "border-teal-500 ring-2 ring-teal-500/20 bg-teal-50/20 dark:bg-teal-950/20 shadow-md"
                        : "border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-900/70 hover:border-slate-300 dark:hover:border-slate-700"
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="space-y-0.5">
                        <span className="font-mono text-xs font-bold text-teal-600 dark:text-teal-400">
                          Quadrant {q.id}
                        </span>
                        <h3 className="text-base font-bold text-slate-900 dark:text-slate-100">
                          {q.name}
                        </h3>
                      </div>
                      <Badge variant="outline" className="text-[10px] font-mono">
                        {q.compensationTier.split(" ")[0]}
                      </Badge>
                    </div>

                    <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                      {q.profile}
                    </p>

                    <div className="pt-2 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between text-xs font-mono text-[11px] text-slate-500">
                      <span>{q.technicalCriteria}</span>
                      <span>•</span>
                      <span>{q.behavioralCriteria}</span>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Selected Quadrant Detailed Breakdown */}
            <div className="p-6 rounded-2xl border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-900/90 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
                <div className="flex items-center space-x-2">
                  <Badge className="bg-teal-500 text-slate-950 font-bold font-mono">
                    {currentQ.id}
                  </Badge>
                  <h3 className="text-lg font-bold text-slate-900 dark:text-slate-50">
                    {currentQ.name} Deep Dive
                  </h3>
                </div>
                <span className="font-mono text-xs text-teal-600 dark:text-teal-400 font-semibold">
                  Band: {currentQ.compensationTier}
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
                <div className="space-y-3">
                  <h4 className="font-semibold text-slate-900 dark:text-slate-200">
                    Target Development Interventions
                  </h4>
                  <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                    {currentQ.transitionIntervention}
                  </p>
                  <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-950/60 border border-slate-200/80 dark:border-slate-800 text-[11px] space-y-1">
                    <span className="font-semibold text-rose-600 dark:text-rose-400 block">
                      Primary Career Risk:
                    </span>
                    <span className="text-slate-600 dark:text-slate-400">{currentQ.risk}</span>
                  </div>
                </div>

                <div className="space-y-3">
                  <h4 className="font-semibold text-slate-900 dark:text-slate-200">
                    Next Progression Step
                  </h4>
                  <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                    Transitioning to the next career phase requires targeted cultivation of the under-advertised Career Velocity currency (Storytelling + Math/Stats for junior tiers; Openness + Conscientiousness for leadership).
                  </p>
                  <Link href="/roadmap">
                    <Button size="sm" variant="outline" className="text-xs">
                      <span>View Full Stakeholder Action Blueprint</span>
                      <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
                    </Button>
                  </Link>
                </div>
              </div>
            </div>
          </div>

          {/* 4-TIER CAREER PROGRESSION ROADMAP */}
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
                The 4-Tier Career Progression Roadmap
              </h2>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Empirically validated trajectory across 0 to 12+ years of industry experience.
              </p>
            </div>

            <div className="space-y-4">
              {CAREER_STAGES.map((s, idx) => (
                <div
                  key={s.stage}
                  className="p-5 rounded-xl border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-900/80 space-y-3"
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <div className="flex items-center space-x-3">
                      <span className="w-7 h-7 rounded-lg bg-teal-500/10 text-teal-600 dark:text-teal-400 font-mono font-bold text-xs flex items-center justify-center border border-teal-500/20">
                        0{idx + 1}
                      </span>
                      <div>
                        <h4 className="text-sm font-bold text-slate-900 dark:text-slate-100">
                          {s.stage}
                        </h4>
                        <span className="text-[11px] font-mono text-slate-500">
                          {s.experienceRange}
                        </span>
                      </div>
                    </div>
                    <Badge variant="outline" className="font-mono text-xs text-teal-600 dark:text-teal-400 border-teal-500/30">
                      Comp Envelope: {s.salaryBand}
                    </Badge>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2 text-xs">
                    <div className="space-y-0.5">
                      <span className="text-[10px] uppercase font-semibold text-slate-400">Core Deliverable</span>
                      <p className="text-slate-700 dark:text-slate-300 font-medium">{s.coreDeliverable}</p>
                    </div>
                    <div className="space-y-0.5">
                      <span className="text-[10px] uppercase font-semibold text-slate-400">Dominant Currencies</span>
                      <p className="text-teal-600 dark:text-teal-400 font-mono text-[11px]">{s.dominantCurrencies}</p>
                    </div>
                    <div className="space-y-0.5">
                      <span className="text-[10px] uppercase font-semibold text-slate-400">Key Barrier to Break</span>
                      <p className="text-slate-500 dark:text-slate-400">{s.keyTransitionBarrier}</p>
                    </div>
                  </div>
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

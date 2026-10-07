"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { Grid, ArrowRight, Award } from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { ChartCard } from "@/components/ChartCard";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { QuadrantMatrixVisual } from "@/components/QuadrantMatrixVisual";
import { EvidenceModal, EvidenceDetail } from "@/components/EvidenceModal";

import {
  fetchTalentMatrix,
  fetchCompetencies,
  TalentMatrixItem,
  CompetencyItem,
} from "@/lib/api";

export default function CareerReadinessPage() {
  const [talentMatrix, setTalentMatrix] = useState<TalentMatrixItem[]>([]);
  const [competencies, setCompetencies] = useState<CompetencyItem[]>([]);

  const [selectedEvidence, setSelectedEvidence] = useState<EvidenceDetail | null>(null);
  const [isEvidenceOpen, setIsEvidenceOpen] = useState(false);

  useEffect(() => {
    Promise.all([
      fetchTalentMatrix(),
      fetchCompetencies(),
    ]).then(([matrixRes, compRes]) => {
      setTalentMatrix(matrixRes.records);
      setCompetencies(compRes.records);
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
              <Grid className="w-3.5 h-3.5 mr-1" />
              <span>Phase 8 Four-Quadrant Career-Readiness Framework</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900 dark:text-slate-50">
              Four-Quadrant Talent Positioning Framework
            </h1>
            <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400 leading-relaxed max-w-3xl">
              An evidence-backed framework derived from CART decision trees and multi-model coefficients. Replaces subjective career advice with clear diagnostic quadrants, concrete transition interventions, and progression milestones.
            </p>
          </div>

          {/* Quick Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-1">
              <span className="text-[11px] font-mono text-slate-400 uppercase">Q1 Velocity Rate</span>
              <p className="text-xl font-bold text-emerald-600 dark:text-emerald-400">100%</p>
              <p className="text-[11px] text-slate-500">JDS CART Rule 1 (N=45)</p>
            </div>
            <div className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-1">
              <span className="text-[11px] font-mono text-slate-400 uppercase">Q2 Execution Engine</span>
              <p className="text-xl font-bold text-indigo-600 dark:text-indigo-400">66-82%</p>
              <p className="text-[11px] text-slate-500">Salary Velocity Drop</p>
            </div>
            <div className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-1">
              <span className="text-[11px] font-mono text-slate-400 uppercase">Storytelling AOR</span>
              <p className="text-xl font-bold text-teal-600 dark:text-teal-400">3.23x</p>
              <p className="text-[11px] text-slate-500">Top Salary Hike Odds</p>
            </div>
            <div className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-1">
              <span className="text-[11px] font-mono text-slate-400 uppercase">Openness AOR</span>
              <p className="text-xl font-bold text-amber-600 dark:text-amber-400">7.72x</p>
              <p className="text-[11px] text-slate-500">Consulting Success Odds</p>
            </div>
          </div>

          {/* Interactive Four-Quadrant Visual */}
          <ChartCard
            title="Interactive Four-Quadrant Talent Positioning Matrix"
            subtitle="Explore empirical profiles, cohort observations, positioning, and developmental priorities"
            badge={<Badge variant="outline" className="text-[10px]">Phase 8 Framework</Badge>}
          >
            <QuadrantMatrixVisual
              quadrants={talentMatrix}
              onOpenEvidence={() =>
                openEvidence({
                  title: "Four-Quadrant Matrix Decision Tree Synthesis",
                  phase: "Phase 8: Career-Readiness Framework",
                  dataset: "Synthesized from JDS (N=139) & SDS (N=161)",
                  sampleSize: "N = 300 total practitioners",
                  method: "CART classification tree rule integration mapping technical modeling thresholds with executive narrative proficiency.",
                  interpretation: "Reveals the mechanism of career stagnation: candidates in Q2 possess strong math and coding skills but stall at mid-tier compensation because they cannot bridge computational results to business decisions.",
                  limitation: "Framework reflects diagnostic archetypes; real practitioner capability exists on a continuum.",
                })
              }
            />
          </ChartCard>

          {/* Competency Priority Hierarchy */}
          <div className="space-y-4">
            <div className="space-y-1">
              <h2 className="text-xl font-bold text-slate-900 dark:text-slate-100 flex items-center space-x-2">
                <Award className="w-5 h-5 text-teal-500" />
                <span>Empirical Competency Priority Hierarchy</span>
              </h2>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Tiered ranking based on observed promotional lift and wage multipliers.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {competencies.map((comp, idx) => (
                <div
                  key={idx}
                  className="p-4 rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 space-y-2 flex flex-col justify-between"
                >
                  <div className="space-y-1.5">
                    <div className="flex items-center justify-between">
                      <Badge
                        variant="outline"
                        className={`text-[10px] font-mono ${
                          comp.priority_tier.includes("Tier 1")
                            ? "border-teal-500/30 text-teal-600 dark:text-teal-400 bg-teal-500/10"
                            : comp.priority_tier.includes("Tier 2")
                            ? "border-indigo-500/30 text-indigo-600 dark:text-indigo-400 bg-indigo-500/10"
                            : "text-slate-400"
                        }`}
                      >
                        {comp.priority_tier.split(":")[0]}
                      </Badge>
                      <span className="text-[11px] font-mono font-bold text-teal-600 dark:text-teal-400">
                        {comp.roi_multiplier.split(" ")[0]} Multiplier
                      </span>
                    </div>
                    <h3 className="text-xs sm:text-sm font-bold text-slate-900 dark:text-slate-100">
                      {comp.competency}
                    </h3>
                    <p className="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed">
                      {comp.rationale}
                    </p>
                  </div>
                  <div className="pt-2 border-t border-slate-100 dark:border-slate-800/80 text-[10px] text-slate-400 font-mono">
                    Target: {comp.target_audience}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Assessment CTA */}
          <div className="p-6 rounded-2xl border border-teal-500/20 bg-linear-to-r from-teal-500/5 via-indigo-500/5 to-transparent flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="space-y-1">
              <h3 className="text-base font-bold text-slate-900 dark:text-slate-100">
                Determine your quadrant positioning today
              </h3>
              <p className="text-xs text-slate-600 dark:text-slate-400">
                Run your skill profile through the validated Phase 5 logistic scoring engine to view your radar gaps and customized roadmap.
              </p>
            </div>
            <Link href="/assessment">
              <Button className="bg-teal-600 hover:bg-teal-500 text-white font-medium text-xs h-9 shrink-0">
                <span>Evaluate My Profile</span>
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

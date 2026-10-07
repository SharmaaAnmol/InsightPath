"use client";

import React, { useState } from "react";
import { Info, HelpCircle, ArrowUpRight, ShieldCheck, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { TalentMatrixItem } from "@/lib/api";

interface QuadrantMatrixVisualProps {
  quadrants: TalentMatrixItem[];
  onOpenEvidence?: () => void;
  className?: string;
}

export function QuadrantMatrixVisual({
  quadrants,
  onOpenEvidence,
  className = "",
}: QuadrantMatrixVisualProps) {
  const [selectedQuadrantId, setSelectedQuadrantId] = useState<string>("Q1");

  const selectedQuad = quadrants.find((q) => q.quadrant_id === selectedQuadrantId) || quadrants[0];

  const quadrantStyles: Record<string, { bg: string; border: string; badge: string; text: string }> = {
    Q1: {
      bg: "bg-emerald-500/10 hover:bg-emerald-500/15",
      border: "border-emerald-500/30",
      badge: "bg-emerald-500/20 text-emerald-700 dark:text-emerald-300",
      text: "text-emerald-700 dark:text-emerald-300",
    },
    Q2: {
      bg: "bg-indigo-500/10 hover:bg-indigo-500/15",
      border: "border-indigo-500/30",
      badge: "bg-indigo-500/20 text-indigo-700 dark:text-indigo-300",
      text: "text-indigo-700 dark:text-indigo-300",
    },
    Q3: {
      bg: "bg-cyan-500/10 hover:bg-cyan-500/15",
      border: "border-cyan-500/30",
      badge: "bg-cyan-500/20 text-cyan-700 dark:text-cyan-300",
      text: "text-cyan-700 dark:text-cyan-300",
    },
    Q4: {
      bg: "bg-amber-500/10 hover:bg-amber-500/15",
      border: "border-amber-500/30",
      badge: "bg-amber-500/20 text-amber-700 dark:text-amber-300",
      text: "text-amber-700 dark:text-amber-300",
    },
  };

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-2">
        <span className="text-[11px] font-mono text-slate-400">
          Four-Quadrant Empirical Talent Matrix (Phase 8 Synthesis)
        </span>
        {onOpenEvidence && (
          <Button
            variant="ghost"
            size="sm"
            onClick={onOpenEvidence}
            className="h-6 text-[11px] text-teal-600 dark:text-teal-400 hover:bg-teal-50 dark:hover:bg-teal-950/40 px-2 py-0"
          >
            <Info className="w-3 h-3 mr-1" />
            Methodology & Evidence
          </Button>
        )}
      </div>

      {/* 2x2 Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {quadrants.map((q) => {
          const style = quadrantStyles[q.quadrant_id] || quadrantStyles.Q1;
          const isSelected = q.quadrant_id === selectedQuadrantId;

          return (
            <div
              key={q.quadrant_id}
              onClick={() => setSelectedQuadrantId(q.quadrant_id)}
              className={`p-4 rounded-xl border cursor-pointer transition-all ${style.bg} ${
                isSelected ? `${style.border} ring-2 ring-teal-500 shadow-md` : "border-slate-200/70 dark:border-slate-800"
              }`}
            >
              <div className="flex items-start justify-between gap-2">
                <div>
                  <div className="flex items-center space-x-2">
                    <span className={`text-xs font-mono font-bold px-2 py-0.5 rounded-md ${style.badge}`}>
                      {q.quadrant_id}
                    </span>
                    <h4 className="text-xs sm:text-sm font-bold text-slate-900 dark:text-slate-100">
                      {q.quadrant_name}
                    </h4>
                  </div>
                  <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-1">
                    {q.market_positioning}
                  </p>
                </div>
                <ArrowUpRight className={`w-4 h-4 shrink-0 ${isSelected ? "text-teal-500" : "text-slate-400"}`} />
              </div>

              <div className="mt-3 pt-2.5 border-t border-slate-200/50 dark:border-slate-800/80 grid grid-cols-2 gap-2 text-[10px] font-mono">
                <div>
                  <span className="text-slate-400 block">Technical:</span>
                  <span className="text-slate-700 dark:text-slate-300 font-medium truncate block">
                    {q.technical_execution_level}
                  </span>
                </div>
                <div>
                  <span className="text-slate-400 block">Behavioral:</span>
                  <span className="text-slate-700 dark:text-slate-300 font-medium truncate block">
                    {q.communication_behavioral_level}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Selected Quadrant Detailed Breakdown */}
      {selectedQuad && (
        <div className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/80 shadow-xs space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-teal-600 dark:text-teal-400 flex items-center space-x-1.5">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Diagnostic Deep-Dive: {selectedQuad.quadrant_id} — {selectedQuad.quadrant_name}</span>
            </h4>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <div className="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-lg border border-slate-200/60 dark:border-slate-800 space-y-1">
              <span className="font-semibold text-slate-700 dark:text-slate-300 block">
                Observed Cohort Behavior:
              </span>
              <p className="text-slate-600 dark:text-slate-400 text-[11px] leading-relaxed">
                {selectedQuad.observed_cohort_behavior}
              </p>
            </div>

            <div className="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-lg border border-slate-200/60 dark:border-slate-800 space-y-1">
              <span className="font-semibold text-teal-700 dark:text-teal-300 block">
                Evidence Development Priority:
              </span>
              <p className="text-slate-600 dark:text-slate-400 text-[11px] leading-relaxed">
                {selectedQuad.development_priority}
              </p>
            </div>
          </div>

          <div className="p-2.5 rounded-lg bg-amber-500/10 border border-amber-300/40 dark:border-amber-900/40 text-[11px] text-amber-800 dark:text-amber-300 flex items-start space-x-1.5">
            <AlertCircle className="w-3.5 h-3.5 text-amber-500 shrink-0 mt-0.5" />
            <div>
              <strong>Risk Profile: </strong>
              {selectedQuad.risk_profile}
            </div>
          </div>
        </div>
      )}

      {/* "What this means" explanation */}
      <div className="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-lg border border-slate-200/60 dark:border-slate-800 flex items-start space-x-2 text-xs text-slate-600 dark:text-slate-400">
        <HelpCircle className="w-4 h-4 text-teal-500 shrink-0 mt-0.5" />
        <div className="leading-relaxed">
          <span className="font-semibold text-slate-800 dark:text-slate-200">What this means: </span>
          The Four-Quadrant Matrix illustrates why technical mastery alone is insufficient for elite compensation velocity. Q2 practitioners face promotional bottlenecks despite high coding skill, while Q1 professionals leverage dual-currency mastery (modeling + executive narrative) to achieve top promotion velocity and premium salary envelopes.
        </div>
      </div>
    </div>
  );
}

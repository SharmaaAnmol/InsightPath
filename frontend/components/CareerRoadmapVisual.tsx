"use client";

import React, { useState } from "react";
import { Info, HelpCircle, CheckCircle2, Award, Layers } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { CareerStageItem } from "@/lib/api";

interface CareerRoadmapVisualProps {
  stages: CareerStageItem[];
  onOpenEvidence?: () => void;
  className?: string;
}

export function CareerRoadmapVisual({
  stages,
  onOpenEvidence,
  className = "",
}: CareerRoadmapVisualProps) {
  const [activeStageId, setActiveStageId] = useState<string>("STAGE-2");

  const activeStage = stages.find((s) => s.stage_id === activeStageId) || stages[0];

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-2">
        <span className="text-[11px] font-mono text-slate-400">
          Four-Tier Empirical Career Progression Framework (Phase 8 Synthesis)
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

      {/* Stage selector bar / timeline */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
        {stages.map((stage) => {
          const isSelected = stage.stage_id === activeStageId;
          return (
            <button
              key={stage.stage_id}
              type="button"
              onClick={() => setActiveStageId(stage.stage_id)}
              className={`p-3 rounded-xl border text-left transition-all ${
                isSelected
                  ? "border-teal-500 bg-teal-50/60 dark:bg-teal-950/30 shadow-xs ring-1 ring-teal-500"
                  : "border-slate-200/70 dark:border-slate-800 bg-white dark:bg-slate-900/50 hover:bg-slate-50 dark:hover:bg-slate-800/40"
              }`}
            >
              <div className="flex items-center justify-between text-[10px] font-mono mb-1">
                <span className={isSelected ? "text-teal-600 dark:text-teal-400 font-bold" : "text-slate-400"}>
                  {stage.stage_id}
                </span>
                <span className="text-slate-400">
                  {stage.stage_name.split("(")[1]?.replace(")", "") || ""}
                </span>
              </div>
              <h4 className="text-xs font-bold text-slate-800 dark:text-slate-200 truncate">
                {stage.stage_name.split("(")[0].trim()}
              </h4>
            </button>
          );
        })}
      </div>

      {/* Active Stage Detailed Card */}
      {activeStage && (
        <div className="p-5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/80 shadow-xs space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 dark:border-slate-800 pb-3">
            <div>
              <div className="text-[11px] font-mono text-teal-600 dark:text-teal-400 font-bold">
                {activeStage.stage_id}
              </div>
              <h3 className="text-base font-bold text-slate-900 dark:text-slate-100">
                {activeStage.stage_name}
              </h3>
            </div>
            <Badge variant="outline" className="text-xs font-mono text-indigo-600 dark:text-indigo-400 border-indigo-500/30">
              Primary: {activeStage.primary_stakeholder}
            </Badge>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div className="space-y-1">
              <span className="font-semibold text-slate-700 dark:text-slate-300 flex items-center space-x-1">
                <Layers className="w-3.5 h-3.5 text-teal-500" />
                <span>Priority Competencies:</span>
              </span>
              <p className="text-slate-600 dark:text-slate-400 bg-slate-50 dark:bg-slate-800/40 p-2.5 rounded-lg border border-slate-200/60 dark:border-slate-800">
                {activeStage.priority_competencies}
              </p>
            </div>

            <div className="space-y-1">
              <span className="font-semibold text-slate-700 dark:text-slate-300 flex items-center space-x-1">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                <span>Why It Matters (Empirical Rationale):</span>
              </span>
              <p className="text-slate-600 dark:text-slate-400 bg-emerald-50/40 dark:bg-emerald-950/20 p-2.5 rounded-lg border border-emerald-200/50 dark:border-emerald-900/30">
                {activeStage.why_it_matters}
              </p>
            </div>
          </div>

          <div className="p-3 bg-indigo-50/40 dark:bg-indigo-950/20 rounded-lg border border-indigo-200/50 dark:border-indigo-900/40 text-xs space-y-1.5">
            <div className="font-semibold text-indigo-900 dark:text-indigo-200 flex items-center space-x-1.5">
              <Award className="w-3.5 h-3.5 text-indigo-500" />
              <span>Recommended Milestone & Measurable Success Indicator:</span>
            </div>
            <p className="text-slate-700 dark:text-slate-300 text-[11px] leading-relaxed">
              <strong>Action: </strong>{activeStage.recommended_development_action}
            </p>
            <p className="text-slate-700 dark:text-slate-300 text-[11px] leading-relaxed">
              <strong>Metric KPI: </strong>{activeStage.measurable_success_indicator}
            </p>
          </div>
        </div>
      )}

      {/* "What this means" explanation */}
      <div className="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-lg border border-slate-200/60 dark:border-slate-800 flex items-start space-x-2 text-xs text-slate-600 dark:text-slate-400">
        <HelpCircle className="w-4 h-4 text-teal-500 shrink-0 mt-0.5" />
        <div className="leading-relaxed">
          <span className="font-semibold text-slate-800 dark:text-slate-200">What this means: </span>
          The four stages document how career value creation shifts systematically from syntactic entry compliance (Stage 1) to salary hike velocity via storytelling and statistical modeling (Stage 2), premium stack differentiation (Stage 3), and advisory leadership adaptability (Stage 4).
        </div>
      </div>
    </div>
  );
}

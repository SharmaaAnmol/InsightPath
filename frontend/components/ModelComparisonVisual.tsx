"use client";

import React, { useState } from "react";
import { Info, HelpCircle, Trophy } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ModelPerformanceItem } from "@/lib/api";

interface ModelComparisonVisualProps {
  models: ModelPerformanceItem[];
  championName: string;
  metricType?: "roc_auc" | "macro_f1" | "accuracy";
  cohortTitle: "JDS Phase 5" | "SDS Phase 6";
  onOpenEvidence?: () => void;
  className?: string;
}

export function ModelComparisonVisual({
  models,
  championName,
  cohortTitle,
  onOpenEvidence,
  className = "",
}: ModelComparisonVisualProps) {
  const [activeMetric, setActiveMetric] = useState<"roc_auc" | "macro_f1" | "accuracy">("roc_auc");

  const getMetricValue = (m: ModelPerformanceItem) => {
    if (activeMetric === "roc_auc") return m.roc_auc_mean;
    if (activeMetric === "macro_f1") return m.macro_f1_mean;
    if (activeMetric === "accuracy") return (m.accuracy_mean || (m.accuracy_pct ? m.accuracy_pct / 100 : 0));
    return m.roc_auc_mean;
  };

  const metricLabel = {
    roc_auc: "ROC-AUC (Discrimination)",
    macro_f1: "Macro F1-Score (Class Balance)",
    accuracy: "Balanced Accuracy",
  }[activeMetric];

  const sortedModels = [...models].sort((a, b) => getMetricValue(b) - getMetricValue(a));

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Metric selection tabs and header */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 dark:border-slate-800 pb-2.5">
        <div className="flex items-center space-x-1 bg-slate-100 dark:bg-slate-800/80 p-0.5 rounded-lg text-xs">
          <button
            type="button"
            onClick={() => setActiveMetric("roc_auc")}
            className={`px-2.5 py-1 rounded-md font-medium transition-all ${
              activeMetric === "roc_auc"
                ? "bg-white dark:bg-slate-900 text-teal-600 dark:text-teal-400 shadow-xs"
                : "text-slate-500 hover:text-slate-800 dark:hover:text-slate-200"
            }`}
          >
            ROC-AUC
          </button>
          <button
            type="button"
            onClick={() => setActiveMetric("macro_f1")}
            className={`px-2.5 py-1 rounded-md font-medium transition-all ${
              activeMetric === "macro_f1"
                ? "bg-white dark:bg-slate-900 text-teal-600 dark:text-teal-400 shadow-xs"
                : "text-slate-500 hover:text-slate-800 dark:hover:text-slate-200"
            }`}
          >
            Macro F1
          </button>
          <button
            type="button"
            onClick={() => setActiveMetric("accuracy")}
            className={`px-2.5 py-1 rounded-md font-medium transition-all ${
              activeMetric === "accuracy"
                ? "bg-white dark:bg-slate-900 text-teal-600 dark:text-teal-400 shadow-xs"
                : "text-slate-500 hover:text-slate-800 dark:hover:text-slate-200"
            }`}
          >
            Accuracy
          </button>
        </div>

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

      {/* Axis context */}
      <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
        <span>Zero-to-1.0 Scale ({metricLabel})</span>
        <span>Baseline Chance = 0.500</span>
      </div>

      {/* Model bars */}
      <div className="space-y-3">
        {sortedModels.map((m, idx) => {
          const val = getMetricValue(m);
          const pct = Math.min(Math.max(val * 100, 0), 100);
          const isChampion =
            m.is_champion ||
            m.model_name.toLowerCase() === championName.toLowerCase() ||
            (m.model_name.toLowerCase().includes("logistic") &&
             m.model_name.toLowerCase().includes("l2"));

          return (
            <div
              key={idx}
              className={`p-3 rounded-xl border transition-all ${
                isChampion
                  ? "border-teal-500/40 bg-teal-500/5 dark:bg-teal-500/10 shadow-xs"
                  : "border-slate-200/70 dark:border-slate-800 bg-white dark:bg-slate-900/60"
              }`}
            >
              <div className="flex items-center justify-between text-xs mb-1.5">
                <div className="flex items-center space-x-2">
                  <span className="font-semibold text-slate-800 dark:text-slate-200">
                    {m.model_name.replace(/_/g, " ")}
                  </span>
                  {isChampion && (
                    <Badge className="bg-teal-600 text-white text-[10px] py-0 px-1.5 flex items-center space-x-1">
                      <Trophy className="w-2.5 h-2.5 mr-0.5" />
                      <span>Champion</span>
                    </Badge>
                  )}
                </div>
                <div className="flex items-center space-x-2 font-mono">
                  <span
                    className={`font-bold ${
                      isChampion
                        ? "text-teal-600 dark:text-teal-400"
                        : "text-slate-700 dark:text-slate-300"
                    }`}
                  >
                    {val.toFixed(4)}
                  </span>
                  {m.roc_auc_std !== undefined && activeMetric === "roc_auc" && (
                    <span className="text-[10px] text-slate-400">
                      (±{m.roc_auc_std.toFixed(3)})
                    </span>
                  )}
                </div>
              </div>

              {/* Progress bar track */}
              <div className="h-2 w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden flex relative">
                {/* 0.50 baseline marker */}
                <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-slate-300 dark:bg-slate-600 z-10" />
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    isChampion
                      ? "bg-teal-500"
                      : val < 0.6
                      ? "bg-slate-300 dark:bg-slate-600"
                      : "bg-indigo-500"
                  }`}
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* "What this means" explanation */}
      <div className="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-lg border border-slate-200/60 dark:border-slate-800 flex items-start space-x-2 text-xs text-slate-600 dark:text-slate-400">
        <HelpCircle className="w-4 h-4 text-teal-500 shrink-0 mt-0.5" />
        <div className="leading-relaxed">
          <span className="font-semibold text-slate-800 dark:text-slate-200">What this means: </span>
          {cohortTitle === "JDS Phase 5" ? (
            <>
              Across 25 repeated cross-validation splits, <strong className="text-slate-800 dark:text-slate-200">Logistic Regression L2</strong> achieved the highest generalization score (ROC-AUC = 0.9035, Macro F1 = 0.8506). Regularization prevented overfitting in this small-sample cohort (N=139), outperforming complex gradient boosting and tree algorithms while preserving full odds-ratio interpretability.
            </>
          ) : (
            <>
              Under strict Stratified Group K-Fold cross-validation preventing duplicate subject leakage (152 unique subjects, N=161), <strong className="text-slate-800 dark:text-slate-200">Logistic Regression L2</strong> achieved 0.9699 ROC-AUC and 92.68% accuracy. Note that personality traits are developmental self-awareness indicators only and must never be used for gatekeeping.
            </>
          )}
        </div>
      </div>
    </div>
  );
}

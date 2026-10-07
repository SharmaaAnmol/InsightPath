"use client";

import React from "react";
import { Info, HelpCircle, Sparkles, Zap } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ReducedFeaturesItem } from "@/lib/api";

interface SimplifiedInsightVisualProps {
  reducedData?: ReducedFeaturesItem[];
  pctRetained?: number;
  fullAuc?: number;
  reducedAuc?: number;
  onOpenEvidence?: () => void;
  className?: string;
}

export function SimplifiedInsightVisual({
  reducedData,
  pctRetained = 96.75,
  fullAuc = 0.9035,
  reducedAuc = 0.8741,
  onOpenEvidence,
  className = "",
}: SimplifiedInsightVisualProps) {
  return (
    <div className={`space-y-4 ${className}`}>
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 dark:border-slate-800 pb-2">
        <div className="flex items-center space-x-2">
          <Badge className="bg-teal-500/10 text-teal-600 dark:text-teal-400 border-teal-500/20 text-xs py-0.5">
            <Zap className="w-3 h-3 mr-1 text-teal-500" />
            Parsimonious 2-Feature Core
          </Badge>
          <span className="text-xs text-slate-500 font-mono">
            60% Feature Reduction
          </span>
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

      {/* Hero comparison callout */}
      <div className="p-4 rounded-xl border border-teal-500/20 bg-linear-to-r from-teal-500/5 via-indigo-500/5 to-transparent space-y-3">
        <div className="flex items-center justify-between text-xs font-semibold text-slate-700 dark:text-slate-300">
          <span>Full 5-Feature Pipeline</span>
          <span className="font-mono text-slate-500">ROC-AUC: {fullAuc.toFixed(4)} (100%)</span>
        </div>
        <div className="h-3 w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
          <div className="h-full bg-slate-400 dark:bg-slate-600 rounded-full w-full" />
        </div>

        <div className="flex items-center justify-between text-xs font-semibold text-teal-700 dark:text-teal-300 pt-1">
          <span className="flex items-center space-x-1.5">
            <Sparkles className="w-3.5 h-3.5 text-teal-500" />
            <span>Maths/Stats + Storytelling Only (2 Features)</span>
          </span>
          <span className="font-mono font-bold text-teal-600 dark:text-teal-400">
            ROC-AUC: {reducedAuc.toFixed(4)} ({pctRetained.toFixed(1)}% Retained)
          </span>
        </div>
        <div className="h-3 w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
          <div
            className="h-full bg-teal-500 rounded-full transition-all duration-500"
            style={{ width: `${pctRetained}%` }}
          />
        </div>
      </div>

      {/* Comparison table across algorithm families if available */}
      {reducedData && reducedData.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border border-slate-200/60 dark:border-slate-800 rounded-lg overflow-hidden">
            <thead className="bg-slate-50 dark:bg-slate-800/60 text-slate-500 font-mono text-[11px]">
              <tr>
                <th className="p-2.5">Algorithm</th>
                <th className="p-2.5">Full AUC (5 Feat)</th>
                <th className="p-2.5">Reduced AUC (2 Feat)</th>
                <th className="p-2.5">AUC Retained</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800/80 font-mono">
              {reducedData.map((row, i) => (
                <tr key={i} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/30">
                  <td className="p-2.5 font-sans font-medium text-slate-800 dark:text-slate-200">
                    {row.algorithm_family}
                  </td>
                  <td className="p-2.5 text-slate-500">{row.full_roc_auc.toFixed(4)}</td>
                  <td className="p-2.5 text-teal-600 dark:text-teal-400 font-semibold">{row.reduced_roc_auc.toFixed(4)}</td>
                  <td className="p-2.5 text-indigo-600 dark:text-indigo-400 font-bold">{row.pct_auc_retained.toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* "What this means" explanation */}
      <div className="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-lg border border-slate-200/60 dark:border-slate-800 flex items-start space-x-2 text-xs text-slate-600 dark:text-slate-400">
        <HelpCircle className="w-4 h-4 text-teal-500 shrink-0 mt-0.5" />
        <div className="leading-relaxed">
          <span className="font-semibold text-slate-800 dark:text-slate-200">What this means: </span>
          Mathematical modeling and executive storytelling alone capture <strong>96.75% of the total predictive power</strong> of the entire 5-feature battery. Distributed cluster administration (Big Data) and generic procedural coding add minimal incremental promotion signal once analytical rigor and narrative delivery are established.
        </div>
      </div>
    </div>
  );
}

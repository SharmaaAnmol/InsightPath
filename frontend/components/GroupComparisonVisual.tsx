"use client";

import React from "react";
import { Info, HelpCircle, AlertTriangle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { SDSGroupTestItem } from "@/lib/api";

interface GroupComparisonVisualProps {
  tests: SDSGroupTestItem[];
  highSuccessCount?: number;
  lowSuccessCount?: number;
  onOpenEvidence?: () => void;
  className?: string;
}

export function GroupComparisonVisual({
  tests,
  highSuccessCount = 85,
  lowSuccessCount = 76,
  onOpenEvidence,
  className = "",
}: GroupComparisonVisualProps) {
  const maxScore = 70; // Big Five trait sum scale max is 68.0

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Header and Controls */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 dark:border-slate-800 pb-2">
        <div className="flex items-center space-x-3 text-xs">
          <div className="flex items-center space-x-1.5">
            <span className="w-3 h-3 rounded-full bg-teal-500 inline-block" />
            <span className="font-semibold text-slate-700 dark:text-slate-300">
              High Success Cohort (N={highSuccessCount})
            </span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-3 h-3 rounded-full bg-slate-300 dark:bg-slate-600 inline-block" />
            <span className="text-slate-500 dark:text-slate-400">
              Low Success Cohort (N={lowSuccessCount})
            </span>
          </div>
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

      {/* Trait comparison rows */}
      <div className="space-y-4">
        {tests.map((item, idx) => {
          const highPct = (item.mean_group1 / maxScore) * 100;
          const lowPct = (item.mean_group2 / maxScore) * 100;
          const isSignificant = item.p_value_t < 0.05;
          const traitName = item.variable
            .replace(/_/g, " ")
            .replace(/\b\w/g, (c) => c.toUpperCase());

          return (
            <div key={idx} className="space-y-1.5 p-3 rounded-xl border border-slate-200/60 dark:border-slate-800 bg-white dark:bg-slate-900/60">
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center space-x-2">
                  <span className="font-semibold text-slate-800 dark:text-slate-200">
                    {traitName}
                  </span>
                  <Badge
                    variant={isSignificant ? "default" : "outline"}
                    className={`text-[10px] py-0 px-1.5 font-mono ${
                      isSignificant
                        ? "bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border-indigo-500/20"
                        : "text-slate-400"
                    }`}
                  >
                    {isSignificant
                      ? `Cohen's d = +${item.cohens_d.toFixed(2)} (Large)`
                      : `d = ${item.cohens_d.toFixed(2)} (Not Significant)`}
                  </Badge>
                </div>

                <div className="font-mono text-xs text-right">
                  <span className="text-teal-600 dark:text-teal-400 font-bold">
                    {item.mean_group1.toFixed(1)}
                  </span>
                  <span className="text-slate-400 mx-1">vs</span>
                  <span className="text-slate-500 dark:text-slate-400">
                    {item.mean_group2.toFixed(1)}
                  </span>
                  <span className="text-slate-400 text-[10px] ml-1">/ 70</span>
                </div>
              </div>

              {/* Dual bars */}
              <div className="space-y-1">
                {/* High success bar */}
                <div className="h-2 w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden flex">
                  <div
                    className="h-full bg-teal-500 rounded-full transition-all duration-500"
                    style={{ width: `${highPct}%` }}
                  />
                </div>
                {/* Low success bar */}
                <div className="h-2 w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden flex">
                  <div
                    className="h-full bg-slate-300 dark:bg-slate-600 rounded-full transition-all duration-500"
                    style={{ width: `${lowPct}%` }}
                  />
                </div>
              </div>

              <div className="flex justify-between items-center text-[10px] text-slate-400 pt-0.5">
                <span>Mean Diff: {item.mean_diff > 0 ? `+${item.mean_diff.toFixed(1)}` : item.mean_diff.toFixed(1)} pts</span>
                <span>Welch&apos;s p {item.p_value_t < 0.001 ? "< 0.001" : `= ${item.p_value_t.toFixed(3)}`}</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Mandatory Ethical Non-Gatekeeping Notice */}
      <div className="p-3.5 rounded-xl border border-amber-300/60 dark:border-amber-900/60 bg-amber-500/10 text-amber-900 dark:text-amber-200 flex items-start space-x-2 text-xs">
        <AlertTriangle className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
        <div className="leading-relaxed">
          <strong className="font-semibold">MANDATORY METHODOLOGICAL NOTICE: </strong>
          Personality scores reflect developmental coaching indicators observed within a senior consulting cohort. Big Five traits must <span className="underline font-bold">NEVER</span> be used as automated hiring, screening, or termination gates.
        </div>
      </div>

      {/* "What this means" explanation */}
      <div className="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-lg border border-slate-200/60 dark:border-slate-800 flex items-start space-x-2 text-xs text-slate-600 dark:text-slate-400">
        <HelpCircle className="w-4 h-4 text-teal-500 shrink-0 mt-0.5" />
        <div className="leading-relaxed">
          <span className="font-semibold text-slate-800 dark:text-slate-200">What this means: </span>
          Conscientiousness (+17.95 pts, d=1.85, p&lt;0.001) and Openness (+15.18 pts, d=1.80, p&lt;0.001) show the largest separation between high and low performing senior consultants, reflecting the necessity of delivery rigor and intellectual adaptability when handling ambiguous advisory mandates. Neuroticism shows zero significant difference (d=-0.01, p=0.941).
        </div>
      </div>
    </div>
  );
}

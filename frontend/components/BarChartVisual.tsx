"use client";

import React from "react";
import { Info, HelpCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export interface BarChartItem {
  label: string;
  value: number;
  secondaryValue?: string | number;
  unit?: string;
  category?: string;
  highlight?: boolean;
  color?: string; // e.g. "teal", "indigo", "emerald", "amber", "rose"
}

interface BarChartVisualProps {
  items: BarChartItem[];
  maxValue?: number;
  unitLabel: string;
  meaning: string;
  onOpenEvidence?: () => void;
  orientation?: "horizontal" | "vertical";
  className?: string;
}

export function BarChartVisual({
  items,
  maxValue,
  unitLabel,
  meaning,
  onOpenEvidence,
  className = "",
}: BarChartVisualProps) {
  const max = maxValue || Math.max(...items.map((i) => i.value), 1) * 1.1;

  const colorStyles: Record<string, { bar: string; text: string }> = {
    teal: { bar: "bg-teal-500", text: "text-teal-600 dark:text-teal-400" },
    indigo: { bar: "bg-indigo-500", text: "text-indigo-600 dark:text-indigo-400" },
    emerald: { bar: "bg-emerald-500", text: "text-emerald-600 dark:text-emerald-400" },
    amber: { bar: "bg-amber-500", text: "text-amber-600 dark:text-amber-400" },
    rose: { bar: "bg-rose-500", text: "text-rose-600 dark:text-rose-400" },
  };

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Zero baseline indication */}
      <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 border-b border-slate-100 dark:border-slate-800 pb-1.5">
        <span>Zero-baseline scale (Units: {unitLabel})</span>
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

      {/* Bars list */}
      <div className="space-y-3">
        {items.map((item, idx) => {
          const pct = Math.min(Math.max((item.value / max) * 100, 0), 100);
          const color = item.color || (item.highlight ? "teal" : "indigo");
          const cStyle = colorStyles[color] || colorStyles.indigo;

          return (
            <div key={idx} className="group space-y-1">
              <div className="flex items-center justify-between text-xs font-medium">
                <div className="flex items-center space-x-2 truncate">
                  <span className="text-slate-700 dark:text-slate-300 truncate">
                    {item.label}
                  </span>
                  {item.category && (
                    <Badge variant="outline" className="text-[10px] py-0 px-1.5 text-slate-400 font-normal">
                      {item.category}
                    </Badge>
                  )}
                </div>
                <div className="flex items-center space-x-2 shrink-0 font-mono text-xs">
                  {item.secondaryValue !== undefined && (
                    <span className="text-slate-400 text-[11px]">
                      {item.secondaryValue}
                    </span>
                  )}
                  <span className={`font-semibold ${cStyle.text}`}>
                    {typeof item.value === "number" && Number.isInteger(item.value)
                      ? item.value.toLocaleString()
                      : typeof item.value === "number"
                      ? item.value.toFixed(2)
                      : item.value}{" "}
                    {item.unit || ""}
                  </span>
                </div>
              </div>

              {/* Bar track starting from 0 */}
              <div className="h-2.5 w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden flex">
                <div
                  className={`h-full ${cStyle.bar} rounded-full transition-all duration-500 ease-out`}
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
          {meaning}
        </div>
      </div>
    </div>
  );
}

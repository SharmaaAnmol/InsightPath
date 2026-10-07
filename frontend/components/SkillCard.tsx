"use client";

import React from "react";
import { Sparkles, KeyRound, ShieldAlert } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ProgressBar } from "@/components/ProgressBar";
import { cn } from "@/lib/utils";

interface SkillCardProps {
  name: string;
  category: "Technical Tool" | "Mathematical Rigor" | "Communication & Story" | "Executive Behavior";
  currencyType: "Market Access" | "Career Velocity" | "Saturated Foundation";
  prevalencePercent: number; // e.g. 48.2 for SQL
  oddsRatio?: number; // e.g. 3.23 for Storytelling
  effectSize?: string; // e.g. "d = 1.32"
  description: string;
  stageRelevance: "Entry (0-2y)" | "Velocity (3-5y)" | "Expansion (6-9y)" | "Leadership (10+y)";
  className?: string;
}

export function SkillCard({
  name,
  category,
  currencyType,
  prevalencePercent,
  oddsRatio,
  effectSize,
  description,
  stageRelevance,
  className,
}: SkillCardProps) {
  const currencyBadge = {
    "Career Velocity": {
      color: "bg-teal-500/10 text-teal-600 dark:text-teal-400 border-teal-500/30",
      icon: Sparkles,
      label: "Career Velocity Currency",
    },
    "Market Access": {
      color: "bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border-indigo-500/30",
      icon: KeyRound,
      label: "Table-Stakes Access",
    },
    "Saturated Foundation": {
      color: "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/30",
      icon: ShieldAlert,
      label: "Saturated / Low Marginal Lift",
    },
  }[currencyType];

  const CurrencyIcon = currencyBadge.icon;

  return (
    <Card className={cn("border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-900/80 hover:border-slate-300 dark:hover:border-slate-700 transition-all", className)}>
      <CardContent className="p-5 space-y-3.5">
        <div className="flex items-start justify-between">
          <div className="space-y-0.5">
            <span className="text-[10px] font-semibold tracking-wider uppercase text-slate-500 dark:text-slate-400">
              {category}
            </span>
            <h4 className="text-base font-bold text-slate-900 dark:text-slate-50 tracking-tight">
              {name}
            </h4>
          </div>
          <span className={cn("inline-flex items-center gap-1 text-[10px] font-medium px-2 py-0.5 rounded-full border", currencyBadge.color)}>
            <CurrencyIcon className="w-3 h-3" />
            {currencyBadge.label}
          </span>
        </div>

        <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
          {description}
        </p>

        <div className="space-y-2 pt-1">
          <ProgressBar
            value={prevalencePercent}
            label="Market Posting Prevalence"
            color={currencyType === "Career Velocity" ? "teal" : "indigo"}
            size="sm"
          />
        </div>

        <div className="pt-2 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between text-xs">
          <div className="flex items-center space-x-2">
            {oddsRatio && (
              <span className="font-mono text-[11px] font-semibold text-teal-600 dark:text-teal-400">
                AOR: {oddsRatio.toFixed(2)}x
              </span>
            )}
            {effectSize && (
              <span className="text-[11px] text-slate-500 dark:text-slate-400 font-mono">
                {effectSize}
              </span>
            )}
          </div>
          <Badge variant="outline" className="text-[10px] px-1.5 py-0 font-normal">
            {stageRelevance}
          </Badge>
        </div>
      </CardContent>
    </Card>
  );
}

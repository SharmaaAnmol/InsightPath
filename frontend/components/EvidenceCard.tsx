"use client";

import React from "react";
import { CheckCircle2, AlertCircle, FileText, Database } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface EvidenceCardProps {
  claim: string;
  finding: string;
  datasetName: "DataScience Jobs" | "Analytics Jobs" | "JDS Skill Traits" | "SDS Personality Traits" | "Cross-Dataset Synthesis";
  sampleSize: string;
  metric: string;
  verdict: "Supported" | "Refuted" | "Divergent" | "Synthesized";
  hypothesisId?: string; // H1 to H6 or RQ1 to RQ9
  implication: string;
  className?: string;
}

export function EvidenceCard({
  claim,
  finding,
  datasetName,
  sampleSize,
  metric,
  verdict,
  hypothesisId,
  implication,
  className,
}: EvidenceCardProps) {
  const verdictBadge = {
    Supported: {
      variant: "default" as const,
      color: "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20",
      icon: CheckCircle2,
    },
    Refuted: {
      variant: "destructive" as const,
      color: "bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/20",
      icon: AlertCircle,
    },
    Divergent: {
      variant: "secondary" as const,
      color: "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20",
      icon: AlertCircle,
    },
    Synthesized: {
      variant: "outline" as const,
      color: "bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border-indigo-500/20",
      icon: CheckCircle2,
    },
  }[verdict];

  const VerdictIcon = verdictBadge.icon;

  return (
    <Card className={cn("border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-900/80 hover:border-slate-300 dark:hover:border-slate-700 transition-all", className)}>
      <CardContent className="p-5 space-y-3.5">
        <div className="flex items-start justify-between gap-2">
          <div className="flex items-center space-x-2">
            {hypothesisId && (
              <Badge variant="outline" className="font-mono text-[10px] uppercase font-semibold">
                {hypothesisId}
              </Badge>
            )}
            <span className="flex items-center text-xs text-slate-500 dark:text-slate-400 space-x-1">
              <Database className="w-3 h-3 text-slate-400" />
              <span>{datasetName}</span>
              <span className="text-slate-300 dark:text-slate-700">•</span>
              <span className="font-mono">{sampleSize}</span>
            </span>
          </div>
          <span className={cn("inline-flex items-center gap-1 text-[11px] font-medium px-2 py-0.5 rounded-full border", verdictBadge.color)}>
            <VerdictIcon className="w-3 h-3" />
            {verdict}
          </span>
        </div>

        <div>
          <h4 className="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-1 leading-snug">
            {claim}
          </h4>
          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            {finding}
          </p>
        </div>

        <div className="pt-2 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between text-xs">
          <div className="flex items-center space-x-1 font-mono text-[11px] text-teal-600 dark:text-teal-400 bg-teal-50 dark:bg-teal-950/40 px-2 py-0.5 rounded-md border border-teal-200/60 dark:border-teal-900/60">
            <span>Metric:</span>
            <span className="font-semibold">{metric}</span>
          </div>
          <div className="flex items-center space-x-1 text-slate-500 dark:text-slate-400 max-w-[55%] truncate text-[11px]">
            <FileText className="w-3 h-3 shrink-0 text-slate-400" />
            <span className="truncate" title={implication}>{implication}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

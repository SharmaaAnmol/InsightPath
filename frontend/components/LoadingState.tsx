"use client";

import React from "react";
import { Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface LoadingStateProps {
  label?: string;
  description?: string;
  className?: string;
}

export function LoadingState({
  label = "Processing Analytics...",
  description = "Querying verified empirical evidence and pipeline models.",
  className,
}: LoadingStateProps) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center p-12 text-center rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white/50 dark:bg-slate-900/40 backdrop-blur-xs",
        className
      )}
    >
      <Loader2 className="w-8 h-8 text-teal-500 animate-spin mb-3" />
      <h4 className="text-sm font-medium text-slate-900 dark:text-slate-100 mb-1">{label}</h4>
      <p className="text-xs text-slate-500 dark:text-slate-400 max-w-xs">{description}</p>
    </div>
  );
}

"use client";

import React from "react";
import { cn } from "@/lib/utils";

interface ProgressBarProps {
  value: number; // 0 to 100
  max?: number;
  label?: string;
  sublabel?: string;
  showPercent?: boolean;
  color?: "teal" | "indigo" | "emerald" | "amber" | "rose" | "cyan";
  size?: "sm" | "md" | "lg";
  className?: string;
}

export function ProgressBar({
  value,
  max = 100,
  label,
  sublabel,
  showPercent = true,
  color = "teal",
  size = "md",
  className,
}: ProgressBarProps) {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));

  const colorStyles = {
    teal: "bg-teal-500 shadow-teal-500/20",
    indigo: "bg-indigo-500 shadow-indigo-500/20",
    emerald: "bg-emerald-500 shadow-emerald-500/20",
    amber: "bg-amber-500 shadow-amber-500/20",
    rose: "bg-rose-500 shadow-rose-500/20",
    cyan: "bg-cyan-500 shadow-cyan-500/20",
  }[color];

  const heightStyles = {
    sm: "h-1.5",
    md: "h-2",
    lg: "h-3",
  }[size];

  return (
    <div className={cn("w-full space-y-1.5", className)}>
      {(label || showPercent) && (
        <div className="flex items-center justify-between text-xs">
          {label && (
            <span className="font-medium text-slate-700 dark:text-slate-300">
              {label}
              {sublabel && <span className="ml-1 text-slate-500 dark:text-slate-500 font-normal">({sublabel})</span>}
            </span>
          )}
          {showPercent && (
            <span className="font-mono text-slate-600 dark:text-slate-400 font-medium ml-auto">
              {percentage.toFixed(1)}%
            </span>
          )}
        </div>
      )}
      <div className={cn("w-full bg-slate-200/80 dark:bg-slate-800/80 rounded-full overflow-hidden", heightStyles)}>
        <div
          className={cn("h-full rounded-full transition-all duration-500 ease-out", colorStyles)}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

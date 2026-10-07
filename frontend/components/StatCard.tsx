"use client";

import React from "react";
import { LucideIcon, TrendingUp, TrendingDown, Minus } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface StatCardProps {
  label: string;
  value: string | number;
  subvalue?: string;
  trend?: {
    value: string;
    direction: "up" | "down" | "neutral";
  };
  badgeText?: string;
  badgeVariant?: "default" | "secondary" | "outline" | "destructive";
  icon?: LucideIcon;
  color?: "teal" | "indigo" | "emerald" | "amber" | "slate";
  className?: string;
}

export function StatCard({
  label,
  value,
  subvalue,
  trend,
  badgeText,
  badgeVariant = "secondary",
  icon: Icon,
  color = "slate",
  className,
}: StatCardProps) {
  const iconBg = {
    teal: "text-teal-500 bg-teal-500/10 border-teal-500/20",
    indigo: "text-indigo-500 bg-indigo-500/10 border-indigo-500/20",
    emerald: "text-emerald-500 bg-emerald-500/10 border-emerald-500/20",
    amber: "text-amber-500 bg-amber-500/10 border-amber-500/20",
    slate: "text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-800 border-slate-200 dark:border-slate-700",
  }[color];

  return (
    <Card className={cn("relative overflow-hidden transition-all duration-200 hover:border-slate-300 dark:hover:border-slate-700 group", className)}>
      <CardContent className="p-5">
        <div className="flex items-start justify-between">
          <div className="space-y-1">
            <p className="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">
              {label}
            </p>
            <div className="flex items-baseline space-x-2">
              <span className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-50 font-mono">
                {value}
              </span>
              {subvalue && (
                <span className="text-xs text-slate-500 dark:text-slate-400 font-normal">
                  {subvalue}
                </span>
              )}
            </div>
          </div>
          {Icon && (
            <div className={cn("p-2 rounded-lg border", iconBg)}>
              <Icon className="w-4 h-4" />
            </div>
          )}
        </div>

        {(trend || badgeText) && (
          <div className="mt-3.5 pt-3 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between text-xs">
            {trend && (
              <div className="flex items-center space-x-1 font-medium">
                {trend.direction === "up" && <TrendingUp className="w-3.5 h-3.5 text-emerald-500" />}
                {trend.direction === "down" && <TrendingDown className="w-3.5 h-3.5 text-rose-500" />}
                {trend.direction === "neutral" && <Minus className="w-3.5 h-3.5 text-slate-400" />}
                <span
                  className={cn(
                    trend.direction === "up" && "text-emerald-600 dark:text-emerald-400",
                    trend.direction === "down" && "text-rose-600 dark:text-rose-400",
                    trend.direction === "neutral" && "text-slate-500 dark:text-slate-400"
                  )}
                >
                  {trend.value}
                </span>
              </div>
            )}
            {badgeText && (
              <Badge variant={badgeVariant} className="text-[10px] px-1.5 py-0">
                {badgeText}
              </Badge>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

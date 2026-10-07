"use client";

import React from "react";
import { Info } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Tooltip } from "@/components/Tooltip";
import { cn } from "@/lib/utils";

interface ChartCardProps {
  title: string;
  subtitle?: string;
  infoTooltip?: string;
  badge?: React.ReactNode;
  action?: React.ReactNode;
  children: React.ReactNode;
  footer?: React.ReactNode;
  className?: string;
}

export function ChartCard({
  title,
  subtitle,
  infoTooltip,
  badge,
  action,
  children,
  footer,
  className,
}: ChartCardProps) {
  return (
    <Card className={cn("overflow-hidden border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-900/90 shadow-xs", className)}>
      <CardHeader className="pb-3 border-b border-slate-100 dark:border-slate-800/80">
        <div className="flex items-start justify-between">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <CardTitle className="text-base font-semibold text-slate-900 dark:text-slate-100 tracking-tight">
                {title}
              </CardTitle>
              {infoTooltip && (
                <Tooltip content={infoTooltip}>
                  <button type="button" aria-label="More information" className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors">
                    <Info className="w-3.5 h-3.5" />
                  </button>
                </Tooltip>
              )}
              {badge}
            </div>
            {subtitle && (
              <CardDescription className="text-xs text-slate-500 dark:text-slate-400">
                {subtitle}
              </CardDescription>
            )}
          </div>
          {action && <div className="flex items-center space-x-2">{action}</div>}
        </div>
      </CardHeader>
      <CardContent className="pt-5">{children}</CardContent>
      {footer && (
        <div className="px-6 py-3 bg-slate-50/70 dark:bg-slate-950/40 border-t border-slate-100 dark:border-slate-800/80 text-xs text-slate-500 dark:text-slate-400">
          {footer}
        </div>
      )}
    </Card>
  );
}

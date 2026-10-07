"use client";

import React from "react";
import { GraduationCap, Building2, Users, Briefcase, ArrowUpRight, Clock, Target } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface RecommendationCardProps {
  stakeholder: "Student" | "University" | "Mentor" | "Employer";
  title: string;
  actionItem: string;
  rationalEvidence: string;
  kpiTarget: string;
  priority: "High" | "Medium" | "Strategic";
  timeline: string;
  className?: string;
}

export function RecommendationCard({
  stakeholder,
  title,
  actionItem,
  rationalEvidence,
  kpiTarget,
  priority,
  timeline,
  className,
}: RecommendationCardProps) {
  const stakeholderConfig = {
    Student: {
      icon: GraduationCap,
      color: "text-teal-500 bg-teal-500/10 border-teal-500/20",
    },
    University: {
      icon: Building2,
      color: "text-indigo-500 bg-indigo-500/10 border-indigo-500/20",
    },
    Mentor: {
      icon: Users,
      color: "text-cyan-500 bg-cyan-500/10 border-cyan-500/20",
    },
    Employer: {
      icon: Briefcase,
      color: "text-amber-500 bg-amber-500/10 border-amber-500/20",
    },
  }[stakeholder];

  const Icon = stakeholderConfig.icon;

  const priorityColor = {
    High: "text-rose-600 dark:text-rose-400 border-rose-500/30 bg-rose-500/10",
    Medium: "text-amber-600 dark:text-amber-400 border-amber-500/30 bg-amber-500/10",
    Strategic: "text-indigo-600 dark:text-indigo-400 border-indigo-500/30 bg-indigo-500/10",
  }[priority];

  return (
    <Card className={cn("border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-900/80 hover:border-slate-300 dark:hover:border-slate-700 transition-all group", className)}>
      <CardContent className="p-5 space-y-3.5">
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-2">
            <div className={cn("p-1.5 rounded-md border", stakeholderConfig.color)}>
              <Icon className="w-3.5 h-3.5" />
            </div>
            <span className="text-xs font-semibold text-slate-700 dark:text-slate-300">
              {stakeholder} Blueprint
            </span>
          </div>
          <span className={cn("text-[10px] font-semibold px-2 py-0.5 rounded-full border", priorityColor)}>
            {priority} Priority
          </span>
        </div>

        <div>
          <h4 className="text-sm font-bold text-slate-900 dark:text-slate-50 mb-1 leading-snug group-hover:text-teal-600 dark:group-hover:text-teal-400 transition-colors">
            {title}
          </h4>
          <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            {actionItem}
          </p>
        </div>

        <div className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-950/50 border border-slate-100 dark:border-slate-800/80 space-y-1.5 text-xs">
          <div className="flex items-start space-x-1.5 text-slate-500 dark:text-slate-400 text-[11px]">
            <Target className="w-3 h-3 text-teal-500 shrink-0 mt-0.5" />
            <span><strong className="text-slate-700 dark:text-slate-300">Target KPI:</strong> {kpiTarget}</span>
          </div>
          <div className="flex items-center space-x-1.5 text-slate-500 dark:text-slate-400 text-[11px]">
            <Clock className="w-3 h-3 text-indigo-500 shrink-0" />
            <span><strong className="text-slate-700 dark:text-slate-300">Timeline:</strong> {timeline}</span>
          </div>
        </div>

        <div className="pt-1 text-[11px] text-slate-500 dark:text-slate-400 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between">
          <span className="truncate max-w-[85%] italic">Basis: {rationalEvidence}</span>
          <ArrowUpRight className="w-3 h-3 text-slate-400 group-hover:text-teal-500 transition-colors" />
        </div>
      </CardContent>
    </Card>
  );
}

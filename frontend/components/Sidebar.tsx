"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  BarChart2,
  Sparkles,
  Grid,
  MapPin,
  FileCheck2,
  SlidersHorizontal,
  FileText,
  ShieldAlert,
} from "lucide-react";
import { cn } from "@/lib/utils";

const SIDEBAR_ITEMS = [
  { href: "/dashboard", label: "Executive Dashboard", icon: LayoutDashboard },
  { href: "/market", label: "Market Intelligence", icon: BarChart2 },
  { href: "/skills", label: "Skills Dual-Currency", icon: Sparkles },
  { href: "/career-readiness", label: "4-Quadrant Framework", icon: Grid },
  { href: "/roadmap", label: "Stakeholder Blueprints", icon: MapPin },
  { href: "/assessment", label: "Diagnostic Scorer", icon: SlidersHorizontal },
  { href: "/methodology", label: "Methodology & Audit", icon: FileCheck2 },
  { href: "/about", label: "About RUSTY WOLVES", icon: FileText },
];

export function Sidebar({ className = "" }: { className?: string }) {
  const pathname = usePathname();

  return (
    <aside
      className={cn(
        "w-64 shrink-0 border-r border-slate-200/80 dark:border-slate-800/80 bg-slate-50/50 dark:bg-[#07090e]/60 min-h-[calc(100vh-4rem)] p-4 flex flex-col justify-between hidden md:flex",
        className
      )}
    >
      <div className="space-y-6">
        <div>
          <p className="px-3 text-[10px] font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-2">
            Analytical Navigation
          </p>
          <nav className="space-y-1">
            {SIDEBAR_ITEMS.map((item) => {
              const isActive = pathname === item.href;
              const Icon = item.icon;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "flex items-center space-x-2.5 px-3 py-2 rounded-lg text-xs font-medium transition-colors group",
                    isActive
                      ? "text-teal-600 dark:text-teal-400 bg-teal-500/10 dark:bg-teal-500/15 font-semibold"
                      : "text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-200/50 dark:hover:bg-slate-800/50"
                  )}
                >
                  <Icon
                    className={cn(
                      "w-4 h-4 transition-colors",
                      isActive ? "text-teal-500" : "text-slate-400 group-hover:text-slate-600 dark:group-hover:text-slate-300"
                    )}
                  />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>

        <div className="p-3 rounded-lg border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/60 text-xs space-y-1.5">
          <div className="flex items-center space-x-1.5 text-slate-700 dark:text-slate-200 font-semibold text-[11px]">
            <span className="w-2 h-2 rounded-full bg-teal-500" />
            <span>Phases 0–9 Complete</span>
          </div>
          <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">
            Consuming validated joblib pipelines & 105 analytical CSV matrices.
          </p>
        </div>
      </div>

      <div className="pt-4 border-t border-slate-200/60 dark:border-slate-800/60 flex items-start space-x-2 text-[10px] text-slate-400 dark:text-slate-500">
        <ShieldAlert className="w-3.5 h-3.5 shrink-0 text-amber-500 mt-0.5" />
        <span>Ethical directive: Non-gatekeeping diagnostic use only.</span>
      </div>
    </aside>
  );
}

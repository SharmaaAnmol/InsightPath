"use client";

import React from "react";
import Link from "next/link";
import { Compass } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t border-slate-200/80 dark:border-slate-800/80 bg-white/50 dark:bg-[#07090e]/80 py-12 px-4 sm:px-6 lg:px-8 mt-auto">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8">
        <div className="space-y-3">
          <div className="flex items-center space-x-2">
            <div className="w-6 h-6 rounded-md bg-gradient-to-tr from-teal-500 to-indigo-600 flex items-center justify-center text-white">
              <Compass className="w-3.5 h-3.5" />
            </div>
            <span className="font-bold text-sm tracking-tight text-slate-900 dark:text-slate-100">
              InsightPath
            </span>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
            Evidence-Based Career Intelligence for Data Science & Analytics. Official analytical submission for the SAS CU Hackathon Round 2 by Team RUSTY WOLVES.
          </p>
          <div className="text-[11px] font-mono text-slate-400 dark:text-slate-500">
            Validated across 17,443 job requisitions & 300 practitioner profiles.
          </div>
        </div>

        <div>
          <h4 className="text-xs font-semibold text-slate-900 dark:text-slate-100 uppercase tracking-wider mb-3">
            Analytical Lenses
          </h4>
          <ul className="space-y-2 text-xs text-slate-600 dark:text-slate-400">
            <li>
              <Link href="/market" className="hover:text-teal-500 transition-colors">
                Macro Market Demand (DS Jobs)
              </Link>
            </li>
            <li>
              <Link href="/market" className="hover:text-teal-500 transition-colors">
                Micro Skill Ecosystem (Analytics Jobs)
              </Link>
            </li>
            <li>
              <Link href="/skills" className="hover:text-teal-500 transition-colors">
                Junior Skill Traits (JDS Model)
              </Link>
            </li>
            <li>
              <Link href="/skills" className="hover:text-teal-500 transition-colors">
                Senior Personality Traits (SDS Model)
              </Link>
            </li>
          </ul>
        </div>

        <div>
          <h4 className="text-xs font-semibold text-slate-900 dark:text-slate-100 uppercase tracking-wider mb-3">
            Framework & Actions
          </h4>
          <ul className="space-y-2 text-xs text-slate-600 dark:text-slate-400">
            <li>
              <Link href="/career-readiness" className="hover:text-teal-500 transition-colors">
                Four-Quadrant Talent Matrix
              </Link>
            </li>
            <li>
              <Link href="/roadmap" className="hover:text-teal-500 transition-colors">
                Student & University Blueprints
              </Link>
            </li>
            <li>
              <Link href="/roadmap" className="hover:text-teal-500 transition-colors">
                Mentor & Employer Strategies
              </Link>
            </li>
            <li>
              <Link href="/assessment" className="hover:text-teal-500 transition-colors">
                Interactive Diagnostic Scorer
              </Link>
            </li>
          </ul>
        </div>

        <div className="space-y-3">
          <h4 className="text-xs font-semibold text-slate-900 dark:text-slate-100 uppercase tracking-wider">
            Governance & Ethics
          </h4>
          <div className="p-3 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/60 text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">
            <span className="font-semibold text-slate-700 dark:text-slate-200 block mb-1">
              Ethical Non-Gatekeeping
            </span>
            Personality and behavioral models serve exclusively for coaching, self-awareness, and mentoring. Never for automated hiring or dismissal.
          </div>
          <div className="flex items-center space-x-4 text-xs text-slate-400">
            <Link href="/methodology" className="hover:text-slate-600 dark:hover:text-slate-300">
              Audit & Methodology
            </Link>
            <span>•</span>
            <Link href="/about" className="hover:text-slate-600 dark:hover:text-slate-300">
              RUSTY WOLVES
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto pt-8 mt-8 border-t border-slate-200/60 dark:border-slate-800/60 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-400 dark:text-slate-500">
        <div>© 2026 InsightPath • SAS CU Hackathon Round 2 • Team RUSTY WOLVES</div>
        <div className="flex items-center space-x-4 mt-2 sm:mt-0 font-mono text-[11px]">
          <span>Python 3.13 • FastAPI • Next.js 15</span>
          <span>•</span>
          <span className="text-emerald-500">Pipeline Validated</span>
        </div>
      </div>
    </footer>
  );
}

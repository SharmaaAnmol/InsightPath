import React from "react";
import { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, ExternalLink, Zap } from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { JudgeDemoFlow } from "@/components/JudgeDemoFlow";
import { Button } from "@/components/ui/button";

export const metadata: Metadata = {
  title: "Judge Demo Mode | InsightPath",
  description:
    "2-minute judge walkthrough of InsightPath: interactive career-readiness assessment, champion L2-logistic model signal, evidence audit, and career roadmap.",
};

export default function DemoPage() {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-[#07090e] text-slate-900 dark:text-slate-100 transition-colors">
      <Navbar />

      <main className="flex-1 py-10">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
          {/* Quick Breadcrumbs / Top Nav */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
            <div className="flex items-center space-x-3">
              <Link
                href="/dashboard"
                className="text-xs text-slate-500 hover:text-slate-900 dark:hover:text-slate-200 flex items-center gap-1 transition-colors"
              >
                <ArrowLeft className="w-3.5 h-3.5" />
                <span>Back to Overview</span>
              </Link>
              <span className="text-slate-300 dark:text-slate-700">/</span>
              <div className="flex items-center space-x-1.5">
                <Zap className="w-3.5 h-3.5 text-teal-500" />
                <span className="text-xs font-semibold text-slate-900 dark:text-slate-100">
                  Judge Demo Mode
                </span>
              </div>
            </div>

            <div className="flex items-center space-x-3 text-xs">
              <Link href="/methodology" className="text-slate-500 hover:text-teal-500 flex items-center gap-1">
                <span>Methodology Audit</span>
                <ExternalLink className="w-3 h-3" />
              </Link>
              <Link href="/assessment">
                <Button size="sm" variant="ghost" className="h-7 text-xs px-2.5">
                  Full Self-Assessment
                </Button>
              </Link>
            </div>
          </div>

          {/* Interactive Judge Demo Flow */}
          <JudgeDemoFlow />
        </div>
      </main>

      <Footer />
    </div>
  );
}

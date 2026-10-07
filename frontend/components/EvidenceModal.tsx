"use client";

import React, { useEffect } from "react";
import { X, Database, FlaskConical, AlertTriangle, BookOpen, Layers } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export interface EvidenceDetail {
  title: string;
  phase: string;
  dataset: string;
  sampleSize: string;
  method: string;
  interpretation: string;
  limitation: string;
}

interface EvidenceModalProps {
  isOpen: boolean;
  onClose: () => void;
  evidence: EvidenceDetail | null;
}

export function EvidenceModal({ isOpen, onClose, evidence }: EvidenceModalProps) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    if (isOpen) {
      document.body.style.overflow = "hidden";
      window.addEventListener("keydown", handleKeyDown);
    } else {
      document.body.style.overflow = "unset";
    }
    return () => {
      document.body.style.overflow = "unset";
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [isOpen, onClose]);

  if (!isOpen || !evidence) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-slate-950/60 backdrop-blur-xs transition-opacity animate-in fade-in duration-200">
      <div
        className="fixed inset-0"
        onClick={onClose}
        aria-hidden="true"
      />
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="evidence-modal-title"
        className="relative w-full max-w-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl z-10 overflow-hidden animate-in zoom-in-95 duration-200 max-h-[90vh] flex flex-col"
      >
        {/* Header */}
        <div className="px-6 py-5 border-b border-slate-100 dark:border-slate-800 flex items-start justify-between gap-4 bg-slate-50/50 dark:bg-slate-900/50">
          <div className="space-y-1.5">
            <div className="flex items-center space-x-2">
              <Badge variant="outline" className="text-[11px] font-mono text-teal-600 dark:text-teal-400 border-teal-500/30 bg-teal-500/10">
                <Layers className="w-3 h-3 mr-1" />
                {evidence.phase}
              </Badge>
              <Badge variant="secondary" className="text-[11px] font-mono text-slate-600 dark:text-slate-400">
                <Database className="w-3 h-3 mr-1" />
                {evidence.sampleSize}
              </Badge>
            </div>
            <h3 id="evidence-modal-title" className="text-lg font-bold text-slate-900 dark:text-slate-100">
              {evidence.title}
            </h3>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 h-8 w-8 p-0 rounded-full"
            aria-label="Close modal"
          >
            <X className="w-4 h-4" />
          </Button>
        </div>

        {/* Content Body */}
        <div className="p-6 space-y-5 overflow-y-auto">
          {/* Dataset & Scope */}
          <div className="space-y-1.5">
            <div className="flex items-center space-x-2 text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              <Database className="w-3.5 h-3.5 text-teal-500" />
              <span>Dataset & Sample Scope</span>
            </div>
            <p className="text-sm text-slate-800 dark:text-slate-200 bg-slate-50 dark:bg-slate-800/40 p-3 rounded-lg border border-slate-200/60 dark:border-slate-800 font-mono text-xs">
              {evidence.dataset} • ({evidence.sampleSize})
            </p>
          </div>

          {/* Analytical Method */}
          <div className="space-y-1.5">
            <div className="flex items-center space-x-2 text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              <FlaskConical className="w-3.5 h-3.5 text-indigo-500" />
              <span>Analytical Methodology</span>
            </div>
            <div className="p-3.5 rounded-lg border border-indigo-200/50 dark:border-indigo-900/40 bg-indigo-50/40 dark:bg-indigo-950/20 text-xs sm:text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
              {evidence.method}
            </div>
          </div>

          {/* Interpretation */}
          <div className="space-y-1.5">
            <div className="flex items-center space-x-2 text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              <BookOpen className="w-3.5 h-3.5 text-emerald-500" />
              <span>Empirical Interpretation (&quot;What This Means&quot;)</span>
            </div>
            <div className="p-3.5 rounded-lg border border-emerald-200/50 dark:border-emerald-900/40 bg-emerald-50/40 dark:bg-emerald-950/20 text-xs sm:text-sm text-slate-700 dark:text-slate-300 leading-relaxed font-sans">
              {evidence.interpretation}
            </div>
          </div>

          {/* Methodological Limitation */}
          <div className="space-y-1.5">
            <div className="flex items-center space-x-2 text-xs font-semibold uppercase tracking-wider text-amber-600 dark:text-amber-400">
              <AlertTriangle className="w-3.5 h-3.5 text-amber-500" />
              <span>Methodological Boundary & Limitation</span>
            </div>
            <div className="p-3.5 rounded-lg border border-amber-200/60 dark:border-amber-900/40 bg-amber-50/50 dark:bg-amber-950/30 text-xs text-amber-800 dark:text-amber-300 leading-relaxed">
              {evidence.limitation}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-3.5 border-t border-slate-100 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-900/60 flex items-center justify-between">
          <span className="text-[11px] text-slate-400">
            Validated against InsightPath Phase 0-9 Empirical Artifacts
          </span>
          <Button
            size="sm"
            onClick={onClose}
            className="bg-slate-900 hover:bg-slate-800 dark:bg-slate-100 dark:text-slate-900 dark:hover:bg-slate-200 text-white text-xs h-8 px-4"
          >
            Dismiss
          </Button>
        </div>
      </div>
    </div>
  );
}

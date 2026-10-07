"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Compass,
  BarChart3,
  Sparkles,
  Layers,
  MapPin,
  BookOpen,
  Menu,
  X,
  ClipboardCheck,
} from "lucide-react";
import { ThemeToggle } from "@/components/ui/theme-toggle";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

const NAV_LINKS = [
  { href: "/dashboard", label: "Overview", icon: Compass },
  { href: "/market", label: "Market", icon: BarChart3 },
  { href: "/skills", label: "Skills", icon: Sparkles },
  { href: "/career-readiness", label: "Career Readiness", icon: Layers },
  { href: "/roadmap", label: "Roadmap", icon: MapPin },
  { href: "/methodology", label: "Methodology", icon: BookOpen },
];

export function Navbar() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200/80 dark:border-slate-800/80 bg-white/80 dark:bg-[#07090e]/80 backdrop-blur-md transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand */}
          <div className="flex items-center space-x-6">
            <Link href="/" className="flex items-center space-x-2.5 group">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-teal-500 to-indigo-600 flex items-center justify-center text-white shadow-xs group-hover:scale-105 transition-transform">
                <Compass className="w-4 h-4" />
              </div>
              <div className="flex flex-col">
                <span className="font-bold text-sm tracking-tight text-slate-900 dark:text-slate-50 flex items-center gap-1.5">
                  InsightPath
                  <Badge variant="outline" className="text-[10px] py-0 px-1 font-mono hidden sm:inline-flex border-teal-500/30 text-teal-600 dark:text-teal-400">
                    SAS Round 2
                  </Badge>
                </span>
                <span className="text-[10px] text-slate-500 dark:text-slate-400 tracking-wider -mt-0.5">
                  Career Intelligence
                </span>
              </div>
            </Link>

            {/* Desktop Navigation Links */}
            <nav className="hidden md:flex items-center space-x-1">
              {NAV_LINKS.map((link) => {
                const isActive = pathname === link.href || (link.href !== "/dashboard" && pathname.startsWith(link.href));
                const Icon = link.icon;
                return (
                  <Link
                    key={link.href}
                    href={link.href}
                    className={cn(
                      "flex items-center space-x-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors",
                      isActive
                        ? "text-teal-600 dark:text-teal-400 bg-teal-500/10 font-semibold"
                        : "text-slate-600 dark:text-slate-400 hover:text-slate-950 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800/60"
                    )}
                  >
                    <Icon className="w-3.5 h-3.5" />
                    <span>{link.label}</span>
                  </Link>
                );
              })}
            </nav>
          </div>

          {/* Right Controls */}
          <div className="flex items-center space-x-2.5">
            <div className="hidden sm:flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-[11px] font-mono text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 border border-emerald-500/20">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              <span>Models Online</span>
            </div>

            <Link href="/about" className="hidden lg:inline-flex text-xs text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 px-2 py-1 transition-colors">
              About
            </Link>

            <Link href="/assessment">
              <Button size="sm" className="h-8 text-xs bg-slate-900 hover:bg-slate-800 dark:bg-teal-500 dark:hover:bg-teal-400 dark:text-slate-950 text-white font-medium shadow-xs">
                <ClipboardCheck className="w-3.5 h-3.5 mr-1.5" />
                <span>Take Assessment</span>
              </Button>
            </Link>

            <ThemeToggle />

            {/* Mobile Hamburger Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              type="button"
              className="md:hidden p-1.5 rounded-md text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-slate-200 dark:border-slate-800 bg-white/95 dark:bg-[#07090e]/95 px-4 pt-2 pb-4 space-y-1">
          {NAV_LINKS.map((link) => {
            const isActive = pathname === link.href;
            const Icon = link.icon;
            return (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className={cn(
                  "flex items-center space-x-2.5 px-3 py-2 rounded-md text-xs font-medium",
                  isActive
                    ? "text-teal-600 dark:text-teal-400 bg-teal-500/10 font-semibold"
                    : "text-slate-600 dark:text-slate-400 hover:text-slate-950 dark:hover:text-slate-100"
                )}
              >
                <Icon className="w-4 h-4" />
                <span>{link.label}</span>
              </Link>
            );
          })}
          <div className="pt-2 border-t border-slate-100 dark:border-slate-800 flex justify-between items-center px-1">
            <Link
              href="/about"
              onClick={() => setMobileMenuOpen(false)}
              className="text-xs text-slate-500 dark:text-slate-400 hover:text-slate-900"
            >
              About Project
            </Link>
            <div className="flex items-center space-x-1 text-[11px] font-mono text-emerald-500">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
              <span>ROC-AUC 0.90+ Validated</span>
            </div>
          </div>
        </div>
      )}
    </header>
  );
}

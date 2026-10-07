"use client";

import React from "react";
import { cn } from "@/lib/utils";

export interface RadarPoint {
  skill_key: string;
  skill_name: string;
  user_score: number;
  cohort_benchmark: number;
  importance_rank?: number;
}

interface RadarChartProps {
  data: RadarPoint[];
  size?: number;
  className?: string;
}

export function RadarChart({ data, size = 360, className }: RadarChartProps) {
  if (!data || data.length === 0) return null;

  const cx = size / 2;
  const cy = size / 2;
  const radius = (size / 2) * 0.62;
  const numAxes = data.length;
  const angleStep = (Math.PI * 2) / numAxes;

  // Grid levels (1.0 to 5.0)
  const levels = [1.0, 2.0, 3.0, 4.0, 5.0];

  // Helper to compute (x, y) given an index and a normalized value [0, 5.0]
  const getCoordinates = (index: number, value: number) => {
    const angle = -Math.PI / 2 + index * angleStep;
    const r = (value / 5.0) * radius;
    return {
      x: cx + r * Math.cos(angle),
      y: cy + r * Math.sin(angle),
    };
  };

  // Label coordinates (positioned slightly outside outer ring)
  const getLabelCoordinates = (index: number) => {
    const angle = -Math.PI / 2 + index * angleStep;
    const r = radius + 28;
    return {
      x: cx + r * Math.cos(angle),
      y: cy + r * Math.sin(angle),
    };
  };

  // Build polygon path strings
  const userPoints = data.map((d, i) => getCoordinates(i, d.user_score));
  const userPath = userPoints.map((p) => `${p.x},${p.y}`).join(" ");

  const benchPoints = data.map((d, i) => getCoordinates(i, d.cohort_benchmark));
  const benchPath = benchPoints.map((p) => `${p.x},${p.y}`).join(" ");

  return (
    <div className={cn("flex flex-col items-center select-none", className)}>
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        className="max-w-full h-auto overflow-visible"
        role="img"
        aria-label="Skill radar chart comparing user score to observed cohort benchmark"
      >
        {/* Background Grid Concentric Polygons */}
        {levels.map((lvl) => {
          const points = data
            .map((_, i) => {
              const { x, y } = getCoordinates(i, lvl);
              return `${x},${y}`;
            })
            .join(" ");
          return (
            <g key={lvl}>
              <polygon
                points={points}
                fill="none"
                className="stroke-slate-200/80 dark:stroke-slate-800/80"
                strokeWidth="1"
              />
              {/* Level value on the vertical top axis */}
              <text
                x={cx + 4}
                y={cy - (lvl / 5.0) * radius + 3}
                className="text-[9px] font-mono fill-slate-400 dark:fill-slate-600"
              >
                {lvl.toFixed(0)}
              </text>
            </g>
          );
        })}

        {/* Axis Rays */}
        {data.map((_, i) => {
          const { x, y } = getCoordinates(i, 5.0);
          return (
            <line
              key={i}
              x1={cx}
              y1={cy}
              x2={x}
              y2={y}
              className="stroke-slate-200/90 dark:stroke-slate-800/90"
              strokeWidth="1"
            />
          );
        })}

        {/* High-Hike Benchmark Polygon */}
        <polygon
          points={benchPath}
          fill="rgba(99, 102, 241, 0.12)"
          className="stroke-indigo-500/80 dark:stroke-indigo-400/80"
          strokeWidth="1.75"
          strokeDasharray="4 3"
        />

        {/* Candidate User Polygon */}
        <polygon
          points={userPath}
          fill="rgba(13, 148, 136, 0.25)"
          className="stroke-teal-600 dark:stroke-teal-400"
          strokeWidth="2.5"
        />

        {/* User Vertex Points */}
        {userPoints.map((p, i) => (
          <circle
            key={i}
            cx={p.x}
            cy={p.y}
            r="4.5"
            className="fill-teal-500 stroke-white dark:stroke-slate-900"
            strokeWidth="2"
          />
        ))}

        {/* Axis Labels */}
        {data.map((d, i) => {
          const { x, y } = getLabelCoordinates(i);
          const isRight = i === 1;
          let textAnchor: "middle" | "start" | "end" = "middle";
          if (isRight) textAnchor = "start";
          else if (i === 4) textAnchor = "end";

          return (
            <g key={d.skill_key}>
              <text
                x={x}
                y={y}
                textAnchor={textAnchor}
                className="text-[11px] font-semibold fill-slate-800 dark:fill-slate-200 tracking-tight"
              >
                {d.skill_name}
              </text>
              <text
                x={x}
                y={y + 13}
                textAnchor={textAnchor}
                className="text-[10px] font-mono fill-teal-600 dark:fill-teal-400 font-bold"
              >
                {d.user_score.toFixed(1)} / {d.cohort_benchmark.toFixed(1)}
              </text>
            </g>
          );
        })}
      </svg>

      {/* Legend */}
      <div className="flex items-center space-x-6 mt-4 text-xs">
        <div className="flex items-center space-x-2">
          <span className="w-3 h-3 rounded-full bg-teal-500 border border-teal-600" />
          <span className="text-slate-700 dark:text-slate-300 font-medium">Your Assessment</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-3.5 h-0.5 border-t-2 border-dashed border-indigo-500" />
          <span className="text-slate-500 dark:text-slate-400">Observed High-Hike Benchmark</span>
        </div>
      </div>
    </div>
  );
}

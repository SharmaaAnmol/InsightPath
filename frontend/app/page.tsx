import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-900 p-8 flex flex-col items-center justify-center">
      <div className="max-w-3xl w-full space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-slate-900">InsightPath Web Platform</h1>
            <p className="text-slate-600 mt-1">Evidence-Based Data Science Career-Readiness & Progression System</p>
          </div>
          <Badge variant="secondary" className="px-3 py-1 font-mono text-xs">
            v1.0.0-foundation
          </Badge>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Architecture Foundation</CardTitle>
            <CardDescription>Consuming validated Phases 0–9 data science and machine learning artifacts.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4 text-sm text-slate-700">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="p-4 bg-slate-100 rounded-lg border border-slate-200">
                <span className="font-semibold block text-slate-900">JDS Skill Model</span>
                <span className="text-xs text-slate-500">Logistic L2 Champion (ROC-AUC: 0.9035)</span>
              </div>
              <div className="p-4 bg-slate-100 rounded-lg border border-slate-200">
                <span className="font-semibold block text-slate-900">SDS Personality Model</span>
                <span className="text-xs text-slate-500">Logistic L2 Champion (ROC-AUC: 0.9699)</span>
              </div>
              <div className="p-4 bg-slate-100 rounded-lg border border-slate-200">
                <span className="font-semibold block text-slate-900">Methodological Synthesis</span>
                <span className="text-xs text-slate-500">9 Cross-Dataset Triangulation Tables</span>
              </div>
              <div className="p-4 bg-slate-100 rounded-lg border border-slate-200">
                <span className="font-semibold block text-slate-900">Career Framework</span>
                <span className="text-xs text-slate-500">4-Quadrant Matrix & 4 Stakeholder Blueprints</span>
              </div>
            </div>
            <p className="text-xs text-slate-500 pt-2 border-t border-slate-200">
              Backend API endpoints provide health monitoring, predictive model scoring, and precomputed market tables.
            </p>
          </CardContent>
        </Card>
      </div>
    </main>
  );
}

'use client';
import { useEffect, useState } from 'react';
import { FileText, Download, Loader2, ArrowRight, Gauge, ShieldAlert, TrendingUp, Target, Activity, BriefcaseBusiness, ChartColumn, BadgeCheck } from 'lucide-react';
import Link from 'next/link';

interface Run {
  run_id: string;
  idea: string;
  status: string;
  created_at: string;
  battle_score: number | Record<string, unknown> | null;
  confidence_score: number | Record<string, unknown> | null;
  verdict: string | null;
  has_report: boolean;
}

export default function ReportsPage() {
  const [runs, setRuns] = useState<Run[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const reportSections = ['Market Research', 'SWOT', 'Competitors', 'Pricing', 'Financials', 'GTM', 'Critic', 'Evidence', 'Recommendation'];

  function getMetricValue(value: Run['battle_score'] | Run['confidence_score'], key?: string): number | null {
    if (typeof value === 'number') return value;
    if (value && typeof value === 'object') {
      const raw = key ? (value as Record<string, unknown>)[key] : (value as Record<string, unknown>).composite_score;
      const num = typeof raw === 'number' ? raw : Number(raw);
      return Number.isFinite(num) ? num : null;
    }
    return null;
  }

  function getTextValue(value: Run['battle_score'] | Run['confidence_score'], key: string): string {
    if (value && typeof value === 'object') {
      const raw = (value as Record<string, unknown>)[key];
      return raw === undefined || raw === null ? '--' : String(raw);
    }
    return '--';
  }

  function MetricCard({ label, value, suffix, icon: Icon, tone }: { label: string; value: string | number | null; suffix?: string; icon: any; tone: string; }) {
    return (
      <div className="rounded-2xl border border-zinc-800/80 bg-zinc-900/60 p-4 shadow-lg shadow-black/10">
        <div className="flex items-center gap-2 text-zinc-400 mb-2">
          <Icon className={`w-4 h-4 ${tone}`} />
          <span className="text-xs font-semibold uppercase tracking-wider">{label}</span>
        </div>
        <div className="text-lg font-bold text-white">
          {value ?? '--'}
          {suffix && value !== null && <span className="ml-1 text-sm text-zinc-500">{suffix}</span>}
        </div>
      </div>
    );
  }

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const res = await fetch(`${API_URL}/api/v1/runs/`);
        if (!res.ok) throw new Error('Failed to fetch reports');
        const data = await res.json();
        // Filter runs that have a report
        setRuns((data.runs || []).filter((r: Run) => r.has_report));
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'Failed to fetch reports');
      } finally {
        setLoading(false);
      }
    };
    fetchReports();
  }, [API_URL]);

  return (
    <div className="min-h-screen py-12 md:py-20">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-10">
          <h1 className="text-3xl font-bold text-white mb-2">Executive Reports</h1>
          <p className="text-zinc-400">View and download completed startup analysis reports.</p>
        </div>

        {loading && (
          <div className="flex justify-center p-12">
            <Loader2 className="w-8 h-8 animate-spin text-indigo-500" />
          </div>
        )}

        {error && (
          <div className="glass-card p-6 border-red-900/50 bg-red-900/10 text-red-400">
            Error loading reports: {error}
          </div>
        )}

        {!loading && !error && runs.length === 0 && (
          <div className="glass-card p-12 text-center">
            <FileText className="w-14 h-14 text-zinc-700 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-zinc-400 mb-2">No Reports Yet</h3>
            <p className="text-sm text-zinc-500 max-w-sm mx-auto mb-6">
              Run a startup analysis from the Battlefield page. Reports will appear here after completion.
            </p>
            <Link href="/analyze" className="inline-flex items-center gap-2 px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-sm font-semibold transition-colors">
              Analyze a Startup <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        )}

        {!loading && !error && runs.length > 0 && (
          <div className="grid gap-6">
            {runs.map((run) => (
              <div key={run.run_id} className="glass-card p-6 flex flex-col md:flex-row gap-6 items-start md:items-center justify-between hover:border-zinc-700 transition-colors">
                
                {/* Info */}
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-900/30 text-emerald-400 border border-emerald-800/50">
                      Report Ready
                    </span>
                    <span className="text-xs text-zinc-500 font-mono">
                      {new Date(run.created_at).toLocaleString()}
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-white mb-1 line-clamp-1" title={run.idea}>
                    {run.idea || 'Unknown Startup Idea'}
                  </h3>
                  <div className="flex flex-wrap gap-x-6 gap-y-2 mt-3">
                    <div className="flex flex-col">
                      <span className="text-xs text-zinc-500 uppercase">Score</span>
                      <span className="text-sm font-semibold text-white">{getMetricValue(run.battle_score, 'composite_score') ?? getMetricValue(run.battle_score) ?? '--'}/100</span>
                    </div>
                    <div className="flex flex-col">
                      <span className="text-xs text-zinc-500 uppercase">Confidence</span>
                      <span className="text-sm font-semibold text-white">
                        {(() => {
                          const confidence = getMetricValue(run.confidence_score, 'overall_confidence');
                          return confidence !== null ? `${(confidence * 100).toFixed(0)}%` : '--';
                        })()}
                      </span>
                    </div>
                    <div className="flex flex-col">
                      <span className="text-xs text-zinc-500 uppercase">Verdict</span>
                      <span className="text-sm font-semibold text-indigo-400">{run.verdict}</span>
                    </div>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 mt-4">
                    <MetricCard label="Composite Score" value={getMetricValue(run.battle_score, 'composite_score') ?? getMetricValue(run.battle_score)} suffix="/100" icon={Gauge} tone="text-indigo-400" />
                    <MetricCard label="Risk Level" value={getTextValue(run.battle_score, 'risk_level')} icon={ShieldAlert} tone="text-rose-400" />
                    <MetricCard label="Market Opportunity" value={getMetricValue(run.battle_score, 'market_opportunity')} icon={TrendingUp} tone="text-emerald-400" />
                    <MetricCard label="Revenue Potential" value={getMetricValue(run.battle_score, 'revenue_potential')} icon={Target} tone="text-sky-400" />
                    <MetricCard label="Execution Complexity" value={getMetricValue(run.battle_score, 'execution_complexity')} icon={Activity} tone="text-amber-400" />
                    <MetricCard label="Investment Readiness" value={getMetricValue(run.battle_score, 'investment_readiness')} icon={BriefcaseBusiness} tone="text-violet-400" />
                    <MetricCard label="Competition Difficulty" value={getMetricValue(run.battle_score, 'competition_difficulty')} icon={ChartColumn} tone="text-fuchsia-400" />
                    <MetricCard label="Confidence" value={getMetricValue(run.confidence_score, 'overall_confidence') !== null ? `${((getMetricValue(run.confidence_score, 'overall_confidence') ?? 0) * 100).toFixed(0)}%` : '--'} icon={BadgeCheck} tone="text-emerald-400" />
                  </div>
                  <div className="flex flex-wrap gap-2 mt-4">
                    {reportSections.map((section) => (
                      <span key={section} className="px-2 py-1 rounded-md text-xs bg-zinc-800/70 text-zinc-300 border border-zinc-700">
                        {section}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Actions */}
                <div className="flex flex-wrap gap-2 shrink-0">
                  <a
                    href={`${API_URL}/outputs/reports/report_${run.run_id}.pdf`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-semibold transition-colors"
                  >
                    <Download className="w-4 h-4" /> PDF
                  </a>
                  <a
                    href={`${API_URL}/outputs/reports/report_${run.run_id}.md`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 border border-zinc-700 rounded-lg text-sm font-medium transition-colors"
                  >
                    <Download className="w-4 h-4" /> MD
                  </a>
                  <a
                    href={`${API_URL}/outputs/reports/report_${run.run_id}.json`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 border border-zinc-700 rounded-lg text-sm font-medium transition-colors"
                  >
                    <Download className="w-4 h-4" /> JSON
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

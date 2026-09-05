'use client';
import { useEffect, useState } from 'react';
import { FileText, Download, Loader2, ArrowRight, Search, RefreshCw } from 'lucide-react';
import Link from 'next/link';
import { VerdictBadge, StatusBadge } from '@/components/ui/Badge';
import { EmptyState, LoadingState, ErrorState } from '@/components/ui/States';
import { deriveDisplayName } from '@/components/ui/MarkdownRenderer';

interface Run {
  run_id: string;
  idea: string;
  status: string;
  created_at: string;
  battle_score: number | Record<string, unknown> | null;
  confidence_score: number | null;
  verdict: string | null;
  has_report: boolean;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

function getScore(val: Run['battle_score']): number | null {
  if (typeof val === 'number') return val;
  if (val && typeof val === 'object') {
    const cs = (val as Record<string, unknown>).composite_score;
    const n = Number(cs);
    return Number.isFinite(n) ? n : null;
  }
  return null;
}

function ScoreBubble({ score }: { score: number | null }) {
  if (score === null) return <span style={{ color: 'var(--text-tertiary)', fontSize: 13 }}>—</span>;
  const color = score >= 65 ? 'var(--success)' : score >= 40 ? 'var(--warning)' : 'var(--danger)';
  const bg    = score >= 65 ? 'var(--success-light)' : score >= 40 ? 'var(--warning-light)' : 'var(--danger-light)';
  const border= score >= 65 ? 'var(--success-border)': score >= 40 ? 'var(--warning-border)': 'var(--danger-border)';
  return (
    <span style={{ display: 'inline-flex', alignItems: 'baseline', gap: 2, padding: '3px 10px', borderRadius: 100, background: bg, border: `1px solid ${border}`, fontWeight: 700, fontSize: 13, color }}>
      {score}<span style={{ fontSize: 11, fontWeight: 400, color: 'var(--text-tertiary)' }}>/100</span>
    </span>
  );
}

export default function ReportsPage() {
  const [runs, setRuns] = useState<Run[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');

  const fetchReports = async () => {
    setLoading(true); setError(null);
    try {
      const res = await fetch(`${API_URL}/api/v1/runs/`);
      if (!res.ok) throw new Error(`Server error ${res.status}`);
      const data = await res.json();
      setRuns((data.runs || []).filter((r: Run) => r.has_report));
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to fetch reports');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchReports(); }, []);

  const filtered = runs.filter(r =>
    r.idea?.toLowerCase().includes(search.toLowerCase()) ||
    r.run_id.includes(search)
  );

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-page)', padding: '40px 0 64px' }}>
      <div className="container">

        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: 16, marginBottom: 32 }}>
          <div>
            <div className="section-label">Report Library</div>
            <h1 style={{ fontSize: 28, fontWeight: 800, color: 'var(--text-primary)', margin: '0 0 6px', letterSpacing: '-0.02em' }}>
              Executive Reports
            </h1>
            <p style={{ fontSize: 14, color: 'var(--text-secondary)', margin: 0 }}>
              Download comprehensive 21-section startup analysis reports as PDF, Markdown or JSON.
            </p>
          </div>
          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <div style={{ position: 'relative' }}>
              <Search className="w-4 h-4" style={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-tertiary)' }} />
              <input
                type="text" value={search} onChange={e => setSearch(e.target.value)}
                placeholder="Search reports…" className="input-field"
                style={{ paddingLeft: 32, width: 220, fontSize: 13 }}
              />
            </div>
            <button onClick={fetchReports} className="btn btn-secondary btn-sm btn-icon" title="Refresh">
              <RefreshCw className="w-4 h-4" />
            </button>
            <Link href="/analyze" className="btn btn-primary btn-sm" style={{ textDecoration: 'none' }}>
              New Analysis <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>

        {/* States */}
        {loading && <div className="card"><LoadingState message="Loading reports…" /></div>}
        {error && <ErrorState message={error} />}
        {!loading && !error && runs.length === 0 && (
          <div className="card">
            <EmptyState
              icon={FileText}
              title="No reports yet"
              description="Complete a startup analysis on the Battlefield to generate your first executive report."
              actionLabel="Analyze a startup"
              actionHref="/analyze"
            />
          </div>
        )}
        {!loading && !error && runs.length > 0 && filtered.length === 0 && (
          <div className="card" style={{ padding: '32px', textAlign: 'center' }}>
            <p style={{ fontSize: 14, color: 'var(--text-secondary)' }}>No reports match "<strong>{search}</strong>"</p>
          </div>
        )}

        {/* Report cards */}
        {!loading && !error && filtered.length > 0 && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {filtered.map(run => {
              const score = getScore(run.battle_score);
              const name = deriveDisplayName(run.idea, 60);
              return (
                <div key={run.run_id} className="card card-hover" style={{ padding: '20px 24px' }}>
                  <div style={{ display: 'flex', gap: 20, alignItems: 'flex-start', flexWrap: 'wrap' }}>
                    {/* Info */}
                    <div style={{ flex: 1, minWidth: 240 }}>
                      {/* Badges row */}
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 8 }}>
                        <span className="badge badge-green">Report Ready</span>
                        <VerdictBadge verdict={run.verdict} />
                        <ScoreBubble score={score} />
                      </div>
                      <h2 style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-primary)', margin: '0 0 4px', lineHeight: 1.4 }}
                        title={run.idea}>
                        {name}
                      </h2>
                      <p style={{ fontSize: 12, color: 'var(--text-tertiary)', margin: '0 0 12px' }}>
                        {new Date(run.created_at).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' })}
                        {' · '}
                        <span style={{ fontFamily: 'monospace' }}>{run.run_id.slice(0, 8)}…</span>
                      </p>
                      {run.idea && run.idea !== name && (
                        <p style={{ fontSize: 13, color: 'var(--text-secondary)', margin: 0, lineHeight: 1.5, overflow: 'hidden', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical' }}>
                          {run.idea}
                        </p>
                      )}
                    </div>

                    {/* Actions */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 8, flexShrink: 0 }}>
                      <a
                        href={`${API_URL}/outputs/reports/report_${run.run_id}.pdf`}
                        target="_blank" rel="noopener noreferrer"
                        className="btn btn-primary btn-sm"
                        style={{ textDecoration: 'none', justifyContent: 'center' }}
                      >
                        <Download className="w-3.5 h-3.5" /> PDF Report
                      </a>
                      <div style={{ display: 'flex', gap: 6 }}>
                        <a href={`${API_URL}/outputs/reports/report_${run.run_id}.md`} target="_blank" rel="noopener noreferrer" className="btn btn-secondary btn-sm" style={{ textDecoration: 'none', flex: 1, justifyContent: 'center' }}>
                          <Download className="w-3 h-3" /> MD
                        </a>
                        <a href={`${API_URL}/outputs/reports/report_${run.run_id}.json`} target="_blank" rel="noopener noreferrer" className="btn btn-secondary btn-sm" style={{ textDecoration: 'none', flex: 1, justifyContent: 'center' }}>
                          <Download className="w-3 h-3" /> JSON
                        </a>
                      </div>
                      <Link href={`/battlefield?run_id=${run.run_id}`} className="btn btn-ghost btn-sm" style={{ textDecoration: 'none', justifyContent: 'center', fontSize: 12 }}>
                        View Analysis →
                      </Link>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

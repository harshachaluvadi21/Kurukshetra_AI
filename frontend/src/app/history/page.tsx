'use client';
import { useEffect, useState } from 'react';
import { Clock, ExternalLink, FileText, Search, RefreshCw, Swords } from 'lucide-react';
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

function ScoreCell({ score }: { score: number | null }) {
  if (score === null) return <span style={{ color: 'var(--text-tertiary)' }}>—</span>;
  const color = score >= 65 ? 'var(--success)' : score >= 40 ? 'var(--warning)' : 'var(--danger)';
  return <span style={{ fontWeight: 700, color }}>{score}<span style={{ fontSize: 11, fontWeight: 400, color: 'var(--text-tertiary)' }}>/100</span></span>;
}

export default function HistoryPage() {
  const [runs, setRuns] = useState<Run[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');

  const fetchHistory = async () => {
    setLoading(true); setError(null);
    try {
      const res = await fetch(`${API_URL}/api/v1/runs/`);
      if (!res.ok) throw new Error(`Server error ${res.status}`);
      const data = await res.json();
      setRuns(data.runs || []);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to fetch history');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchHistory(); }, []);

  const filtered = runs.filter(r =>
    r.idea?.toLowerCase().includes(search.toLowerCase()) ||
    r.run_id.includes(search)
  );

  const completedCount = runs.filter(r => r.status === 'completed').length;
  const avgScore = (() => {
    const scores = runs.map(r => getScore(r.battle_score)).filter((s): s is number => s !== null);
    return scores.length > 0 ? (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(0) : null;
  })();

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-page)', padding: '40px 0 64px' }}>
      <div className="container">

        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: 16, marginBottom: 24 }}>
          <div>
            <div className="section-label">Analysis History</div>
            <h1 style={{ fontSize: 28, fontWeight: 800, color: 'var(--text-primary)', margin: '0 0 4px', letterSpacing: '-0.02em' }}>
              History
            </h1>
            <p style={{ fontSize: 14, color: 'var(--text-secondary)', margin: 0 }}>All your startup battle analyses.</p>
          </div>
          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <div style={{ position: 'relative' }}>
              <Search className="w-4 h-4" style={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-tertiary)' }} />
              <input type="text" value={search} onChange={e => setSearch(e.target.value)} placeholder="Search…" className="input-field" style={{ paddingLeft: 32, width: 200, fontSize: 13 }} />
            </div>
            <button onClick={fetchHistory} className="btn btn-secondary btn-sm btn-icon"><RefreshCw className="w-4 h-4" /></button>
            <Link href="/analyze" className="btn btn-primary btn-sm" style={{ textDecoration: 'none' }}>New Analysis</Link>
          </div>
        </div>

        {/* Stats row */}
        {runs.length > 0 && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12, marginBottom: 24 }}>
            {[
              { label: 'Total Runs',    value: runs.length },
              { label: 'Completed',     value: completedCount },
              { label: 'With Reports',  value: runs.filter(r => r.has_report).length },
              { label: 'Avg. Score',    value: avgScore ? `${avgScore}/100` : '—' },
            ].map(s => (
              <div key={s.label} className="metric-card">
                <div className="metric-card-label">{s.label}</div>
                <div className="metric-card-value" style={{ fontSize: 22 }}>{s.value}</div>
              </div>
            ))}
          </div>
        )}

        {/* States */}
        {loading && <div className="card"><LoadingState message="Loading history…" /></div>}
        {error && <ErrorState message={error} />}
        {!loading && !error && runs.length === 0 && (
          <div className="card">
            <EmptyState icon={Swords} title="No analysis history" description="Your completed startup analyses will appear here." actionLabel="Analyze a startup" actionHref="/analyze" />
          </div>
        )}

        {/* Table */}
        {!loading && !error && filtered.length > 0 && (
          <div className="card" style={{ overflow: 'hidden' }}>
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}>
                    {['Startup Idea', 'Status', 'Score', 'Verdict', 'Date', 'Actions'].map(h => (
                      <th key={h} style={{ padding: '10px 16px', textAlign: 'left', fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--text-secondary)', background: 'var(--bg-subtle)', whiteSpace: 'nowrap' }}>
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {filtered.map(run => (
                    <tr key={run.run_id} style={{ borderBottom: '1px solid var(--border)' }}
                      onMouseEnter={e => (e.currentTarget.style.background = 'var(--bg-hover)')}
                      onMouseLeave={e => (e.currentTarget.style.background = 'transparent')}>
                      <td style={{ padding: '12px 16px', maxWidth: 320 }}>
                        <p style={{ fontSize: 14, fontWeight: 600, color: 'var(--text-primary)', margin: '0 0 2px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                          {deriveDisplayName(run.idea, 55)}
                        </p>
                        <p style={{ fontSize: 11, color: 'var(--text-tertiary)', margin: 0, fontFamily: 'monospace' }}>
                          {run.run_id.slice(0, 12)}…
                        </p>
                      </td>
                      <td style={{ padding: '12px 16px', whiteSpace: 'nowrap' }}>
                        <StatusBadge status={run.status} />
                      </td>
                      <td style={{ padding: '12px 16px', whiteSpace: 'nowrap' }}>
                        <ScoreCell score={getScore(run.battle_score)} />
                      </td>
                      <td style={{ padding: '12px 16px', whiteSpace: 'nowrap' }}>
                        {run.verdict ? <VerdictBadge verdict={run.verdict} /> : <span style={{ color: 'var(--text-tertiary)', fontSize: 13 }}>—</span>}
                      </td>
                      <td style={{ padding: '12px 16px', whiteSpace: 'nowrap', fontSize: 13, color: 'var(--text-secondary)' }}>
                        {new Date(run.created_at).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })}
                      </td>
                      <td style={{ padding: '12px 16px', whiteSpace: 'nowrap' }}>
                        <div style={{ display: 'flex', gap: 4, alignItems: 'center' }}>
                          {run.has_report && (
                            <Link href="/reports" title="View report" className="btn btn-ghost btn-sm btn-icon" style={{ textDecoration: 'none' }}>
                              <FileText className="w-3.5 h-3.5" />
                            </Link>
                          )}
                          <Link href={`/battlefield?run_id=${run.run_id}`} title="Open in Battlefield" className="btn btn-secondary btn-sm" style={{ textDecoration: 'none', fontSize: 12 }}>
                            Open <ExternalLink className="w-3 h-3" />
                          </Link>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {filtered.length === 0 && (
              <div style={{ padding: '32px', textAlign: 'center' }}>
                <p style={{ fontSize: 14, color: 'var(--text-secondary)', margin: 0 }}>No runs match "<strong>{search}</strong>"</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

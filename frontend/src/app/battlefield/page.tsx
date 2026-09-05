'use client';
import { useState, useEffect, Suspense, useCallback } from 'react';
import { useSearchParams } from 'next/navigation';
import {
  Play, RotateCcw, Plug, Loader2,
  Download, Terminal, MessageSquare, ChevronDown, ChevronRight,
  Swords, CheckCircle2, Circle, Eye, Brain, FileText,
  TrendingUp, ShieldAlert, Users, Sparkles, Gauge, BarChart3,
  Globe, AlertTriangle, Zap, RefreshCw, ArrowRight
} from 'lucide-react';
import Link from 'next/link';

import { useBattlefieldSocket } from '@/hooks/useBattlefieldSocket';
import { useBattlefieldStore } from '@/stores/battlefieldStore';
import { MetricCard, ScoreDisplay } from '@/components/ui/MetricCard';
import { ScoreBar } from '@/components/ui/ScoreBar';
import { VerdictBadge } from '@/components/ui/Badge';
import { EmptyState, LoadingState, ErrorState } from '@/components/ui/States';
import { MarkdownRenderer, deriveDisplayName } from '@/components/ui/MarkdownRenderer';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/* ─── Types ─── */
type TabId = 'overview' | 'market' | 'competition' | 'financials' | 'strategy' | 'risks' | 'report';

interface ReportSection { title: string; content_markdown?: string; }
interface ReportData {
  sections?: ReportSection[];
  executive_summary?: ReportSection;
  market_research?: ReportSection;
  market_analysis?: ReportSection;
  swot_analysis?: ReportSection;
  competitor_analysis?: ReportSection;
  pricing_strategy?: ReportSection;
  financial_analysis?: ReportSection;
  go_to_market_strategy?: ReportSection;
  critic_analysis?: ReportSection;
  risk_analysis?: ReportSection;
  evidence_citations?: ReportSection;
  final_recommendation?: ReportSection;
  recommendations?: ReportSection;
  target_market?: string;
  currency_symbol?: string;
  [key: string]: unknown;
}

/* ─── Helpers ─── */
function getReport(finalReport: unknown): ReportData | null {
  if (!finalReport || typeof finalReport !== 'object') return null;
  const r = finalReport as Record<string, unknown>;
  if (r.final_report && typeof r.final_report === 'object') return r.final_report as ReportData;
  return finalReport as ReportData;
}

function extractBullets(section: ReportSection | null | undefined, heading?: string): string[] {
  const content = section?.content_markdown || '';
  if (!content) return [];
  if (!heading) {
    return content.split('\n').filter(l => l.trim().startsWith('- ')).map(l => l.trim().slice(2).trim()).slice(0, 5);
  }
  const pattern = new RegExp(`\\*\\*${heading}\\*\\*[\\s\\S]*?(?=\\n\\*\\*|$)`);
  const match = content.match(pattern);
  if (!match) return [];
  return match[0].split('\n').filter(l => l.trim().startsWith('- ')).map(l => l.trim().slice(2).trim()).filter(Boolean).slice(0, 5);
}

function getScoreColor(score: number | null): string {
  if (score === null) return 'var(--text-tertiary)';
  if (score >= 65) return 'var(--success)';
  if (score >= 40) return 'var(--warning)';
  return 'var(--danger)';
}

/* ─── Sub-components ─── */

function ProgressBar({ label, steps }: { label: string; steps: { label: string; done: boolean; active: boolean }[] }) {
  return (
    <div className="card" style={{ padding: '20px 24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 20 }}>
        <Loader2 className="w-4 h-4 animate-spin" style={{ color: 'var(--accent)' }} />
        <span style={{ fontSize: 14, fontWeight: 600, color: 'var(--text-primary)' }}>{label}</span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 0 }}>
        {steps.map((step, i) => (
          <div key={step.label} style={{ display: 'flex', alignItems: 'center', flex: 1 }}>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', flex: 1 }}>
              <div style={{ width: 28, height: 28, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', background: step.done ? 'var(--success-light)' : step.active ? 'var(--accent-light)' : 'var(--bg-subtle)', border: `2px solid ${step.done ? 'var(--success)' : step.active ? 'var(--accent)' : 'var(--border-strong)'}`, marginBottom: 6 }}>
                {step.done
                  ? <CheckCircle2 className="w-3.5 h-3.5" style={{ color: 'var(--success)' }} />
                  : step.active
                    ? <Loader2 className="w-3.5 h-3.5 animate-spin" style={{ color: 'var(--accent)' }} />
                    : <Circle className="w-3.5 h-3.5" style={{ color: 'var(--border-strong)' }} />
                }
              </div>
              <span style={{ fontSize: 11, color: step.done ? 'var(--text-secondary)' : step.active ? 'var(--accent-text)' : 'var(--text-tertiary)', fontWeight: step.active ? 600 : 400 }}>{step.label}</span>
            </div>
            {i < steps.length - 1 && (
              <div style={{ height: 2, flex: 1, background: step.done ? 'var(--success)' : 'var(--border)', margin: '0 4px', marginTop: -16 }} />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

function SwotPanel({ report }: { report: ReportData | null }) {
  const s = extractBullets(report?.swot_analysis, 'Strengths');
  const w = extractBullets(report?.swot_analysis, 'Weaknesses');
  const o = extractBullets(report?.swot_analysis, 'Opportunities');
  const t = extractBullets(report?.swot_analysis, 'Threats');

  const cells = [
    { key: 'S', label: 'Strengths',     items: s, cellClass: 'swot-cell-strengths',     labelClass: 'swot-label-s', dotColor: '#15803D' },
    { key: 'W', label: 'Weaknesses',    items: w, cellClass: 'swot-cell-weaknesses',    labelClass: 'swot-label-w', dotColor: '#B45309' },
    { key: 'O', label: 'Opportunities', items: o, cellClass: 'swot-cell-opportunities', labelClass: 'swot-label-o', dotColor: '#1D4ED8' },
    { key: 'T', label: 'Threats',       items: t, cellClass: 'swot-cell-threats',       labelClass: 'swot-label-t', dotColor: '#BE123C' },
  ];

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <h3 style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-primary)', margin: '0 0 4px' }}>SWOT Analysis</h3>
        <p style={{ fontSize: 13, color: 'var(--text-secondary)', margin: 0 }}>Extracted from research and critique layers</p>
      </div>
      <div className="swot-grid">
        {cells.map(cell => (
          <div key={cell.key} className={`swot-cell ${cell.cellClass}`}>
            <div className={`swot-label ${cell.labelClass}`}>{cell.label}</div>
            {cell.items.length > 0
              ? cell.items.map((item, i) => (
                  <div key={i} className="swot-item">
                    <div className="swot-item-dot" style={{ background: cell.dotColor }} />
                    <span>{item.replace(/\*\*/g, '')}</span>
                  </div>
                ))
              : <p style={{ fontSize: 12, color: 'var(--text-tertiary)', fontStyle: 'italic', margin: 0 }}>Not generated</p>
            }
          </div>
        ))}
      </div>
    </div>
  );
}

function DebatePanel({ history }: { history: { speaker: string; message: string; timestamp: string }[] }) {
  if (history.length === 0) {
    return <EmptyState icon={MessageSquare} title="No debate yet" description="Agents will debate once research is complete." />;
  }
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      {history.map((turn, i) => {
        const cls = turn.speaker === 'Proponent' ? 'debate-proponent' : turn.speaker === 'Skeptic' ? 'debate-skeptic' : 'debate-judge';
        const color = turn.speaker === 'Proponent' ? 'var(--success-text)' : turn.speaker === 'Skeptic' ? 'var(--danger-text)' : 'var(--accent-text)';
        return (
          <div key={i} className={`card ${cls}`} style={{ padding: '14px 16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
              <span style={{ fontSize: 11, fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.07em', color }}>
                {turn.speaker}
              </span>
              <span style={{ fontSize: 11, color: 'var(--text-tertiary)' }}>
                {new Date(turn.timestamp).toLocaleTimeString()}
              </span>
            </div>
            <p style={{ fontSize: 13, color: 'var(--text-secondary)', margin: 0, lineHeight: 1.65 }}>{turn.message}</p>
          </div>
        );
      })}
    </div>
  );
}

function EventLog({ events }: { events: import('@/stores/battlefieldStore').AppEvent[] }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="card" style={{ overflow: 'hidden' }}>
      <button
        onClick={() => setOpen(!open)}
        style={{ width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '14px 20px', background: 'none', border: 'none', cursor: 'pointer' }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Terminal className="w-4 h-4" style={{ color: 'var(--success)' }} />
          <span style={{ fontSize: 14, fontWeight: 600, color: 'var(--text-primary)' }}>Event Log</span>
          <span className="badge badge-slate">{events.length}</span>
        </div>
        {open ? <ChevronDown className="w-4 h-4" style={{ color: 'var(--text-tertiary)' }} /> : <ChevronRight className="w-4 h-4" style={{ color: 'var(--text-tertiary)' }} />}
      </button>
      {open && (
        <div style={{ maxHeight: 240, overflowY: 'auto', borderTop: '1px solid var(--border)', background: '#FAFAFA', padding: '12px 16px', fontFamily: 'monospace', fontSize: 12 }}>
          {events.length === 0 && <p style={{ color: 'var(--text-tertiary)', margin: 0 }}>No events yet.</p>}
          {events.map((ev, i) => {
            const data = ev.data as Record<string, unknown>;
            const msg = data?.message ? String(data.message) : ev.event_type;
            const agent = data?.agent_name ? String(data.agent_name) : '';
            let color = 'var(--text-secondary)';
            if (ev.event_type.includes('error')) color = 'var(--danger)';
            else if (ev.event_type.includes('completed')) color = 'var(--success)';
            else if (ev.event_type.includes('thinking')) color = 'var(--warning)';
            return (
              <div key={i} style={{ display: 'flex', gap: 10, marginBottom: 4, lineHeight: 1.5 }}>
                <span style={{ color: 'var(--text-tertiary)', flexShrink: 0 }}>{new Date(ev.timestamp).toLocaleTimeString()}</span>
                <span style={{ color: 'var(--accent)', flexShrink: 0 }}>{ev.event_type}</span>
                <span style={{ color }}>{agent ? <strong>{agent}:</strong> : ''} {msg}</span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

/* ─── 21-Section Report Reader ─── */
const SECTION_KEYS_ORDERED = [
  'executive_summary', 'market_research', 'market_analysis', 'swot_analysis',
  'competitor_analysis', 'pricing_strategy', 'financial_analysis',
  'go_to_market_strategy', 'critic_analysis', 'risk_analysis',
  'evidence_citations', 'final_recommendation', 'recommendations',
];

function ReportReader({ report }: { report: ReportData | null }) {
  const [activeSection, setActiveSection] = useState(0);

  if (!report) {
    return <EmptyState icon={FileText} title="No report yet" description="Complete an analysis to generate the full 21-section report." />;
  }

  // Build section list
  let sections: ReportSection[] = [];
  if (report.sections && report.sections.length > 0) {
    sections = report.sections;
  } else {
    for (const key of SECTION_KEYS_ORDERED) {
      const s = report[key] as ReportSection | undefined;
      if (s?.title) sections.push(s);
    }
  }

  if (sections.length === 0) {
    return <EmptyState icon={FileText} title="Report sections not found" description="The report data format may differ. Try downloading the PDF." />;
  }

  const current = sections[activeSection];

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '220px 1fr', gap: 24, alignItems: 'start' }}>
      {/* Sidebar */}
      <div className="card" style={{ padding: '12px 8px', position: 'sticky', top: 80 }}>
        <p style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-tertiary)', padding: '4px 12px 8px', margin: 0 }}>
          Sections
        </p>
        <div style={{ maxHeight: 'calc(100vh - 200px)', overflowY: 'auto' }}>
          {sections.map((sec, i) => (
            <button
              key={i}
              onClick={() => setActiveSection(i)}
              className={`report-nav-item ${i === activeSection ? 'active' : ''}`}
            >
              <span className="report-nav-num">{String(i + 1).padStart(2, '0')}</span>
              <span style={{ fontSize: 12, lineHeight: 1.4 }}>{sec.title}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="card" style={{ padding: 32, minHeight: 400 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 24, paddingBottom: 16, borderBottom: '1px solid var(--border)' }}>
          <div style={{ width: 36, height: 36, borderRadius: 8, background: 'var(--accent-light)', border: '1px solid var(--accent-border)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, fontSize: 12, color: 'var(--accent-text)', flexShrink: 0 }}>
            {String(activeSection + 1).padStart(2, '0')}
          </div>
          <h2 style={{ fontSize: 18, fontWeight: 700, color: 'var(--text-primary)', margin: 0 }}>{current.title}</h2>
        </div>
        <MarkdownRenderer content={current.content_markdown} suppressTitle={current.title} />

        {/* Navigation */}
        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 32, paddingTop: 16, borderTop: '1px solid var(--border)' }}>
          <button
            onClick={() => setActiveSection(Math.max(0, activeSection - 1))}
            disabled={activeSection === 0}
            className="btn btn-secondary btn-sm"
          >
            ← Previous
          </button>
          <span style={{ fontSize: 13, color: 'var(--text-tertiary)' }}>
            {activeSection + 1} / {sections.length}
          </span>
          <button
            onClick={() => setActiveSection(Math.min(sections.length - 1, activeSection + 1))}
            disabled={activeSection === sections.length - 1}
            className="btn btn-primary btn-sm"
          >
            Next →
          </button>
        </div>
      </div>
    </div>
  );
}

/* ─── Main Content ─── */
function BattlefieldContent() {
  const searchParams = useSearchParams();
  const urlRunId = searchParams.get('run_id');

  const {
    isRunning, setIsRunning, runId, setRunId, reportLinks,
    battleScore, confidenceScore, verdict, pivotMandated,
    events, debateHistory, setFinalState,
  } = useBattlefieldStore();

  const finalReport = useBattlefieldStore(s => s.finalReport);
  const report = getReport(finalReport);
  const reset = useBattlefieldStore(s => s.reset);

  const [isMockMode, setIsMockMode] = useState(false);
  const [startupIdea, setStartupIdea] = useState('');
  const [problemStatement, setProblemStatement] = useState('');
  const [targetUsers, setTargetUsers] = useState('');
  const [revenueModel, setRevenueModel] = useState('');
  const [activeTab, setActiveTab] = useState<TabId>('overview');
  const [inputOpen, setInputOpen] = useState(true);

  const { isConnected, triggerMockReplay } = useBattlefieldSocket(runId, isMockMode);

  // Load from sessionStorage
  useEffect(() => {
    const saved = sessionStorage.getItem('kurukshetra_idea');
    if (!saved || urlRunId) return;
    try {
      const p = JSON.parse(saved);
      setStartupIdea(p.idea || '');
      setProblemStatement(p.problemStatement || '');
      setTargetUsers(p.targetUsers || '');
      setRevenueModel(p.revenueModel || '');
      sessionStorage.removeItem('kurukshetra_idea');
    } catch { /* noop */ }
  }, [urlRunId]);

  // Load existing run
  useEffect(() => {
    if (!urlRunId || urlRunId === runId) return;
    setRunId(urlRunId);
    setInputOpen(false);
    fetch(`${API_URL}/api/v1/runs/${urlRunId}`)
      .then(r => r.json())
      .then(data => {
        if (data.final_state) {
          setFinalState(data.final_state);
          const fs = data.final_state;
          if (fs.battle_score) useBattlefieldStore.setState({ battleScore: fs.battle_score.composite_score, pivotMandated: fs.battle_score.pivot_mandated });
          if (fs.confidence_score) useBattlefieldStore.setState({ confidenceScore: fs.confidence_score.overall_confidence });
          if (fs.battle_verdict) useBattlefieldStore.setState({ verdict: fs.battle_verdict });
          if (fs.startup_idea) {
            setStartupIdea(fs.startup_idea.business_concept || fs.startup_idea.company_name || '');
            setProblemStatement(fs.startup_idea.problem_statement || '');
            setTargetUsers(fs.startup_idea.target_users || '');
            setRevenueModel(fs.startup_idea.revenue_model || '');
          }
          if (fs.final_report) {
            useBattlefieldStore.setState({
              reportLinks: {
                pdf_path: `/outputs/reports/report_${urlRunId}.pdf`,
                md_path:  `/outputs/reports/report_${urlRunId}.md`,
                json_path:`/outputs/reports/report_${urlRunId}.json`,
              }
            });
          }
        }
      })
      .catch(console.error);
  }, [urlRunId, runId, setFinalState, setRunId]);

  // Load JSON report once links are available
  useEffect(() => {
    if (!reportLinks?.json_path) return;
    fetch(`${API_URL}${reportLinks.json_path}`)
      .then(r => r.json())
      .then(data => { setFinalState({ final_report: data }); setActiveTab('report'); })
      .catch(console.error);
  }, [reportLinks?.json_path, setFinalState]);

  const handleStart = async () => {
    reset();
    setInputOpen(false);
    if (isMockMode) { triggerMockReplay(); return; }
    setIsRunning(true);
    try {
      const res = await fetch(`${API_URL}/api/v1/runs/`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ project_id: '00000000-0000-0000-0000-000000000000', idea: startupIdea, problem_statement: problemStatement, target_users: targetUsers, revenue_model: revenueModel }),
      });
      if (!res.ok) throw new Error('Failed to create run');
      const data = await res.json();
      if (data.run_id) {
        setRunId(data.run_id);
        const execRes = await fetch(`${API_URL}/api/v1/runs/${data.run_id}/execute`, { method: 'POST', headers: { 'Content-Type': 'application/json' } });
        if (!execRes.ok) throw new Error('Failed to execute run');
      }
    } catch (err) {
      console.error(err);
      setIsRunning(false);
      setInputOpen(true);
      alert('Failed to start analysis. Please check that the backend is running.');
    }
  };

  const displayName = deriveDisplayName(startupIdea || report?.executive_summary?.content_markdown?.match(/\*\*(?:Idea|Company):\*\*\s*(.+)/)?.[1]);
  const market = report?.target_market || 'India';

  const progressSteps = [
    { label: 'Created',  done: !!runId,                  active: isRunning && !events.length },
    { label: 'Research', done: events.some(e => e.event_type === 'agent_completed'), active: isRunning && !!runId && !events.some(e => e.event_type === 'debate_started') },
    { label: 'Debate',   done: !!verdict,                 active: isRunning && events.some(e => e.event_type === 'debate_started') },
    { label: 'Scoring',  done: battleScore !== null,      active: isRunning && !!verdict && battleScore === null },
    { label: 'Report',   done: !!reportLinks?.pdf_path,   active: isRunning && battleScore !== null && !reportLinks },
    { label: 'Done',     done: !isRunning && !!verdict,   active: false },
  ];

  const TABS: { id: TabId; label: string; icon: React.ElementType }[] = [
    { id: 'overview',     label: 'Overview',     icon: Eye },
    { id: 'market',       label: 'Market',       icon: TrendingUp },
    { id: 'competition',  label: 'Competition',  icon: Users },
    { id: 'financials',   label: 'Financials',   icon: BarChart3 },
    { id: 'strategy',     label: 'Strategy',     icon: Sparkles },
    { id: 'risks',        label: 'Risks',        icon: ShieldAlert },
    { id: 'report',       label: 'Full Report',  icon: FileText },
  ];

  const strengths    = extractBullets(report?.swot_analysis, 'Strengths').slice(0, 3);
  const risks        = extractBullets(report?.critic_analysis || report?.risk_analysis, 'Failure Risks').slice(0, 3);
  const actions      = extractBullets(report?.final_recommendation || report?.recommendations).slice(0, 3);

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-page)' }}>

      {/* ── Sticky input / header bar ── */}
      <div style={{ position: 'sticky', top: 64, zIndex: 40, background: '#fff', borderBottom: '1px solid var(--border)' }}>
        <div className="container" style={{ padding: '12px 32px' }}>

          {/* Top bar: title + controls */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
            <div style={{ flex: 1, minWidth: 200 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <h1 style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-primary)', margin: 0 }}>
                  {displayName}
                </h1>
                {verdict && <VerdictBadge verdict={verdict} />}
                {isRunning && <span className="badge badge-indigo"><Loader2 className="w-3 h-3 animate-spin" style={{ display: 'inline' }} /> Running</span>}
              </div>
              {startupIdea && (
                <p style={{ fontSize: 12, color: 'var(--text-tertiary)', margin: '2px 0 0', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: 600 }}>
                  {startupIdea}
                </p>
              )}
            </div>

            {/* Mode + connection + controls */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexShrink: 0 }}>
              <button
                onClick={() => setIsMockMode(!isMockMode)}
                className={`badge ${isMockMode ? 'badge-amber' : 'badge-green'}`}
                style={{ cursor: 'pointer', border: 'none', fontSize: 11 }}
                title="Toggle live/mock mode"
              >
                <span style={{ width: 6, height: 6, borderRadius: '50%', background: isMockMode ? 'var(--warning)' : 'var(--success)', display: 'inline-block', flexShrink: 0 }} />
                {isMockMode ? 'Mock' : 'Live'}
              </button>

              {!isMockMode && (
                <span className={`badge ${isConnected ? 'badge-green' : 'badge-red'}`}>
                  <Plug className="w-3 h-3" /> {isConnected ? 'Connected' : 'Offline'}
                </span>
              )}

              <button
                onClick={() => setInputOpen(!inputOpen)}
                className="btn btn-secondary btn-sm"
                title="Toggle input panel"
              >
                {inputOpen ? 'Hide Input' : 'Edit Idea'}
              </button>

              <button
                onClick={() => { reset(); setStartupIdea(''); setProblemStatement(''); setTargetUsers(''); setRevenueModel(''); setInputOpen(true); setActiveTab('overview'); }}
                className="btn btn-ghost btn-sm btn-icon"
                title="Reset"
              >
                <RotateCcw className="w-3.5 h-3.5" />
              </button>

              <button
                onClick={handleStart}
                disabled={isRunning || (!isMockMode && !startupIdea.trim())}
                className="btn btn-primary btn-sm"
              >
                {isRunning ? <><Loader2 className="w-3.5 h-3.5 animate-spin" />Running…</> : <><Play className="w-3.5 h-3.5" />Start Battle</>}
              </button>
            </div>
          </div>

          {/* Collapsible input row */}
          {inputOpen && (
            <div style={{ marginTop: 12, padding: 16, background: 'var(--bg-subtle)', borderRadius: 10, border: '1px solid var(--border)', display: 'flex', gap: 12, flexWrap: 'wrap', alignItems: 'flex-end' }}>
              <div style={{ flex: 2, minWidth: 240 }}>
                <label className="label" style={{ fontSize: 12 }}>Startup Idea</label>
                <input type="text" value={startupIdea} onChange={e => setStartupIdea(e.target.value)} placeholder="Describe your startup idea…" className="input-field" style={{ fontSize: 13 }} />
              </div>
              <div style={{ flex: 1, minWidth: 140 }}>
                <label className="label" style={{ fontSize: 12 }}>Problem Statement</label>
                <input type="text" value={problemStatement} onChange={e => setProblemStatement(e.target.value)} placeholder="Optional" className="input-field" style={{ fontSize: 13 }} />
              </div>
              <div style={{ flex: 1, minWidth: 140 }}>
                <label className="label" style={{ fontSize: 12 }}>Target Users</label>
                <input type="text" value={targetUsers} onChange={e => setTargetUsers(e.target.value)} placeholder="Optional" className="input-field" style={{ fontSize: 13 }} />
              </div>
              <div style={{ flex: 1, minWidth: 120 }}>
                <label className="label" style={{ fontSize: 12 }}>Revenue Model</label>
                <input type="text" value={revenueModel} onChange={e => setRevenueModel(e.target.value)} placeholder="Optional" className="input-field" style={{ fontSize: 13 }} />
              </div>
            </div>
          )}
        </div>
      </div>

      {/* ── Main content ── */}
      <div className="container" style={{ padding: '24px 32px' }}>

        {/* Progress bar */}
        {(isRunning || (runId && !verdict)) && (
          <div style={{ marginBottom: 24 }}>
            <ProgressBar label="Battle in progress…" steps={progressSteps} />
          </div>
        )}

        {/* KPI Row */}
        {verdict && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12, marginBottom: 24 }}>
            <div className="metric-card" style={{ border: `1px solid ${getScoreColor(battleScore)}33` }}>
              <div className="metric-card-label">Battle Score</div>
              <ScoreDisplay score={battleScore} size="lg" />
              <div className="metric-card-sub">out of 100</div>
            </div>
            <div className="metric-card">
              <div className="metric-card-label">Verdict</div>
              <div style={{ marginTop: 4 }}>
                <VerdictBadge verdict={verdict} />
                {pivotMandated && <div style={{ marginTop: 6, display: 'flex', alignItems: 'center', gap: 4, fontSize: 12, color: 'var(--warning-text)' }}><AlertTriangle className="w-3 h-3" />Pivot recommended</div>}
              </div>
            </div>
            <div className="metric-card">
              <div className="metric-card-label">Confidence</div>
              <div className="metric-card-value" style={{ color: 'var(--accent)' }}>
                {confidenceScore !== null ? `${(confidenceScore * 100).toFixed(0)}%` : '—'}
              </div>
            </div>
            <div className="metric-card">
              <div className="metric-card-label">Target Market</div>
              <div className="metric-card-value" style={{ fontSize: 18, color: 'var(--text-primary)' }}>{market}</div>
            </div>
          </div>
        )}

        {/* Score visualization */}
        {verdict && battleScore !== null && (
          <div className="card" style={{ padding: 24, marginBottom: 24 }}>
            <div style={{ display: 'grid', gridTemplateColumns: '160px 1fr', gap: 32, alignItems: 'center' }}>
              {/* Big number */}
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: 64, fontWeight: 900, color: getScoreColor(battleScore), lineHeight: 1 }}>
                  {battleScore}
                </div>
                <div style={{ fontSize: 14, color: 'var(--text-tertiary)', marginTop: 4 }}>/100</div>
                <div style={{ marginTop: 8 }}><VerdictBadge verdict={verdict} /></div>
              </div>
              {/* Dimension bars */}
              <div>
                <h3 style={{ fontSize: 14, fontWeight: 700, color: 'var(--text-primary)', margin: '0 0 16px' }}>Score Dimensions</h3>
                <p style={{ fontSize: 12, color: 'var(--text-tertiary)', margin: '0 0 16px' }}>Based on multi-agent analysis signals</p>
                <ScoreBar label="Overall Battle Score"  value={battleScore} max={100} />
                {confidenceScore !== null && <ScoreBar label="Confidence Score" value={Math.round(confidenceScore * 100)} max={100} />}
              </div>
            </div>
          </div>
        )}

        {/* Executive Summary 3-col */}
        {verdict && report && (
          <div className="card" style={{ padding: 24, marginBottom: 24 }}>
            <h3 style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-primary)', margin: '0 0 4px' }}>Executive Summary</h3>
            <p style={{ fontSize: 13, color: 'var(--text-secondary)', margin: '0 0 20px' }}>{displayName}</p>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 20 }}>
              {[
                { label: 'TOP STRENGTHS', color: '#15803D', bg: '#F0FDF4', items: strengths },
                { label: 'KEY RISKS',     color: '#BE123C', bg: '#FFF1F2', items: risks },
                { label: 'NEXT ACTIONS',  color: 'var(--accent-text)', bg: 'var(--accent-light)', items: actions },
              ].map(col => (
                <div key={col.label} style={{ background: col.bg, borderRadius: 10, padding: '16px' }}>
                  <p style={{ fontSize: 10, fontWeight: 800, letterSpacing: '0.08em', textTransform: 'uppercase', color: col.color, margin: '0 0 10px' }}>{col.label}</p>
                  {col.items.length > 0
                    ? col.items.map((item, i) => (
                        <div key={i} style={{ display: 'flex', gap: 8, marginBottom: 6, fontSize: 13, color: '#374151', lineHeight: 1.5 }}>
                          <span style={{ color: col.color, fontWeight: 700, flexShrink: 0 }}>›</span>
                          <span>{item.replace(/\*\*/g, '')}</span>
                        </div>
                      ))
                    : <p style={{ fontSize: 12, color: 'var(--text-tertiary)', fontStyle: 'italic', margin: 0 }}>Not yet generated</p>
                  }
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Download bar */}
        {reportLinks?.pdf_path && (
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 24, padding: '12px 16px', borderRadius: 10, background: 'var(--success-light)', border: '1px solid var(--success-border)' }}>
            <CheckCircle2 className="w-4 h-4" style={{ color: 'var(--success)', flexShrink: 0 }} />
            <span style={{ fontSize: 13, color: 'var(--success-text)', fontWeight: 500, flex: 1 }}>Report generated successfully.</span>
            <a href={`${API_URL}${reportLinks.pdf_path}`} target="_blank" rel="noopener noreferrer" className="btn btn-primary btn-sm">
              <Download className="w-3.5 h-3.5" /> PDF
            </a>
            <a href={`${API_URL}${reportLinks.md_path}`} target="_blank" rel="noopener noreferrer" className="btn btn-secondary btn-sm">
              <Download className="w-3.5 h-3.5" /> MD
            </a>
            <a href={`${API_URL}${reportLinks.json_path}`} target="_blank" rel="noopener noreferrer" className="btn btn-secondary btn-sm">
              <Download className="w-3.5 h-3.5" /> JSON
            </a>
          </div>
        )}

        {/* Empty state before any run */}
        {!isRunning && !runId && !verdict && (
          <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
            <EmptyState
              icon={Swords}
              title="No analysis running"
              description="Enter your startup idea above and click Start Battle to begin the multi-agent analysis."
              actionLabel="Analyze a new idea"
              actionHref="/analyze"
            />
          </div>
        )}

        {/* Tabs */}
        {(verdict || report) && (
          <>
            <div className="tab-list" style={{ marginBottom: 24 }}>
              {TABS.map(tab => (
                <button key={tab.id} className={`tab-item ${activeTab === tab.id ? 'active' : ''}`} onClick={() => setActiveTab(tab.id)}>
                  <tab.icon className="w-3.5 h-3.5" />
                  {tab.label}
                </button>
              ))}
            </div>

            {/* Tab panels */}
            <div className="animate-fade-in">
              {activeTab === 'overview' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
                  <SwotPanel report={report} />
                  <EventLog events={events} />
                </div>
              )}

              {activeTab === 'market' && (
                <div className="card" style={{ padding: 28 }}>
                  <h3 style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-primary)', margin: '0 0 16px' }}>Market Research & Opportunity</h3>
                  <MarkdownRenderer content={report?.market_research?.content_markdown || report?.market_analysis?.content_markdown} suppressTitle="Market" />
                </div>
              )}

              {activeTab === 'competition' && (
                <div className="card" style={{ padding: 28 }}>
                  <h3 style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-primary)', margin: '0 0 16px' }}>Competitive Landscape</h3>
                  {report?.competitor_analysis?.content_markdown
                    ? <MarkdownRenderer content={report.competitor_analysis.content_markdown} suppressTitle="Competitor" />
                    : <EmptyState icon={Users} title="No competitor data" description="Competitor analysis was not generated or is unavailable." />
                  }
                </div>
              )}

              {activeTab === 'financials' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
                  <div className="card" style={{ padding: 28 }}>
                    <h3 style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-primary)', margin: '0 0 16px' }}>Pricing Strategy</h3>
                    <MarkdownRenderer content={report?.pricing_strategy?.content_markdown} suppressTitle="Pricing" />
                  </div>
                  <div className="card" style={{ padding: 28 }}>
                    <h3 style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-primary)', margin: '0 0 16px' }}>Financial Analysis</h3>
                    <MarkdownRenderer content={report?.financial_analysis?.content_markdown} suppressTitle="Financial" />
                  </div>
                </div>
              )}

              {activeTab === 'strategy' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
                  <div className="card" style={{ padding: 28 }}>
                    <h3 style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-primary)', margin: '0 0 16px' }}>Go-To-Market Strategy</h3>
                    <MarkdownRenderer content={report?.go_to_market_strategy?.content_markdown} suppressTitle="Go-To-Market" />
                  </div>
                  <div className="card" style={{ padding: 28 }}>
                    <h3 style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-primary)', margin: '0 0 16px' }}>Agent Debate</h3>
                    <DebatePanel history={debateHistory} />
                  </div>
                </div>
              )}

              {activeTab === 'risks' && (
                <div className="card" style={{ padding: 28 }}>
                  <h3 style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-primary)', margin: '0 0 16px' }}>Risk Analysis & Failure Scenarios</h3>
                  <MarkdownRenderer content={report?.critic_analysis?.content_markdown || report?.risk_analysis?.content_markdown} suppressTitle="Risk" />
                </div>
              )}

              {activeTab === 'report' && <ReportReader report={report} />}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default function BattlefieldPage() {
  return (
    <Suspense fallback={<div style={{ minHeight: '60vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}><LoadingState message="Loading battlefield…" /></div>}>
      <BattlefieldContent />
    </Suspense>
  );
}

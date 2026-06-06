'use client';
import { useState } from 'react';
import { useBattlefieldSocket } from '@/hooks/useBattlefieldSocket';
import { useBattlefieldStore } from '@/stores/battlefieldStore';
import {
  Play, RotateCcw, Plug, Loader2, Target, Activity, Download,
  Gavel, AlertTriangle, Terminal, MessageSquare,
  ChevronDown, ChevronRight, Swords, ArrowRight,
  CheckCircle2, Circle, Eye, Brain,
  FileText, TrendingUp, ShieldAlert, Users, Sparkles, BriefcaseBusiness, Gauge, ChartColumn, BadgeCheck
} from 'lucide-react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { useEffect, Suspense } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/* ─── Tab type ─── */
type TabId = 'overview' | 'market' | 'competition' | 'financials' | 'strategy' | 'report';

type ReportSectionData = {
  title: string;
  content_markdown?: string;
};

type ReportData = {
  executive_summary?: ReportSectionData;
  market_research?: ReportSectionData;
  market_analysis?: ReportSectionData;
  swot_analysis?: ReportSectionData;
  competitor_analysis?: ReportSectionData;
  pricing_strategy?: ReportSectionData;
  financial_analysis?: ReportSectionData;
  go_to_market_strategy?: ReportSectionData;
  critic_analysis?: ReportSectionData;
  risk_analysis?: ReportSectionData;
  evidence_citations?: ReportSectionData;
  final_recommendation?: ReportSectionData;
  recommendations?: ReportSectionData;
};

function asReportState(value: unknown): { final_report?: ReportData } | null {
  return value && typeof value === 'object' ? value as { final_report?: ReportData } : null;
}

function asSection(value?: ReportSectionData | null): string[] {
  if (!value?.content_markdown) return [];
  return value.content_markdown
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line.startsWith('- '))
    .map((line) => line.replace(/^-\s*/, ''));
}

function firstItem(items: string[] | undefined, fallback = 'Not generated') {
  return items && items.length > 0 ? items[0] : fallback;
}

function extractCompetitorName(section?: ReportSectionData | null) {
  const lines = asSection(section);
  for (const line of lines) {
    const match = line.match(/^\*\*(.*?)\*\*/);
    if (match?.[1]) return match[1];
  }
  return 'Not generated';
}

function extractBulletGroup(section?: ReportSectionData | null, heading?: string) {
  const content = section?.content_markdown || '';
  if (!content || !heading) return [] as string[];
  const pattern = new RegExp(`\\*\\*${heading}\\*\\*[\\s\\S]*?(?=\\n\\*\\*|$)`);
  const match = content.match(pattern);
  if (!match) return [] as string[];
  return match[0]
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line.startsWith('-'))
    .map((line) => line.replace(/^-\s*/, '').trim())
    .filter(Boolean);
}

function stripLeadingHeading(content?: string, title?: string) {
  if (!content || !title) return content;
  const lines = content.split('\n');
  while (lines.length > 0 && !lines[0].trim()) {
    lines.shift();
  }
  const normalizedTitle = title.trim().toLowerCase();
  while (lines.length > 0) {
    const normalizedLine = lines[0].trim().replace(/^#{1,6}\s*/, '').trim().toLowerCase();
    if (normalizedLine === normalizedTitle) {
      lines.shift();
      while (lines.length > 0 && !lines[0].trim()) {
        lines.shift();
      }
    } else {
      break;
    }
  }
  return lines.join('\n');
}

function StatCard({ label, value, icon: Icon, tone, suffix }: {
  label: string;
  value: string | number | null | undefined;
  icon: React.ElementType;
  tone: string;
  suffix?: string;
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-4 backdrop-blur-md shadow-lg shadow-black/10">
      <div className="flex items-center gap-2 text-zinc-400 mb-2">
        <Icon className={`w-4 h-4 ${tone}`} />
        <span className="text-xs font-semibold uppercase tracking-wider">{label}</span>
      </div>
      <div className="text-lg font-bold text-white">
        {value ?? '--'}
        {suffix && value !== null && value !== undefined && <span className="ml-1 text-sm text-zinc-500">{suffix}</span>}
      </div>
    </div>
  );
}

function SwotMatrix({ report }: { report?: ReportData | null }) {
  const strengths = extractBulletGroup(report?.swot_analysis, 'Strengths');
  const weaknesses = extractBulletGroup(report?.swot_analysis, 'Weaknesses');
  const opportunities = extractBulletGroup(report?.swot_analysis, 'Opportunities');
  const threats = extractBulletGroup(report?.swot_analysis, 'Threats');

  const cells = [
    { title: 'Strengths', items: strengths },
    { title: 'Weaknesses', items: weaknesses },
    { title: 'Opportunities', items: opportunities },
    { title: 'Threats', items: threats },
  ];

  return (
    <div className="glass-card p-6">
      <div className="flex items-center justify-between mb-5">
        <div>
          <h3 className="text-lg font-bold text-white">SWOT Matrix</h3>
          <p className="text-sm text-zinc-500">Business signals extracted from the research and critique layers</p>
        </div>
        <Sparkles className="w-5 h-5 text-indigo-400" />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {cells.map((cell) => (
          <div key={cell.title} className="rounded-2xl border border-zinc-800/80 bg-zinc-950/60 p-4">
            <div className="text-xs font-bold uppercase tracking-wider text-indigo-400 mb-3">{cell.title}</div>
            <ul className="space-y-2">
              {cell.items.length > 0 ? cell.items.map((item, index) => (
                <li key={`${cell.title}-${index}`} className="text-sm text-zinc-300 flex gap-2">
                  <span className="text-indigo-400 mt-0.5">•</span>
                  <span>{item}</span>
                </li>
              )) : <li className="text-sm text-zinc-500">Not generated</li>}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}

function SectionPanel({ title, section, emptyMessage = 'Not generated.' }: { title: string; section?: ReportSectionData | null; emptyMessage?: string; }) {
  return (
    <div className="glass-card p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-white">{title}</h3>
        <Target className="w-4 h-4 text-indigo-400" />
      </div>
      {section?.content_markdown ? (
        <div className="prose prose-invert max-w-none">
          {renderMarkdown(section.content_markdown)}
        </div>
      ) : (
        <p className="text-sm text-zinc-500 italic">{emptyMessage}</p>
      )}
    </div>
  );
}

/* ─── Score Card ─── */
function ScoreCard({ label, value, suffix, icon: Icon, color }: {
  label: string; value: string | number | null; suffix?: string;
  icon: React.ElementType; color: string;
}) {
  return (
    <div className="glass-card p-5 flex flex-col gap-2">
      <div className="flex items-center gap-2 text-zinc-400">
        <Icon className={`w-4 h-4 ${color}`} />
        <span className="text-xs font-semibold uppercase tracking-wider">{label}</span>
      </div>
      <div className="text-3xl md:text-4xl font-extrabold text-white">
        {value ?? <span className="text-zinc-600">--</span>}
        {suffix && value !== null && <span className="text-lg text-zinc-500 ml-1">{suffix}</span>}
      </div>
    </div>
  );
}

/* ─── Progress Step ─── */
function ProgressStep({ label, status }: { label: string; status: 'done' | 'active' | 'pending' }) {
  return (
    <div className="flex items-center gap-3">
      {status === 'done' && <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />}
      {status === 'active' && <Loader2 className="w-5 h-5 text-indigo-400 animate-spin shrink-0" />}
      {status === 'pending' && <Circle className="w-5 h-5 text-zinc-600 shrink-0" />}
      <span className={`text-sm ${
        status === 'done' ? 'text-zinc-300' : status === 'active' ? 'text-white font-semibold' : 'text-zinc-500'
      }`}>{label}</span>
    </div>
  );
}

/* ─── Event Feed (collapsible) ─── */
function EventFeedPanel() {
  const events = useBattlefieldStore((s) => s.events);
  const [open, setOpen] = useState(false);
  return (
    <div className="glass-card overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between p-4 hover:bg-zinc-800/30 transition-colors"
      >
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-emerald-400" />
          <span className="text-sm font-semibold text-white">Event Feed</span>
          <span className="text-xs text-zinc-500 ml-2">{events.length} events</span>
        </div>
        {open ? <ChevronDown className="w-4 h-4 text-zinc-400" /> : <ChevronRight className="w-4 h-4 text-zinc-400" />}
      </button>
      {open && (
        <div className="max-h-64 overflow-y-auto border-t border-zinc-800 p-4 font-mono text-xs space-y-1">
          {events.length === 0 && (
            <p className="text-zinc-500 italic">No events yet. Start a simulation.</p>
          )}
          {events.map((ev, i) => {
            const time = new Date(ev.timestamp).toLocaleTimeString();
            const eventData = ev.data && typeof ev.data === 'object' ? ev.data as Record<string, unknown> : null;
            const agentName = eventData?.agent_name ? String(eventData.agent_name) : '';
            const message = eventData?.message ? String(eventData.message) : JSON.stringify(ev.data);
            let color = 'text-zinc-400';
            if (ev.event_type.includes('error')) color = 'text-red-400';
            else if (ev.event_type.includes('completed')) color = 'text-emerald-400';
            else if (ev.event_type.includes('thinking')) color = 'text-amber-300';
            return (
              <div key={i} className="flex gap-2">
                <span className="text-zinc-600 w-20 shrink-0">[{time}]</span>
                <span className="text-indigo-400 w-36 shrink-0">{ev.event_type.toUpperCase()}</span>
                <span className={color}>
                  {agentName && <span className="font-bold">{agentName}: </span>}
                  {message}
                </span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

/* ─── Debate Timeline ─── */
function DebateTimeline() {
  const history = useBattlefieldStore((s) => s.debateHistory);
  if (history.length === 0) {
    return (
      <div className="glass-card p-8 text-center">
        <MessageSquare className="w-10 h-10 text-zinc-700 mx-auto mb-3" />
        <p className="text-zinc-500 text-sm">No debate started. Agents will debate once research is complete.</p>
      </div>
    );
  }
  return (
    <div className="space-y-4">
      {history.map((turn, idx) => {
        const isSkeptic = turn.speaker === 'Skeptic';
        const isProponent = turn.speaker === 'Proponent';
        const isJudge = turn.speaker === 'Judge';
        let borderColor = 'border-zinc-700';
        let badge = 'bg-zinc-800 text-zinc-300';
        if (isSkeptic) { borderColor = 'border-red-800/50'; badge = 'bg-red-900/30 text-red-400'; }
        if (isProponent) { borderColor = 'border-emerald-800/50'; badge = 'bg-emerald-900/30 text-emerald-400'; }
        if (isJudge) { borderColor = 'border-indigo-800/50'; badge = 'bg-indigo-900/30 text-indigo-400'; }
        return (
          <div key={idx} className={`glass-card p-4 border-l-2 ${borderColor}`}>
            <span className={`inline-block px-2 py-0.5 rounded text-xs font-bold mb-2 ${badge}`}>{turn.speaker}</span>
            <p className="text-sm text-zinc-300 leading-relaxed">{turn.message}</p>
          </div>
        );
      })}
    </div>
  );
}

/* ─── Agent Insight Tab ─── */
function AgentInsights() {
  const events = useBattlefieldStore((s) => s.events);
  const [activeAgent, setActiveAgent] = useState('Intelligence Scout');
  const agents = ['Intelligence Scout', 'Opponent Analyst', 'Treasury Advisor', 'Strategy Commander'];
  const agentEvents = events.filter(e => e.data?.agent_name === activeAgent);

  // If we have finalReport, use it for rich insights instead of raw events
  const finalReport = useBattlefieldStore((s) => s.finalReport);
  const reportState = asReportState(finalReport);
  
  let content = null;
  
  if (reportState?.final_report) {
    const report = reportState.final_report;
    if (activeAgent === 'Intelligence Scout') {
      content = report.market_analysis?.content_markdown || 'No market analysis available.';
    } else if (activeAgent === 'Opponent Analyst') {
      content = report.competitor_analysis?.content_markdown || 'No competitor analysis available.';
    } else if (activeAgent === 'Treasury Advisor') {
      content = report.financial_analysis?.content_markdown || 'No financial analysis available.';
    } else if (activeAgent === 'Strategy Commander') {
      content = report.recommendations?.content_markdown || 'No recommendations available.';
    }
  }

  return (
    <div>
      {/* Agent tabs */}
      <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
        {agents.map(a => (
          <button
            key={a}
            onClick={() => setActiveAgent(a)}
            className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-all ${
              activeAgent === a
                ? 'bg-indigo-600 text-white'
                : 'bg-zinc-800/50 text-zinc-400 hover:text-white hover:bg-zinc-800'
            }`}
          >
            {a.split(' ')[0]}
          </button>
        ))}
      </div>

      {/* Agent content */}
      <div className="glass-card p-6">
        <h3 className="text-lg font-bold text-white mb-1">{activeAgent}</h3>
        <p className="text-sm text-zinc-500 mb-6">Agent findings and analysis</p>
        
        {content ? (
          <div className="prose prose-invert max-w-none text-sm text-zinc-300">
            {/* Simple markdown render for the agent's section */}
            {content.split('\n').map((line: string, i: number) => {
              if (line.startsWith('##')) return <h3 key={i} className="text-lg font-bold text-white mt-4 mb-2">{line.replace('##', '')}</h3>;
              if (line.startsWith('#')) return null;
              if (line.trim() === '') return <br key={i} />;
              if (line.startsWith('-')) return <li key={i} className="ml-4 list-disc">{line.substring(1)}</li>;
              return <p key={i} className="mb-2">{line}</p>;
            })}
          </div>
        ) : agentEvents.length === 0 ? (
          <p className="text-sm text-zinc-500 italic">No data from this agent yet.</p>
        ) : (
          <div className="space-y-3">
            {agentEvents.map((ev, i) => {
              const eventData = ev.data && typeof ev.data === 'object' ? ev.data as Record<string, unknown> : null;
              let msg = eventData?.message ? String(eventData.message) : '';
              if (!msg && eventData) {
                // Try to extract readable parts instead of raw JSON
                const vulnerabilities = Array.isArray(eventData.vulnerabilities) ? eventData.vulnerabilities : [];
                const competitors = Array.isArray(eventData.competitors) ? eventData.competitors : [];
                if (vulnerabilities.length > 0) msg = `Identified ${vulnerabilities.length} vulnerabilities.`;
                else if (competitors.length > 0) msg = `Found ${competitors.length} competitors.`;
                else msg = "Agent generated output.";
              }
              return (
                <div key={i} className="p-3 rounded-lg bg-zinc-800/50 border border-zinc-700/50">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs text-indigo-400 font-mono">{ev.event_type.toUpperCase()}</span>
                    <span className="text-xs text-zinc-600">{new Date(ev.timestamp).toLocaleTimeString()}</span>
                  </div>
                  <p className="text-sm text-zinc-300">{msg}</p>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

function renderMarkdown(content?: string, title?: string) {
  const normalizedContent = stripLeadingHeading(content, title);
  if (!normalizedContent) return <p className="text-sm text-zinc-500 italic">Not generated.</p>;
  return normalizedContent.split('\n').map((line: string, i: number) => {
    if (line.startsWith('##')) return <h3 key={i} className="text-lg font-bold text-white mt-5 mb-3">{line.replace(/^##\s*/, '')}</h3>;
    if (line.startsWith('#')) return <h2 key={i} className="text-xl font-bold text-white mt-4 mb-3">{line.replace(/^#\s*/, '')}</h2>;
    if (line.startsWith('- **')) return <li key={i} className="ml-4 mb-1 text-sm text-zinc-300 list-disc" dangerouslySetInnerHTML={{ __html: line.substring(2).replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }} />;
    if (line.startsWith('-')) return <li key={i} className="ml-4 mb-1 text-sm text-zinc-300 list-disc">{line.substring(1).trim()}</li>;
    if (line.startsWith('**')) return <p key={i} className="text-sm font-bold text-indigo-300 mt-4 mb-2">{line.replace(/\*\*/g, '')}</p>;
    if (line.trim() === '') return <br key={i} />;
    return <p key={i} className="text-sm text-zinc-300 mb-2 leading-relaxed" dangerouslySetInnerHTML={{ __html: line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }} />;
  });
}

function IntelligenceReport() {
  const finalReport = useBattlefieldStore((s) => s.finalReport);
  const reportState = asReportState(finalReport);
  const report = reportState?.final_report || (finalReport && typeof finalReport === 'object' ? finalReport as ReportData : null);
  if (!report) {
    return (
      <div className="glass-card p-8 text-center">
        <Brain className="w-12 h-12 text-zinc-700 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-zinc-400 mb-2">No Intelligence Report Yet</h3>
        <p className="text-sm text-zinc-500">Run a live analysis to generate market, SWOT, competitor, pricing, financial, GTM, critic, evidence, and recommendation sections.</p>
      </div>
    );
  }

  const sections = [
    report.executive_summary,
    report.market_research || report.market_analysis,
    report.swot_analysis,
    report.competitor_analysis,
    report.pricing_strategy,
    report.financial_analysis,
    report.go_to_market_strategy,
    report.critic_analysis || report.risk_analysis,
    report.evidence_citations,
    report.final_recommendation || report.recommendations,
  ].filter((section): section is ReportSectionData => Boolean(section));

  return (
    <div className="space-y-5">
      {sections.map((section) => (
        <section key={section.title} className="glass-card p-6">
          <div className="prose prose-invert max-w-none">
            {renderMarkdown(section.content_markdown, section.title)}
          </div>
        </section>
      ))}
    </div>
  );
}

function BattlefieldContent() {
  const searchParams = useSearchParams();
  const urlRunId = searchParams.get('run_id');

  const {
    isRunning, setIsRunning, runId, setRunId, reportLinks,
    battleScore, confidenceScore, verdict, pivotMandated, events,
    setFinalState
  } = useBattlefieldStore();
  const finalReport = useBattlefieldStore((s) => s.finalReport);
  const reportState = asReportState(finalReport);
  const report = reportState?.final_report;
  const [isMockMode, setIsMockMode] = useState<boolean>(false);
  const [startupIdea, setStartupIdea] = useState<string>('');
  const [problemStatement, setProblemStatement] = useState<string>('');
  const [targetUsers, setTargetUsers] = useState<string>('');
  const [revenueModel, setRevenueModel] = useState<string>('');
  const [activeTab, setActiveTab] = useState<TabId>('overview');

  const { isConnected, triggerMockReplay } = useBattlefieldSocket(runId, isMockMode);
  const reset = useBattlefieldStore((s) => s.reset);

  useEffect(() => {
    const saved = sessionStorage.getItem('kurukshetra_idea');
    if (!saved || urlRunId) return;
    try {
      const parsed = JSON.parse(saved);
      window.setTimeout(() => {
        setStartupIdea(parsed.idea || '');
        setProblemStatement(parsed.problemStatement || '');
        setTargetUsers(parsed.targetUsers || '');
        setRevenueModel(parsed.revenueModel || '');
        setIsMockMode(false);
      }, 0);
    } catch (e) {
      console.error('Failed to load saved idea', e);
    }
  }, [urlRunId]);

  useEffect(() => {
    if (urlRunId && urlRunId !== runId) {
      // Load historical run
      window.setTimeout(() => {
        setIsMockMode(false);
        setRunId(urlRunId);
      }, 0);
      fetch(`${API_URL}/api/v1/runs/${urlRunId}`)
        .then(res => res.json())
        .then(data => {
          if (data.final_state) {
            setFinalState(data.final_state);
            // Populate score cards
            if (data.final_state.battle_score) {
               useBattlefieldStore.setState({ 
                 battleScore: data.final_state.battle_score.composite_score,
                 pivotMandated: data.final_state.battle_score.pivot_mandated
               });
            }
            if (data.final_state.confidence_score) {
               useBattlefieldStore.setState({ confidenceScore: data.final_state.confidence_score.overall_confidence });
            }
            if (data.final_state.battle_verdict) {
               useBattlefieldStore.setState({ verdict: data.final_state.battle_verdict });
            }
            if (data.final_state.startup_idea) {
               setStartupIdea(data.final_state.startup_idea.business_concept || data.final_state.startup_idea.company_name);
               setProblemStatement(data.final_state.startup_idea.problem_statement || '');
               setTargetUsers(data.final_state.startup_idea.target_users || '');
               setRevenueModel(data.final_state.startup_idea.revenue_model || '');
            }
            if (data.final_state.final_report) {
               useBattlefieldStore.setState({ 
                 reportLinks: {
                   pdf_path: `/outputs/reports/report_${urlRunId}.pdf`,
                   md_path: `/outputs/reports/report_${urlRunId}.md`,
                   json_path: `/outputs/reports/report_${urlRunId}.json`,
                 }
               });
            }
          }
        })
        .catch(console.error);
    }
  }, [urlRunId, runId, setFinalState, setRunId]);

  useEffect(() => {
    if (!reportLinks?.json_path) return;
    fetch(`${API_URL}${reportLinks.json_path}`)
      .then(res => res.json())
      .then(data => {
        setFinalState({ final_report: data });
        setActiveTab('report');
      })
      .catch(console.error);
  }, [reportLinks?.json_path, setFinalState]);

  const startupName = startupIdea || report?.executive_summary?.content_markdown?.match(/\*\*Idea:\*\*\s*(.+)/)?.[1] || 'Startup';
  const marketOpportunity = firstItem(extractBulletGroup(report?.swot_analysis, 'Opportunities'), firstItem(asSection(report?.market_research || report?.market_analysis)));
  const topRisk = firstItem(extractBulletGroup(report?.critic_analysis || report?.risk_analysis, 'Failure Risks'));
  const topCompetitor = extractCompetitorName(report?.competitor_analysis);
  const topStrength = firstItem(extractBulletGroup(report?.swot_analysis, 'Strengths'));
  const recommendedActions = asSection(report?.final_recommendation || report?.recommendations).slice(0, 4);

  const handleStart = async () => {
    reset();
    if (isMockMode) {
      triggerMockReplay();
      return;
    }
    setIsRunning(true);
    try {
      const res = await fetch(`${API_URL}/api/v1/runs/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_id: '00000000-0000-0000-0000-000000000000',
          idea: startupIdea,
          problem_statement: problemStatement,
          target_users: targetUsers,
          revenue_model: revenueModel,
        }),
      });
      if (!res.ok) throw new Error('Failed to start run');
      const data = await res.json();
      if (data.run_id) {
        setRunId(data.run_id);
        const execRes = await fetch(
          `${API_URL}/api/v1/runs/${data.run_id}/execute`,
          { method: 'POST', headers: { 'Content-Type': 'application/json' } }
        );
        if (!execRes.ok) throw new Error('Failed to execute run');
      }
    } catch (err) {
      console.error('Failed to trigger run:', err);
      setIsRunning(false);
      alert('Failed to trigger backend run.');
    }
  };

  /* Progress status helpers */
  const hasEvents = events.length > 0;
  const progressSteps = [
    { label: 'Run Created', status: runId ? 'done' as const : isRunning ? 'active' as const : 'pending' as const },
    { label: 'Research Started', status: hasEvents ? 'done' as const : runId ? 'active' as const : 'pending' as const },
    { label: 'Debate Running', status: verdict ? 'done' as const : hasEvents && !verdict ? 'active' as const : 'pending' as const },
    { label: 'Battle Score Generated', status: battleScore !== null ? 'done' as const : 'pending' as const },
    { label: 'Report Generated', status: reportLinks?.pdf_path ? 'done' as const : battleScore !== null ? 'active' as const : 'pending' as const },
    { label: 'Completed', status: !isRunning && verdict ? 'done' as const : 'pending' as const },
  ];

  const tabs: { id: TabId; label: string; icon: React.ElementType }[] = [
    { id: 'overview', label: 'Overview', icon: Eye },
    { id: 'market', label: 'Market', icon: TrendingUp },
    { id: 'competition', label: 'Competition', icon: Users },
    { id: 'financials', label: 'Financials', icon: BriefcaseBusiness },
    { id: 'strategy', label: 'Strategy', icon: Sparkles },
    { id: 'report', label: 'Report', icon: FileText },
  ];

  const SummaryCards = () => (
    <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-8">
      <StatCard label="Startup" value={startupName} icon={BriefcaseBusiness} tone="text-indigo-400" />
      <StatCard label="Verdict" value={verdict ?? '--'} icon={BadgeCheck} tone={pivotMandated ? 'text-red-400' : 'text-emerald-400'} />
      <StatCard label="Battle Score" value={battleScore !== null ? battleScore : '--'} suffix="/100" icon={Gauge} tone="text-emerald-400" />
      <StatCard label="Confidence" value={confidenceScore !== null ? `${(confidenceScore * 100).toFixed(0)}%` : '--'} icon={Activity} tone="text-sky-400" />
      <StatCard label="Market Opportunity" value={marketOpportunity} icon={TrendingUp} tone="text-emerald-400" />
      <StatCard label="Top Risk" value={topRisk} icon={ShieldAlert} tone="text-rose-400" />
      <StatCard label="Top Competitor" value={topCompetitor} icon={ChartColumn} tone="text-fuchsia-400" />
      <StatCard label="Top Strength" value={topStrength} icon={ArrowRight} tone="text-amber-400" />
    </div>
  );

  const renderSection = (title: string, section?: ReportSectionData | null, emptyMessage = 'Not generated.') => (
    <SectionPanel title={title} section={section} emptyMessage={emptyMessage} />
  );

  return (
    <div className="min-h-screen pb-16">
      {/* Input section */}
      <section className="border-b border-zinc-800 bg-zinc-950">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row items-end gap-4">
            {/* Idea Input */}
            <div className="flex-1 w-full">
              <label htmlFor="idea" className="block text-sm font-semibold text-zinc-300 mb-2">Startup Idea</label>
              <input
                id="idea"
                type="text"
                placeholder="e.g. AI Attendance System for Colleges"
                value={startupIdea}
                onChange={(e) => setStartupIdea(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-zinc-900 text-white placeholder-zinc-600 border border-zinc-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all text-base"
              />
              <p className="text-xs text-zinc-600 mt-1.5">
                Try: AI Attendance System · Campus Cab Sharing · AI Resume Builder · Porter Booking
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mt-3">
                <input
                  type="text"
                  placeholder="Problem statement"
                  value={problemStatement}
                  onChange={(e) => setProblemStatement(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-zinc-900 text-white placeholder-zinc-600 border border-zinc-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
                />
                <input
                  type="text"
                  placeholder="Target users"
                  value={targetUsers}
                  onChange={(e) => setTargetUsers(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-zinc-900 text-white placeholder-zinc-600 border border-zinc-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
                />
                <input
                  type="text"
                  placeholder="Revenue model"
                  value={revenueModel}
                  onChange={(e) => setRevenueModel(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-zinc-900 text-white placeholder-zinc-600 border border-zinc-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
                />
              </div>
            </div>

            {/* Mode Toggle */}
            <div className="shrink-0">
              <span className="block text-xs font-semibold text-zinc-500 mb-2 uppercase tracking-wider">Mode</span>
              <button
                onClick={() => setIsMockMode(!isMockMode)}
                className={`px-4 py-3 rounded-xl text-sm font-bold transition-all border ${
                  isMockMode
                    ? 'bg-amber-900/20 text-amber-400 border-amber-800/40 hover:bg-amber-900/30'
                    : 'bg-emerald-900/20 text-emerald-400 border-emerald-800/40 hover:bg-emerald-900/30'
                }`}
              >
                {isMockMode ? '⚡ Mock' : '🔴 Live'}
              </button>
            </div>

            {/* WS indicator */}
            {!isMockMode && (
              <div className={`shrink-0 flex items-center gap-2 px-4 py-3 rounded-xl text-sm font-semibold border ${
                isConnected
                  ? 'bg-emerald-900/20 text-emerald-400 border-emerald-800/40'
                  : 'bg-red-900/20 text-red-400 border-red-800/40'
              }`}>
                <Plug className="w-4 h-4" />
                {isConnected ? 'Connected' : 'Offline'}
              </div>
            )}

            {/* Actions */}
            <div className="flex items-center gap-2 shrink-0">
              <button onClick={() => { reset(); setStartupIdea(''); setProblemStatement(''); setTargetUsers(''); setRevenueModel(''); }} className="p-3 text-zinc-500 hover:text-white hover:bg-zinc-800 rounded-xl border border-zinc-800 transition-colors" title="Reset">
                <RotateCcw className="w-5 h-5" />
              </button>
              <button
                onClick={handleStart}
                disabled={isRunning || (!isMockMode && !startupIdea.trim())}
                className={`flex items-center gap-2 px-6 py-3 rounded-xl text-sm font-bold transition-all ${
                  isRunning || (!isMockMode && !startupIdea.trim())
                    ? 'bg-zinc-800 text-zinc-500 cursor-not-allowed'
                    : 'bg-indigo-600 text-white hover:bg-indigo-500 shadow-lg shadow-indigo-600/20'
                }`}
              >
                {isRunning ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4 fill-current" />}
                {isRunning ? 'Running...' : 'Start Battle'}
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Results + Dashboard */}
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">

        {verdict && report && (
          <div className="glass-card p-6 mb-8 border border-indigo-900/50 bg-indigo-950/20">
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-5">
              <div>
                <h2 className="text-2xl font-bold text-white">Founder Dashboard</h2>
                <p className="text-sm text-zinc-400">A compact summary of startup-specific signals for {startupName}.</p>
              </div>
              {reportLinks?.pdf_path ? (
                <a
                  href={`${API_URL}${reportLinks.pdf_path}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold bg-indigo-600 text-white hover:bg-indigo-500 transition-colors"
                >
                  <Download className="w-4 h-4" /> Download Report
                </a>
              ) : (
                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-sm bg-zinc-800 text-zinc-400 border border-zinc-700">
                  <Loader2 className="w-4 h-4 animate-spin" /> Generating Report...
                </div>
              )}
            </div>
            <SummaryCards />
          </div>
        )}

        {verdict && !isRunning && (
          <div className="flex flex-wrap items-center gap-3 mb-8">
            <button
              onClick={() => { reset(); setStartupIdea(''); setProblemStatement(''); setTargetUsers(''); setRevenueModel(''); }}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-bold border border-zinc-700 text-zinc-300 hover:text-white hover:bg-zinc-800 transition-colors"
            >
              <RotateCcw className="w-4 h-4" /> Run Another
            </button>
          </div>
        )}

        {/* Progress Timeline */}
        {(isRunning || runId) && !verdict && (
          <div className="glass-card p-6 mb-8">
            <h3 className="text-sm font-semibold text-zinc-400 uppercase tracking-wider mb-4">Battle Progress</h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4">
              {progressSteps.map((step) => (
                <ProgressStep key={step.label} {...step} />
              ))}
            </div>
          </div>
        )}

        {verdict && report && (
          <div className="glass-card p-8 mb-8 border-indigo-900/50 relative overflow-hidden">
            <div className="absolute top-0 left-0 w-1 h-full bg-indigo-500"></div>
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
              <Target className="w-6 h-6 text-indigo-400" />
              Executive Summary
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="space-y-4">
                <h3 className="text-sm font-bold text-emerald-400 uppercase tracking-wider">Top Strengths</h3>
                <ul className="space-y-2">
                  {extractBulletGroup(report.swot_analysis, 'Strengths').slice(0,3).map((s: string, i: number) => (
                    <li key={i} className="text-sm text-zinc-300 flex items-start gap-2">
                      <span className="text-emerald-400 mt-0.5">•</span> {s}
                    </li>
                  )) || <li className="text-sm text-zinc-500">None identified</li>}
                </ul>
              </div>
              
              <div className="space-y-4">
                <h3 className="text-sm font-bold text-red-400 uppercase tracking-wider">Top Risks</h3>
                <ul className="space-y-2">
                  {extractBulletGroup(report.critic_analysis || report.risk_analysis, 'Failure Risks').slice(0,3).map((w: string, i: number) => (
                    <li key={i} className="text-sm text-zinc-300 flex items-start gap-2">
                      <span className="text-red-400 mt-0.5">•</span> {w}
                    </li>
                  )) || <li className="text-sm text-zinc-500">None identified</li>}
                </ul>
              </div>

              <div className="space-y-4">
                <h3 className="text-sm font-bold text-indigo-400 uppercase tracking-wider">Recommended Actions</h3>
                <div className="prose prose-invert text-sm text-zinc-300 max-h-40 overflow-y-auto pr-2 custom-scrollbar">
                  {recommendedActions.map((l:string, i:number) => (
                    <p key={i} className="mb-2">{l.replace('- ', '')}</p>
                  )) || <p>No recommendations available.</p>}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Tab Navigation */}
        <div className="flex gap-1 mb-6 border-b border-zinc-800 overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-all whitespace-nowrap ${
                activeTab === tab.id
                  ? 'border-indigo-500 text-white'
                  : 'border-transparent text-zinc-500 hover:text-zinc-300'
              }`}
            >
              <tab.icon className="w-4 h-4" />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="animate-fade-in">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <SwotMatrix report={report} />
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                {renderSection('Executive Summary', report?.executive_summary, 'No executive summary generated yet.')}
                <div className="space-y-6">
                  <EventFeedPanel />
                  {renderSection('Recommended Actions', report?.final_recommendation || report?.recommendations, 'No recommendations available yet.')}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'market' && renderSection('Market Research', report?.market_research || report?.market_analysis, 'No market research generated yet.')}

          {activeTab === 'competition' && (
            <div className="space-y-6">
              {renderSection('Competitor Analysis', report?.competitor_analysis, 'No competitor analysis generated yet.')}
              <div className="glass-card p-6">
                <h3 className="text-lg font-bold text-white mb-4">Top Competitor</h3>
                <p className="text-zinc-300">{topCompetitor}</p>
              </div>
            </div>
          )}

          {activeTab === 'financials' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {renderSection('Pricing Strategy', report?.pricing_strategy, 'No pricing strategy generated yet.')}
              {renderSection('Financial Analysis', report?.financial_analysis, 'No financial analysis generated yet.')}
            </div>
          )}

          {activeTab === 'strategy' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {renderSection('Go-To-Market Strategy', report?.go_to_market_strategy, 'No GTM strategy generated yet.')}
                {renderSection('Critic Analysis', report?.critic_analysis || report?.risk_analysis, 'No critic analysis generated yet.')}
              </div>
              <DebateTimeline />
            </div>
          )}

          {activeTab === 'report' && <IntelligenceReport />}
        </div>
      </div>
    </div>
  );
}

export default function BattlefieldPage() {
  return (
    <Suspense fallback={<div className="min-h-screen flex items-center justify-center text-white"><Loader2 className="w-8 h-8 animate-spin text-indigo-500" /></div>}>
      <BattlefieldContent />
    </Suspense>
  );
}

'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import {
  Swords, ArrowRight, Brain, Globe, Users, TrendingUp,
  Shield, FileText, CheckCircle, ChevronRight, BarChart2,
  Target, Zap, Sparkles, Scale, Activity, ArrowUpRight,
  Cpu, Compass, Check, Layers, AlertTriangle, Lightbulb
} from 'lucide-react';

/* ─── Data: Capabilities ─── */
const CAPABILITIES = [
  {
    icon: Globe,
    title: 'Market Intelligence',
    desc: 'Understand market size, CAGR, demand signals and growth trends specific to your target geography and demographic cohorts.',
    metric: 'TAM · SAM · SOM Analysis',
    tag: 'Macro Validation'
  },
  {
    icon: Users,
    title: 'Competitive Intelligence',
    desc: 'Identify direct competitors, substitute models and hidden market gaps using real-time search and multi-source web intelligence.',
    metric: 'Real-time Web Scrapes',
    tag: 'Moat Assessment'
  },
  {
    icon: BarChart2,
    title: 'Financial Feasibility',
    desc: 'Evaluate pricing strategy, CAC, LTV and unit economics against AI-modeled industry benchmarks and margin tolerances.',
    metric: 'Unit Economics Stress-Test',
    tag: 'Capital Efficiency'
  },
  {
    icon: Shield,
    title: 'Risk & Stress Testing',
    desc: 'Challenge every key hypothesis with an adversarial Skeptic agent designed specifically to uncover fatal operational failure modes.',
    metric: 'Adversarial Stress Test',
    tag: 'Failure Scenarios'
  },
  {
    icon: Target,
    title: 'Go-To-Market Strategy',
    desc: 'Formulate an actionable channel architecture, viral growth triggers, and regional customer acquisition roadmaps.',
    metric: 'Channel Acquisition Matrix',
    tag: 'Execution Blueprint'
  },
  {
    icon: FileText,
    title: 'Executive Report',
    desc: 'Generate and download an authoritative 21-section executive dossier with citations, risk matrices and clear strategic counsel.',
    metric: 'PDF · JSON · Markdown',
    tag: 'Investor-Ready'
  },
];

/* ─── Data: 7 AI Battlefield Agents ─── */
const AGENTS = [
  {
    id: 'scout',
    name: 'Intelligence Scout',
    role: 'Market Research',
    color: '#5B5CEB',
    bg: '#F1F0FF',
    weapon: 'Global & Regional TAM/SAM Scrutiny',
    description: 'Scours live web signals, market sizing datasets, and growth CAGRs to validate whether genuine market pull exists.',
    coordinates: { top: '6%', left: '50%' }
  },
  {
    id: 'opponent',
    name: 'Opponent Analyst',
    role: 'Competitive Intel',
    color: '#0EA5E9',
    bg: '#F0F9FF',
    weapon: 'Adversarial Moat & Rival Mapping',
    description: 'Maps incumbents, emerging startups, and substitute behaviors to discover whether your product possesses defensibility.',
    coordinates: { top: '22%', left: '84%' }
  },
  {
    id: 'treasury',
    name: 'Treasury Advisor',
    role: 'Financial Analysis',
    color: '#C99A3D',
    bg: '#FCFAF5',
    weapon: 'Unit Economics & CAC/LTV Stress-Test',
    description: 'Dissects gross margins, churn sensitivity, customer acquisition costs, and path to profitable scale.',
    coordinates: { top: '65%', left: '88%' }
  },
  {
    id: 'commander',
    name: 'Strategy Commander',
    role: 'GTM & Strategy',
    color: '#8B5CF6',
    bg: '#F5F3FF',
    weapon: 'Channel Defense & Growth Playbooks',
    description: 'Orchestrates go-to-market penetration, distribution flywheel design, and customer retention loops.',
    coordinates: { top: '88%', left: '50%' }
  },
  {
    id: 'critic',
    name: 'Critic Agent',
    role: 'Risk & Failure Modes',
    color: '#EF4444',
    bg: '#FEF2F2',
    weapon: 'Skeptic Scrutiny & Blindspot Detection',
    description: 'Acts as the ruthless devil’s advocate, challenging optimistic founder bias and exposing regulatory or operational death traps.',
    coordinates: { top: '65%', left: '12%' }
  },
  {
    id: 'debate',
    name: 'Debate Engine',
    role: 'Tri-Party Deliberation',
    color: '#10B981',
    bg: '#ECFDF5',
    weapon: 'Proponent · Skeptic · Judicial Weighing',
    description: 'Stages a structured adversarial debate where proponent arguments clash directly against skeptical cross-examinations.',
    coordinates: { top: '22%', left: '16%' }
  },
  {
    id: 'score',
    name: 'Battle Score',
    role: 'Scoring & Synthesis',
    color: '#6366F1',
    bg: '#EEF2FF',
    weapon: '100+ Multi-Signal Quantitative Index',
    description: 'Calculates the definitive composite Battle Score (0-100), confidence percentage, and conclusive verdict.',
    coordinates: { top: '50%', left: '50%' }
  },
];

/* ─── Data: 5 Pipeline Stages ─── */
const PIPELINE_STAGES = [
  {
    stage: '01',
    title: 'YOUR STARTUP IDEA',
    subtitle: 'Strategic Ingestion',
    agent: 'Founder Input',
    desc: 'The concept enters the Kurukshetra arena. Key hypotheses, target market, and value proposition are parsed into structured evaluation vectors.',
    badge: 'Stage 1: Input Vector'
  },
  {
    stage: '02',
    title: 'PARALLEL INTELLIGENCE',
    subtitle: 'Simultaneous Multi-Scout Analysis',
    agent: 'Scout · Opponent · Treasury · Commander',
    desc: 'Four specialized agents launch simultaneous deep-dives: market sizing, rival benchmarking, unit economics, and channel distribution models.',
    badge: 'Stage 2: 100+ Data Signals'
  },
  {
    stage: '03',
    title: 'DEBATE ENGINE',
    subtitle: 'Adversarial Dialectic Arena',
    agent: 'Proponent vs. Skeptic vs. Judge',
    desc: 'An unsparing multi-turn debate. The Proponent defends viability while the Critic cross-examines every assumption until a neutral Judge delivers a verdict.',
    badge: 'Stage 3: Cross-Examination'
  },
  {
    stage: '04',
    title: 'BATTLE SCORE',
    subtitle: 'Quantitative Multi-Signal Index',
    agent: 'Battle Score Synthesizer',
    desc: 'Weighted algorithmic synthesis aggregates signals into Market Demand (25%), Unit Economics (25%), Defensibility (20%), and Execution Feasibility (30%).',
    badge: 'Stage 4: Algorithmic Synthesis'
  },
  {
    stage: '05',
    title: 'FINAL VERDICT & REPORT',
    subtitle: 'Actionable Strategic Blueprint',
    agent: 'Executive Dossier Generator',
    desc: 'A definitive determination (Proceed / Pivot / High Caution) accompanied by an exhaustive 21-section executive PDF, markdown, and raw JSON export.',
    badge: 'Stage 5: 21-Section Blueprint'
  },
];

/* ─── Data: 5 How-It-Works Steps ─── */
const STEPS = [
  {
    num: '01',
    title: 'Describe',
    tagline: 'Your startup enters Kurukshetra',
    desc: 'Submit your startup concept in 1–3 sentences. Define your target customer and value proposition.'
  },
  {
    num: '02',
    title: 'Research',
    tagline: 'Agents gather live intelligence',
    desc: 'Agents search the live web, retrieve competitor benchmarks, and extract market demand signals.'
  },
  {
    num: '03',
    title: 'Debate',
    tagline: 'AI specialists challenge assumptions',
    desc: 'A Proponent defends viability, a Skeptic attacks blindspots, and an impartial Judge evaluates.'
  },
  {
    num: '04',
    title: 'Score',
    tagline: 'Signals become a Battle Score',
    desc: 'Over 100 quantitative and qualitative signals produce an objective Battle Score and Confidence Index.'
  },
  {
    num: '05',
    title: 'Report',
    tagline: 'A complete intelligence dossier is born',
    desc: 'An authoritative 21-section executive dossier is generated with strategic roadmap and citation evidence.'
  },
];

/* ─── Data: 21 Report Sections ─── */
const REPORT_CATEGORIES = [
  {
    category: 'Strategic Foundations',
    sections: [
      '01 Executive Summary',
      '02 Business Concept & Vision',
      '03 Problem Statement & Customer Persona',
      '04 Market Opportunity & TAM/SAM/SOM'
    ]
  },
  {
    category: 'Market & Competitive Battle',
    sections: [
      '05 Competitive Landscape & Moat Matrix',
      '06 SWOT & Defensibility Analysis',
      '07 Revenue Model & Pricing Strategy',
      '08 Financial Projections & Unit Economics'
    ]
  },
  {
    category: 'Execution & Operations',
    sections: [
      '09 Go-To-Market & Channel Distribution',
      '10 Operations & Unit Scaling Plan',
      '11 Risk Matrix & Threat Hierarchy',
      '12 Failure Scenarios & Black Swans'
    ]
  },
  {
    category: 'The AI Debate & Ruling',
    sections: [
      '13 Regulatory & Compliance Review',
      '14 AI Agent Battlefield Debate Transcript',
      '15 Proponent Defense Brief',
      '16 Skeptic Adversarial Critique',
      '17 Judge’s Formal Verdict'
    ]
  },
  {
    category: 'Verdict & Execution Roadmap',
    sections: [
      '18 Battle Score & Confidence Breakdown',
      '19 Strategic Recommendations',
      '20 90-Day Validation Roadmap',
      '21 Evidence, Citations & Data Signals'
    ]
  }
];

/* ─── Data: Metrics ─── */
const STATS = [
  { value: '7', label: 'AI Agents', sub: 'Specialized battlefield analysts' },
  { value: '21', label: 'Report Sections', sub: 'Comprehensive intelligence dossier' },
  { value: '100+', label: 'Data Signals', sub: 'Calculated across every domain' },
  { value: '<5 min', label: 'Analysis Time', sub: 'Instantaneous multi-agent execution' },
];

export default function LandingPage() {
  const [selectedAgent, setSelectedAgent] = useState(AGENTS[0]);
  const [selectedStage, setSelectedStage] = useState(0);
  const [previewTab, setPreviewTab] = useState<'score' | 'debate' | 'evidence'>('score');

  return (
    <div style={{ background: '#F5F7FA', color: '#101828', minHeight: '100vh', overflowX: 'hidden' }}>

      {/* ══════════════════════════════════════════════
          01 HERO SECTION — THE AI BATTLEFIELD FOR STARTUPS
      ══════════════════════════════════════════════ */}
      <section style={{
        position: 'relative',
        padding: '72px 0 64px',
        borderBottom: '1px solid rgba(16, 24, 40, 0.08)',
        background: 'linear-gradient(180deg, #FFFFFF 0%, #F5F7FA 100%)',
        overflow: 'hidden'
      }} className="kuruk-grid-pattern">

        {/* ─── ANIMATED MAHABHARATA BATTLEFIELD BACKGROUND ─── */}
        <div style={{
          position: 'absolute',
          inset: 0,
          pointerEvents: 'none',
          overflow: 'hidden',
          zIndex: 1
        }}>

          {/* 1. Grand Chariot Wheel of Kurukshetra (Dharma / War Formation Chakra) */}
          <div style={{
            position: 'absolute',
            top: '38%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: 760,
            height: 760,
            opacity: 0.16,
            pointerEvents: 'none'
          }}>
            <svg
              viewBox="0 0 500 500"
              width="100%"
              height="100%"
              fill="none"
              className="animate-chakra-wheel"
            >
              <defs>
                <radialGradient id="chakraGold" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stopColor="#C99A3D" stopOpacity="0.4" />
                  <stop offset="70%" stopColor="#5B5CEB" stopOpacity="0.15" />
                  <stop offset="100%" stopColor="transparent" stopOpacity="0" />
                </radialGradient>
              </defs>

              {/* Ambient Radial Core */}
              <circle cx="250" cy="250" r="240" fill="url(#chakraGold)" />

              {/* Outer Chariot Wheel Rim */}
              <circle cx="250" cy="250" r="235" stroke="#C99A3D" strokeWidth="1.5" strokeDasharray="4 6" />
              <circle cx="250" cy="250" r="222" stroke="#101828" strokeWidth="1" strokeOpacity="0.3" />
              <circle cx="250" cy="250" r="205" stroke="#C99A3D" strokeWidth="2" />

              {/* 32 Serrated Formation Arrow Teeth on Rim */}
              {Array.from({ length: 32 }).map((_, i) => {
                const angle = (i * 360) / 32;
                return (
                  <line
                    key={`tooth-${i}`}
                    x1="250"
                    y1="15"
                    x2="250"
                    y2="28"
                    stroke="#C99A3D"
                    strokeWidth="1.8"
                    transform={`rotate(${angle} 250 250)`}
                  />
                );
              })}

              {/* Middle Tactical Ring */}
              <circle cx="250" cy="250" r="145" stroke="#5B5CEB" strokeWidth="1.5" strokeDasharray="6 6" />
              <circle cx="250" cy="250" r="95" stroke="#C99A3D" strokeWidth="1.2" />

              {/* 16 Chariot Spokes (Kurukshetra War Strategy Axes) */}
              {Array.from({ length: 16 }).map((_, i) => {
                const angle = (i * 360) / 16;
                return (
                  <g key={`spoke-${i}`} transform={`rotate(${angle} 250 250)`}>
                    <line x1="250" y1="250" x2="250" y2="45" stroke="#C99A3D" strokeWidth="1.6" />
                    {/* Spoke ornamental diamond */}
                    <polygon points="250,115 253,122 250,129 247,122" fill="#5B5CEB" opacity="0.6" />
                  </g>
                );
              })}

              {/* Inner Hub (The Sovereign Center) */}
              <circle cx="250" cy="250" r="32" fill="#FCFAF5" stroke="#C99A3D" strokeWidth="2" />
              <circle cx="250" cy="250" r="14" fill="#C99A3D" opacity="0.7" />
              <circle cx="250" cy="250" r="6" fill="#101828" />
            </svg>
          </div>

          {/* 2. Flying Astras (Luminous Battlefield Arrows Gliding Across the Skies) */}
          {/* Astra 1: Golden Agneyastra Streak (Left to Right) */}
          <div
            className="animate-astra-1"
            style={{
              position: 'absolute',
              top: '26%',
              left: 0,
              width: 140,
              height: 24,
              pointerEvents: 'none'
            }}
          >
            <svg viewBox="0 0 140 24" width="100%" height="100%" fill="none">
              <defs>
                <linearGradient id="astraGoldGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#C99A3D" stopOpacity="0" />
                  <stop offset="70%" stopColor="#C99A3D" stopOpacity="0.7" />
                  <stop offset="100%" stopColor="#FFD700" stopOpacity="1" />
                </linearGradient>
              </defs>
              {/* Luminous Trail */}
              <line x1="0" y1="12" x2="120" y2="12" stroke="url(#astraGoldGrad)" strokeWidth="2" strokeLinecap="round" />
              <line x1="20" y1="12" x2="115" y2="12" stroke="#FFFFFF" strokeWidth="1" strokeOpacity="0.8" />
              {/* Arrowhead */}
              <polygon points="120,7 136,12 120,17 124,12" fill="#C99A3D" />
              <circle cx="134" cy="12" r="3" fill="#FFDF78" style={{ filter: 'drop-shadow(0 0 6px #C99A3D)' }} />
            </svg>
          </div>

          {/* Astra 2: Electric Indigo Brahmastra Streak (Right to Left) */}
          <div
            className="animate-astra-2"
            style={{
              position: 'absolute',
              top: '52%',
              left: 0,
              width: 130,
              height: 24,
              pointerEvents: 'none'
            }}
          >
            <svg viewBox="0 0 130 24" width="100%" height="100%" fill="none">
              <defs>
                <linearGradient id="astraPurpleGrad" x1="100%" y1="0%" x2="0%" y2="0%">
                  <stop offset="0%" stopColor="#5B5CEB" stopOpacity="0" />
                  <stop offset="70%" stopColor="#5B5CEB" stopOpacity="0.7" />
                  <stop offset="100%" stopColor="#818CF8" stopOpacity="1" />
                </linearGradient>
              </defs>
              {/* Counter Trail */}
              <line x1="130" y1="12" x2="14" y2="12" stroke="url(#astraPurpleGrad)" strokeWidth="2" strokeLinecap="round" />
              <line x1="110" y1="12" x2="18" y2="12" stroke="#FFFFFF" strokeWidth="0.8" strokeOpacity="0.8" />
              {/* Counter Arrowhead */}
              <polygon points="14,7 0,12 14,17 10,12" fill="#5B5CEB" />
              <circle cx="2" cy="12" r="2.5" fill="#C7D2FE" style={{ filter: 'drop-shadow(0 0 6px #5B5CEB)' }} />
            </svg>
          </div>

          {/* Astra 3: High-Altitude Scouting Arrow (Left to Right, High Arc) */}
          <div
            className="animate-astra-3"
            style={{
              position: 'absolute',
              top: '12%',
              left: 0,
              width: 120,
              height: 20,
              pointerEvents: 'none'
            }}
          >
            <svg viewBox="0 0 120 20" width="100%" height="100%" fill="none">
              <defs>
                <linearGradient id="astraCyanGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#0EA5E9" stopOpacity="0" />
                  <stop offset="75%" stopColor="#0EA5E9" stopOpacity="0.65" />
                  <stop offset="100%" stopColor="#38BDF8" stopOpacity="1" />
                </linearGradient>
              </defs>
              <line x1="0" y1="10" x2="105" y2="10" stroke="url(#astraCyanGrad)" strokeWidth="1.5" strokeLinecap="round" />
              <polygon points="105,6 118,10 105,14 108,10" fill="#0EA5E9" />
            </svg>
          </div>

          {/* 3. Floating Battlefield Embers / Sparks */}
          <div style={{ position: 'absolute', bottom: 40, left: '12%', width: 6, height: 6, borderRadius: '50%', background: '#C99A3D', boxShadow: '0 0 8px #C99A3D' }} className="animate-ember-1" />
          <div style={{ position: 'absolute', bottom: 60, left: '26%', width: 5, height: 5, borderRadius: '50%', background: '#5B5CEB', boxShadow: '0 0 8px #5B5CEB' }} className="animate-ember-2" />
          <div style={{ position: 'absolute', bottom: 50, left: '48%', width: 7, height: 7, borderRadius: '50%', background: '#C99A3D', boxShadow: '0 0 10px #C99A3D' }} className="animate-ember-3" />
          <div style={{ position: 'absolute', bottom: 70, left: '72%', width: 5, height: 5, borderRadius: '50%', background: '#5B5CEB', boxShadow: '0 0 8px #5B5CEB' }} className="animate-ember-4" />
          <div style={{ position: 'absolute', bottom: 35, left: '88%', width: 6, height: 6, borderRadius: '50%', background: '#C99A3D', boxShadow: '0 0 8px #C99A3D' }} className="animate-ember-5" />

          {/* 4. Gandiva Bow Curves (Framing Left and Right Margin Arcs) */}
          <div style={{ position: 'absolute', top: 40, left: -20, width: 100, height: 480, opacity: 0.25 }}>
            <svg viewBox="0 0 100 480" width="100%" height="100%" fill="none">
              <path d="M 0,20 Q 80,240 0,460" stroke="#C99A3D" strokeWidth="2" strokeDasharray="6 6" />
              <circle cx="40" cy="240" r="4" fill="#C99A3D" />
            </svg>
          </div>

          <div style={{ position: 'absolute', top: 40, right: -20, width: 100, height: 480, opacity: 0.25 }}>
            <svg viewBox="0 0 100 480" width="100%" height="100%" fill="none">
              <path d="M 100,20 Q 20,240 100,460" stroke="#5B5CEB" strokeWidth="2" strokeDasharray="6 6" />
              <circle cx="60" cy="240" r="4" fill="#5B5CEB" />
            </svg>
          </div>

          {/* 5. Twilight Horizon Glow of Kurukshetra */}
          <div style={{
            position: 'absolute',
            bottom: 0,
            left: 0,
            right: 0,
            height: 120,
            background: 'radial-gradient(ellipse at 50% 100%, rgba(201, 154, 61, 0.12) 0%, rgba(91, 92, 235, 0.05) 50%, transparent 80%)',
            pointerEvents: 'none'
          }} className="animate-battlefield-aura" />

        </div>

        {/* Ambient Battlefield Glow */}
        <div className="kuruk-hero-glow" />

        {/* Subtle decorative geometric background markers */}
        <div style={{
          position: 'absolute', top: 24, left: 32,
          fontSize: 10, fontFamily: 'var(--font-mono)', letterSpacing: '0.15em',
          color: 'rgba(16, 24, 40, 0.25)', textTransform: 'uppercase', pointerEvents: 'none'
        }}>
          COORD: 29.9695° N, 76.8783° E // SECTOR-AI
        </div>

        <div style={{
          position: 'absolute', top: 24, right: 32,
          fontSize: 10, fontFamily: 'var(--font-mono)', letterSpacing: '0.15em',
          color: 'rgba(201, 154, 61, 0.6)', textTransform: 'uppercase', pointerEvents: 'none',
          display: 'flex', alignItems: 'center', gap: 6
        }}>
          <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#10B981', display: 'inline-block' }} />
          SYSTEM LIVE · 7 AGENTS READY
        </div>

        <div className="container" style={{ position: 'relative', zIndex: 2 }}>

          {/* Hero Header Block */}
          <div style={{ maxWidth: 880, margin: '0 auto', textAlign: 'center' }}>

            {/* Battlefield Badge */}
            <div style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 10,
              padding: '7px 18px',
              borderRadius: 100,
              background: '#F1F0FF',
              border: '1px solid rgba(201, 154, 61, 0.45)',
              boxShadow: '0 2px 8px rgba(91, 92, 235, 0.1)',
              marginBottom: 28,
              transition: 'transform 0.2s ease'
            }}>
              <span style={{
                display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
                width: 18, height: 18, borderRadius: '50%', background: 'rgba(201, 154, 61, 0.15)',
                color: '#C99A3D', fontSize: 11
              }}>
                ⚔
              </span>
              <span style={{
                fontSize: 12,
                fontWeight: 800,
                color: '#5B5CEB',
                letterSpacing: '0.08em',
                textTransform: 'uppercase'
              }}>
                THE AI BATTLEFIELD FOR STARTUPS
              </span>
              <span style={{
                width: 5, height: 5, borderRadius: '50%', background: '#C99A3D'
              }} />
            </div>

            {/* Main Headline */}
            <h1 style={{
              fontSize: 'clamp(40px, 6.2vw, 68px)',
              fontWeight: 900,
              color: '#101828',
              lineHeight: 1.08,
              letterSpacing: '-0.035em',
              margin: '0 0 24px'
            }}>
              Put your startup idea<br />
              <span style={{
                color: '#5B5CEB',
                position: 'relative',
                display: 'inline-block'
              }}>
                on the battlefield.
                <svg
                  style={{
                    position: 'absolute', bottom: -8, left: 0, width: '100%', height: 8,
                    overflow: 'visible'
                  }}
                  viewBox="0 0 200 8" fill="none" preserveAspectRatio="none"
                >
                  <path d="M0 6 Q 100 0, 200 6" stroke="#C99A3D" strokeWidth="2.5" strokeLinecap="round" strokeDasharray="6 4" opacity="0.75" />
                </svg>
              </span>
            </h1>

            {/* Supporting Text */}
            <p style={{
              fontSize: 'clamp(16px, 2.2vw, 19px)',
              color: '#475569',
              lineHeight: 1.65,
              maxWidth: 680,
              margin: '0 auto 36px',
              fontWeight: 450
            }}>
              Seven AI agents challenge your market, competition, financial assumptions and strategy before you invest your time or capital.
            </p>

            {/* CTAs */}
            <div style={{
              display: 'flex',
              gap: 14,
              justifyContent: 'center',
              alignItems: 'center',
              flexWrap: 'wrap',
              marginBottom: 48
            }}>
              <Link
                href="/analyze"
                className="btn btn-lg"
                style={{
                  textDecoration: 'none',
                  background: '#5B5CEB',
                  color: '#FFFFFF',
                  fontWeight: 700,
                  fontSize: 15,
                  padding: '14px 28px',
                  borderRadius: 10,
                  boxShadow: '0 4px 18px rgba(91, 92, 235, 0.35)',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 10,
                  border: '1px solid rgba(201, 154, 61, 0.4)',
                  transition: 'all 0.2s ease'
                }}
              >
                <span>⚔</span>
                <span>Battle-Test My Idea</span>
                <ArrowRight className="w-4 h-4 animate-arrow-shift" />
              </Link>

              <Link
                href="/battlefield"
                className="btn btn-lg"
                style={{
                  textDecoration: 'none',
                  background: '#FFFFFF',
                  color: '#101828',
                  fontWeight: 600,
                  fontSize: 15,
                  padding: '14px 26px',
                  borderRadius: 10,
                  border: '1px solid rgba(16, 24, 40, 0.15)',
                  boxShadow: '0 2px 6px rgba(0, 0, 0, 0.04)',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 8,
                  transition: 'all 0.2s ease'
                }}
              >
                <span>Explore the Battlefield</span>
                <ArrowUpRight className="w-4 h-4" style={{ color: '#64748B' }} />
              </Link>
            </div>

            {/* Metrics Row */}
            <div className="kuruk-metrics-grid" style={{
              maxWidth: 780,
              margin: '0 auto 52px',
              padding: '18px 24px',
              background: '#FFFFFF',
              borderRadius: 14,
              border: '1px solid rgba(16, 24, 40, 0.08)',
              boxShadow: '0 2px 10px rgba(0, 0, 0, 0.03)'
            }}>
              {STATS.map((s, idx) => (
                <div key={s.label} style={{
                  textAlign: 'center',
                  borderRight: idx < STATS.length - 1 ? '1px solid rgba(16, 24, 40, 0.07)' : 'none',
                  padding: '0 8px'
                }}>
                  <div style={{
                    fontSize: 26,
                    fontWeight: 900,
                    color: '#101828',
                    letterSpacing: '-0.02em',
                    lineHeight: 1.1
                  }}>
                    {s.value}
                  </div>
                  <div style={{
                    fontSize: 12,
                    fontWeight: 700,
                    color: '#5B5CEB',
                    textTransform: 'uppercase',
                    letterSpacing: '0.04em',
                    marginTop: 4
                  }}>
                    {s.label}
                  </div>
                  <div style={{
                    fontSize: 11,
                    color: '#94A3B8',
                    marginTop: 2,
                    display: 'none'
                  }}>
                    {s.sub}
                  </div>
                </div>
              ))}
            </div>

          </div>

          {/* ──────────────────────────────────────────────
              HERO ANIMATION: THE AI BATTLEFIELD VISUAL
          ────────────────────────────────────────────── */}
          <div style={{
            position: 'relative',
            maxWidth: 960,
            margin: '0 auto',
            background: '#FFFFFF',
            borderRadius: 20,
            border: '1px solid rgba(201, 154, 61, 0.3)',
            boxShadow: '0 16px 40px -10px rgba(91, 92, 235, 0.12), 0 0 0 1px rgba(16, 24, 40, 0.04)',
            overflow: 'hidden',
            padding: '36px 24px 28px'
          }}>

            {/* Tactical Frame Headers */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              borderBottom: '1px solid rgba(16, 24, 40, 0.06)',
              paddingBottom: 16,
              marginBottom: 28
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <div style={{ display: 'flex', gap: 6 }}>
                  <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#EF4444' }} />
                  <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#F59E0B' }} />
                  <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#10B981' }} />
                </div>
                <div style={{
                  fontSize: 12,
                  fontFamily: 'var(--font-mono)',
                  color: '#64748B',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 6
                }}>
                  <span style={{ color: '#5B5CEB', fontWeight: 600 }}>kurukshetra.ai</span>
                  <span>/</span>
                  <span>arena:orchestrator-v2</span>
                </div>
              </div>

              <div style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 8,
                background: '#FCFAF5',
                border: '1px solid rgba(201, 154, 61, 0.4)',
                padding: '4px 12px',
                borderRadius: 100,
                fontSize: 11,
                fontWeight: 700,
                color: '#C99A3D'
              }}>
                <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#10B981' }} />
                STRATEGY RADAR ACTIVE
              </div>
            </div>

            {/* Visual Radar Formation Canvas */}
            <div style={{
              position: 'relative',
              width: '100%',
              minHeight: 460,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              background: 'radial-gradient(circle at center, #F1F0FF 0%, #FCFAF5 35%, #FFFFFF 70%)',
              borderRadius: 16,
              border: '1px solid rgba(16, 24, 40, 0.05)',
              overflow: 'hidden'
            }}>

              {/* Concentric Battlefield Rings SVG */}
              <svg
                style={{
                  position: 'absolute',
                  inset: 0,
                  width: '100%',
                  height: '100%',
                  pointerEvents: 'none'
                }}
                viewBox="0 0 900 460"
                fill="none"
              >
                <defs>
                  <radialGradient id="battleGlow" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stopColor="#5B5CEB" stopOpacity="0.12" />
                    <stop offset="60%" stopColor="#C99A3D" stopOpacity="0.04" />
                    <stop offset="100%" stopColor="transparent" stopOpacity="0" />
                  </radialGradient>
                </defs>

                <circle cx="450" cy="230" r="210" fill="url(#battleGlow)" />

                {/* Outer Concentric Radar Ring */}
                <circle
                  cx="450" cy="230" r="190"
                  stroke="rgba(201, 154, 61, 0.3)"
                  strokeWidth="1"
                  strokeDasharray="4 8"
                  className="animate-radar-slow"
                  style={{ transformOrigin: '450px 230px' }}
                />

                {/* Middle Tactical Ring */}
                <circle
                  cx="450" cy="230" r="130"
                  stroke="rgba(91, 92, 235, 0.3)"
                  strokeWidth="1.2"
                  strokeDasharray="8 6"
                  className="animate-radar-rev"
                  style={{ transformOrigin: '450px 230px' }}
                />

                {/* Inner Core Ring */}
                <circle
                  cx="450" cy="230" r="70"
                  stroke="rgba(201, 154, 61, 0.4)"
                  strokeWidth="1.5"
                />

                {/* Crosshairs & Tactical Axis */}
                <line x1="240" y1="230" x2="660" y2="230" stroke="rgba(16, 24, 40, 0.08)" strokeDasharray="3 3" />
                <line x1="450" y1="40" x2="450" y2="420" stroke="rgba(16, 24, 40, 0.08)" strokeDasharray="3 3" />

                {/* Laser Telemetry Lines connecting Central Idea to 6 Perimeter Agent Nodes */}
                {/* 1. Scout (Top) */}
                <line x1="450" y1="190" x2="450" y2="90" stroke="#5B5CEB" strokeWidth="1.5" className="animate-laser-line" />
                {/* 2. Opponent (Top Right) */}
                <line x1="480" y1="205" x2="640" y2="120" stroke="#0EA5E9" strokeWidth="1.5" className="animate-laser-line" />
                {/* 3. Treasury (Bottom Right) */}
                <line x1="480" y1="250" x2="640" y2="340" stroke="#C99A3D" strokeWidth="1.5" className="animate-laser-line" />
                {/* 4. Commander (Bottom) */}
                <line x1="450" y1="270" x2="450" y2="370" stroke="#8B5CF6" strokeWidth="1.5" className="animate-laser-line" />
                {/* 5. Critic (Bottom Left) */}
                <line x1="420" y1="250" x2="260" y2="340" stroke="#EF4444" strokeWidth="1.5" className="animate-laser-line" />
                {/* 6. Debate (Top Left) */}
                <line x1="420" y1="205" x2="260" y2="120" stroke="#10B981" strokeWidth="1.5" className="animate-laser-line" />
              </svg>

              {/* ── Central Core: "YOUR STARTUP IDEA" ── */}
              <div style={{
                position: 'relative',
                zIndex: 10,
                textAlign: 'center',
                cursor: 'pointer'
              }}>
                <div style={{
                  width: 90,
                  height: 90,
                  borderRadius: '50%',
                  background: 'linear-gradient(135deg, #101828 0%, #1D2939 100%)',
                  border: '2px solid #C99A3D',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  boxShadow: '0 0 30px rgba(91, 92, 235, 0.4), 0 0 15px rgba(201, 154, 61, 0.4)',
                  margin: '0 auto',
                  position: 'relative'
                }} className="animate-tactical-pulse">
                  <span style={{ fontSize: 22 }}>💡</span>
                  <span style={{
                    fontSize: 9,
                    fontWeight: 800,
                    color: '#FCFAF5',
                    letterSpacing: '0.08em',
                    textTransform: 'uppercase',
                    marginTop: 2
                  }}>
                    STARTUP
                  </span>
                  <div style={{
                    position: 'absolute',
                    inset: -6,
                    borderRadius: '50%',
                    border: '1px dashed rgba(201, 154, 61, 0.5)'
                  }} />
                </div>
                <div style={{
                  fontSize: 12,
                  fontWeight: 800,
                  color: '#101828',
                  marginTop: 8,
                  letterSpacing: '0.04em'
                }}>
                  YOUR STARTUP IDEA
                </div>
                <div style={{
                  fontSize: 10,
                  fontWeight: 600,
                  color: '#5B5CEB',
                  background: '#F1F0FF',
                  padding: '2px 8px',
                  borderRadius: 100,
                  display: 'inline-block',
                  marginTop: 2
                }}>
                  Core Target Vector
                </div>
              </div>

              {/* ── Perimeter Agent Cards ── */}

              {/* 1. Intelligence Scout (Top) */}
              <div
                onClick={() => setSelectedAgent(AGENTS[0])}
                style={{
                  position: 'absolute', top: 22, left: '50%', transform: 'translateX(-50%)',
                  zIndex: 10, cursor: 'pointer'
                }}
                className="animate-float-1"
              >
                <div style={{
                  background: '#FFFFFF',
                  padding: '8px 14px',
                  borderRadius: 10,
                  border: selectedAgent.id === 'scout' ? '2px solid #5B5CEB' : '1px solid rgba(91, 92, 235, 0.25)',
                  boxShadow: '0 4px 14px rgba(91, 92, 235, 0.12)',
                  display: 'flex', alignItems: 'center', gap: 8,
                  transition: 'all 0.2s ease'
                }}>
                  <div style={{ width: 24, height: 24, borderRadius: 6, background: '#F1F0FF', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Globe className="w-3.5 h-3.5" style={{ color: '#5B5CEB' }} />
                  </div>
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 800, color: '#101828' }}>Intelligence Scout</div>
                    <div style={{ fontSize: 9, color: '#5B5CEB', fontWeight: 600 }}>Market Research</div>
                  </div>
                </div>
              </div>

              {/* 2. Opponent Analyst (Top Right) */}
              <div
                onClick={() => setSelectedAgent(AGENTS[1])}
                style={{
                  position: 'absolute', top: 50, right: '8%',
                  zIndex: 10, cursor: 'pointer'
                }}
                className="animate-float-2"
              >
                <div style={{
                  background: '#FFFFFF',
                  padding: '8px 14px',
                  borderRadius: 10,
                  border: selectedAgent.id === 'opponent' ? '2px solid #0EA5E9' : '1px solid rgba(14, 165, 233, 0.25)',
                  boxShadow: '0 4px 14px rgba(14, 165, 233, 0.12)',
                  display: 'flex', alignItems: 'center', gap: 8,
                  transition: 'all 0.2s ease'
                }}>
                  <div style={{ width: 24, height: 24, borderRadius: 6, background: '#F0F9FF', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Users className="w-3.5 h-3.5" style={{ color: '#0EA5E9' }} />
                  </div>
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 800, color: '#101828' }}>Opponent Analyst</div>
                    <div style={{ fontSize: 9, color: '#0EA5E9', fontWeight: 600 }}>Competitive Moats</div>
                  </div>
                </div>
              </div>

              {/* 3. Treasury Advisor (Bottom Right) */}
              <div
                onClick={() => setSelectedAgent(AGENTS[2])}
                style={{
                  position: 'absolute', bottom: 50, right: '8%',
                  zIndex: 10, cursor: 'pointer'
                }}
                className="animate-float-1"
              >
                <div style={{
                  background: '#FFFFFF',
                  padding: '8px 14px',
                  borderRadius: 10,
                  border: selectedAgent.id === 'treasury' ? '2px solid #C99A3D' : '1px solid rgba(201, 154, 61, 0.35)',
                  boxShadow: '0 4px 14px rgba(201, 154, 61, 0.15)',
                  display: 'flex', alignItems: 'center', gap: 8,
                  transition: 'all 0.2s ease'
                }}>
                  <div style={{ width: 24, height: 24, borderRadius: 6, background: '#FCFAF5', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <BarChart2 className="w-3.5 h-3.5" style={{ color: '#C99A3D' }} />
                  </div>
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 800, color: '#101828' }}>Treasury Advisor</div>
                    <div style={{ fontSize: 9, color: '#C99A3D', fontWeight: 600 }}>Financial Feasibility</div>
                  </div>
                </div>
              </div>

              {/* 4. Strategy Commander (Bottom) */}
              <div
                onClick={() => setSelectedAgent(AGENTS[3])}
                style={{
                  position: 'absolute', bottom: 22, left: '50%', transform: 'translateX(-50%)',
                  zIndex: 10, cursor: 'pointer'
                }}
                className="animate-float-2"
              >
                <div style={{
                  background: '#FFFFFF',
                  padding: '8px 14px',
                  borderRadius: 10,
                  border: selectedAgent.id === 'commander' ? '2px solid #8B5CF6' : '1px solid rgba(139, 92, 246, 0.25)',
                  boxShadow: '0 4px 14px rgba(139, 92, 246, 0.12)',
                  display: 'flex', alignItems: 'center', gap: 8,
                  transition: 'all 0.2s ease'
                }}>
                  <div style={{ width: 24, height: 24, borderRadius: 6, background: '#F5F3FF', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Target className="w-3.5 h-3.5" style={{ color: '#8B5CF6' }} />
                  </div>
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 800, color: '#101828' }}>Strategy Commander</div>
                    <div style={{ fontSize: 9, color: '#8B5CF6', fontWeight: 600 }}>GTM Architecture</div>
                  </div>
                </div>
              </div>

              {/* 5. Critic Agent (Bottom Left) */}
              <div
                onClick={() => setSelectedAgent(AGENTS[4])}
                style={{
                  position: 'absolute', bottom: 50, left: '8%',
                  zIndex: 10, cursor: 'pointer'
                }}
                className="animate-float-1"
              >
                <div style={{
                  background: '#FFFFFF',
                  padding: '8px 14px',
                  borderRadius: 10,
                  border: selectedAgent.id === 'critic' ? '2px solid #EF4444' : '1px solid rgba(239, 68, 68, 0.25)',
                  boxShadow: '0 4px 14px rgba(239, 68, 68, 0.12)',
                  display: 'flex', alignItems: 'center', gap: 8,
                  transition: 'all 0.2s ease'
                }}>
                  <div style={{ width: 24, height: 24, borderRadius: 6, background: '#FEF2F2', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Shield className="w-3.5 h-3.5" style={{ color: '#EF4444' }} />
                  </div>
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 800, color: '#101828' }}>Critic Agent</div>
                    <div style={{ fontSize: 9, color: '#EF4444', fontWeight: 600 }}>Adversarial Skeptic</div>
                  </div>
                </div>
              </div>

              {/* 6. Debate Engine (Top Left) */}
              <div
                onClick={() => setSelectedAgent(AGENTS[5])}
                style={{
                  position: 'absolute', top: 50, left: '8%',
                  zIndex: 10, cursor: 'pointer'
                }}
                className="animate-float-2"
              >
                <div style={{
                  background: '#FFFFFF',
                  padding: '8px 14px',
                  borderRadius: 10,
                  border: selectedAgent.id === 'debate' ? '2px solid #10B981' : '1px solid rgba(16, 185, 129, 0.25)',
                  boxShadow: '0 4px 14px rgba(16, 185, 129, 0.12)',
                  display: 'flex', alignItems: 'center', gap: 8,
                  transition: 'all 0.2s ease'
                }}>
                  <div style={{ width: 24, height: 24, borderRadius: 6, background: '#ECFDF5', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Scale className="w-3.5 h-3.5" style={{ color: '#10B981' }} />
                  </div>
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 800, color: '#101828' }}>Debate Engine</div>
                    <div style={{ fontSize: 9, color: '#10B981', fontWeight: 600 }}>Tri-Party Scrutiny</div>
                  </div>
                </div>
              </div>

            </div>

            {/* Selected Agent Briefing Bar */}
            <div style={{
              marginTop: 20,
              padding: '14px 20px',
              borderRadius: 12,
              background: '#F8FAFC',
              border: '1px solid rgba(16, 24, 40, 0.08)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              flexWrap: 'wrap',
              gap: 12
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <span style={{ fontSize: 13, fontWeight: 800, color: '#101828' }}>
                  ACTIVE AGENT COUNSEL:
                </span>
                <span style={{
                  fontSize: 12,
                  fontWeight: 700,
                  color: selectedAgent.color,
                  background: selectedAgent.bg,
                  padding: '3px 10px',
                  borderRadius: 6
                }}>
                  {selectedAgent.name} ({selectedAgent.role})
                </span>
                <span style={{ fontSize: 12, color: '#475569' }}>
                  {selectedAgent.weapon}
                </span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <span style={{ fontSize: 11, color: '#64748B' }}>Flow Direction:</span>
                <span style={{ fontSize: 11, fontWeight: 700, color: '#5B5CEB', letterSpacing: '0.04em' }}>
                  IDEA → 7 AGENTS → VERDICT
                </span>
              </div>
            </div>

          </div>

        </div>
      </section>

      {/* ══════════════════════════════════════════════
          02 NEW SECTION: THE BATTLEFIELD
      ══════════════════════════════════════════════ */}
      <section style={{
        padding: '96px 0 88px',
        background: '#FFFFFF',
        borderBottom: '1px solid rgba(16, 24, 40, 0.08)',
        position: 'relative'
      }}>
        <div className="container">

          {/* Section Header */}
          <div style={{ textAlign: 'center', maxWidth: 760, margin: '0 auto 60px' }}>
            <div style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 8,
              fontSize: 12,
              fontWeight: 800,
              letterSpacing: '0.1em',
              textTransform: 'uppercase',
              color: '#C99A3D',
              marginBottom: 12
            }}>
              <span>⚔</span> THE BATTLEFIELD <span>⚔</span>
            </div>

            <h2 style={{
              fontSize: 'clamp(32px, 4.5vw, 48px)',
              fontWeight: 900,
              color: '#101828',
              letterSpacing: '-0.03em',
              lineHeight: 1.15,
              margin: '0 0 16px'
            }}>
              Every startup idea enters the battlefield.
            </h2>

            <p style={{
              fontSize: 18,
              color: '#64748B',
              lineHeight: 1.6,
              margin: 0
            }}>
              One idea. Seven AI specialists. One final verdict.
            </p>
          </div>

          {/* Interactive 5-Stage Battlefield Pipeline */}
          <div style={{ maxWidth: 1040, margin: '0 auto' }}>

            {/* Stage Selector Pills */}
            <div className="kuruk-pipeline-tabs" style={{
              marginBottom: 32
            }}>
              {PIPELINE_STAGES.map((s, idx) => (
                <button
                  key={s.stage}
                  onClick={() => setSelectedStage(idx)}
                  style={{
                    background: selectedStage === idx ? '#101828' : '#F8FAFC',
                    color: selectedStage === idx ? '#FFFFFF' : '#475569',
                    border: selectedStage === idx ? '1px solid #101828' : '1px solid rgba(16, 24, 40, 0.08)',
                    borderRadius: 10,
                    padding: '12px 10px',
                    textAlign: 'left',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                    boxShadow: selectedStage === idx ? '0 4px 14px rgba(16, 24, 40, 0.15)' : 'none'
                  }}
                >
                  <div style={{
                    fontSize: 11,
                    fontWeight: 800,
                    fontFamily: 'var(--font-mono)',
                    color: selectedStage === idx ? '#C99A3D' : '#94A3B8',
                    marginBottom: 4
                  }}>
                    {s.stage} //
                  </div>
                  <div style={{
                    fontSize: 12,
                    fontWeight: 700,
                    whiteSpace: 'nowrap',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis'
                  }}>
                    {s.title}
                  </div>
                </button>
              ))}
            </div>

            {/* Active Stage Spotlight Card */}
            <div style={{
              background: '#FCFAF5',
              border: '1px solid rgba(201, 154, 61, 0.35)',
              borderRadius: 18,
              padding: '32px 36px',
              boxShadow: '0 8px 24px rgba(0, 0, 0, 0.04)',
              position: 'relative'
            }}>
              <div className="tactical-bracket-tl" />
              <div className="tactical-bracket-br" />

              <div style={{
                display: 'flex',
                alignItems: 'flex-start',
                justifyContent: 'space-between',
                flexWrap: 'wrap',
                gap: 20,
                marginBottom: 20
              }}>
                <div>
                  <div style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: 6,
                    padding: '4px 12px',
                    borderRadius: 100,
                    background: '#F1F0FF',
                    border: '1px solid rgba(91, 92, 235, 0.3)',
                    color: '#5B5CEB',
                    fontSize: 11,
                    fontWeight: 700,
                    marginBottom: 12
                  }}>
                    {PIPELINE_STAGES[selectedStage].badge}
                  </div>

                  <h3 style={{
                    fontSize: 26,
                    fontWeight: 800,
                    color: '#101828',
                    margin: '0 0 6px',
                    letterSpacing: '-0.02em'
                  }}>
                    {PIPELINE_STAGES[selectedStage].title}
                  </h3>

                  <div style={{ fontSize: 14, fontWeight: 600, color: '#C99A3D' }}>
                    {PIPELINE_STAGES[selectedStage].subtitle}
                  </div>
                </div>

                <div style={{
                  background: '#FFFFFF',
                  border: '1px solid rgba(16, 24, 40, 0.08)',
                  borderRadius: 12,
                  padding: '12px 18px',
                  textAlign: 'right'
                }}>
                  <div style={{ fontSize: 11, color: '#94A3B8', fontWeight: 600, textTransform: 'uppercase' }}>
                    Responsible AI Agents
                  </div>
                  <div style={{ fontSize: 13, fontWeight: 700, color: '#5B5CEB', marginTop: 2 }}>
                    {PIPELINE_STAGES[selectedStage].agent}
                  </div>
                </div>
              </div>

              <p style={{
                fontSize: 16,
                color: '#334155',
                lineHeight: 1.7,
                margin: '0 0 24px',
                maxWidth: 820
              }}>
                {PIPELINE_STAGES[selectedStage].desc}
              </p>

              {/* Connecting Pipeline Graphic */}
              <div style={{
                borderTop: '1px solid rgba(201, 154, 61, 0.25)',
                paddingTop: 20,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                flexWrap: 'wrap',
                gap: 12
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 12, color: '#64748B' }}>
                  <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#10B981' }} />
                  <span>Deterministic execution via LangGraph multi-agent choreography</span>
                </div>

                <Link
                  href="/battlefield"
                  style={{
                    fontSize: 13,
                    fontWeight: 700,
                    color: '#5B5CEB',
                    textDecoration: 'none',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: 6
                  }}
                >
                  Inspect Live Battlefield Graph <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            </div>

          </div>

        </div>
      </section>

      {/* ══════════════════════════════════════════════
          03 PLATFORM PREVIEW — BATTLE SCORE DASHBOARD
      ══════════════════════════════════════════════ */}
      <section style={{
        padding: '96px 0',
        background: '#F5F7FA',
        borderBottom: '1px solid rgba(16, 24, 40, 0.08)'
      }}>
        <div className="container">

          {/* Section Header */}
          <div style={{ textAlign: 'center', maxWidth: 720, margin: '0 auto 48px' }}>
            <div style={{
              fontSize: 11,
              fontWeight: 800,
              letterSpacing: '0.1em',
              textTransform: 'uppercase',
              color: '#5B5CEB',
              marginBottom: 10
            }}>
              PLATFORM PREVIEW
            </div>

            <h2 style={{
              fontSize: 'clamp(28px, 4vw, 42px)',
              fontWeight: 900,
              color: '#101828',
              letterSpacing: '-0.025em',
              margin: '0 0 14px'
            }}>
              Intelligence for every startup decision
            </h2>

            <p style={{ fontSize: 16, color: '#64748B', margin: 0 }}>
              The definitive Battle Score dashboard synthesized from 100+ multi-agent market vectors.
            </p>
          </div>

          {/* High-Fidelity Interactive Dashboard Preview Card */}
          <div style={{
            maxWidth: 960,
            margin: '0 auto',
            background: '#FFFFFF',
            borderRadius: 18,
            border: '1px solid rgba(16, 24, 40, 0.1)',
            boxShadow: '0 20px 45px -12px rgba(91, 92, 235, 0.12)',
            overflow: 'hidden'
          }}>

            {/* Browser / Shell Header */}
            <div style={{
              background: '#101828',
              padding: '14px 20px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#EF4444' }} />
                <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#F59E0B' }} />
                <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#10B981' }} />
                <span style={{ marginLeft: 12, fontSize: 12, color: 'rgba(255, 255, 255, 0.5)', fontFamily: 'var(--font-mono)' }}>
                  kurukshetra.ai/battlefield/session-4089
                </span>
              </div>

              {/* Preview Mode Switcher */}
              <div style={{ display: 'flex', gap: 4 }}>
                <button
                  onClick={() => setPreviewTab('score')}
                  style={{
                    padding: '4px 12px',
                    borderRadius: 6,
                    fontSize: 12,
                    fontWeight: 600,
                    cursor: 'pointer',
                    background: previewTab === 'score' ? '#5B5CEB' : 'transparent',
                    color: previewTab === 'score' ? '#FFFFFF' : 'rgba(255, 255, 255, 0.7)',
                    border: 'none'
                  }}
                >
                  Score Summary
                </button>
                <button
                  onClick={() => setPreviewTab('debate')}
                  style={{
                    padding: '4px 12px',
                    borderRadius: 6,
                    fontSize: 12,
                    fontWeight: 600,
                    cursor: 'pointer',
                    background: previewTab === 'debate' ? '#5B5CEB' : 'transparent',
                    color: previewTab === 'debate' ? '#FFFFFF' : 'rgba(255, 255, 255, 0.7)',
                    border: 'none'
                  }}
                >
                  Live Debate
                </button>
                <button
                  onClick={() => setPreviewTab('evidence')}
                  style={{
                    padding: '4px 12px',
                    borderRadius: 6,
                    fontSize: 12,
                    fontWeight: 600,
                    cursor: 'pointer',
                    background: previewTab === 'evidence' ? '#5B5CEB' : 'transparent',
                    color: previewTab === 'evidence' ? '#FFFFFF' : 'rgba(255, 255, 255, 0.7)',
                    border: 'none'
                  }}
                >
                  Evidence & Signals
                </button>
              </div>
            </div>

            {/* Dashboard Content Panes */}
            <div style={{ padding: 28 }}>

              {previewTab === 'score' && (
                <div>
                  {/* KPI Row */}
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 14, marginBottom: 24 }}>
                    {[
                      { label: 'BATTLE SCORE', value: '72 / 100', color: '#10B981', sub: 'Calculated from 100+ metrics' },
                      { label: 'FINAL VERDICT', value: 'PROCEED', color: '#10B981', sub: 'High conviction with guardrails' },
                      { label: 'CONFIDENCE', value: '84%', color: '#5B5CEB', sub: 'High statistical confidence' },
                      { label: 'TARGET GEOGRAPHY', value: 'India (₹)', color: '#C99A3D', sub: 'Tier 1 & Tier 2 Focus' },
                    ].map(k => (
                      <div key={k.label} style={{
                        background: '#FCFAF5',
                        borderRadius: 12,
                        padding: '16px 18px',
                        border: '1px solid rgba(201, 154, 61, 0.25)'
                      }}>
                        <div style={{ fontSize: 11, fontWeight: 800, color: '#64748B', letterSpacing: '0.06em', marginBottom: 4 }}>
                          {k.label}
                        </div>
                        <div style={{ fontSize: 24, fontWeight: 900, color: k.color, letterSpacing: '-0.02em' }}>
                          {k.value}
                        </div>
                        <div style={{ fontSize: 11, color: '#94A3B8', marginTop: 2 }}>
                          {k.sub}
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Strategic Score Vector Bars */}
                  <div style={{
                    display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginBottom: 24,
                    padding: '20px', background: '#F8FAFC', borderRadius: 12, border: '1px solid rgba(16, 24, 40, 0.06)'
                  }}>
                    <div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, fontWeight: 700, marginBottom: 6 }}>
                        <span>Market Sizing & Demand Pull</span>
                        <span style={{ color: '#10B981' }}>78 / 100</span>
                      </div>
                      <div style={{ height: 6, borderRadius: 3, background: '#E2E8F0', overflow: 'hidden' }}>
                        <div style={{ width: '78%', height: '100%', background: '#10B981', borderRadius: 3 }} />
                      </div>

                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, fontWeight: 700, margin: '14px 0 6px' }}>
                        <span>Unit Economics & Margin Viability</span>
                        <span style={{ color: '#5B5CEB' }}>74 / 100</span>
                      </div>
                      <div style={{ height: 6, borderRadius: 3, background: '#E2E8F0', overflow: 'hidden' }}>
                        <div style={{ width: '74%', height: '100%', background: '#5B5CEB', borderRadius: 3 }} />
                      </div>
                    </div>

                    <div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, fontWeight: 700, marginBottom: 6 }}>
                        <span>Competitive Defensibility & Moat</span>
                        <span style={{ color: '#C99A3D' }}>68 / 100</span>
                      </div>
                      <div style={{ height: 6, borderRadius: 3, background: '#E2E8F0', overflow: 'hidden' }}>
                        <div style={{ width: '68%', height: '100%', background: '#C99A3D', borderRadius: 3 }} />
                      </div>

                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, fontWeight: 700, margin: '14px 0 6px' }}>
                        <span>Execution & GTM Feasibility</span>
                        <span style={{ color: '#10B981' }}>82 / 100</span>
                      </div>
                      <div style={{ height: 6, borderRadius: 3, background: '#E2E8F0', overflow: 'hidden' }}>
                        <div style={{ width: '82%', height: '100%', background: '#10B981', borderRadius: 3 }} />
                      </div>
                    </div>
                  </div>

                  {/* SWOT Insights Box */}
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14 }}>
                    <div style={{ background: '#F0FDF4', borderRadius: 10, padding: '16px 20px', border: '1px solid rgba(16, 185, 129, 0.25)' }}>
                      <div style={{ fontSize: 11, fontWeight: 800, color: '#15803D', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 8, display: 'flex', alignItems: 'center', gap: 6 }}>
                        <CheckCircle className="w-3.5 h-3.5" /> CONFIRMED STRATEGIC STRENGTHS
                      </div>
                      <div style={{ fontSize: 13, color: '#334155', padding: '3px 0' }}>• High customer willingness-to-pay identified in Tier 1 cities</div>
                      <div style={{ fontSize: 13, color: '#334155', padding: '3px 0' }}>• Zero friction onboarding with UPI & IndiaStack integration</div>
                    </div>

                    <div style={{ background: '#FFF1F2', borderRadius: 10, padding: '16px 20px', border: '1px solid rgba(239, 68, 68, 0.25)' }}>
                      <div style={{ fontSize: 11, fontWeight: 800, color: '#BE123C', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 8, display: 'flex', alignItems: 'center', gap: 6 }}>
                        <AlertTriangle className="w-3.5 h-3.5" /> CRITICAL RISKS STRESS-TESTED
                      </div>
                      <div style={{ fontSize: 13, color: '#334155', padding: '3px 0' }}>• Paid CAC inflation if organic word-of-mouth fails in Year 1</div>
                      <div style={{ fontSize: 13, color: '#334155', padding: '3px 0' }}>• Mandatory RBI & GST compliance audit required prior to launch</div>
                    </div>
                  </div>
                </div>
              )}

              {previewTab === 'debate' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
                  <div style={{ background: '#F0FDF4', border: '1px solid #BBF7D0', borderRadius: 10, padding: '14px 18px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
                      <span style={{ fontSize: 12, fontWeight: 800, color: '#15803D' }}>PROPONENT AGENT · DEFENSE ARGUMENT</span>
                      <span style={{ fontSize: 10, color: '#64748B' }}>Round 1</span>
                    </div>
                    <p style={{ fontSize: 13, color: '#1E293B', margin: 0, lineHeight: 1.6 }}>
                      "The market TAM in India is expanding at 28.4% CAGR. Rapid smartphone adoption and native UPI AutoPay mechanisms dramatically compress customer acquisition cycles."
                    </p>
                  </div>

                  <div style={{ background: '#FEF2F2', border: '1px solid #FECACA', borderRadius: 10, padding: '14px 18px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
                      <span style={{ fontSize: 12, fontWeight: 800, color: '#B91C1C' }}>CRITIC SKEPTIC · CROSS-EXAMINATION</span>
                      <span style={{ fontSize: 10, color: '#64748B' }}>Round 2</span>
                    </div>
                    <p style={{ fontSize: 13, color: '#1E293B', margin: 0, lineHeight: 1.6 }}>
                      "Rebuttal: CAC in Tier 2 cities remains unproven. If unit economics assume an LTV/CAC ratio of 3.5x without factoring customer churn in month 3, the business will face severe cash bleed."
                    </p>
                  </div>

                  <div style={{ background: '#FCFAF5', border: '1px solid rgba(201, 154, 61, 0.4)', borderRadius: 10, padding: '14px 18px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
                      <span style={{ fontSize: 12, fontWeight: 800, color: '#C99A3D' }}>JUDGE AGENT · RULING & VERDICT</span>
                      <span style={{ fontSize: 10, color: '#64748B' }}>Final Synthesis</span>
                    </div>
                    <p style={{ fontSize: 13, color: '#1E293B', margin: 0, lineHeight: 1.6 }}>
                      "Ruling: The core thesis holds, but the founder must adjust initial GTM to focus purely on Tier 1 organic density before expanding capital expenditure to regional markets. Verdict: PROCEED with guardrails."
                    </p>
                  </div>
                </div>
              )}

              {previewTab === 'evidence' && (
                <div>
                  <div style={{ fontSize: 13, fontWeight: 700, color: '#101828', marginBottom: 12 }}>
                    Live Retrieved Citations & Data Signals
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                    {[
                      { source: 'Tavily Deep Web Search', query: 'India B2B SaaS adoption trends 2025', confidence: '94%' },
                      { source: 'Serper Intelligence Radar', query: 'Direct competitor pricing models & seat tiers', confidence: '89%' },
                      { source: 'ChromaDB Knowledge Base', query: 'Reserve Bank of India regulatory compliance benchmarks', confidence: '98%' }
                    ].map((e, idx) => (
                      <div key={idx} style={{
                        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                        background: '#F8FAFC', padding: '12px 16px', borderRadius: 8, border: '1px solid rgba(16, 24, 40, 0.06)'
                      }}>
                        <div>
                          <div style={{ fontSize: 12, fontWeight: 700, color: '#5B5CEB' }}>{e.source}</div>
                          <div style={{ fontSize: 12, color: '#475569', marginTop: 2 }}>{e.query}</div>
                        </div>
                        <span style={{ fontSize: 11, fontWeight: 700, color: '#10B981', background: '#ECFDF5', padding: '3px 8px', borderRadius: 6 }}>
                          {e.confidence} Verified
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

            </div>

          </div>

        </div>
      </section>

      {/* ══════════════════════════════════════════════
          04 CAPABILITIES (6 CARDS)
      ══════════════════════════════════════════════ */}
      <section style={{
        padding: '96px 0',
        background: '#FFFFFF',
        borderBottom: '1px solid rgba(16, 24, 40, 0.08)'
      }}>
        <div className="container">

          {/* Section Header */}
          <div style={{ textAlign: 'center', maxWidth: 720, margin: '0 auto 56px' }}>
            <div style={{
              fontSize: 11,
              fontWeight: 800,
              letterSpacing: '0.1em',
              textTransform: 'uppercase',
              color: '#5B5CEB',
              marginBottom: 10
            }}>
              CAPABILITIES
            </div>

            <h2 style={{
              fontSize: 'clamp(32px, 4vw, 44px)',
              fontWeight: 900,
              color: '#101828',
              letterSpacing: '-0.03em',
              margin: '0 0 16px'
            }}>
              Everything you need to validate a startup
            </h2>

            <p style={{ fontSize: 16, color: '#64748B', margin: 0 }}>
              A comprehensive multi-agent AI pipeline that leaves no assumption unchallenged.
            </p>
          </div>

          {/* 6 Capabilities Grid */}
          <div className="kuruk-capabilities-grid">
            {CAPABILITIES.map(c => (
              <div
                key={c.title}
                className="tactical-corner-card"
                style={{ padding: '32px 28px' }}
              >
                <div className="tactical-bracket-tl" />
                <div className="tactical-bracket-br" />

                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  marginBottom: 20
                }}>
                  <div style={{
                    width: 44,
                    height: 44,
                    borderRadius: 12,
                    background: '#F1F0FF',
                    border: '1px solid rgba(91, 92, 235, 0.25)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    boxShadow: '0 2px 8px rgba(91, 92, 235, 0.15)'
                  }}>
                    <c.icon className="w-5 h-5" style={{ color: '#5B5CEB' }} />
                  </div>

                  <span style={{
                    fontSize: 11,
                    fontWeight: 700,
                    color: '#C99A3D',
                    background: '#FCFAF5',
                    border: '1px solid rgba(201, 154, 61, 0.3)',
                    padding: '3px 8px',
                    borderRadius: 6
                  }}>
                    {c.tag}
                  </span>
                </div>

                <h3 style={{
                  fontSize: 18,
                  fontWeight: 800,
                  color: '#101828',
                  margin: '0 0 10px',
                  letterSpacing: '-0.01em'
                }}>
                  {c.title}
                </h3>

                <p style={{
                  fontSize: 14,
                  color: '#475569',
                  lineHeight: 1.65,
                  margin: '0 0 20px'
                }}>
                  {c.desc}
                </p>

                <div style={{
                  borderTop: '1px solid rgba(16, 24, 40, 0.06)',
                  paddingTop: 14,
                  fontSize: 12,
                  fontWeight: 600,
                  color: '#5B5CEB',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 6
                }}>
                  <span style={{ width: 4, height: 4, borderRadius: '50%', background: '#C99A3D' }} />
                  {c.metric}
                </div>
              </div>
            ))}
          </div>

        </div>
      </section>

      {/* ══════════════════════════════════════════════
          05 HOW IT WORKS — BATTLEFIELD JOURNEY
      ══════════════════════════════════════════════ */}
      <section id="how-it-works" style={{
        padding: '96px 0',
        background: '#F5F7FA',
        borderBottom: '1px solid rgba(16, 24, 40, 0.08)'
      }}>
        <div className="container">

          {/* Section Header */}
          <div style={{ textAlign: 'center', maxWidth: 720, margin: '0 auto 60px' }}>
            <div style={{
              fontSize: 11,
              fontWeight: 800,
              letterSpacing: '0.1em',
              textTransform: 'uppercase',
              color: '#C99A3D',
              marginBottom: 10
            }}>
              HOW IT WORKS
            </div>

            <h2 style={{
              fontSize: 'clamp(32px, 4vw, 44px)',
              fontWeight: 900,
              color: '#101828',
              letterSpacing: '-0.03em',
              margin: '0 0 16px'
            }}>
              The 5-Stage Battlefield Journey
            </h2>

            <p style={{ fontSize: 16, color: '#64748B', margin: 0 }}>
              From initial founder thesis to an unsparing, data-backed strategic verdict.
            </p>
          </div>

          {/* Connected Steps Pipeline */}
          <div className="kuruk-steps-grid" style={{ position: 'relative' }}>
            {STEPS.map((s, idx) => (
              <div
                key={s.num}
                style={{
                  background: '#FFFFFF',
                  borderRadius: 14,
                  padding: '24px 20px',
                  border: '1px solid rgba(16, 24, 40, 0.08)',
                  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.03)',
                  display: 'flex',
                  flexDirection: 'column',
                  position: 'relative',
                  transition: 'transform 0.2s ease, border-color 0.2s ease'
                }}
              >
                {/* Step Marker */}
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  marginBottom: 16
                }}>
                  <div style={{
                    width: 34,
                    height: 34,
                    borderRadius: '50%',
                    background: idx === 0 ? '#101828' : '#F1F0FF',
                    color: idx === 0 ? '#C99A3D' : '#5B5CEB',
                    border: '1px solid rgba(201, 154, 61, 0.3)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 13,
                    fontWeight: 800,
                    fontFamily: 'var(--font-mono)'
                  }}>
                    {s.num}
                  </div>

                  <span style={{ fontSize: 10, fontWeight: 700, color: '#94A3B8', textTransform: 'uppercase' }}>
                    STAGE {idx + 1}
                  </span>
                </div>

                <h3 style={{
                  fontSize: 17,
                  fontWeight: 800,
                  color: '#101828',
                  margin: '0 0 4px',
                  letterSpacing: '-0.01em'
                }}>
                  {s.title}
                </h3>

                <div style={{
                  fontSize: 12,
                  fontWeight: 600,
                  color: '#C99A3D',
                  marginBottom: 10
                }}>
                  {s.tagline}
                </div>

                <p style={{
                  fontSize: 13,
                  color: '#475569',
                  lineHeight: 1.6,
                  margin: 0,
                  flex: 1
                }}>
                  {s.desc}
                </p>
              </div>
            ))}
          </div>

        </div>
      </section>

      {/* ══════════════════════════════════════════════
          06 REPORT PREVIEW — 21 SECTIONS
      ══════════════════════════════════════════════ */}
      <section style={{
        padding: '96px 0',
        background: '#FFFFFF',
        borderBottom: '1px solid rgba(16, 24, 40, 0.08)'
      }}>
        <div className="container">

          <div className="kuruk-report-split">

            {/* Left Column: Report Value Proposition */}
            <div>
              <div style={{
                fontSize: 11,
                fontWeight: 800,
                letterSpacing: '0.1em',
                textTransform: 'uppercase',
                color: '#5B5CEB',
                marginBottom: 12
              }}>
                INTELLIGENCE REPORT
              </div>

              <h2 style={{
                fontSize: 'clamp(32px, 4vw, 46px)',
                fontWeight: 900,
                color: '#101828',
                lineHeight: 1.15,
                letterSpacing: '-0.03em',
                margin: '0 0 18px'
              }}>
                21-section startup report — instantly
              </h2>

              <p style={{
                fontSize: 16,
                color: '#475569',
                lineHeight: 1.7,
                margin: '0 0 28px'
              }}>
                Every analysis generates an exhaustive strategic dossier covering executive vision, market sizing, competitive dynamics, unit economics, black swan risks, and the multi-agent debate transcript.
              </p>

              {/* Export Formats */}
              <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginBottom: 32 }}>
                {['PDF Export', 'Markdown Export', 'JSON Export'].map(fmt => (
                  <span
                    key={fmt}
                    style={{
                      padding: '6px 14px',
                      borderRadius: 100,
                      background: '#FCFAF5',
                      border: '1px solid rgba(201, 154, 61, 0.4)',
                      color: '#101828',
                      fontSize: 12,
                      fontWeight: 700,
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: 6
                    }}
                  >
                    <span style={{ color: '#C99A3D' }}>✦</span> {fmt}
                  </span>
                ))}
              </div>

              <div>
                <Link
                  href="/reports"
                  className="btn btn-secondary btn-lg"
                  style={{
                    textDecoration: 'none',
                    border: '1px solid rgba(16, 24, 40, 0.15)',
                    fontWeight: 700,
                    gap: 8
                  }}
                >
                  <span>View Sample Reports</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            </div>

            {/* Right Column: 21 Report Sections Matrix */}
            <div style={{
              background: '#FCFAF5',
              border: '1px solid rgba(201, 154, 61, 0.35)',
              borderRadius: 18,
              padding: '28px',
              boxShadow: '0 12px 30px rgba(0, 0, 0, 0.04)',
              position: 'relative'
            }}>
              <div className="tactical-bracket-tl" />
              <div className="tactical-bracket-br" />

              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                borderBottom: '1px solid rgba(201, 154, 61, 0.25)',
                paddingBottom: 14,
                marginBottom: 20
              }}>
                <div style={{ fontSize: 13, fontWeight: 800, color: '#101828' }}>
                  DOSSIER BLUEPRINT STRUCTURE
                </div>
                <div style={{ fontSize: 11, fontWeight: 700, color: '#C99A3D', textTransform: 'uppercase' }}>
                  21 Complete Sections
                </div>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
                {REPORT_CATEGORIES.map(cat => (
                  <div key={cat.category}>
                    <div style={{
                      fontSize: 11,
                      fontWeight: 800,
                      color: '#5B5CEB',
                      textTransform: 'uppercase',
                      letterSpacing: '0.06em',
                      marginBottom: 6
                    }}>
                      {cat.category}
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 6 }}>
                      {cat.sections.map(s => (
                        <div
                          key={s}
                          style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: 8,
                            fontSize: 12,
                            color: '#334155',
                            padding: '3px 0'
                          }}
                        >
                          <Check className="w-3.5 h-3.5" style={{ color: '#10B981', flexShrink: 0 }} />
                          <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{s}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>

            </div>

          </div>

        </div>
      </section>

      {/* ══════════════════════════════════════════════
          07 INDIA-FIRST INTELLIGENCE
      ══════════════════════════════════════════════ */}
      <section style={{
        padding: '96px 0',
        background: '#F5F7FA',
        borderBottom: '1px solid rgba(16, 24, 40, 0.08)'
      }}>
        <div className="container">

          <div className="kuruk-split-grid">

            {/* Left: Strategic Matrix Display */}
            <div style={{
              background: '#FFFFFF',
              borderRadius: 18,
              border: '1px solid rgba(16, 24, 40, 0.1)',
              padding: '32px',
              boxShadow: '0 8px 24px rgba(0, 0, 0, 0.04)',
              position: 'relative'
            }}>
              {/* Badge Chips */}
              <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 24 }}>
                {[
                  'UPI & Digital Payments',
                  'Tier 1/2/3 Markets',
                  'GST & Compliance',
                  'Regional Languages',
                  'Aadhaar/eKYC',
                  'B2B & B2C Channels'
                ].map(tag => (
                  <span
                    key={tag}
                    style={{
                      padding: '5px 12px',
                      borderRadius: 100,
                      background: '#F1F0FF',
                      color: '#5B5CEB',
                      fontSize: 11,
                      fontWeight: 700,
                      border: '1px solid rgba(91, 92, 235, 0.2)'
                    }}
                  >
                    {tag}
                  </span>
                ))}
              </div>

              {/* 4 Dimension Matrix */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14 }}>
                {[
                  { label: 'Default Currency & Market', value: 'India (₹ INR)', detail: 'Localized purchasing power benchmarks' },
                  { label: 'Demographic Segmentation', value: 'Tier 1 · 2 · 3', detail: 'Spending propensity & price sensitivity' },
                  { label: 'Regulatory Intelligence', value: 'India-Aware', detail: 'RBI, SEBI, GST & DPDP compliance checks' },
                  { label: 'Global Flexibility', value: 'User-Defined', detail: 'Toggle instantly to US ($), EU (€), or SEA' },
                ].map(m => (
                  <div key={m.label} style={{
                    background: '#FCFAF5',
                    borderRadius: 12,
                    padding: '16px',
                    border: '1px solid rgba(201, 154, 61, 0.3)'
                  }}>
                    <div style={{ fontSize: 10, color: '#94A3B8', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 4 }}>
                      {m.label}
                    </div>
                    <div style={{ fontSize: 15, fontWeight: 800, color: '#101828', marginBottom: 2 }}>
                      {m.value}
                    </div>
                    <div style={{ fontSize: 11, color: '#64748B' }}>
                      {m.detail}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Right: Copy */}
            <div>
              <div style={{
                fontSize: 11,
                fontWeight: 800,
                letterSpacing: '0.1em',
                textTransform: 'uppercase',
                color: '#C99A3D',
                marginBottom: 12
              }}>
                INDIA-FIRST INTELLIGENCE
              </div>

              <h2 style={{
                fontSize: 'clamp(32px, 4vw, 44px)',
                fontWeight: 900,
                color: '#101828',
                lineHeight: 1.15,
                letterSpacing: '-0.03em',
                margin: '0 0 18px'
              }}>
                Built for the Indian market — by default
              </h2>

              <p style={{
                fontSize: 16,
                color: '#475569',
                lineHeight: 1.7,
                margin: '0 0 16px'
              }}>
                India is the default analysis benchmark. Every report models Indian price elasticity, Tier 1/2/3 customer cohorts, digital public infrastructure (IndiaStack), and regulatory frameworks.
              </p>

              <p style={{
                fontSize: 15,
                color: '#64748B',
                lineHeight: 1.7,
                margin: 0
              }}>
                Targeting global markets? Simply state your geography in the prompt — Kurukshetra’s multi-agent scouts pivot their currency, search queries, and regulatory parameters dynamically.
              </p>
            </div>

          </div>

        </div>
      </section>

      {/* ══════════════════════════════════════════════
          08 FINAL CTA — ENTER THE BATTLEFIELD
      ══════════════════════════════════════════════ */}
      <section style={{
        padding: '96px 0',
        background: '#FFFFFF',
        borderBottom: '1px solid rgba(16, 24, 40, 0.08)'
      }}>
        <div className="container" style={{ maxWidth: 860 }}>

          <div style={{
            background: 'linear-gradient(135deg, #101828 0%, #1D2939 100%)',
            borderRadius: 24,
            padding: '64px 40px',
            textAlign: 'center',
            position: 'relative',
            border: '2px solid rgba(201, 154, 61, 0.5)',
            boxShadow: '0 24px 50px -12px rgba(16, 24, 40, 0.4), 0 0 30px rgba(91, 92, 235, 0.15)',
            overflow: 'hidden'
          }}>

            {/* Corner Tactical Accents */}
            <div style={{ position: 'absolute', top: 12, left: 12, width: 12, height: 12, borderTop: '2px solid #C99A3D', borderLeft: '2px solid #C99A3D' }} />
            <div style={{ position: 'absolute', bottom: 12, right: 12, width: 12, height: 12, borderBottom: '2px solid #C99A3D', borderRight: '2px solid #C99A3D' }} />

            {/* Ambient Purple Center Glow */}
            <div style={{
              position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
              width: 400, height: 400,
              background: 'radial-gradient(circle, rgba(91, 92, 235, 0.25) 0%, transparent 70%)',
              pointerEvents: 'none'
            }} />

            <div style={{ position: 'relative', zIndex: 2 }}>
              <div style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 8,
                padding: '6px 14px',
                borderRadius: 100,
                background: 'rgba(201, 154, 61, 0.15)',
                border: '1px solid rgba(201, 154, 61, 0.4)',
                color: '#C99A3D',
                fontSize: 12,
                fontWeight: 800,
                letterSpacing: '0.08em',
                textTransform: 'uppercase',
                marginBottom: 20
              }}>
                <span>⚔</span> ENTER KURUKSHETRA
              </div>

              <h2 style={{
                fontSize: 'clamp(32px, 5vw, 48px)',
                fontWeight: 900,
                color: '#FFFFFF',
                letterSpacing: '-0.03em',
                lineHeight: 1.15,
                margin: '0 0 16px'
              }}>
                Ready to enter the battlefield?
              </h2>

              <p style={{
                fontSize: 17,
                color: 'rgba(255, 255, 255, 0.8)',
                lineHeight: 1.65,
                maxWidth: 600,
                margin: '0 auto 36px'
              }}>
                Battle-test your startup idea with seven AI agents and get a complete intelligence report in under 5 minutes.
              </p>

              <div style={{
                display: 'flex',
                gap: 14,
                justifyContent: 'center',
                alignItems: 'center',
                flexWrap: 'wrap',
                marginBottom: 28
              }}>
                <Link
                  href="/analyze"
                  className="btn btn-lg"
                  style={{
                    textDecoration: 'none',
                    background: '#5B5CEB',
                    color: '#FFFFFF',
                    fontWeight: 700,
                    fontSize: 15,
                    padding: '14px 28px',
                    borderRadius: 10,
                    boxShadow: '0 4px 18px rgba(91, 92, 235, 0.4)',
                    border: '1px solid rgba(201, 154, 61, 0.5)',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: 10
                  }}
                >
                  <span>⚔</span>
                  <span>Battle-Test My Idea</span>
                  <ArrowRight className="w-4 h-4 animate-arrow-shift" />
                </Link>

                <Link
                  href="/reports"
                  className="btn btn-lg"
                  style={{
                    textDecoration: 'none',
                    background: 'rgba(255, 255, 255, 0.08)',
                    color: '#FFFFFF',
                    fontWeight: 600,
                    fontSize: 15,
                    padding: '14px 26px',
                    borderRadius: 10,
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: 8
                  }}
                >
                  <span>View Sample Reports</span>
                </Link>
              </div>

              <p style={{
                fontSize: 13,
                color: 'rgba(255, 255, 255, 0.5)',
                margin: 0,
                fontWeight: 500
              }}>
                Free · India-first · Instant results · No credit card
              </p>
            </div>

          </div>

        </div>
      </section>

      {/* ══════════════════════════════════════════════
          09 FOOTER
      ══════════════════════════════════════════════ */}
      <footer style={{
        background: '#101828',
        borderTop: '1px solid rgba(201, 154, 61, 0.3)',
        padding: '40px 0 32px'
      }}>
        <div className="container">
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: 20,
            paddingBottom: 24,
            borderBottom: '1px solid rgba(255, 255, 255, 0.08)'
          }}>
            {/* Logo */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <div style={{
                width: 32,
                height: 32,
                borderRadius: 8,
                background: 'linear-gradient(135deg, #5B5CEB 0%, #3B3CBF 100%)',
                border: '1px solid rgba(201, 154, 61, 0.4)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <Swords className="w-4 h-4" style={{ color: '#FFFFFF' }} />
              </div>
              <div style={{ display: 'flex', flexDirection: 'column' }}>
                <span style={{ fontSize: 16, fontWeight: 800, color: '#FFFFFF', letterSpacing: '-0.01em' }}>
                  Kurukshetra<span style={{ color: '#5B5CEB' }}>.ai</span>
                </span>
                <span style={{ fontSize: 9, fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase', color: '#C99A3D' }}>
                  The AI Battlefield for Startups
                </span>
              </div>
            </div>

            {/* Links */}
            <div style={{ display: 'flex', gap: 28, flexWrap: 'wrap' }}>
              {[
                { href: '/analyze', label: 'Analyze' },
                { href: '/battlefield', label: 'Battlefield' },
                { href: '/reports', label: 'Reports' },
                { href: '/history', label: 'History' },
              ].map(link => (
                <Link
                  key={link.href}
                  href={link.href}
                  style={{
                    fontSize: 13,
                    fontWeight: 600,
                    color: 'rgba(255, 255, 255, 0.7)',
                    textDecoration: 'none',
                    transition: 'color 0.15s ease'
                  }}
                >
                  {link.label}
                </Link>
              ))}
            </div>
          </div>

          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: 12,
            paddingTop: 20
          }}>
            <p style={{ fontSize: 12, color: 'rgba(255, 255, 255, 0.45)', margin: 0 }}>
              © 2025 Kurukshetra AI · Multi-Agent Startup Intelligence Platform
            </p>
            <p style={{ fontSize: 12, color: 'rgba(255, 255, 255, 0.45)', margin: 0 }}>
              Built with LangGraph, Google Gemini, Groq, ChromaDB & Neon PostgreSQL
            </p>
          </div>
        </div>
      </footer>

    </div>
  );
}

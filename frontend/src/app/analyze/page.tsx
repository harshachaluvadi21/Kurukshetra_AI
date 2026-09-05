'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  Swords, ArrowRight, ChevronRight, MapPin, Sparkles,
  Shield, Brain, Scale, Target, CheckCircle2, Globe,
  Users, BarChart2, Compass
} from 'lucide-react';

/* ─── Data: Quick Battle Scenarios ─── */
const EXAMPLES = [
  'AI Attendance System for Colleges',
  'Campus Cab Sharing Platform',
  'AI Resume Builder for Fresh Graduates',
  'Peer-to-Peer Textbook Exchange',
  'On-demand Porter Booking for Railway Stations',
  'B2B Agri-Input Marketplace for Rural Retailers',
];

/* ─── Data: Business Models ─── */
const BUSINESS_MODELS = [
  'SaaS / Subscription',
  'Marketplace / Commission',
  'Freemium',
  'D2C / E-commerce',
  'B2B Enterprise',
  'Franchise',
  'Advertising',
  'Hardware + Software',
];

/* ─── Data: Statistics ─── */
const STATS = [
  { value: '7', label: 'AI Agents' },
  { value: '21', label: 'Report Sections' },
  { value: '100+', label: 'Data Signals' },
  { value: '<5 min', label: 'Analysis Time' },
];

/* ─── Data: Minimal Seven Agents Flow ─── */
const AGENT_NODES = [
  { name: 'Market Scout', role: 'TAM / Demand' },
  { name: 'Opponent Analyst', role: 'Moat / Rivals' },
  { name: 'Treasury Advisor', role: 'Unit Economics' },
  { name: 'Strategy Commander', role: 'GTM Flywheel' },
  { name: 'Critic Agent', role: 'Failure Scenarios' },
];

export default function AnalyzePage() {
  const router = useRouter();
  const [idea, setIdea] = useState('');
  const [problemStatement, setProblemStatement] = useState('');
  const [targetUsers, setTargetUsers] = useState('');
  const [revenueModel, setRevenueModel] = useState('');
  const [geography, setGeography] = useState('');
  const [industry, setIndustry] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const charCount = idea.length;
  const maxChars = 500;

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!idea.trim() || isSubmitting) return;

    setIsSubmitting(true);
    sessionStorage.setItem('kurukshetra_idea', JSON.stringify({
      idea: idea.trim(),
      problemStatement: problemStatement.trim(),
      targetUsers: targetUsers.trim(),
      revenueModel: revenueModel.trim(),
      geography: geography.trim(),
      industry: industry.trim(),
    }));

    router.push('/battlefield');
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: '#F5F7FA',
      color: '#101828',
      position: 'relative',
      padding: '72px 0 100px',
      overflowX: 'hidden'
    }} className="kuruk-grid-pattern">

      {/* ── Subtle Apple-Style Battlefield Ambient Lighting ── */}
      <div style={{
        position: 'absolute',
        top: '6%',
        left: '50%',
        transform: 'translateX(-50%)',
        width: 800,
        height: 500,
        background: 'radial-gradient(circle at center, rgba(91, 92, 235, 0.07) 0%, rgba(201, 154, 61, 0.03) 45%, transparent 70%)',
        pointerEvents: 'none',
        zIndex: 0
      }} />

      {/* ── Very Subtle Line-Art Battlefield Formation (Apple-Like Minimal Geometry) ── */}
      <div style={{
        position: 'absolute',
        top: 40,
        left: '50%',
        transform: 'translateX(-50%)',
        width: 600,
        height: 380,
        opacity: 0.12,
        pointerEvents: 'none',
        zIndex: 0
      }}>
        <svg viewBox="0 0 600 380" width="100%" height="100%" fill="none">
          {/* Subtle concentric rings */}
          <circle cx="300" cy="180" r="160" stroke="#C99A3D" strokeWidth="1" strokeDasharray="4 8" className="animate-radar-slow" style={{ transformOrigin: '300px 180px' }} />
          <circle cx="300" cy="180" r="100" stroke="#5B5CEB" strokeWidth="1" strokeDasharray="6 6" className="animate-radar-rev" style={{ transformOrigin: '300px 180px' }} />
          <circle cx="300" cy="180" r="40" stroke="#101828" strokeWidth="1" />

          {/* Calibrated cardinal axes */}
          <line x1="80" y1="180" x2="520" y2="180" stroke="#101828" strokeWidth="0.8" strokeDasharray="3 4" />
          <line x1="300" y1="20" x2="300" y2="340" stroke="#101828" strokeWidth="0.8" strokeDasharray="3 4" />

          {/* Minimal diamond markers */}
          <polygon points="300,16 304,20 300,24 296,20" fill="#C99A3D" />
          <polygon points="300,336 304,340 300,344 296,340" fill="#C99A3D" />
          <polygon points="76,180 80,184 76,188 72,184" fill="#5B5CEB" />
          <polygon points="516,180 520,184 516,188 512,184" fill="#5B5CEB" />
        </svg>
      </div>

      <div className="container" style={{ position: 'relative', zIndex: 2 }}>

        {/* ══════════════════════════════════════════════
            01 HERO SECTION — SPACIOUS, CONFIDENT, EDITORIAL
        ══════════════════════════════════════════════ */}
        <div style={{ maxWidth: 760, margin: '0 auto 56px', textAlign: 'center' }}>

          {/* Small Eyebrow Badge */}
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 8,
            padding: '5px 14px',
            borderRadius: 100,
            background: '#F1F0FF',
            border: '1px solid rgba(201, 154, 61, 0.35)',
            boxShadow: '0 2px 8px rgba(91, 92, 235, 0.06)',
            marginBottom: 24
          }}>
            <span style={{ fontSize: 11, color: '#C99A3D' }}>⚔</span>
            <span style={{
              fontSize: 11,
              fontWeight: 700,
              color: '#5B5CEB',
              letterSpacing: '0.09em',
              textTransform: 'uppercase'
            }}>
              ENTER THE BATTLEFIELD
            </span>
          </div>

          {/* Main Large Confident Headline */}
          <h1 style={{
            fontSize: 'clamp(38px, 5.4vw, 62px)',
            fontWeight: 800,
            color: '#101828',
            lineHeight: 1.02,
            letterSpacing: '-0.04em',
            margin: '0 0 20px'
          }}>
            Prepare your startup<br />
            <span style={{ color: '#5B5CEB' }}>for battle.</span>
          </h1>

          {/* Supporting Copy */}
          <p style={{
            fontSize: 'clamp(16px, 2.1vw, 18px)',
            color: '#667085',
            lineHeight: 1.65,
            maxWidth: 620,
            margin: '0 auto 28px',
            fontWeight: 400
          }}>
            Describe your idea and seven AI agents will research, challenge, debate and score it before you invest your time or capital.
          </p>

          {/* Editorial Phrase Highlight */}
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 8,
            fontSize: 13,
            fontWeight: 600,
            color: '#101828',
            letterSpacing: '-0.01em'
          }}>
            <span>Seven AI specialists.</span>
            <span style={{ color: '#5B5CEB' }}>One final verdict.</span>
          </div>

        </div>

        {/* ══════════════════════════════════════════════
            02 STATS ROW — APPLE-STYLE TYPOGRAPHY ONLY
        ══════════════════════════════════════════════ */}
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: 'clamp(28px, 5vw, 64px)',
          margin: '0 auto 52px',
          maxWidth: 720
        }}>
          {STATS.map(s => (
            <div key={s.label} style={{ textAlign: 'center' }}>
              <div style={{
                fontSize: 'clamp(26px, 3.2vw, 34px)',
                fontWeight: 800,
                color: '#101828',
                letterSpacing: '-0.03em',
                lineHeight: 1
              }}>
                {s.value}
              </div>
              <div style={{
                fontSize: 12,
                color: '#667085',
                fontWeight: 600,
                textTransform: 'uppercase',
                letterSpacing: '0.04em',
                marginTop: 6
              }}>
                {s.label}
              </div>
            </div>
          ))}
        </div>

        {/* ══════════════════════════════════════════════
            03 MAIN FORM: BATTLEFIELD BRIEF (APPLE-STYLE CARD)
        ══════════════════════════════════════════════ */}
        <div style={{ maxWidth: 820, margin: '0 auto 36px' }}>

          <div className="apple-card" style={{
            padding: 'clamp(24px, 4.5vw, 44px) clamp(20px, 4.5vw, 48px)',
            position: 'relative'
          }}>
            {/* Subtle Tiny Gold Corner Markers */}
            <div className="tactical-bracket-tl" style={{ opacity: 0.6 }} />
            <div className="tactical-bracket-br" style={{ opacity: 0.6 }} />

            {/* Card Header */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              borderBottom: '1px solid rgba(16, 24, 40, 0.07)',
              paddingBottom: 18,
              marginBottom: 28
            }}>
              <div>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 8,
                  fontSize: 17,
                  fontWeight: 800,
                  color: '#101828',
                  letterSpacing: '-0.02em'
                }}>
                  <span style={{ color: '#C99A3D', fontSize: 14 }}>⚔</span>
                  <span>BATTLEFIELD BRIEF</span>
                </div>
                <div style={{ fontSize: 13, color: '#667085', marginTop: 3 }}>
                  Give the agents enough context to challenge your idea.
                </div>
              </div>

              <div style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 6,
                padding: '4px 10px',
                borderRadius: 100,
                background: '#FCFAF5',
                border: '1px solid rgba(201, 154, 61, 0.35)',
                fontSize: 11,
                fontWeight: 700,
                color: '#C99A3D'
              }}>
                <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#10B981' }} />
                READY
              </div>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit}>

              {/* ── Primary Field: YOUR STARTUP IDEA ── */}
              <div style={{ marginBottom: 24 }}>
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'baseline',
                  marginBottom: 8
                }}>
                  <label style={{
                    fontSize: 12,
                    fontWeight: 700,
                    color: '#101828',
                    letterSpacing: '0.04em',
                    textTransform: 'uppercase',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 6
                  }}>
                    <span>YOUR STARTUP IDEA</span>
                    <span style={{ color: '#EF4444', fontWeight: 600 }}>*</span>
                  </label>
                  <span style={{
                    fontSize: 12,
                    fontFamily: 'var(--font-mono)',
                    fontWeight: 500,
                    color: charCount > maxChars * 0.85 ? '#EF4444' : '#667085'
                  }}>
                    {charCount} / {maxChars}
                  </span>
                </div>

                <textarea
                  value={idea}
                  onChange={e => setIdea(e.target.value.slice(0, maxChars))}
                  placeholder="Describe your startup concept in 1–3 sentences. What does it do, who does it serve, and how does it make money?"
                  rows={4}
                  className="apple-input kuruk-textarea"
                  style={{
                    resize: 'vertical',
                    fontSize: 15,
                    lineHeight: 1.65,
                    minHeight: 110
                  }}
                  autoFocus
                />
              </div>

              {/* ── Quick Battle Scenarios ── */}
              <div style={{ marginBottom: 30 }}>
                <div style={{
                  fontSize: 11,
                  fontWeight: 700,
                  color: '#667085',
                  textTransform: 'uppercase',
                  letterSpacing: '0.06em',
                  marginBottom: 10
                }}>
                  QUICK BATTLE SCENARIOS
                </div>

                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                  {EXAMPLES.map(ex => (
                    <button
                      type="button"
                      key={ex}
                      onClick={() => setIdea(ex)}
                      className={`apple-chip ${idea === ex ? 'apple-chip-active' : ''}`}
                    >
                      {idea === ex && <CheckCircle2 className="w-3.5 h-3.5" style={{ color: '#5B5CEB' }} />}
                      <span>{ex}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* ── Divider & Optional Context ── */}
              <div style={{
                borderTop: '1px solid rgba(16, 24, 40, 0.07)',
                paddingTop: 24,
                marginBottom: 20
              }}>
                <div style={{
                  fontSize: 12,
                  fontWeight: 700,
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                  color: '#101828'
                }}>
                  OPTIONAL — STRENGTHEN YOUR BATTLE BRIEF
                </div>
                <p style={{ fontSize: 13, color: '#667085', margin: '3px 0 0' }}>
                  More context gives the agents more evidence to challenge.
                </p>
              </div>

              {/* Problem Statement & Target Users */}
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
                gap: 16,
                marginBottom: 16
              }}>
                <div>
                  <label style={{ display: 'block', fontSize: 12, fontWeight: 600, color: '#334155', marginBottom: 6 }}>
                    Problem Statement
                  </label>
                  <textarea
                    value={problemStatement}
                    onChange={e => setProblemStatement(e.target.value)}
                    placeholder="What painful problem does this solve?"
                    rows={3}
                    className="apple-input kuruk-textarea"
                    style={{ resize: 'vertical', fontSize: 13 }}
                  />
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: 12, fontWeight: 600, color: '#334155', marginBottom: 6 }}>
                    Target Users
                  </label>
                  <textarea
                    value={targetUsers}
                    onChange={e => setTargetUsers(e.target.value)}
                    placeholder="e.g. College students, HR managers, kirana store owners"
                    rows={3}
                    className="apple-input kuruk-textarea"
                    style={{ resize: 'vertical', fontSize: 13 }}
                  />
                </div>
              </div>

              {/* Revenue Model & Industry */}
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
                gap: 16,
                marginBottom: 16
              }}>
                <div>
                  <label style={{ display: 'block', fontSize: 12, fontWeight: 600, color: '#334155', marginBottom: 6 }}>
                    Revenue Model
                  </label>
                  <input
                    type="text"
                    list="revenue-models"
                    value={revenueModel}
                    onChange={e => setRevenueModel(e.target.value)}
                    placeholder="e.g. SaaS subscription, marketplace commission"
                    className="apple-input kuruk-textarea"
                    style={{ fontSize: 13 }}
                  />
                  <datalist id="revenue-models">
                    {BUSINESS_MODELS.map(m => <option key={m} value={m} />)}
                  </datalist>
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: 12, fontWeight: 600, color: '#334155', marginBottom: 6 }}>
                    Industry / Sector
                  </label>
                  <input
                    type="text"
                    value={industry}
                    onChange={e => setIndustry(e.target.value)}
                    placeholder="e.g. EdTech, AgriTech, FinTech, SaaS"
                    className="apple-input kuruk-textarea"
                    style={{ fontSize: 13 }}
                  />
                </div>
              </div>

              {/* Target Geography */}
              <div style={{ marginBottom: 32 }}>
                <label style={{ display: 'block', fontSize: 12, fontWeight: 600, color: '#334155', marginBottom: 6 }}>
                  Target Geography
                </label>
                <div style={{ position: 'relative' }}>
                  <MapPin className="w-4 h-4" style={{ position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)', color: '#667085' }} />
                  <input
                    type="text"
                    value={geography}
                    onChange={e => setGeography(e.target.value)}
                    placeholder="Leave blank for India (default) · or specify e.g. USA, Southeast Asia"
                    className="apple-input kuruk-textarea"
                    style={{ paddingLeft: 38, fontSize: 13 }}
                  />
                </div>
              </div>

              {/* ── Start Battle CTA Button ── */}
              <button
                type="submit"
                disabled={!idea.trim() || isSubmitting}
                style={{
                  width: '100%',
                  padding: '16px 24px',
                  fontSize: 15,
                  fontWeight: 700,
                  borderRadius: 14,
                  background: !idea.trim() || isSubmitting ? '#E2E8F0' : '#5B5CEB',
                  color: !idea.trim() || isSubmitting ? '#94A3B8' : '#FFFFFF',
                  border: 'none',
                  boxShadow: !idea.trim() || isSubmitting ? 'none' : '0 4px 18px rgba(91, 92, 235, 0.35)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: 10,
                  cursor: !idea.trim() || isSubmitting ? 'not-allowed' : 'pointer',
                  transition: 'all 0.2s cubic-bezier(0.16, 1, 0.3, 1)'
                }}
              >
                <span style={{ fontSize: 15 }}>⚔</span>
                <span>{isSubmitting ? 'DEPLOYING TO BATTLEFIELD...' : 'START BATTLE ANALYSIS'}</span>
                <ArrowRight className="w-4 h-4 animate-arrow-shift" />
              </button>

            </form>
          </div>

        </div>

        {/* ══════════════════════════════════════════════
            04 SEVEN AGENTS VISUAL (MINIMAL LINE-ART STYLE)
        ══════════════════════════════════════════════ */}
        <div style={{
          maxWidth: 820,
          margin: '0 auto 24px',
          background: '#FFFFFF',
          borderRadius: 18,
          border: '1px solid rgba(16, 24, 40, 0.06)',
          padding: '20px 24px',
          boxShadow: '0 2px 10px rgba(0, 0, 0, 0.02)'
        }}>
          <div style={{
            fontSize: 11,
            fontWeight: 700,
            textTransform: 'uppercase',
            letterSpacing: '0.06em',
            color: '#667085',
            marginBottom: 14,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}>
            <span>THE MULTI-AGENT BATTLEFIELD SEQUENCE</span>
            <span style={{ color: '#5B5CEB' }}>7 Specialists Synchronized</span>
          </div>

          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: 10
          }}>
            {/* Stage 1: Idea */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <div style={{ width: 8, height: 8, borderRadius: '50%', background: '#C99A3D' }} />
              <span style={{ fontSize: 12, fontWeight: 700, color: '#101828' }}>Your Brief</span>
            </div>

            <span style={{ color: '#D0D5DD', fontSize: 12 }}>→</span>

            {/* Stage 2: 5 Scouts */}
            <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
              {AGENT_NODES.map(a => (
                <span
                  key={a.name}
                  style={{
                    fontSize: 11,
                    fontWeight: 600,
                    color: '#475569',
                    background: '#F8FAFC',
                    padding: '3px 9px',
                    borderRadius: 6,
                    border: '1px solid rgba(16, 24, 40, 0.06)'
                  }}
                >
                  {a.name}
                </span>
              ))}
            </div>

            <span style={{ color: '#D0D5DD', fontSize: 12 }}>→</span>

            {/* Stage 3: Debate */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <Scale className="w-3.5 h-3.5" style={{ color: '#10B981' }} />
              <span style={{ fontSize: 12, fontWeight: 700, color: '#101828' }}>Debate</span>
            </div>

            <span style={{ color: '#D0D5DD', fontSize: 12 }}>→</span>

            {/* Stage 4: Verdict */}
            <div style={{
              fontSize: 11,
              fontWeight: 700,
              color: '#5B5CEB',
              background: '#F1F0FF',
              padding: '4px 10px',
              borderRadius: 6
            }}>
              Battle Score & Verdict
            </div>
          </div>
        </div>

        {/* ══════════════════════════════════════════════
            05 INDIA-FIRST INTELLIGENCE STRIP
        ══════════════════════════════════════════════ */}
        <div style={{
          maxWidth: 820,
          margin: '0 auto',
          background: '#F1F0FF',
          borderRadius: 14,
          border: '1px solid rgba(91, 92, 235, 0.2)',
          padding: '14px 20px',
          display: 'flex',
          alignItems: 'center',
          gap: 12
        }}>
          <div style={{
            width: 28,
            height: 28,
            borderRadius: 8,
            background: '#FFFFFF',
            border: '1px solid rgba(91, 92, 235, 0.3)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexShrink: 0
          }}>
            <Compass className="w-4 h-4" style={{ color: '#5B5CEB' }} />
          </div>
          <div>
            <div style={{
              fontSize: 11,
              fontWeight: 700,
              textTransform: 'uppercase',
              letterSpacing: '0.06em',
              color: '#5B5CEB',
              marginBottom: 2
            }}>
              INDIA-FIRST INTELLIGENCE
            </div>
            <p style={{ fontSize: 13, color: '#334155', margin: 0, lineHeight: 1.55 }}>
              <strong>India is the default market</strong> — pricing, regulations, competitors and distribution channels are evaluated for India unless you specify another geography.
            </p>
          </div>
        </div>

      </div>
    </div>
  );
}

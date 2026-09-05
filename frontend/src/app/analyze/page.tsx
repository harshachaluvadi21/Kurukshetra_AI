'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  Swords, ArrowRight, ChevronRight, MapPin, Sparkles,
  Shield, Brain, Scale, Target, CheckCircle2, Globe,
  Users, BarChart2, Zap, ArrowUpRight, Compass, Layers
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

/* ─── Data: Seven Agents Summary ─── */
const PIPELINE_AGENTS = [
  { name: 'Intelligence Scout', role: 'Market Sizing & TAM', color: '#5B5CEB', icon: Globe },
  { name: 'Opponent Analyst', role: 'Competitive Moats', color: '#0EA5E9', icon: Users },
  { name: 'Treasury Advisor', role: 'Unit Economics & CAC', color: '#C99A3D', icon: BarChart2 },
  { name: 'Strategy Commander', role: 'GTM Distribution', color: '#8B5CF6', icon: Target },
  { name: 'Critic Agent', role: 'Failure Scenarios', color: '#EF4444', icon: Shield },
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
      background: 'linear-gradient(180deg, #FFFFFF 0%, #F5F7FA 100%)',
      color: '#101828',
      position: 'relative',
      padding: '40px 0 72px',
      overflowX: 'hidden'
    }} className="kuruk-grid-pattern">

      {/* Subtle Ambient Battlefield Background Glows */}
      <div style={{
        position: 'absolute', top: '10%', right: '-5%', width: 500, height: 500,
        background: 'radial-gradient(circle, rgba(91, 92, 235, 0.08) 0%, transparent 70%)',
        pointerEvents: 'none', zIndex: 0
      }} />

      <div style={{
        position: 'absolute', bottom: '15%', left: '-5%', width: 450, height: 450,
        background: 'radial-gradient(circle, rgba(201, 154, 61, 0.07) 0%, transparent 70%)',
        pointerEvents: 'none', zIndex: 0
      }} />

      {/* Background Rotating Strategic Ring Motif */}
      <div style={{
        position: 'absolute',
        top: 60,
        left: '2%',
        width: 320,
        height: 320,
        opacity: 0.12,
        pointerEvents: 'none',
        zIndex: 0
      }}>
        <svg viewBox="0 0 300 300" width="100%" height="100%" fill="none" className="animate-radar-slow">
          <circle cx="150" cy="150" r="140" stroke="#C99A3D" strokeWidth="1.5" strokeDasharray="6 6" />
          <circle cx="150" cy="150" r="95" stroke="#5B5CEB" strokeWidth="1.2" strokeDasharray="4 8" />
          <circle cx="150" cy="150" r="50" stroke="#C99A3D" strokeWidth="1" />
          <line x1="10" y1="150" x2="290" y2="150" stroke="#101828" strokeWidth="1" strokeDasharray="2 4" />
          <line x1="150" y1="10" x2="150" y2="290" stroke="#101828" strokeWidth="1" strokeDasharray="2 4" />
        </svg>
      </div>

      <div className="container" style={{ position: 'relative', zIndex: 2 }}>

        {/* ── Two-Column Battlefield Layout ── */}
        <div className="kuruk-analyze-grid">

          {/* ══════════════════════════════════════════════
              LEFT COLUMN: HERO, BRIEFING & PIPELINE
          ══════════════════════════════════════════════ */}
          <div>

            {/* Eyebrow Badge */}
            <div style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 8,
              padding: '6px 14px',
              borderRadius: 100,
              background: '#F1F0FF',
              border: '1px solid rgba(201, 154, 61, 0.4)',
              boxShadow: '0 2px 8px rgba(91, 92, 235, 0.08)',
              marginBottom: 20
            }}>
              <span style={{ fontSize: 12, color: '#C99A3D' }}>⚔</span>
              <span style={{
                fontSize: 11,
                fontWeight: 800,
                color: '#5B5CEB',
                letterSpacing: '0.08em',
                textTransform: 'uppercase'
              }}>
                ENTER THE BATTLEFIELD
              </span>
              <span style={{ width: 5, height: 5, borderRadius: '50%', background: '#10B981' }} />
            </div>

            {/* Page Heading */}
            <h1 style={{
              fontSize: 'clamp(32px, 3.8vw, 46px)',
              fontWeight: 900,
              color: '#101828',
              lineHeight: 1.12,
              letterSpacing: '-0.03em',
              margin: '0 0 16px'
            }}>
              Prepare your startup<br />
              <span style={{ color: '#5B5CEB', position: 'relative', display: 'inline-block' }}>
                for battle.
                <svg
                  style={{ position: 'absolute', bottom: -6, left: 0, width: '100%', height: 6, overflow: 'visible' }}
                  viewBox="0 0 150 6" fill="none" preserveAspectRatio="none"
                >
                  <path d="M0 5 Q 75 0, 150 5" stroke="#C99A3D" strokeWidth="2" strokeDasharray="4 4" opacity="0.8" />
                </svg>
              </span>
            </h1>

            {/* Supporting Copy */}
            <p style={{
              fontSize: 15,
              color: '#475569',
              lineHeight: 1.65,
              margin: '0 0 28px',
              fontWeight: 450
            }}>
              Describe your idea and let seven AI agents research, challenge, debate and score it before you invest your time or capital.
            </p>

            {/* Tactical Metrics Bar */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: 10,
              padding: '12px 14px',
              background: '#FFFFFF',
              borderRadius: 12,
              border: '1px solid rgba(16, 24, 40, 0.08)',
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.02)',
              marginBottom: 28
            }}>
              {[
                { val: '7', label: 'AI AGENTS' },
                { val: '21', label: 'REPORT SECTIONS' },
                { val: '100+', label: 'SIGNALS' },
              ].map((m, i) => (
                <div key={m.label} style={{
                  textAlign: 'center',
                  borderRight: i < 2 ? '1px solid rgba(16, 24, 40, 0.08)' : 'none'
                }}>
                  <div style={{ fontSize: 18, fontWeight: 900, color: '#101828', lineHeight: 1 }}>{m.val}</div>
                  <div style={{ fontSize: 9, fontWeight: 700, color: '#5B5CEB', marginTop: 3, letterSpacing: '0.04em' }}>{m.label}</div>
                </div>
              ))}
            </div>

            {/* ── Seven Agents Tactical Pipeline Visual ── */}
            <div style={{
              background: '#FFFFFF',
              borderRadius: 16,
              border: '1px solid rgba(201, 154, 61, 0.3)',
              padding: '20px',
              boxShadow: '0 6px 18px rgba(91, 92, 235, 0.06)',
              marginBottom: 24,
              position: 'relative'
            }}>
              <div className="tactical-bracket-tl" />
              <div className="tactical-bracket-br" />

              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                borderBottom: '1px solid rgba(16, 24, 40, 0.06)',
                paddingBottom: 10,
                marginBottom: 14
              }}>
                <div style={{ fontSize: 11, fontWeight: 800, color: '#101828', letterSpacing: '0.06em', textTransform: 'uppercase' }}>
                  ⚔ ACTIVE AGENT DEPLOYMENT
                </div>
                <div style={{ fontSize: 10, fontWeight: 700, color: '#C99A3D', textTransform: 'uppercase' }}>
                  7 Specialists
                </div>
              </div>

              {/* Agent Sequence */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                {PIPELINE_AGENTS.map((a) => (
                  <div key={a.name} style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '8px 12px',
                    borderRadius: 8,
                    background: '#F8FAFC',
                    border: '1px solid rgba(16, 24, 40, 0.05)'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <div style={{
                        width: 22, height: 22, borderRadius: 6,
                        background: '#FFFFFF', display: 'flex', alignItems: 'center', justifyContent: 'center',
                        boxShadow: '0 1px 3px rgba(0,0,0,0.06)'
                      }}>
                        <a.icon className="w-3 h-3" style={{ color: a.color }} />
                      </div>
                      <span style={{ fontSize: 12, fontWeight: 700, color: '#101828' }}>{a.name}</span>
                    </div>
                    <span style={{ fontSize: 11, color: '#64748B', fontWeight: 500 }}>{a.role}</span>
                  </div>
                ))}

                {/* Debate & Verdict Flow Footer */}
                <div style={{
                  marginTop: 6,
                  padding: '10px 12px',
                  borderRadius: 8,
                  background: '#FCFAF5',
                  border: '1px solid rgba(201, 154, 61, 0.35)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    <Scale className="w-3.5 h-3.5" style={{ color: '#10B981' }} />
                    <span style={{ fontSize: 11, fontWeight: 800, color: '#101828' }}>Debate Engine & Verdict</span>
                  </div>
                  <span style={{ fontSize: 10, fontWeight: 700, color: '#5B5CEB' }}>
                    Score 0–100
                  </span>
                </div>
              </div>
            </div>

            {/* ── India-First Intelligence Card ── */}
            <div style={{
              background: '#F1F0FF',
              border: '1px solid rgba(91, 92, 235, 0.25)',
              borderRadius: 12,
              padding: '14px 18px',
              display: 'flex',
              alignItems: 'flex-start',
              gap: 12
            }}>
              <div style={{
                width: 28, height: 28, borderRadius: 7,
                background: '#FFFFFF', border: '1px solid rgba(91, 92, 235, 0.3)',
                display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0
              }}>
                <MapPin className="w-3.5 h-3.5" style={{ color: '#5B5CEB' }} />
              </div>
              <div>
                <div style={{ fontSize: 11, fontWeight: 800, color: '#5B5CEB', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 2 }}>
                  INDIA-FIRST INTELLIGENCE
                </div>
                <p style={{ fontSize: 12, color: '#334155', margin: 0, lineHeight: 1.55 }}>
                  <strong>India is the default market</strong> — pricing, regulations, competitors and distribution channels are evaluated for India unless you specify another geography.
                </p>
              </div>
            </div>

          </div>

          {/* ══════════════════════════════════════════════
              RIGHT COLUMN: BATTLEFIELD BRIEF FORM
          ══════════════════════════════════════════════ */}
          <div>
            <div className="tactical-corner-card" style={{
              padding: '32px 28px',
              boxShadow: '0 12px 36px -8px rgba(91, 92, 235, 0.12), 0 0 0 1px rgba(16, 24, 40, 0.04)'
            }}>
              <div className="tactical-bracket-tl" />
              <div className="tactical-bracket-br" />

              {/* Card Header */}
              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                borderBottom: '1px solid rgba(16, 24, 40, 0.08)',
                paddingBottom: 16,
                marginBottom: 24
              }}>
                <div>
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 8,
                    fontSize: 16,
                    fontWeight: 800,
                    color: '#101828',
                    letterSpacing: '-0.01em'
                  }}>
                    <span style={{ color: '#C99A3D' }}>⚔</span>
                    <span>BATTLEFIELD BRIEF</span>
                  </div>
                  <div style={{ fontSize: 13, color: '#64748B', marginTop: 2 }}>
                    Give the AI agents enough intelligence to challenge your idea.
                  </div>
                </div>

                <div style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 6,
                  padding: '4px 10px',
                  borderRadius: 100,
                  background: '#FCFAF5',
                  border: '1px solid rgba(201, 154, 61, 0.4)',
                  fontSize: 10,
                  fontWeight: 800,
                  color: '#C99A3D',
                  letterSpacing: '0.04em'
                }}>
                  <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#10B981' }} />
                  READY
                </div>
              </div>

              {/* Form Element */}
              <form onSubmit={handleSubmit}>

                {/* ── Primary Field: YOUR STARTUP IDEA ── */}
                <div style={{ marginBottom: 22 }}>
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'baseline',
                    marginBottom: 8
                  }}>
                    <label style={{
                      fontSize: 13,
                      fontWeight: 800,
                      color: '#101828',
                      letterSpacing: '0.04em',
                      textTransform: 'uppercase',
                      display: 'flex',
                      alignItems: 'center',
                      gap: 6
                    }}>
                      <span>YOUR STARTUP IDEA</span>
                      <span style={{ color: '#EF4444', fontWeight: 800 }}>*</span>
                    </label>
                    <span style={{
                      fontSize: 12,
                      fontFamily: 'var(--font-mono)',
                      fontWeight: 600,
                      color: charCount > maxChars * 0.85 ? '#EF4444' : '#94A3B8'
                    }}>
                      {charCount} / {maxChars}
                    </span>
                  </div>

                  <div style={{ position: 'relative' }}>
                    <textarea
                      value={idea}
                      onChange={e => setIdea(e.target.value.slice(0, maxChars))}
                      placeholder="Describe your startup concept in 1–3 sentences. What does it do, who does it serve, and how does it make money?"
                      rows={4}
                      className="input-field kuruk-textarea"
                      style={{
                        resize: 'vertical',
                        fontSize: 14,
                        lineHeight: 1.65,
                        borderRadius: 10,
                        padding: '14px 16px',
                        background: '#FCFAF5',
                        border: '1px solid rgba(201, 154, 61, 0.35)'
                      }}
                      autoFocus
                    />
                  </div>
                </div>

                {/* ── Quick Battle Scenarios (Chips) ── */}
                <div style={{ marginBottom: 26 }}>
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 6,
                    fontSize: 11,
                    fontWeight: 800,
                    color: '#C99A3D',
                    textTransform: 'uppercase',
                    letterSpacing: '0.08em',
                    marginBottom: 10
                  }}>
                    <Sparkles className="w-3 h-3" />
                    <span>TRY A BATTLE SCENARIO</span>
                  </div>

                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                    {EXAMPLES.map(ex => (
                      <button
                        type="button"
                        key={ex}
                        onClick={() => setIdea(ex)}
                        className="kuruk-chip"
                        style={{
                          padding: '6px 14px',
                          borderRadius: 100,
                          fontSize: 12,
                          fontWeight: 600,
                          background: idea === ex ? '#F1F0FF' : '#FFFFFF',
                          color: idea === ex ? '#5B5CEB' : '#475569',
                          border: idea === ex ? '1px solid #5B5CEB' : '1px solid rgba(16, 24, 40, 0.12)',
                          cursor: 'pointer',
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: 6,
                          boxShadow: idea === ex ? '0 2px 8px rgba(91, 92, 235, 0.15)' : 'none'
                        }}
                      >
                        {idea === ex ? (
                          <CheckCircle2 className="w-3.5 h-3.5" style={{ color: '#5B5CEB' }} />
                        ) : (
                          <span style={{ fontSize: 10, color: '#C99A3D' }}>⚔</span>
                        )}
                        <span>{ex}</span>
                      </button>
                    ))}
                  </div>
                </div>

                {/* ── Divider + Optional Section ── */}
                <div style={{
                  borderTop: '1px solid rgba(16, 24, 40, 0.08)',
                  paddingTop: 22,
                  marginBottom: 18
                }}>
                  <div style={{
                    fontSize: 12,
                    fontWeight: 800,
                    textTransform: 'uppercase',
                    letterSpacing: '0.06em',
                    color: '#101828',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 6
                  }}>
                    <span>OPTIONAL — STRENGTHEN YOUR BATTLE BRIEF</span>
                  </div>
                  <p style={{ fontSize: 12, color: '#64748B', margin: '3px 0 0' }}>
                    More context gives the AI agents more evidence to challenge.
                  </p>
                </div>

                {/* Problem Statement & Target Users */}
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
                  gap: 16,
                  marginBottom: 16
                }}>
                  <div>
                    <label style={{ display: 'block', fontSize: 12, fontWeight: 700, color: '#334155', marginBottom: 6 }}>
                      Problem Statement
                    </label>
                    <textarea
                      value={problemStatement}
                      onChange={e => setProblemStatement(e.target.value)}
                      placeholder="What painful problem does this solve?"
                      rows={3}
                      className="input-field kuruk-textarea"
                      style={{ resize: 'vertical', fontSize: 13, borderRadius: 8 }}
                    />
                  </div>

                  <div>
                    <label style={{ display: 'block', fontSize: 12, fontWeight: 700, color: '#334155', marginBottom: 6 }}>
                      Target Users
                    </label>
                    <textarea
                      value={targetUsers}
                      onChange={e => setTargetUsers(e.target.value)}
                      placeholder="e.g. College students, HR managers, kirana store owners"
                      rows={3}
                      className="input-field kuruk-textarea"
                      style={{ resize: 'vertical', fontSize: 13, borderRadius: 8 }}
                    />
                  </div>
                </div>

                {/* Revenue Model & Industry */}
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
                  gap: 16,
                  marginBottom: 16
                }}>
                  <div>
                    <label style={{ display: 'block', fontSize: 12, fontWeight: 700, color: '#334155', marginBottom: 6 }}>
                      Revenue Model
                    </label>
                    <input
                      type="text"
                      list="revenue-models"
                      value={revenueModel}
                      onChange={e => setRevenueModel(e.target.value)}
                      placeholder="e.g. SaaS subscription, marketplace commission"
                      className="input-field kuruk-textarea"
                      style={{ fontSize: 13, borderRadius: 8 }}
                    />
                    <datalist id="revenue-models">
                      {BUSINESS_MODELS.map(m => <option key={m} value={m} />)}
                    </datalist>
                  </div>

                  <div>
                    <label style={{ display: 'block', fontSize: 12, fontWeight: 700, color: '#334155', marginBottom: 6 }}>
                      Industry / Sector
                    </label>
                    <input
                      type="text"
                      value={industry}
                      onChange={e => setIndustry(e.target.value)}
                      placeholder="e.g. EdTech, AgriTech, FinTech, SaaS"
                      className="input-field kuruk-textarea"
                      style={{ fontSize: 13, borderRadius: 8 }}
                    />
                  </div>
                </div>

                {/* Target Geography */}
                <div style={{ marginBottom: 28 }}>
                  <label style={{ display: 'block', fontSize: 12, fontWeight: 700, color: '#334155', marginBottom: 6 }}>
                    Target Geography
                  </label>
                  <div style={{ position: 'relative' }}>
                    <MapPin className="w-4 h-4" style={{ position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)', color: '#94A3B8' }} />
                    <input
                      type="text"
                      value={geography}
                      onChange={e => setGeography(e.target.value)}
                      placeholder="Leave blank for India (default) · or specify e.g. USA, Southeast Asia"
                      className="input-field kuruk-textarea"
                      style={{ paddingLeft: 40, fontSize: 13, borderRadius: 8 }}
                    />
                  </div>
                </div>

                {/* ── Submit Button ── */}
                <button
                  type="submit"
                  disabled={!idea.trim() || isSubmitting}
                  style={{
                    width: '100%',
                    padding: '16px 24px',
                    fontSize: 15,
                    fontWeight: 800,
                    borderRadius: 12,
                    background: !idea.trim() || isSubmitting ? '#E2E8F0' : '#5B5CEB',
                    color: !idea.trim() || isSubmitting ? '#94A3B8' : '#FFFFFF',
                    border: '1px solid rgba(201, 154, 61, 0.45)',
                    boxShadow: !idea.trim() || isSubmitting ? 'none' : '0 4px 18px rgba(91, 92, 235, 0.35)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: 10,
                    cursor: !idea.trim() || isSubmitting ? 'not-allowed' : 'pointer',
                    transition: 'all 0.2s ease'
                  }}
                >
                  <span style={{ fontSize: 16 }}>⚔</span>
                  <span>{isSubmitting ? 'DEPLOYING TO BATTLEFIELD...' : 'START BATTLE ANALYSIS'}</span>
                  <ArrowRight className="w-4 h-4 animate-arrow-shift" />
                </button>

              </form>

            </div>
          </div>

        </div>

      </div>
    </div>
  );
}

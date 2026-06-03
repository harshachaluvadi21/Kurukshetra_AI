'use client';
import Link from 'next/link';
import {
  Swords, Brain, Globe, BookOpen, Target, Shield,
  FileText, ArrowRight, Zap, MessageSquare, Activity,
  ChevronRight, Sparkles
} from 'lucide-react';

const features = [
  { icon: Brain, title: 'Multi-Agent Analysis', desc: 'Four specialized AI agents research, analyze competitors, evaluate financials, and strategize.', color: 'from-indigo-500 to-purple-500' },
  { icon: MessageSquare, title: 'Live Debate Engine', desc: 'AI Proponent and Skeptic debate your idea while a Judge scores arguments in real-time.', color: 'from-blue-500 to-cyan-500' },
  { icon: Globe, title: 'Web Intelligence', desc: 'Live web search pulls real market data, competitor info, and industry trends.', color: 'from-emerald-500 to-teal-500' },
  { icon: BookOpen, title: 'Knowledge Base (RAG)', desc: 'Retrieval-Augmented Generation draws from curated startup frameworks and case studies.', color: 'from-amber-500 to-orange-500' },
  { icon: Target, title: 'Battle Score', desc: 'Quantified 0-100 viability score based on market, team, product, and financial analysis.', color: 'from-rose-500 to-pink-500' },
  { icon: Shield, title: 'Confidence Score', desc: 'Statistical confidence level measuring reliability of the analysis and data quality.', color: 'from-violet-500 to-fuchsia-500' },
  { icon: FileText, title: 'Executive Reports', desc: 'Download comprehensive PDF reports with insights, recommendations, and action items.', color: 'from-sky-500 to-blue-500' },
];

const steps = [
  { num: '01', title: 'Submit Your Idea', desc: 'Describe your startup concept in a few sentences.' },
  { num: '02', title: 'AI Research Phase', desc: 'Agents gather market data, competitor intel, and financial models.' },
  { num: '03', title: 'Agent Debate', desc: 'Proponent defends, Skeptic challenges, Judge evaluates.' },
  { num: '04', title: 'Scoring Engine', desc: 'Battle Score and Confidence Score are calculated.' },
  { num: '05', title: 'Executive Report', desc: 'Download a comprehensive analysis with actionable insights.' },
];

export default function HomePage() {
  return (
    <div className="min-h-screen">

      {/* Hero Section */}
      <section className="relative overflow-hidden">
        {/* Background effects */}
        <div className="absolute inset-0 bg-gradient-to-b from-indigo-950/30 via-zinc-950 to-zinc-950" />
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-indigo-500/8 rounded-full blur-3xl" />
        <div className="absolute top-20 right-0 w-[400px] h-[400px] bg-purple-500/5 rounded-full blur-3xl" />

        <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-24 md:pt-32 md:pb-36">
          {/* Badge */}
          <div className="flex justify-center mb-8 animate-fade-in">
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-zinc-800 bg-zinc-900/80 text-sm text-zinc-400">
              <Sparkles className="w-4 h-4 text-indigo-400" />
              <span>Powered by Multi-Agent AI</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </div>
          </div>

          {/* Headline */}
          <h1 className="text-center text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.1] mb-6 animate-slide-up gradient-text-hero">
            Battle-Test Your Startup
            <br />
            Before The Market Does
          </h1>

          {/* Subheadline */}
          <p className="text-center text-lg md:text-xl text-zinc-400 max-w-3xl mx-auto mb-10 leading-relaxed animate-slide-up" style={{ animationDelay: '0.1s' }}>
            Kurukshetra AI uses multiple AI agents, live web intelligence, RAG, debates, and scoring engines to evaluate startup ideas before you invest time and money.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-slide-up" style={{ animationDelay: '0.2s' }}>
            <Link
              href="/analyze"
              className="group flex items-center gap-2 px-8 py-3.5 rounded-xl text-base font-semibold bg-indigo-600 text-white hover:bg-indigo-500 transition-all shadow-xl shadow-indigo-600/25 hover:shadow-indigo-600/40 animate-pulse-glow"
            >
              <Swords className="w-5 h-5" />
              Analyze Startup
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link
              href="/battlefield"
              className="flex items-center gap-2 px-8 py-3.5 rounded-xl text-base font-semibold border border-zinc-700 text-zinc-300 hover:text-white hover:border-zinc-600 hover:bg-zinc-800/50 transition-all"
            >
              <Zap className="w-5 h-5" />
              Watch Demo
            </Link>
          </div>

          {/* Stats */}
          <div className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-6 max-w-3xl mx-auto animate-fade-in" style={{ animationDelay: '0.4s' }}>
            {[
              { value: '7', label: 'AI Agents' },
              { value: '100+', label: 'Data Points' },
              { value: '<5min', label: 'Analysis Time' },
              { value: 'PDF', label: 'Export Ready' },
            ].map((stat) => (
              <div key={stat.label} className="text-center">
                <div className="text-2xl md:text-3xl font-bold text-white">{stat.value}</div>
                <div className="text-sm text-zinc-500 mt-1">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="relative py-24 border-t border-zinc-800/50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              Everything You Need to Validate
            </h2>
            <p className="text-lg text-zinc-400 max-w-2xl mx-auto">
              A comprehensive AI-powered analysis pipeline that leaves no stone unturned.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {features.map((feature, i) => (
              <div
                key={feature.title}
                className="group glass-card p-6 hover:border-zinc-700 transition-all duration-300 hover:-translate-y-1"
                style={{ animationDelay: `${i * 0.05}s` }}
              >
                <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${feature.color} flex items-center justify-center mb-4 shadow-lg group-hover:scale-110 transition-transform`}>
                  <feature.icon className="w-5 h-5 text-white" />
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-sm text-zinc-400 leading-relaxed">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="relative py-24 border-t border-zinc-800/50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              How It Works
            </h2>
            <p className="text-lg text-zinc-400">
              From idea to insights in five steps.
            </p>
          </div>

          <div className="space-y-0">
            {steps.map((step, i) => (
              <div key={step.num} className="relative flex gap-6 pb-12 last:pb-0">
                {/* Vertical line */}
                {i < steps.length - 1 && (
                  <div className="absolute left-6 top-14 w-px h-[calc(100%-3.5rem)] bg-gradient-to-b from-indigo-500/40 to-transparent" />
                )}
                {/* Step number */}
                <div className="shrink-0 w-12 h-12 rounded-xl bg-zinc-900 border border-zinc-800 flex items-center justify-center text-sm font-bold text-indigo-400">
                  {step.num}
                </div>
                {/* Content */}
                <div className="pt-1">
                  <h3 className="text-lg font-semibold text-white mb-1">{step.title}</h3>
                  <p className="text-sm text-zinc-400">{step.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="relative py-24 border-t border-zinc-800/50">
        <div className="absolute inset-0 bg-gradient-to-t from-indigo-950/20 to-transparent" />
        <div className="relative max-w-3xl mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Ready to Battle-Test Your Idea?
          </h2>
          <p className="text-lg text-zinc-400 mb-8">
            Get a comprehensive AI-powered analysis in under 5 minutes.
          </p>
          <Link
            href="/analyze"
            className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl text-base font-semibold bg-indigo-600 text-white hover:bg-indigo-500 transition-all shadow-xl shadow-indigo-600/25"
          >
            <Swords className="w-5 h-5" />
            Start Analysis
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-zinc-800/50 py-8">
        <div className="max-w-6xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-sm text-zinc-500">
            <Swords className="w-4 h-4" />
            <span>Kurukshetra AI</span>
          </div>
          <p className="text-sm text-zinc-600">
            Built with multi-agent AI, LangGraph, and RAG
          </p>
        </div>
      </footer>
    </div>
  );
}

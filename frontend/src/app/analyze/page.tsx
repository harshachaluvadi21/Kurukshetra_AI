'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Swords, ArrowRight, Lightbulb, Users, DollarSign, Target } from 'lucide-react';

const examples = [
  'AI Attendance System for Colleges',
  'Campus Cab Sharing Platform',
  'AI Resume Builder for Students',
  'Porter Booking System',
  'Peer-to-Peer Textbook Exchange',
  'AI Study Group Matcher',
];

export default function AnalyzePage() {
  const router = useRouter();
  const [idea, setIdea] = useState('');
  const [problemStatement, setProblemStatement] = useState('');
  const [targetUsers, setTargetUsers] = useState('');
  const [revenueModel, setRevenueModel] = useState('');

  const handleSubmit = () => {
    if (!idea.trim()) return;
    // Store in sessionStorage for battlefield to pick up
    sessionStorage.setItem('kurukshetra_idea', JSON.stringify({
      idea: idea.trim(),
      problemStatement: problemStatement.trim(),
      targetUsers: targetUsers.trim(),
      revenueModel: revenueModel.trim(),
    }));
    router.push('/battlefield');
  };

  return (
    <div className="min-h-screen py-12 md:py-20">
      <div className="max-w-2xl mx-auto px-4 sm:px-6">

        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 mb-6 shadow-lg shadow-indigo-500/20">
            <Swords className="w-7 h-7 text-white" />
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-3">
            Analyze Your Startup
          </h1>
          <p className="text-zinc-400 text-lg">
            Describe your startup idea and our AI agents will battle-test it.
          </p>
        </div>

        {/* Form */}
        <div className="space-y-6">

          {/* Startup Idea (required) */}
          <div>
            <label className="flex items-center gap-2 text-sm font-semibold text-zinc-300 mb-2">
              <Lightbulb className="w-4 h-4 text-amber-400" />
              Startup Idea <span className="text-red-400">*</span>
            </label>
            <textarea
              value={idea}
              onChange={(e) => setIdea(e.target.value)}
              placeholder="Describe your startup idea in 1-3 sentences..."
              rows={3}
              className="w-full px-4 py-3 rounded-xl bg-zinc-900 text-white placeholder-zinc-600 border border-zinc-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all text-base resize-none"
            />
            <div className="flex flex-wrap gap-2 mt-3">
              {examples.map((ex) => (
                <button
                  key={ex}
                  onClick={() => setIdea(ex)}
                  className="text-xs px-3 py-1.5 rounded-lg bg-zinc-800/50 text-zinc-400 hover:text-white hover:bg-zinc-800 border border-zinc-800 transition-colors"
                >
                  {ex}
                </button>
              ))}
            </div>
          </div>

          {/* Problem Statement (optional) */}
          <div>
            <label className="flex items-center gap-2 text-sm font-semibold text-zinc-300 mb-2">
              <Target className="w-4 h-4 text-indigo-400" />
              Problem Statement <span className="text-zinc-600 text-xs">(optional)</span>
            </label>
            <textarea
              value={problemStatement}
              onChange={(e) => setProblemStatement(e.target.value)}
              placeholder="What problem does this solve?"
              rows={2}
              className="w-full px-4 py-3 rounded-xl bg-zinc-900 text-white placeholder-zinc-600 border border-zinc-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all text-base resize-none"
            />
          </div>

          {/* Target Users (optional) */}
          <div>
            <label className="flex items-center gap-2 text-sm font-semibold text-zinc-300 mb-2">
              <Users className="w-4 h-4 text-emerald-400" />
              Target Users <span className="text-zinc-600 text-xs">(optional)</span>
            </label>
            <input
              type="text"
              value={targetUsers}
              onChange={(e) => setTargetUsers(e.target.value)}
              placeholder="e.g. College students, HR managers, small businesses"
              className="w-full px-4 py-3 rounded-xl bg-zinc-900 text-white placeholder-zinc-600 border border-zinc-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all text-base"
            />
          </div>

          {/* Revenue Model (optional) */}
          <div>
            <label className="flex items-center gap-2 text-sm font-semibold text-zinc-300 mb-2">
              <DollarSign className="w-4 h-4 text-amber-400" />
              Revenue Model <span className="text-zinc-600 text-xs">(optional)</span>
            </label>
            <input
              type="text"
              value={revenueModel}
              onChange={(e) => setRevenueModel(e.target.value)}
              placeholder="e.g. SaaS subscription, freemium, marketplace commission"
              className="w-full px-4 py-3 rounded-xl bg-zinc-900 text-white placeholder-zinc-600 border border-zinc-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all text-base"
            />
          </div>

          {/* Submit */}
          <button
            onClick={handleSubmit}
            disabled={!idea.trim()}
            className={`w-full flex items-center justify-center gap-2 px-6 py-4 rounded-xl text-base font-bold transition-all ${
              idea.trim()
                ? 'bg-indigo-600 text-white hover:bg-indigo-500 shadow-xl shadow-indigo-600/25'
                : 'bg-zinc-800 text-zinc-500 cursor-not-allowed'
            }`}
          >
            <Swords className="w-5 h-5" />
            Start Battle Analysis
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}

'use client';
import { useEffect, useState } from 'react';
import { Clock, Play, ExternalLink, Loader2, FileText, Search } from 'lucide-react';
import Link from 'next/link';

interface Run {
  run_id: string;
  idea: string;
  status: string;
  created_at: string;
  battle_score: number | null;
  confidence_score: number | null;
  verdict: string | null;
  has_report: boolean;
}

export default function HistoryPage() {
  const [runs, setRuns] = useState<Run[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await fetch(`${API_URL}/api/v1/runs/`);
        if (!res.ok) throw new Error('Failed to fetch history');
        const data = await res.json();
        setRuns(data.runs || []);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'Failed to fetch history');
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, [API_URL]);

  const filteredRuns = runs.filter((r) => 
    (r.idea || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
    r.run_id.includes(searchTerm)
  );

  return (
    <div className="min-h-screen py-12 md:py-20">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-10">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">History</h1>
            <p className="text-zinc-400">Previous battle analyses and their results.</p>
          </div>
          
          <div className="relative max-w-sm w-full">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
            <input 
              type="text" 
              placeholder="Search by idea or ID..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-zinc-900 border border-zinc-800 rounded-lg text-sm text-white placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </div>

        {loading && (
          <div className="flex justify-center p-12">
            <Loader2 className="w-8 h-8 animate-spin text-indigo-500" />
          </div>
        )}

        {error && (
          <div className="glass-card p-6 border-red-900/50 bg-red-900/10 text-red-400">
            Error loading history: {error}
          </div>
        )}

        {!loading && !error && runs.length === 0 && (
          <div className="glass-card p-12 text-center">
            <Clock className="w-14 h-14 text-zinc-700 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-zinc-400 mb-2">No Previous Battles</h3>
            <p className="text-sm text-zinc-500 max-w-sm mx-auto mb-6">
              Your battle history will appear here after you complete your first analysis.
            </p>
            <Link href="/analyze" className="inline-flex items-center gap-2 px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-sm font-semibold transition-colors">
              Analyze a Startup <Play className="w-4 h-4" />
            </Link>
          </div>
        )}

        {!loading && !error && filteredRuns.length > 0 && (
          <div className="overflow-hidden glass-card">
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-zinc-800 bg-zinc-900/50">
                    <th className="px-6 py-4 text-xs font-semibold text-zinc-400 uppercase tracking-wider">Date</th>
                    <th className="px-6 py-4 text-xs font-semibold text-zinc-400 uppercase tracking-wider">Startup Idea</th>
                    <th className="px-6 py-4 text-xs font-semibold text-zinc-400 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-4 text-xs font-semibold text-zinc-400 uppercase tracking-wider">Score</th>
                    <th className="px-6 py-4 text-xs font-semibold text-zinc-400 uppercase tracking-wider text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-800/50">
                  {filteredRuns.map((run) => (
                    <tr key={run.run_id} className="hover:bg-zinc-800/20 transition-colors">
                      <td className="px-6 py-4 text-sm text-zinc-400 whitespace-nowrap">
                        {new Date(run.created_at).toLocaleDateString()}<br/>
                        <span className="text-xs text-zinc-600">{new Date(run.created_at).toLocaleTimeString()}</span>
                      </td>
                      <td className="px-6 py-4">
                        <div className="text-sm font-semibold text-white line-clamp-2 max-w-md">
                          {run.idea || 'Unknown'}
                        </div>
                        <div className="text-xs text-zinc-600 font-mono mt-1">{run.run_id}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                          run.status === 'completed' ? 'bg-emerald-900/30 text-emerald-400 border border-emerald-800/50' :
                          run.status === 'failed' ? 'bg-red-900/30 text-red-400 border border-red-800/50' :
                          'bg-amber-900/30 text-amber-400 border border-amber-800/50'
                        }`}>
                          {run.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {run.status === 'completed' ? (
                          <div>
                            <div className="text-sm font-bold text-white">{run.battle_score}/100</div>
                            <div className="text-xs text-indigo-400 font-medium">{run.verdict}</div>
                          </div>
                        ) : (
                          <span className="text-zinc-600">--</span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right">
                        <div className="flex items-center justify-end gap-2">
                          {run.has_report && (
                            <Link 
                              href="/reports"
                              className="p-2 text-zinc-400 hover:text-white hover:bg-zinc-800 rounded-lg transition-colors"
                              title="View Report in Reports tab"
                            >
                              <FileText className="w-4 h-4" />
                            </Link>
                          )}
                          <Link
                            href={`/battlefield?run_id=${run.run_id}`}
                            className="p-2 text-zinc-400 hover:text-white hover:bg-zinc-800 rounded-lg transition-colors"
                            title="Open in Battlefield"
                          >
                            <ExternalLink className="w-4 h-4" />
                          </Link>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            
            {filteredRuns.length === 0 && (
              <div className="p-8 text-center text-zinc-500 text-sm">
                No runs match your search.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

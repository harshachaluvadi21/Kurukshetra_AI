'use client';
import { useBattlefieldStore } from '../stores/battlefieldStore';
import { MessageSquare } from 'lucide-react';

export const DebateViewer = () => {
  const history = useBattlefieldStore((state) => state.debateHistory);

  return (
    <div className="flex flex-col h-full bg-slate-900 rounded-lg shadow-md border border-slate-700 overflow-hidden">
      <div className="p-3 bg-slate-800 border-b border-slate-700 flex items-center">
        <MessageSquare className="w-5 h-5 text-blue-400 mr-2" />
        <h3 className="font-semibold text-white">Live Debate Viewer</h3>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {history.length === 0 && (
          <div className="text-slate-500 text-center mt-10 italic">No debate started. Agents will debate once research is complete.</div>
        )}
        
        {history.map((turn, idx) => {
          const isSkeptic = turn.speaker === 'Skeptic';
          const isProponent = turn.speaker === 'Proponent';
          const isJudge = turn.speaker === 'Judge';

          let bubbleColor = 'bg-slate-700 text-white';
          if (isSkeptic) bubbleColor = 'bg-red-900/50 border border-red-500/30 text-red-100';
          if (isProponent) bubbleColor = 'bg-emerald-900/50 border border-emerald-500/30 text-emerald-100';
          if (isJudge) bubbleColor = 'bg-blue-900/50 border border-blue-500/30 text-blue-100';

          return (
            <div key={idx} className={`flex flex-col ${isSkeptic ? 'items-end' : isProponent ? 'items-start' : 'items-center'}`}>
              <span className="text-xs text-slate-400 mb-1 font-semibold">{turn.speaker}</span>
              <div className={`p-3 rounded-xl max-w-[85%] text-sm ${bubbleColor}`}>
                {turn.message}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

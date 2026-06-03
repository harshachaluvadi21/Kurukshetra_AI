'use client';
import { useBattlefieldStore } from '../stores/battlefieldStore';
import { Target, Activity, Gavel, AlertTriangle } from 'lucide-react';

export const ScoreDashboard = () => {
  const { battleScore, confidenceScore, verdict, pivotMandated } = useBattlefieldStore();

  return (
    <div className="grid grid-cols-2 gap-4 h-full">
      {/* Battle Score Card */}
      <div className="bg-white p-4 rounded-lg shadow-md border border-gray-200 flex flex-col justify-between">
        <div className="flex items-center text-slate-600 mb-2">
          <Target className="w-4 h-4 mr-2" />
          <span className="font-semibold text-sm">Battle Score</span>
        </div>
        <div className="text-4xl font-bold text-slate-800">
          {battleScore !== null ? battleScore : '--'}
        </div>
      </div>

      {/* Confidence Score Card */}
      <div className="bg-white p-4 rounded-lg shadow-md border border-gray-200 flex flex-col justify-between">
        <div className="flex items-center text-slate-600 mb-2">
          <Activity className="w-4 h-4 mr-2" />
          <span className="font-semibold text-sm">Confidence</span>
        </div>
        <div className="text-4xl font-bold text-slate-800">
          {confidenceScore !== null ? `${(confidenceScore * 100).toFixed(0)}%` : '--'}
        </div>
      </div>

      {/* Verdict Card */}
      <div className={`col-span-2 p-4 rounded-lg shadow-md border flex items-center justify-between
        ${pivotMandated ? 'bg-red-50 border-red-200' : 'bg-emerald-50 border-emerald-200'}`}>
        <div>
          <div className="flex items-center text-slate-600 mb-1">
            <Gavel className="w-4 h-4 mr-2" />
            <span className="font-semibold text-sm">Final Verdict</span>
          </div>
          <div className={`text-xl font-bold ${pivotMandated ? 'text-red-700' : 'text-emerald-700'}`}>
            {verdict || 'Awaiting analysis...'}
          </div>
        </div>
        
        {pivotMandated && (
          <div className="flex items-center text-red-600 bg-red-100 px-3 py-1 rounded-full font-bold text-sm">
            <AlertTriangle className="w-4 h-4 mr-2" />
            PIVOT MANDATED
          </div>
        )}
      </div>
    </div>
  );
};

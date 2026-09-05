import React from 'react';

interface ScoreBarProps {
  label: string;
  value: number | null;
  max?: number;
}

function getBarClass(value: number, max: number): string {
  const pct = (value / max) * 100;
  if (pct >= 65) return 'score-bar-green';
  if (pct >= 40) return 'score-bar-amber';
  return 'score-bar-red';
}

export function ScoreBar({ label, value, max = 100 }: ScoreBarProps) {
  const pct = value !== null && value !== undefined ? Math.min((value / max) * 100, 100) : 0;
  const barClass = value !== null && value !== undefined ? getBarClass(value, max) : 'score-bar-indigo';

  return (
    <div style={{ marginBottom: 12 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
        <span style={{ fontSize: 13, fontWeight: 500, color: 'var(--text-secondary)' }}>{label}</span>
        <span style={{ fontSize: 13, fontWeight: 700, color: 'var(--text-primary)' }}>
          {value !== null && value !== undefined ? `${value}/${max}` : '—'}
        </span>
      </div>
      <div className="score-bar-track">
        <div
          className={`score-bar-fill ${barClass}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

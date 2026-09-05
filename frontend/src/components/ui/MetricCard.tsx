import React from 'react';

interface MetricCardProps {
  label: string;
  value: string | number | null | undefined;
  sub?: string;
  icon?: React.ElementType;
  iconColor?: string;
  className?: string;
}

export function MetricCard({ label, value, sub, icon: Icon, iconColor = 'text-indigo-500', className = '' }: MetricCardProps) {
  return (
    <div className={`metric-card ${className}`}>
      <div className="flex items-center justify-between">
        <span className="metric-card-label">{label}</span>
        {Icon && <Icon className={`w-4 h-4 ${iconColor} opacity-70`} />}
      </div>
      <div className="metric-card-value">
        {value ?? <span style={{ color: 'var(--text-tertiary)', fontSize: '20px' }}>—</span>}
      </div>
      {sub && <div className="metric-card-sub">{sub}</div>}
    </div>
  );
}

/** Formats a score (0-100) with color-coded text */
export function ScoreDisplay({ score, suffix = '/100', size = 'lg' }: {
  score: number | null;
  suffix?: string;
  size?: 'sm' | 'lg' | 'xl';
}) {
  const color = score === null ? 'var(--text-tertiary)'
    : score >= 65 ? 'var(--success)'
    : score >= 40 ? 'var(--warning)'
    : 'var(--danger)';

  const fontSize = size === 'xl' ? '52px' : size === 'lg' ? '36px' : '22px';

  return (
    <span style={{ fontWeight: 800, fontSize, color, lineHeight: 1 }}>
      {score ?? '—'}
      <span style={{ fontSize: '50%', fontWeight: 500, color: 'var(--text-tertiary)', marginLeft: 4 }}>{score !== null ? suffix : ''}</span>
    </span>
  );
}

import React from 'react';

type BadgeVariant = 'indigo' | 'green' | 'amber' | 'red' | 'slate' | 'gray' | 'fact' | 'estimate' | 'assumption' | 'target';

interface BadgeProps {
  variant?: BadgeVariant;
  children: React.ReactNode;
  className?: string;
}

export function Badge({ variant = 'slate', children, className = '' }: BadgeProps) {
  return (
    <span className={`badge badge-${variant} ${className}`}>
      {children}
    </span>
  );
}

/** Maps raw backend classification labels to badge variants */
export function ClassificationBadge({ raw }: { raw: string }) {
  const lower = raw.toLowerCase();
  if (lower.includes('fact') || lower.includes('user-provided') || lower.includes('verified')) {
    return <Badge variant="fact">Verified</Badge>;
  }
  if (lower.includes('estimate') || lower.includes('source-based')) {
    return <Badge variant="estimate">Estimate</Badge>;
  }
  if (lower.includes('assumption') || lower.includes('modeled') || lower.includes('benchmark')) {
    return <Badge variant="assumption">Assumption</Badge>;
  }
  if (lower.includes('target') || lower.includes('proposed')) {
    return <Badge variant="target">Target</Badge>;
  }
  return <Badge variant="slate">{raw}</Badge>;
}

/** Maps verdict text to appropriate badge */
export function VerdictBadge({ verdict }: { verdict: string | null }) {
  if (!verdict) return <Badge variant="slate">Pending</Badge>;
  const v = verdict.toLowerCase();
  if (v.includes('launch') || v.includes('proceed') || v.includes('promising') || v.includes('strong')) {
    return <Badge variant="green">{verdict}</Badge>;
  }
  if (v.includes('pivot') || v.includes('cautious') || v.includes('conditional') || v.includes('moderate') || v.includes('viable')) {
    return <Badge variant="amber">{verdict}</Badge>;
  }
  if (v.includes('risk') || v.includes('fail') || v.includes('critical') || v.includes('avoid')) {
    return <Badge variant="red">{verdict}</Badge>;
  }
  return <Badge variant="indigo">{verdict}</Badge>;
}

/** Status badge for run status */
export function StatusBadge({ status }: { status: string }) {
  const s = status.toLowerCase();
  if (s === 'completed') return <Badge variant="green">Completed</Badge>;
  if (s === 'failed') return <Badge variant="red">Failed</Badge>;
  if (s === 'running') return <Badge variant="indigo">Running</Badge>;
  return <Badge variant="amber">{status}</Badge>;
}

/** Severity badge for risks */
export function SeverityBadge({ severity }: { severity: string }) {
  const s = severity.toUpperCase();
  if (s === 'HIGH' || s === 'CRITICAL') return <Badge variant="red">High</Badge>;
  if (s === 'MEDIUM' || s === 'MODERATE') return <Badge variant="amber">Medium</Badge>;
  return <Badge variant="green">Low</Badge>;
}

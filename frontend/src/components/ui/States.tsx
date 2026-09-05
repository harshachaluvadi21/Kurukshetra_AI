import React from 'react';
import Link from 'next/link';
import { Loader2 } from 'lucide-react';

interface EmptyStateProps {
  icon?: React.ElementType;
  title: string;
  description?: string;
  actionLabel?: string;
  actionHref?: string;
  onAction?: () => void;
}

export function EmptyState({ icon: Icon, title, description, actionLabel, actionHref, onAction }: EmptyStateProps) {
  return (
    <div className="empty-state">
      {Icon && (
        <div className="empty-state-icon">
          <Icon className="w-6 h-6" />
        </div>
      )}
      <div className="empty-state-title">{title}</div>
      {description && <p className="empty-state-desc">{description}</p>}
      {actionLabel && actionHref && (
        <Link href={actionHref} className="btn btn-primary btn-sm">
          {actionLabel}
        </Link>
      )}
      {actionLabel && onAction && (
        <button onClick={onAction} className="btn btn-primary btn-sm">
          {actionLabel}
        </button>
      )}
    </div>
  );
}

export function LoadingState({ message = 'Loading...' }: { message?: string }) {
  return (
    <div className="empty-state">
      <Loader2 className="w-8 h-8 animate-spin" style={{ color: 'var(--accent)', marginBottom: 12 }} />
      <p style={{ fontSize: 14, color: 'var(--text-secondary)' }}>{message}</p>
    </div>
  );
}

export function ErrorState({ message }: { message: string }) {
  return (
    <div className="card" style={{ padding: '16px 20px', borderColor: 'var(--danger-border)', background: 'var(--danger-light)' }}>
      <p style={{ fontSize: 14, color: 'var(--danger-text)', margin: 0 }}>⚠ {message}</p>
    </div>
  );
}

export function InlineLoader() {
  return <Loader2 className="w-4 h-4 animate-spin" style={{ color: 'var(--accent)' }} />;
}

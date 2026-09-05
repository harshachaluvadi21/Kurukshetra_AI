'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Swords, Mail, Lock, User, ArrowRight, AlertCircle } from 'lucide-react';
import { useAuthStore } from '@/stores/authStore';
import { InlineLoader } from '@/components/ui/States';

export default function RegisterPage() {
  const router = useRouter();
  const { register, isAuthenticated, isLoading: authLoading, error, clearError } = useAuthStore();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [localError, setLocalError] = useState('');

  useEffect(() => { if (isAuthenticated && !authLoading) router.push('/'); }, [isAuthenticated, authLoading, router]);
  useEffect(() => { clearError(); }, [clearError]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError('');
    if (!name || !email || !password || !confirmPassword) { setLocalError('Please fill in all fields'); return; }
    if (password.length < 8) { setLocalError('Password must be at least 8 characters'); return; }
    if (password !== confirmPassword) { setLocalError('Passwords do not match'); return; }
    setSubmitting(true);
    try { await register(name, email, password); router.push('/'); }
    catch (err) { setLocalError(err instanceof Error ? err.message : 'Registration failed'); }
    finally { setSubmitting(false); }
  };

  const displayError = localError || error;

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-page)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '32px 16px' }}>
      <div style={{ width: '100%', maxWidth: 420 }}>
        {/* Logo */}
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <Link href="/" style={{ display: 'inline-flex', alignItems: 'center', gap: 8, textDecoration: 'none' }}>
            <div style={{ width: 36, height: 36, borderRadius: 10, background: 'linear-gradient(135deg,#6366F1,#4F46E5)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Swords style={{ color: '#fff', width: 18, height: 18 }} />
            </div>
            <span style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-primary)' }}>
              Kurukshetra<span style={{ color: 'var(--accent)' }}>.ai</span>
            </span>
          </Link>
        </div>

        {/* Card */}
        <div className="card" style={{ padding: '32px' }}>
          <div style={{ textAlign: 'center', marginBottom: 24 }}>
            <h1 style={{ fontSize: 22, fontWeight: 700, color: 'var(--text-primary)', margin: '0 0 6px' }}>Create your account</h1>
            <p style={{ fontSize: 14, color: 'var(--text-secondary)', margin: 0 }}>Start battle-testing your startup ideas</p>
          </div>

          {/* Google */}
          <a
            href="/api/auth/google"
            style={{ width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 10, padding: '10px 16px', borderRadius: 8, border: '1px solid var(--border-strong)', background: '#fff', fontSize: 14, fontWeight: 500, color: 'var(--text-primary)', cursor: 'pointer', textDecoration: 'none', marginBottom: 20 }}
          >
            <svg viewBox="0 0 24 24" style={{ width: 18, height: 18 }}>
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" />
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
            </svg>
            Sign up with Google
          </a>

          {/* Divider */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 20 }}>
            <div style={{ flex: 1, height: 1, background: 'var(--border)' }} />
            <span style={{ fontSize: 12, color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>or</span>
            <div style={{ flex: 1, height: 1, background: 'var(--border)' }} />
          </div>

          {displayError && (
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '10px 14px', borderRadius: 8, background: 'var(--danger-light)', border: '1px solid var(--danger-border)', marginBottom: 16 }}>
              <AlertCircle className="w-4 h-4" style={{ color: 'var(--danger)', flexShrink: 0 }} />
              <span style={{ fontSize: 13, color: 'var(--danger-text)' }}>{displayError}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            <div>
              <label htmlFor="reg-name" className="label">Full Name</label>
              <div style={{ position: 'relative' }}>
                <User className="w-4 h-4" style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-tertiary)', width: 14, height: 14 }} />
                <input id="reg-name" type="text" value={name} onChange={e => setName(e.target.value)} placeholder="Your name" className="input-field" style={{ paddingLeft: 34 }} autoComplete="name" />
              </div>
            </div>
            <div>
              <label htmlFor="reg-email" className="label">Email</label>
              <div style={{ position: 'relative' }}>
                <Mail className="w-4 h-4" style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-tertiary)', width: 14, height: 14 }} />
                <input id="reg-email" type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="you@example.com" className="input-field" style={{ paddingLeft: 34 }} autoComplete="email" />
              </div>
            </div>
            <div>
              <label htmlFor="reg-password" className="label">Password</label>
              <div style={{ position: 'relative' }}>
                <Lock className="w-4 h-4" style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-tertiary)', width: 14, height: 14 }} />
                <input id="reg-password" type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Min. 8 characters" className="input-field" style={{ paddingLeft: 34 }} autoComplete="new-password" />
              </div>
            </div>
            <div>
              <label htmlFor="reg-confirm" className="label">Confirm Password</label>
              <div style={{ position: 'relative' }}>
                <Lock className="w-4 h-4" style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-tertiary)', width: 14, height: 14 }} />
                <input id="reg-confirm" type="password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} placeholder="Re-enter password" className="input-field" style={{ paddingLeft: 34 }} autoComplete="new-password" />
              </div>
            </div>
            <button type="submit" disabled={submitting} className="btn btn-primary" style={{ justifyContent: 'center', padding: '12px', marginTop: 4 }}>
              {submitting ? <InlineLoader /> : <><span>Create Account</span><ArrowRight className="w-4 h-4" /></>}
            </button>
          </form>

          <p style={{ textAlign: 'center', fontSize: 13, color: 'var(--text-secondary)', marginTop: 20 }}>
            Already have an account?{' '}
            <Link href="/login" style={{ color: 'var(--accent)', fontWeight: 600, textDecoration: 'none' }}>Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  );
}

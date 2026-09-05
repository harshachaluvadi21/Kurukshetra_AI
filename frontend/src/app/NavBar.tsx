'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import { Swords, LogOut, ChevronDown, Menu, X } from 'lucide-react';
import { useAuthStore } from '@/stores/authStore';

const NAV_LINKS = [
  { href: '/analyze',     label: 'Analyze' },
  { href: '/battlefield', label: 'Battlefield' },
  { href: '/reports',     label: 'Reports' },
  { href: '/history',     label: 'History' },
];

export default function NavBar() {
  const pathname = usePathname();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const { user, isAuthenticated, logout } = useAuthStore();

  const isActive = (href: string) =>
    pathname === href || (href !== '/' && pathname.startsWith(href + '/'));

  return (
    <header style={{
      position: 'sticky', top: 0, zIndex: 50,
      background: 'rgba(255, 255, 255, 0.94)',
      backdropFilter: 'blur(12px)',
      WebkitBackdropFilter: 'blur(12px)',
      borderBottom: '1px solid rgba(16, 24, 40, 0.08)',
      height: 64,
    }}>
      <div className="container" style={{ display: 'flex', alignItems: 'center', height: '100%', gap: 0 }}>

        {/* Logo */}
        <Link
          href="/"
          style={{ display: 'flex', alignItems: 'center', gap: 10, textDecoration: 'none', flexShrink: 0, marginRight: 48 }}
        >
          <div style={{
            width: 34, height: 34, borderRadius: 9,
            background: 'linear-gradient(135deg, #5B5CEB 0%, #3B3CBF 100%)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: '0 2px 10px rgba(91, 92, 235, 0.25)',
            border: '1px solid rgba(201, 154, 61, 0.35)',
            position: 'relative'
          }}>
            <Swords className="w-4 h-4" style={{ color: '#fff' }} />
            <div style={{ position: 'absolute', top: -1, right: -1, width: 6, height: 6, borderRadius: '50%', background: '#C99A3D', boxShadow: '0 0 6px #C99A3D' }} />
          </div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span style={{ fontSize: 16, fontWeight: 800, color: '#101828', letterSpacing: '-0.02em', lineHeight: 1.15 }}>
              Kurukshetra<span style={{ color: '#5B5CEB' }}>.ai</span>
            </span>
            <span style={{ fontSize: 9, fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase', color: '#C99A3D', lineHeight: 1 }}>
              AI Battlefield
            </span>
          </div>
        </Link>

        {/* Desktop center nav */}
        <nav style={{ display: 'flex', alignItems: 'center', gap: 4, flex: 1 }} className="desktop-nav">
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              style={{
                padding: '6px 14px',
                borderRadius: 6,
                fontSize: 14,
                fontWeight: 500,
                textDecoration: 'none',
                transition: 'background 0.15s, color 0.15s, border-color 0.15s',
                background: isActive(link.href) ? '#F1F0FF' : 'transparent',
                color: isActive(link.href) ? '#5B5CEB' : 'var(--text-secondary)',
                border: isActive(link.href) ? '1px solid rgba(91, 92, 235, 0.2)' : '1px solid transparent',
              }}
            >
              {link.label}
            </Link>
          ))}
        </nav>

        {/* Right side */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginLeft: 'auto', flexShrink: 0 }}>
          {!isAuthenticated ? (
            <>
              <Link href="/login" className="btn btn-ghost btn-sm" style={{ textDecoration: 'none' }}>Log In</Link>
              <Link href="/register" className="btn btn-primary btn-sm" style={{ textDecoration: 'none' }}>Get Started</Link>
            </>
          ) : (
            <div style={{ position: 'relative' }}>
              <button
                onClick={() => setDropdownOpen(!dropdownOpen)}
                style={{
                  display: 'flex', alignItems: 'center', gap: 8,
                  padding: '6px 10px', borderRadius: 8,
                  border: '1px solid var(--border)', background: '#fff',
                  cursor: 'pointer', fontSize: 14,
                }}
              >
                <div style={{
                  width: 26, height: 26, borderRadius: '50%',
                  background: 'var(--accent-light)', color: 'var(--accent-text)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: 12, fontWeight: 700, textTransform: 'uppercase',
                }}>
                  {user?.name?.charAt(0) || user?.email?.charAt(0) || 'U'}
                </div>
                <span style={{ fontWeight: 500, color: 'var(--text-primary)', maxWidth: 100, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {user?.name?.split(' ')[0] || user?.email?.split('@')[0]}
                </span>
                <ChevronDown className={`w-3.5 h-3.5`} style={{ color: 'var(--text-tertiary)', transform: dropdownOpen ? 'rotate(180deg)' : 'none', transition: 'transform 0.15s' }} />
              </button>

              {dropdownOpen && (
                <>
                  <div
                    style={{ position: 'fixed', inset: 0, zIndex: 10 }}
                    onClick={() => setDropdownOpen(false)}
                  />
                  <div style={{
                    position: 'absolute', right: 0, top: 'calc(100% + 8px)',
                    width: 200, background: '#fff', borderRadius: 10,
                    border: '1px solid var(--border)', boxShadow: 'var(--shadow-md)',
                    zIndex: 100, overflow: 'hidden',
                  }}>
                    <div style={{ padding: '12px 16px', borderBottom: '1px solid var(--border)' }}>
                      <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-primary)', marginBottom: 2, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{user?.name}</div>
                      <div style={{ fontSize: 12, color: 'var(--text-tertiary)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{user?.email}</div>
                    </div>
                    <button
                      onClick={() => { setDropdownOpen(false); logout(); }}
                      style={{
                        width: '100%', display: 'flex', alignItems: 'center', gap: 8,
                        padding: '10px 16px', fontSize: 13, fontWeight: 500,
                        color: 'var(--danger-text)', background: 'transparent',
                        border: 'none', cursor: 'pointer', textAlign: 'left',
                      }}
                      onMouseEnter={e => (e.currentTarget.style.background = 'var(--danger-light)')}
                      onMouseLeave={e => (e.currentTarget.style.background = 'transparent')}
                    >
                      <LogOut className="w-3.5 h-3.5" />
                      Sign Out
                    </button>
                  </div>
                </>
              )}
            </div>
          )}

          {/* Mobile hamburger */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="mobile-menu-btn"
            style={{ padding: 8, borderRadius: 6, border: '1px solid var(--border)', background: '#fff', cursor: 'pointer', display: 'none' }}
          >
            {mobileOpen ? <X className="w-4 h-4" style={{ color: 'var(--text-secondary)' }} /> : <Menu className="w-4 h-4" style={{ color: 'var(--text-secondary)' }} />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div style={{
          background: '#fff', borderTop: '1px solid var(--border)',
          padding: '8px 16px 16px',
        }}>
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setMobileOpen(false)}
              style={{
                display: 'block', padding: '10px 12px',
                borderRadius: 8, marginBottom: 2,
                fontSize: 15, fontWeight: 500, textDecoration: 'none',
                background: isActive(link.href) ? 'var(--accent-light)' : 'transparent',
                color: isActive(link.href) ? 'var(--accent-text)' : 'var(--text-secondary)',
              }}
            >
              {link.label}
            </Link>
          ))}
          {!isAuthenticated && (
            <div style={{ marginTop: 8, paddingTop: 12, borderTop: '1px solid var(--border)', display: 'flex', gap: 8 }}>
              <Link href="/login" onClick={() => setMobileOpen(false)} className="btn btn-secondary btn-sm" style={{ flex: 1, textDecoration: 'none', justifyContent: 'center' }}>Log In</Link>
              <Link href="/register" onClick={() => setMobileOpen(false)} className="btn btn-primary btn-sm" style={{ flex: 1, textDecoration: 'none', justifyContent: 'center' }}>Get Started</Link>
            </div>
          )}
        </div>
      )}

      <style>{`
        @media (max-width: 768px) {
          .desktop-nav { display: none !important; }
          .mobile-menu-btn { display: flex !important; }
        }
      `}</style>
    </header>
  );
}

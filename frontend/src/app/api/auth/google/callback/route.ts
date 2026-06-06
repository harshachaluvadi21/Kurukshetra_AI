import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

function safeNextPath(value: string | undefined) {
  if (!value || !value.startsWith('/') || value.startsWith('//')) return '/';
  if (value.startsWith('/login') || value.startsWith('/register') || value.startsWith('/auth/')) return '/';
  return value;
}

export async function GET(request: Request) {
  const url = new URL(request.url);
  const code = url.searchParams.get('code');
  const state = url.searchParams.get('state');
  const error = url.searchParams.get('error');

  if (error) {
    return NextResponse.redirect(new URL(`/login?error=${encodeURIComponent(error)}`, request.url));
  }

  if (!code || !state) {
    return NextResponse.redirect(new URL('/login?error=Missing+code+or+state', request.url));
  }

  // Validate CSRF state
  const cookieStore = await cookies();
  const savedState = cookieStore.get('kurukshetra_oauth_state')?.value;
  const next = safeNextPath(cookieStore.get('kurukshetra_oauth_next')?.value);

  if (!savedState || state !== savedState) {
    return NextResponse.redirect(new URL('/login?error=Invalid+state', request.url));
  }

  try {
    // Send code to backend to exchange and login/register
    const redirectUri = `${url.origin}/api/auth/google/callback`;
    const res = await fetch(`${BACKEND_URL}/auth/google/callback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, redirect_uri: redirectUri }),
    });

    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      const err = data.detail || 'Google authentication failed on backend';
      return NextResponse.redirect(new URL(`/login?error=${encodeURIComponent(err)}`, request.url));
    }

    const data = await res.json();
    const token = data.access_token;
    
    // Redirect to frontend callback page with the token
    const response = NextResponse.redirect(new URL(`/auth/callback?token=${token}&next=${encodeURIComponent(next)}`, request.url));
    response.cookies.delete('kurukshetra_oauth_state');
    response.cookies.delete('kurukshetra_oauth_next');
    return response;
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : 'Unknown error';
    return NextResponse.redirect(new URL(`/login?error=${encodeURIComponent(msg)}`, request.url));
  }
}

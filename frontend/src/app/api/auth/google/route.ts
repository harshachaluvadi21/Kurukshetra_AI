import { NextResponse } from 'next/server';

function googleClientId() {
  return process.env.GOOGLE_CLIENT_ID || process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || '';
}

function randomState() {
  const bytes = new Uint8Array(24);
  crypto.getRandomValues(bytes);
  return Array.from(bytes, (byte) => byte.toString(16).padStart(2, '0')).join('');
}

export async function GET(request: Request) {
  const clientId = googleClientId();
  if (!clientId) {
    return NextResponse.redirect(new URL('/login?error=missing_google_client_id', request.url));
  }

  const url = new URL(request.url);
  const redirectUri = `${url.origin}/api/auth/google/callback`;
  const state = randomState();
  const googleUrl = new URL('https://accounts.google.com/o/oauth2/v2/auth');

  googleUrl.searchParams.set('client_id', clientId);
  googleUrl.searchParams.set('redirect_uri', redirectUri);
  googleUrl.searchParams.set('response_type', 'code');
  googleUrl.searchParams.set('scope', 'openid email profile');
  googleUrl.searchParams.set('prompt', 'select_account');
  googleUrl.searchParams.set('state', state);

  const response = NextResponse.redirect(googleUrl);
  response.cookies.set('kurukshetra_oauth_state', state, {
    httpOnly: true,
    sameSite: 'lax',
    secure: process.env.NODE_ENV === 'production',
    maxAge: 10 * 60,
    path: '/',
  });
  return response;
}

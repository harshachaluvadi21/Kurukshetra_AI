import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  
  // Public routes that don't require authentication
  const isPublicRoute = 
    pathname === '/' || 
    pathname === '/login' || 
    pathname === '/register' || 
    pathname.startsWith('/api/') || 
    pathname.startsWith('/auth/');
    
  // Allow all static files
  if (
    pathname.startsWith('/_next') ||
    pathname.endsWith('.ico') ||
    pathname.endsWith('.css')
  ) {
    return NextResponse.next();
  }

  // Token is stored in localStorage which isn't accessible here,
  // but we can check if it exists in the browser via client-side check.
  // However, Next.js middleware runs on edge and can't read localStorage.
  // Instead, the Zustand store will handle redirects on initial load.
  // We will let the request pass through and rely on the client-side
  // auth guard in layout.tsx or individual pages for full protection.
  
  return NextResponse.next();
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
};

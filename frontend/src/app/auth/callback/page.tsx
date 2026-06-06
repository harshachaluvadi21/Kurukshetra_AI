'use client';

import { useEffect, useState, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAuthStore } from '@/stores/authStore';
import { Loader2 } from 'lucide-react';

function AuthCallbackContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { loginWithToken } = useAuthStore();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = searchParams.get('token');
    const next = searchParams.get('next') || '/';
    const err = searchParams.get('error');

    if (err) {
      // Redirect to login after 3 seconds on error
      setTimeout(() => setError(decodeURIComponent(err)), 0);
      setTimeout(() => router.push('/login'), 3000);
      return;
    }

    if (token) {
      loginWithToken(token)
        .then(() => {
          router.push(next.startsWith('/') && !next.startsWith('//') ? next : '/');
        })
        .catch(() => {
          setError('Failed to log in with Google');
          setTimeout(() => router.push('/login'), 3000);
        });
    } else {
      setTimeout(() => setError('No token provided'), 0);
      setTimeout(() => router.push('/login'), 3000);
    }
  }, [searchParams, router, loginWithToken]);

  return (
    <div className="text-center">
      {error ? (
        <div className="text-red-400">
          <p className="mb-2">Authentication Error</p>
          <p className="text-sm text-zinc-500">{error}</p>
          <p className="text-sm text-zinc-500 mt-4">Redirecting to login...</p>
        </div>
      ) : (
        <div className="flex flex-col items-center">
          <Loader2 className="w-8 h-8 text-indigo-500 animate-spin mb-4" />
          <p className="text-zinc-400">Authenticating...</p>
        </div>
      )}
    </div>
  );
}

export default function AuthCallbackPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-zinc-950">
      <Suspense fallback={
        <div className="flex flex-col items-center">
          <Loader2 className="w-8 h-8 text-indigo-500 animate-spin mb-4" />
          <p className="text-zinc-400">Loading...</p>
        </div>
      }>
        <AuthCallbackContent />
      </Suspense>
    </div>
  );
}

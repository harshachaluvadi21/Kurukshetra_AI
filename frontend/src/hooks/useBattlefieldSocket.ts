import { useState, useEffect } from 'react';
import { useBattlefieldStore } from '@/stores/battlefieldStore';

export const useBattlefieldSocket = (runId: string | null, isMockMode: boolean) => {
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    if (isMockMode || !runId) return;

    let isClosed = false;

    // Derive WebSocket URL from NEXT_PUBLIC_API_URL env var
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    let host = apiUrl.replace(/^https?:\/\//, '').replace(/\/+$/, '');

    // In browser, synchronize hostname (localhost vs 127.0.0.1) to avoid IPv6/IPv4 mismatch
    if (typeof window !== 'undefined') {
      const currentHost = window.location.hostname;
      if (host.startsWith('localhost:') && currentHost === '127.0.0.1') {
        host = host.replace('localhost:', '127.0.0.1:');
      } else if (host.startsWith('127.0.0.1:') && currentHost === 'localhost') {
        host = host.replace('127.0.0.1:', 'localhost:');
      }
    }

    const base = apiUrl.startsWith('https') ? 'wss://' : 'ws://';
    const wsUrl = `${base}${host}/ws/v1/runs/${runId}`;

    let ws: WebSocket | null = null;
    try {
      ws = new WebSocket(wsUrl);
    } catch (e) {
      console.warn('Failed to initialize WebSocket connection:', e);
      return;
    }

    ws.onopen = () => {
      if (isClosed) return;
      console.log('WebSocket connected:', wsUrl);
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      if (isClosed) return;
      try {
        const data = JSON.parse(event.data);
        useBattlefieldStore.getState().handleEvent(data);
      } catch (e) {
        console.warn('Failed to parse WS message', e);
      }
    };

    ws.onerror = (err) => {
      if (isClosed) return;
      console.warn('WebSocket connection notice:', err);
      setIsConnected(false);
    };

    ws.onclose = () => {
      if (isClosed) return;
      console.log('WebSocket closed');
      setIsConnected(false);
      useBattlefieldStore.getState().setIsRunning(false);
    };

    // Cleanup on unmount or when runId changes
    return () => {
      isClosed = true;
      if (ws) {
        ws.onopen = null;
        ws.onmessage = null;
        ws.onerror = null;
        ws.onclose = null;
        if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
          ws.close();
        }
      }
    };
  }, [runId, isMockMode]);

  const triggerMockReplay = () => {
    // Mock mode logic (unchanged)
  };

  return { isConnected, triggerMockReplay };
};

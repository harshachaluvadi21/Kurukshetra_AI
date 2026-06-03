import { useState, useEffect } from 'react';
import { useBattlefieldStore } from '@/stores/battlefieldStore';

export const useBattlefieldSocket = (runId: string | null, isMockMode: boolean) => {
  const { handleEvent, setIsRunning, setRunId } = useBattlefieldStore();

  const [isConnected, setIsConnected] = useState(false);

  // Derive WebSocket URL from NEXT_PUBLIC_API_URL env var
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const wsUrl = (() => {
    const base = apiUrl.startsWith('https') ? 'wss://' : 'ws://';
    // Strip protocol and possible trailing slash
    const host = apiUrl
    .replace(/^https?:\/\//, '')
    .replace(/\/+$/, '');
    return `${base}${host}/ws/v1/runs/${runId ?? ''}`;
  })();

  useEffect(() => {
    if (isMockMode || !runId) return;

    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log('WebSocket connected:', wsUrl);
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        handleEvent(data);
      } catch (e) {
        console.error('Failed to parse WS message', e);
      }
    };

    ws.onerror = (err) => {
      console.error('WebSocket error', err);
      setIsConnected(false);
    };

    ws.onclose = () => {
      console.log('WebSocket closed');
      setIsConnected(false);
      setIsRunning(false);
    };

    // Cleanup on unmount or when runId changes
    return () => {
      ws.close();
    };
  }, [runId, isMockMode, wsUrl, handleEvent, setIsRunning]);

  const triggerMockReplay = () => {
    // Mock mode logic (unchanged)
  };

  return { isConnected, triggerMockReplay };
};

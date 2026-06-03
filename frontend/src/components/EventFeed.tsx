'use client';
import { useBattlefieldStore } from '../stores/battlefieldStore';
import { useEffect, useRef } from 'react';
import { Terminal } from 'lucide-react';

export const EventFeed = () => {
  const events = useBattlefieldStore((state) => state.events);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [events]);

  return (
    <div className="flex flex-col h-full bg-[#1e1e1e] rounded-lg shadow-md overflow-hidden border border-[#333]">
      <div className="p-2 bg-[#2d2d2d] border-b border-[#444] flex items-center">
        <Terminal className="w-4 h-4 text-emerald-400 mr-2" />
        <span className="text-xs font-mono text-slate-300">live-event-stream.log</span>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 font-mono text-xs space-y-1">
        {events.length === 0 && (
          <div className="text-slate-500 italic text-center mt-8">No events yet. Start a simulation to see live agent activity.</div>
        )}
        {events.map((ev, i) => {
          const time = new Date(ev.timestamp).toLocaleTimeString();
          const eventData = ev.data && typeof ev.data === 'object' ? ev.data as Record<string, unknown> : null;
          const agentName = eventData?.agent_name ? String(eventData.agent_name) : '';
          const message = eventData?.message ? String(eventData.message) : JSON.stringify(ev.data);
          let color = 'text-slate-300';
          if (ev.event_type.includes('error')) color = 'text-red-400';
          else if (ev.event_type.includes('completed')) color = 'text-emerald-400';
          else if (ev.event_type.includes('thinking')) color = 'text-yellow-300';
          
          return (
            <div key={i} className="flex">
              <span className="text-slate-500 mr-3 w-20 shrink-0">[{time}]</span>
              <span className="text-blue-400 mr-3 w-32 shrink-0">{ev.event_type.toUpperCase()}</span>
              <span className={color}>
                {agentName && <span className="font-bold">{agentName}: </span>}
                {message}
              </span>
            </div>
          );
        })}
        <div ref={endRef} />
      </div>
    </div>
  );
};

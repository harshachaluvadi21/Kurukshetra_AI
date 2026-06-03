'use client';
import { ReactFlow, Background, Controls, Node, Edge } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { useBattlefieldStore } from '../stores/battlefieldStore';

const initialNodes: Node[] = [
  { id: 'strategy_commander', position: { x: 250, y: 50 }, data: { label: 'Strategy Commander' } },
  { id: 'intelligence_scout', position: { x: 50, y: 150 }, data: { label: 'Intelligence Scout' } },
  { id: 'opponent_analyst', position: { x: 250, y: 150 }, data: { label: 'Opponent Analyst' } },
  { id: 'treasury_advisor', position: { x: 450, y: 150 }, data: { label: 'Treasury Advisor' } },
  { id: 'swot_gtm', position: { x: 250, y: 250 }, data: { label: 'SWOT + GTM' } },
  { id: 'critic_agent', position: { x: 250, y: 350 }, data: { label: 'Critic Agent' } },
  { id: 'debate_engine', position: { x: 250, y: 450 }, data: { label: 'Debate Engine' } },
  { id: 'battle_score', position: { x: 250, y: 550 }, data: { label: 'Battle Score' } },
  { id: 'confidence', position: { x: 250, y: 650 }, data: { label: 'Confidence Engine' } },
];

const initialEdges: Edge[] = [
  { id: 'e1-2', source: 'strategy_commander', target: 'intelligence_scout', style: { stroke: '#3f3f46' } },
  { id: 'e1-3', source: 'strategy_commander', target: 'opponent_analyst', style: { stroke: '#3f3f46' } },
  { id: 'e1-4', source: 'strategy_commander', target: 'treasury_advisor', style: { stroke: '#3f3f46' } },
  { id: 'e2-5', source: 'intelligence_scout', target: 'swot_gtm', style: { stroke: '#3f3f46' } },
  { id: 'e3-5', source: 'opponent_analyst', target: 'swot_gtm', style: { stroke: '#3f3f46' } },
  { id: 'e4-5', source: 'treasury_advisor', target: 'swot_gtm', style: { stroke: '#3f3f46' } },
  { id: 'e5-6', source: 'swot_gtm', target: 'critic_agent', style: { stroke: '#3f3f46' } },
  { id: 'e6-7', source: 'critic_agent', target: 'debate_engine', style: { stroke: '#3f3f46' } },
  { id: 'e7-8', source: 'debate_engine', target: 'battle_score', style: { stroke: '#3f3f46' } },
  { id: 'e8-9', source: 'battle_score', target: 'confidence', style: { stroke: '#3f3f46' } },
];

export const ReactFlowGraph = () => {
  const nodeStates = useBattlefieldStore((state) => state.nodeStates);

  const nodes = initialNodes.map((node) => {
    const status = nodeStates[node.id];
    let bgColor = '#18181b';
    let borderColor = '#27272a';
    let textColor = '#a1a1aa';
    if (status === 'running') { bgColor = '#1e1b4b'; borderColor = '#6366f1'; textColor = '#c7d2fe'; }
    else if (status === 'completed') { bgColor = '#052e16'; borderColor = '#10b981'; textColor = '#a7f3d0'; }
    else if (status === 'failed') { bgColor = '#450a0a'; borderColor = '#ef4444'; textColor = '#fecaca'; }

    return {
      ...node,
      style: {
        background: bgColor,
        color: textColor,
        border: `1px solid ${borderColor}`,
        borderRadius: '10px',
        padding: '12px 16px',
        fontWeight: '600',
        fontSize: '12px',
        textAlign: 'center' as const,
        width: 160,
        boxShadow: status === 'running' ? '0 0 20px rgba(99,102,241,0.2)' : 'none',
      }
    };
  });

  return (
    <div className="w-full h-full rounded-xl overflow-hidden">
      <ReactFlow nodes={nodes} edges={initialEdges} fitView proOptions={{ hideAttribution: true }}>
        <Background color="#27272a" gap={20} />
        <Controls
          style={{ background: '#18181b', border: '1px solid #27272a', borderRadius: '8px' }}
        />
      </ReactFlow>
    </div>
  );
};

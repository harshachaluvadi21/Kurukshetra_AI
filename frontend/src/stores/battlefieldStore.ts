import { create } from 'zustand';

export type NodeStatus = 'idle' | 'running' | 'completed' | 'failed';

export interface AppEvent {
  event_type: string;
  run_id: string;
  timestamp: string;
  data: Record<string, unknown>;
}

interface BattlefieldState {
  // Node states for React Flow
  nodeStates: Record<string, NodeStatus>;
  
  // Events for terminal feed
  events: AppEvent[];
  
  // Debate history for Debate Viewer
  debateHistory: Array<{ speaker: string; message: string; timestamp: string }>;
  
  // Scores
  battleScore: number | null;
  confidenceScore: number | null;
  verdict: string | null;
  pivotMandated: boolean;
  
  // Actions
  handleEvent: (event: AppEvent) => void;
  reset: () => void;
  
  // Execution states
  isRunning: boolean;
  setIsRunning: (running: boolean) => void;
  runId: string | null;
  setRunId: (id: string | null) => void;
  
  // Report download paths
  reportLinks: {
    report_id?: string;
    manifest_path?: string;
    pdf_path?: string;
    json_path?: string;
    md_path?: string;
  } | null;
  
  // Full final report state
  finalReport: unknown | null;
  setFinalState: (state: unknown) => void;
}

export const useBattlefieldStore = create<BattlefieldState>((set) => ({
  nodeStates: {
    strategy_commander: 'idle',
    intelligence_scout: 'idle',
    opponent_analyst: 'idle',
    treasury_advisor: 'idle',
    swot_gtm: 'idle',
    critic_agent: 'idle',
    debate_engine: 'idle',
    battle_score: 'idle',
    confidence: 'idle',
  },
  events: [],
  debateHistory: [],
  battleScore: null,
  confidenceScore: null,
  verdict: null,
  pivotMandated: false,
  isRunning: false,
  runId: null,
  reportLinks: null,
  finalReport: null,
  
  setIsRunning: (running: boolean) => set({ isRunning: running }),
  setRunId: (id: string | null) => set({ runId: id }),
  setFinalState: (st: unknown) => set({ finalReport: st }),

  reset: () => set({
    nodeStates: {
      strategy_commander: 'idle',
      intelligence_scout: 'idle',
      opponent_analyst: 'idle',
      treasury_advisor: 'idle',
      swot_gtm: 'idle',
      critic_agent: 'idle',
      debate_engine: 'idle',
      battle_score: 'idle',
      confidence: 'idle',
    },
    events: [],
    debateHistory: [],
    battleScore: null,
    confidenceScore: null,
    verdict: null,
    pivotMandated: false,
    reportLinks: null,
    finalReport: null,
    // don't reset runId/isRunning here as it might be in progress
  }),

  handleEvent: (event: AppEvent) => set((state) => {
    const newState = { ...state };
    newState.events = [...state.events, event];

    const type = event.event_type;
    const data = event.data;
    
    // Map Agent names to Node IDs
    const agentToNodeId: Record<string, string> = {
      'Strategy Commander': 'strategy_commander',
      'Intelligence Scout': 'intelligence_scout',
      'Opponent Analyst': 'opponent_analyst',
      'Treasury Advisor': 'treasury_advisor',
      'Critic Agent': 'critic_agent',
    };

    if (type === 'agent_started' || type === 'agent_thinking') {
      const nodeId = agentToNodeId[String(data.agent_name || '')];
      if (nodeId) newState.nodeStates = { ...newState.nodeStates, [nodeId]: 'running' };
    } 
    else if (type === 'agent_completed') {
      const nodeId = agentToNodeId[String(data.agent_name || '')];
      if (nodeId) newState.nodeStates = { ...newState.nodeStates, [nodeId]: 'completed' };
    }
    else if (type === 'debate_started') {
      newState.nodeStates = { ...newState.nodeStates, swot_gtm: 'completed', critic_agent: 'completed' };
      newState.nodeStates = { ...newState.nodeStates, debate_engine: 'running' };
    }
    else if (type === 'debate_turn') {
      newState.debateHistory = [...state.debateHistory, { 
        speaker: String(data.speaker || ''), 
        message: String(data.message || ''), 
        timestamp: event.timestamp 
      }];
    }
    else if (type === 'debate_completed') {
      newState.nodeStates = { ...newState.nodeStates, debate_engine: 'completed' };
    }
    else if (type === 'score_generated') {
      newState.nodeStates = { ...newState.nodeStates, battle_score: 'completed' };
      newState.battleScore = Number(data.score);
      newState.pivotMandated = Boolean(data.pivot_mandated);
    }
    else if (type === 'verdict_generated') {
      newState.verdict = String(data.verdict || '');
    }
    else if (type === 'confidence_generated') {
      newState.nodeStates = { ...newState.nodeStates, confidence: 'completed' };
      newState.confidenceScore = Number(data.overall_confidence);
    }
    else if (type === 'report_generated') {
      newState.reportLinks = {
        report_id: String(data.report_id || ''),
        manifest_path: data.manifest_path ? String(data.manifest_path) : undefined,
        pdf_path: data.pdf_path ? String(data.pdf_path) : undefined,
        json_path: data.json_path ? String(data.json_path) : undefined,
        md_path: data.md_path ? String(data.md_path) : undefined,
      };
    }
    else if (type === 'execution_completed' || type === 'execution_failed') {
      newState.isRunning = false;
    }

    return newState;
  }),
}));

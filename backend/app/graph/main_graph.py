from langgraph.graph import StateGraph, END
from app.graph.state import GraphState
from app.agents.strategy_commander import StrategyCommander
from app.agents.intelligence_scout import IntelligenceScout
from app.agents.opponent_analyst import OpponentAnalyst
from app.agents.treasury_advisor import TreasuryAdvisor
from app.agents.critic_agent import CriticAgent
from app.graph.debate_engine import debate_graph
from app.services.battle_score import BattleScoreEngine
from app.services.business_intelligence import build_gtm_strategy, build_swot
from app.evaluation.evaluator import ConfidenceEngine
from app.reports.report_builder import ReportBuilder
import uuid

# Instantiate nodes
commander = StrategyCommander()
scout = IntelligenceScout()
analyst = OpponentAnalyst()
treasury = TreasuryAdvisor()
critic = CriticAgent()
score_engine = BattleScoreEngine()
confidence_engine = ConfidenceEngine()
report_builder = ReportBuilder()

async def commander_node(state: GraphState):
    return await commander.invoke(state)

async def scout_node(state: GraphState):
    return await scout.invoke(state)

async def analyst_node(state: GraphState):
    return await analyst.invoke(state)

async def treasury_node(state: GraphState):
    return await treasury.invoke(state)

async def swot_gtm_node(state: GraphState):
    return {
        "swot_analysis": build_swot(state),
        "gtm_strategy": build_gtm_strategy(state),
        "execution_logs": ["SWOT and GTM strategy generated successfully."]
    }

async def critic_node(state: GraphState):
    return await critic.invoke(state)

async def debate_engine_node(state: GraphState):
    # Adapt GraphState to DebateState
    debate_initial = {
        "run_id": state.get("run_id"),
        "debate_id": str(uuid.uuid4()),
        "current_round": 1,
        "max_rounds": 2,
        "startup_idea": state.get("startup_idea"),
        "analyst_output": state.get("analyst_output"),
        "treasury_output": state.get("treasury_output"),
        "scout_output": state.get("scout_output"),
        "critic_output": state.get("critic_output"),
        "swot_analysis": state.get("swot_analysis"),
        "vulnerabilities": [],
        "defenses": [],
        "verdict": None,
        "pivot_required": False,
        "debate_history": []
    }
    debate_final = await debate_graph.ainvoke(debate_initial)
    return {
        "debate_records": debate_final.get("debate_history", []),
        "execution_logs": ["Debate Engine executed successfully."]
    }

async def battle_score_node(state: GraphState):
    return await score_engine.calculate(state)

async def confidence_node(state: GraphState):
    return await confidence_engine.evaluate(state)

async def generate_report_node(state: GraphState):
    return await report_builder.build(state)

# Build Graph
builder = StateGraph(GraphState)

builder.add_node("strategy_commander", commander_node)
builder.add_node("intelligence_scout", scout_node)
builder.add_node("opponent_analyst", analyst_node)
builder.add_node("treasury_advisor", treasury_node)
builder.add_node("swot_gtm", swot_gtm_node)
builder.add_node("critic_agent", critic_node)
builder.add_node("debate_engine", debate_engine_node)
builder.add_node("battle_score", battle_score_node)
builder.add_node("confidence", confidence_node)
builder.add_node("report", generate_report_node)

builder.set_entry_point("strategy_commander")

# Parallel execution: commander -> (scout, analyst, treasury) -> debate
builder.add_edge("strategy_commander", "intelligence_scout")
builder.add_edge("strategy_commander", "opponent_analyst")
builder.add_edge("strategy_commander", "treasury_advisor")

builder.add_edge(["intelligence_scout", "opponent_analyst", "treasury_advisor"], "swot_gtm")
builder.add_edge("swot_gtm", "critic_agent")
builder.add_edge("critic_agent", "debate_engine")

# Linear flow after debate
builder.add_edge("debate_engine", "battle_score")
builder.add_edge("battle_score", "confidence")
builder.add_edge("confidence", "report")
builder.add_edge("report", END)

graph = builder.compile()

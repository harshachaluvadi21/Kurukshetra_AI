import asyncio
from datetime import datetime
from app.graph.debate_state import DebateState
from app.graph.debate_models import Vulnerability, Defense, DebateVerdict, DebateHistoryItem
from app.events.event_bus import event_bus
from app.events.event_types import AppEvent, EventType

async def emit_debate_event(event_type: EventType, run_id: str, speaker: str, message: str):
    event = AppEvent(
        event_type=event_type,
        run_id=run_id,
        timestamp=datetime.utcnow(),
        data={
            "speaker": speaker,
            "message": message
        }
    )
    await event_bus.publish(event)

def _data(output):
    return getattr(output, "data", output)


def _startup_context(state):
    idea = state.get("startup_idea")
    company = getattr(idea, "company_name", None) or "the startup"
    concept = getattr(idea, "business_concept", None) or company
    industry = getattr(idea, "industry", None) or "the market"
    return company, concept, industry

def _names(competitors):
    names = []
    for competitor in competitors or []:
        name = getattr(competitor, "name", None)
        if name:
            names.append(name)
    return names

def _first(items, fallback):
    for item in items or []:
        if item:
            return str(item)
    return fallback

async def skeptic_node(state: DebateState):
    run_id = state.get("run_id", "unknown")
    round_num = state.get("current_round", 1)
    company, concept, industry = _startup_context(state)
    
    if round_num == 1:
        await emit_debate_event(EventType.DEBATE_STARTED, run_id, "System", "Debate Engine Initialized.")
        
    await asyncio.sleep(0.5)
    
    scout = _data(state.get("scout_output"))
    analyst = _data(state.get("analyst_output"))
    treasury = _data(state.get("treasury_output"))
    critic = _data(state.get("critic_output"))
    competitors = _names(getattr(analyst, "direct_competitors", []))
    market_threat = _first(getattr(analyst, "market_threats", []), f"competitive response from better-funded players in {industry}")
    failure_risk = _first(getattr(critic, "failure_risks", []), f"the core operating model for {company} may not scale profitably")
    vuln_msg = (
        f"For {company}, the biggest challenge is {failure_risk}. Market growth around "
        f"{getattr(scout, 'growth_rate', 'unknown')}% is attractive, but competitors such as "
        f"{', '.join(competitors[:3]) or 'key incumbents'} and {market_threat} can pressure margins. "
        f"The plan must prove CAC near ${getattr(treasury, 'estimated_cac', 0):,.0f}, LTV near "
        f"${getattr(treasury, 'estimated_ltv', 0):,.0f}, and break-even within "
        f"{getattr(treasury, 'break_even_months', 'unknown')} months for the {concept} wedge."
    )
    await emit_debate_event(EventType.DEBATE_TURN, run_id, "Skeptic", vuln_msg)
    
    new_vuln = Vulnerability(issue=failure_risk[:80], severity=getattr(critic, "risk_level", "High"))
    history_item = DebateHistoryItem(round_num=round_num, speaker="Skeptic", message=vuln_msg)
    
    return {
        "vulnerabilities": [new_vuln],
        "debate_history": [history_item]
    }

async def proponent_node(state: DebateState):
    run_id = state.get("run_id", "unknown")
    round_num = state.get("current_round", 1)
    company, concept, industry = _startup_context(state)
    
    await asyncio.sleep(0.5)
    
    scout = _data(state.get("scout_output"))
    treasury = _data(state.get("treasury_output"))
    swot = state.get("swot_analysis")
    opportunity = _first(getattr(swot, "opportunities", []), _first(getattr(scout, "trends", []), f"market demand for {concept} is expanding"))
    strength = _first(getattr(swot, "strengths", []), f"{company} has identifiable execution advantages")
    def_msg = (
        f"The defense for {company} is that {strength}. {opportunity} creates room for a focused wedge in {industry}, and the "
        f"{getattr(treasury, 'pricing_model', 'proposed pricing model')} can work if pilots validate repeat usage, "
        f"retention, and contribution margin before scaling acquisition."
    )
    await emit_debate_event(EventType.DEBATE_TURN, run_id, "Proponent", def_msg)
    
    new_def = Defense(counter_argument=def_msg[:120], confidence_level="Medium")
    history_item = DebateHistoryItem(round_num=round_num, speaker="Proponent", message=def_msg)
    
    return {
        "defenses": [new_def],
        "debate_history": [history_item],
        "current_round": round_num + 1
    }

async def judge_node(state: DebateState):
    run_id = state.get("run_id", "unknown")
    round_num = state.get("current_round", 1)
    company, concept, industry = _startup_context(state)
    
    await asyncio.sleep(0.5)
    
    critic = _data(state.get("critic_output"))
    swot = state.get("swot_analysis")
    risk_level = getattr(critic, "risk_level", "Medium")
    mitigation = _first(getattr(critic, "mitigation_recommendations", []), f"validate economics in a narrow pilot for {company} before scaling")
    weakness = _first(getattr(swot, "weaknesses", []), f"execution assumptions for {concept} need more proof")
    verdict_msg = (
        f"The skeptic's strongest point is {weakness}. The idea remains investable only if the team can "
        f"{mitigation}. Current risk level for {company}: {risk_level}. No automatic pivot is required, but scale-up should wait "
        f"until the challenged assumptions are proven."
    )
    await emit_debate_event(EventType.DEBATE_TURN, run_id, "Judge", verdict_msg)
    
    verdict = DebateVerdict(
        winner="Draw",
        confidence=0.75,
        pivot_required=str(risk_level).lower() == "critical",
        summary=verdict_msg
    )
    
    history_item = DebateHistoryItem(round_num=round_num, speaker="Judge", message=verdict_msg)
    
    await emit_debate_event(EventType.DEBATE_COMPLETED, run_id, "System", "Debate Engine Execution Finished.")
    
    return {
        "verdict": verdict,
        "pivot_required": str(risk_level).lower() == "critical",
        "debate_history": [history_item]
    }

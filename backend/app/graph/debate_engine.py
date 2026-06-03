from langgraph.graph import StateGraph, END
from app.graph.debate_state import DebateState
from app.graph.debate_nodes import skeptic_node, proponent_node, judge_node

def should_continue(state: DebateState):
    """Routing logic for maximum rounds limit."""
    current_round = state.get("current_round", 1)
    max_rounds = state.get("max_rounds", 2)
    
    if current_round > max_rounds:
        return END
    return "skeptic"

# Build Debate Subgraph
builder = StateGraph(DebateState)

builder.add_node("skeptic", skeptic_node)
builder.add_node("proponent", proponent_node)
builder.add_node("judge", judge_node)

builder.set_entry_point("skeptic")

builder.add_edge("skeptic", "proponent")
builder.add_edge("proponent", "judge")

# Conditional edge from judge back to skeptic or END based on max_rounds
builder.add_conditional_edges(
    "judge",
    should_continue,
    {
        "skeptic": "skeptic",
        END: END
    }
)

# Compile the debate subgraph
debate_graph = builder.compile()

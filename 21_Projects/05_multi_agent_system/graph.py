"""LangGraph StateGraph definition for the multi-agent research system."""

from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict

try:
    from langgraph.graph import END, StateGraph
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False

from agents import research_node, reviewer_node, writer_node


class ResearchState(TypedDict):
    topic:              str
    research_findings:  Optional[str]
    draft_report:       Optional[str]
    final_report:       Optional[str]
    status:             str
    log:                List[str]


def build_graph():
    """Build and compile the research workflow graph."""
    if not LANGGRAPH_AVAILABLE:
        return None

    graph = StateGraph(ResearchState)
    graph.add_node("research", research_node)
    graph.add_node("writer",   writer_node)
    graph.add_node("reviewer", reviewer_node)

    graph.set_entry_point("research")
    graph.add_edge("research", "writer")
    graph.add_edge("writer",   "reviewer")
    graph.add_edge("reviewer", END)

    return graph.compile()


def run_pipeline(topic: str) -> Dict[str, Any]:
    """Run the full research pipeline, with or without LangGraph."""
    initial_state: ResearchState = {
        "topic":             topic,
        "research_findings": None,
        "draft_report":      None,
        "final_report":      None,
        "status":            "started",
        "log":               [f"🚀 Starting research on: {topic}"],
    }

    compiled = build_graph()
    if compiled:
        result = compiled.invoke(initial_state)
    else:
        # Sequential fallback without LangGraph
        state = initial_state.copy()
        state = research_node(state)
        state = writer_node(state)
        state = reviewer_node(state)
        result = state

    return result

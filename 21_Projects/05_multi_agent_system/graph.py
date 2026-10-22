"""LangGraph StateGraph definition for the multi-agent research system."""

from typing import Any, Callable, Dict, List, Optional
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


def run_pipeline(topic: str, on_log: Optional[Callable[[List[str]], None]] = None) -> Dict[str, Any]:
    """Run the full research pipeline, with or without LangGraph.

    on_log (optional) is called with the activity log after every step, so a caller
    (e.g. the API) can show live progress instead of waiting for the end.
    """
    initial_state: ResearchState = {
        "topic":             topic,
        "research_findings": None,
        "draft_report":      None,
        "final_report":      None,
        "status":            "started",
        "log":               [f"🚀 Starting research on: {topic}"],
    }

    def report(state):
        if on_log:
            on_log(list(state.get("log", [])))

    report(initial_state)
    compiled = build_graph()
    if compiled:
        # stream_mode="values" yields the full state after each node finishes
        result = initial_state
        for state in compiled.stream(initial_state, stream_mode="values"):
            result = state
            report(state)
    else:
        # Sequential fallback without LangGraph
        state = initial_state.copy()
        for node in (research_node, writer_node, reviewer_node):
            state = node(state)
            report(state)
        result = state

    return result

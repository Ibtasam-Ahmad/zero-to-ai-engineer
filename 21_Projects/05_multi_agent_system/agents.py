"""Agent definitions for the multi-agent research system."""

import os
from typing import Any, Dict, List

RESEARCH_SYSTEM = """You are a Research Agent. Your job is to search the web for information on a given topic and return a structured summary with key facts, statistics, and relevant quotes. Be thorough and cite your sources."""

WRITER_SYSTEM = """You are a Writer Agent. Given research findings, write a clear, well-structured report with:
- Executive Summary
- Key Findings (bullet points with evidence)
- Detailed Analysis (2-3 paragraphs)
- Conclusions

Use markdown formatting."""

REVIEWER_SYSTEM = """You are a Reviewer Agent. Given a draft report:
1. Check for accuracy and completeness
2. Identify gaps or unsupported claims
3. Suggest improvements
4. Return the improved final report

Be constructive and thorough."""


# Model name in one place. Check the provider's current model list; override with
# the OPENAI_MODEL environment variable instead of editing code.
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def get_llm(model: str = DEFAULT_MODEL):
    """Return a LangChain ChatOpenAI instance if available."""
    try:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=model, temperature=0.3)
    except Exception:  # not only ImportError: a missing OPENAI_API_KEY raises openai.OpenAIError
        return None


class _DDGSSearch:
    """Keyless DuckDuckGo search via the `ddgs` package, with the same .invoke(query) API."""

    def __init__(self, max_results: int = 5):
        from ddgs import DDGS  # raises ImportError if ddgs isn't installed
        self._ddgs = DDGS
        self.max_results = max_results

    def invoke(self, query: str) -> str:
        hits = self._ddgs().text(query, max_results=self.max_results)
        return "\n".join(f"- {h.get('title')}: {h.get('body')} ({h.get('href')})"
                         for h in hits if h.get("title") or h.get("body"))


def get_search_tool():
    """Return Tavily search tool, falling back to DuckDuckGo."""
    try:
        from langchain_community.tools.tavily_search import TavilySearchResults
        return TavilySearchResults(max_results=5)
    except Exception:
        pass
    try:
        return _DDGSSearch(max_results=5)
    except Exception:
        return None


def research_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """ResearchAgent: searches web and returns findings."""
    topic = state["topic"]
    llm = get_llm()
    search = get_search_tool()

    if search:
        try:
            results = search.invoke(topic)
            raw = str(results)
        except Exception as e:
            # e.g. DuckDuckGo rate limits: say so clearly instead of failing silently
            raw = (f"Web search failed for: {topic} ({type(e).__name__}: {str(e)[:150]}). "
                   "Try again later, or set TAVILY_API_KEY for a more reliable search.")
    else:
        raw = f"No search tool available (pip install ddgs, or set TAVILY_API_KEY). Topic: {topic}"

    if llm:
        from langchain_core.messages import HumanMessage, SystemMessage
        resp = llm.invoke([
            SystemMessage(content=RESEARCH_SYSTEM),
            HumanMessage(content=f"Summarize research findings for: {topic}\n\nRaw data:\n{raw[:3000]}"),
        ])
        findings = resp.content
    else:
        findings = f"Research findings for '{topic}':\n{raw[:2000]}\n\n(LLM unavailable install langchain_openai and set OPENAI_API_KEY)"

    return {**state, "research_findings": findings, "status": "research_done",
            "log": state.get("log", []) + [f"✅ Research complete for: {topic}"]}


def writer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """WriterAgent: drafts report from research findings."""
    llm = get_llm()
    findings = state.get("research_findings", "No findings available.")

    if llm:
        from langchain_core.messages import HumanMessage, SystemMessage
        resp = llm.invoke([
            SystemMessage(content=WRITER_SYSTEM),
            HumanMessage(content=f"Write a report based on:\n\n{findings}"),
        ])
        draft = resp.content
    else:
        draft = f"# Report: {state['topic']}\n\n## Summary\n\n{findings}\n\n*(LLM unavailable)*"

    return {**state, "draft_report": draft, "status": "draft_done",
            "log": state.get("log", []) + ["✅ Draft report written"]}


def reviewer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """ReviewerAgent: reviews and improves the draft."""
    llm = get_llm()
    draft = state.get("draft_report", "No draft available.")

    if llm:
        from langchain_core.messages import HumanMessage, SystemMessage
        resp = llm.invoke([
            SystemMessage(content=REVIEWER_SYSTEM),
            HumanMessage(content=f"Review and improve this report:\n\n{draft}"),
        ])
        final = resp.content
    else:
        final = draft + "\n\n---\n*Reviewed: No changes (LLM unavailable)*"

    return {**state, "final_report": final, "status": "complete",
            "log": state.get("log", []) + ["✅ Report reviewed and finalized"]}

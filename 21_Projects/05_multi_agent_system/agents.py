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


def get_llm(model: str = "gpt-4o-mini"):
    """Return a LangChain ChatOpenAI instance if available."""
    try:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=model, temperature=0.3)
    except ImportError:
        return None


def get_search_tool():
    """Return Tavily search tool, falling back to DuckDuckGo."""
    try:
        from langchain_community.tools.tavily_search import TavilySearchResults
        return TavilySearchResults(max_results=5)
    except Exception:
        pass
    try:
        from langchain_community.tools import DuckDuckGoSearchRun
        return DuckDuckGoSearchRun()
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
        except Exception:
            raw = f"Search unavailable for: {topic}"
    else:
        raw = f"No search tool available. Topic: {topic}"

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

"""
Research Agent LangGraph + DuckDuckGo (no API key required)
Requirements: langgraph langchain langchain-community duckduckgo-search openai
Usage:
  python 01_research_agent.py --topic "quantum computing breakthroughs 2024" --depth 3
  python 01_research_agent.py --topic "climate change solutions" --output report.md
"""

import argparse
import os
from datetime import datetime
from pathlib import Path
from typing import Annotated, List, TypedDict

# ── State ─────────────────────────────────────────────────────────────────────

class ResearchState(TypedDict):
    topic: str
    depth: int
    search_results: List[dict]
    summaries: List[str]
    report: str
    current_step: str

# ── Tools ─────────────────────────────────────────────────────────────────────

def web_search(query: str, max_results: int = 5) -> List[dict]:
    """Search using DuckDuckGo (no API key needed)."""
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return [{"title": r.get("title", ""), "body": r.get("body", ""), "href": r.get("href", "")} for r in results]
    except ImportError:
        print("  duckduckgo-search not installed. Using mock results.")
        return _mock_search(query)
    except Exception as e:
        print(f"  Search error: {e}. Using mock results.")
        return _mock_search(query)

def _mock_search(query: str) -> List[dict]:
    """Fallback mock search results."""
    return [
        {"title": f"Overview of {query}", "body": f"{query} is a rapidly evolving field with many recent developments. Researchers have made significant breakthroughs in understanding core principles and practical applications.", "href": "https://example.com/1"},
        {"title": f"Latest advances in {query}", "body": f"Recent studies on {query} show promising results. Key findings include improved efficiency, novel approaches, and broader applicability across domains.", "href": "https://example.com/2"},
        {"title": f"Future of {query}", "body": f"Experts predict {query} will continue to grow in importance. Challenges remain in scaling and deployment, but the outlook is optimistic.", "href": "https://example.com/3"},
    ]

def call_llm(prompt: str) -> str:
    """Call LLM tries OpenAI, then Ollama, then returns structured mock."""
    # Try OpenAI
    if os.environ.get("OPENAI_API_KEY"):
        try:
            import openai
            client = openai.OpenAI()
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"  OpenAI error: {e}")

    # Try Ollama
    try:
        import requests
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2", "prompt": prompt, "stream": False},
            timeout=60,
        )
        if resp.ok:
            return resp.json().get("response", "")
    except Exception:
        pass

    # Mock
    return f"[Mock LLM] Based on the provided context about '{prompt[:50]}...', here is a structured analysis: The topic presents several key aspects worth examining. First, the foundational concepts provide important context. Second, recent developments highlight emerging trends. Third, practical applications demonstrate real-world value."

# ── Agent nodes ───────────────────────────────────────────────────────────────

def search_node(state: ResearchState) -> ResearchState:
    """Search for information on the topic."""
    print(f"\n🔍 Searching: '{state['topic']}' (depth={state['depth']})")
    all_results = []

    # Generate sub-queries for depth
    queries = [state["topic"]]
    if state["depth"] >= 2:
        queries.append(f"{state['topic']} latest research 2024")
    if state["depth"] >= 3:
        queries.append(f"{state['topic']} applications examples")

    for q in queries:
        print(f"  Query: {q}")
        results = web_search(q, max_results=3)
        all_results.extend(results)
        print(f"  Found {len(results)} results")

    return {**state, "search_results": all_results, "current_step": "summarize"}

def summarize_node(state: ResearchState) -> ResearchState:
    """Summarize each search result."""
    print(f"\n📝 Summarizing {len(state['search_results'])} results...")
    summaries = []

    for i, result in enumerate(state["search_results"][:6]):  # Cap at 6
        print(f"  Summarizing result {i+1}...")
        prompt = f"""Summarize this search result in 2-3 sentences, extracting the key facts:

Title: {result['title']}
Content: {result['body']}

Summary:"""
        summary = call_llm(prompt)
        summaries.append(f"**{result['title']}**\n{summary}\nSource: {result['href']}")

    return {**state, "summaries": summaries, "current_step": "write"}

def write_node(state: ResearchState) -> ResearchState:
    """Write a structured research report."""
    print(f"\n✍️  Writing report on: {state['topic']}")

    context = "\n\n".join(state["summaries"])
    prompt = f"""Write a comprehensive research report on the topic: "{state['topic']}"

Based on these research findings:
{context}

Structure your report with:
1. Executive Summary (2-3 sentences)
2. Key Findings (bullet points)
3. Detailed Analysis (3-4 paragraphs)
4. Conclusions & Future Outlook

Be specific, factual, and cite sources where mentioned."""

    report = call_llm(prompt)

    # Add metadata header
    header = f"""# Research Report: {state['topic']}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Search Depth: {state['depth']} | Sources: {len(state['search_results'])}
{'='*60}

"""
    full_report = header + report

    return {**state, "report": full_report, "current_step": "done"}

# ── Graph ─────────────────────────────────────────────────────────────────────

def build_graph():
    try:
        from langgraph.graph import StateGraph, END

        graph = StateGraph(ResearchState)
        graph.add_node("search", search_node)
        graph.add_node("summarize", summarize_node)
        graph.add_node("write", write_node)

        graph.set_entry_point("search")
        graph.add_edge("search", "summarize")
        graph.add_edge("summarize", "write")
        graph.add_edge("write", END)

        return graph.compile()
    except ImportError:
        return None

def run_pipeline(topic: str, depth: int) -> str:
    """Run research pipeline with LangGraph if available, else sequential."""
    initial_state = ResearchState(
        topic=topic,
        depth=depth,
        search_results=[],
        summaries=[],
        report="",
        current_step="search",
    )

    graph = build_graph()
    if graph:
        print("Using LangGraph pipeline...")
        final_state = graph.invoke(initial_state)
    else:
        print("LangGraph not available, running sequentially...")
        state = search_node(initial_state)
        state = summarize_node(state)
        final_state = write_node(state)

    return final_state["report"]

# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Research Agent")
    parser.add_argument("--topic", required=True, help="Research topic")
    parser.add_argument("--depth", type=int, default=2, choices=[1, 2, 3],
                        help="Search depth (1=quick, 2=standard, 3=deep)")
    parser.add_argument("--output", type=str, help="Save report to file (.md)")
    args = parser.parse_args()

    print(f"Research Agent Topic: '{args.topic}'")
    report = run_pipeline(args.topic, args.depth)

    print(f"\n{'='*60}")
    print(report)

    # Save to file
    output_path = args.output or f"report_{args.topic[:30].replace(' ', '_')}.md"
    Path(output_path).write_text(report, encoding="utf-8")
    print(f"\nReport saved to: {output_path}")

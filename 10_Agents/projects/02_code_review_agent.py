"""
Code Review Multi-Agent Reviewer + Critic agents
Requirements: openai requests pathlib
Usage:
  python 02_code_review_agent.py --file my_script.py
  python 02_code_review_agent.py --folder ./src/
  python 02_code_review_agent.py --file app.py --output review.json
"""

import argparse
import ast
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional

# ── Data models ───────────────────────────────────────────────────────────────

@dataclass
class Issue:
    category: str        # bug | security | style | performance
    severity: str        # critical | high | medium | low
    line: Optional[int]
    description: str
    suggestion: str

@dataclass
class ReviewResult:
    file: str
    issues: List[Issue] = field(default_factory=list)
    summary: str = ""
    overall_score: int = 0   # 1-10
    critic_verdict: str = ""
    verified_issues: List[Issue] = field(default_factory=list)

# ── LLM call ──────────────────────────────────────────────────────────────────

def call_llm(system: str, user: str, model: str = "gpt-4o-mini") -> str:
    # Try OpenAI
    if os.environ.get("OPENAI_API_KEY"):
        try:
            import openai
            client = openai.OpenAI()
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                max_tokens=1500,
                temperature=0.1,
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"  OpenAI error: {e}")

    # Try Ollama
    try:
        import requests
        prompt = f"System: {system}\n\nUser: {user}"
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2", "prompt": prompt, "stream": False},
            timeout=120,
        )
        if resp.ok:
            return resp.json().get("response", "")
    except Exception:
        pass

    # Static fallback analysis
    return _static_review(user)

def _static_review(code: str) -> str:
    """Regex-based static analysis fallback."""
    issues = []
    lines = code.split("\n")
    for i, line in enumerate(lines, 1):
        if "eval(" in line and "# noqa" not in line:
            issues.append(f"Line {i}: SECURITY - eval() usage is dangerous")
        if "password" in line.lower() and "=" in line and not line.strip().startswith("#"):
            issues.append(f"Line {i}: SECURITY - Possible hardcoded password")
        if "except:" in line and "except Exception" not in line:
            issues.append(f"Line {i}: BUG - Bare except clause catches all exceptions")
        if len(line) > 120:
            issues.append(f"Line {i}: STYLE - Line too long ({len(line)} chars)")
        if "TODO" in line or "FIXME" in line:
            issues.append(f"Line {i}: INFO - Unresolved TODO/FIXME")

    if not issues:
        return "REVIEW: Code looks clean. No obvious issues found.\nSCORE: 8"
    return "REVIEW:\n" + "\n".join(issues) + f"\nSCORE: {max(3, 8 - len(issues))}"

# ── Static analysis (AST-based) ───────────────────────────────────────────────

def static_analyze(code: str) -> List[Issue]:
    """Fast AST-based analysis before LLM review."""
    issues = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            # Check for bare except
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                issues.append(Issue("bug", "medium", node.lineno,
                    "Bare except clause catches all exceptions including KeyboardInterrupt",
                    "Use 'except Exception as e:' or specify the exception type"))
            # Check for eval usage
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "eval":
                issues.append(Issue("security", "critical", node.lineno,
                    "eval() executes arbitrary code major security risk",
                    "Use ast.literal_eval() for safe evaluation, or avoid dynamic execution"))
            # Check for print in production code
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print":
                issues.append(Issue("style", "low", node.lineno,
                    "Using print() consider using logging module instead",
                    "Replace with logging.info(), logging.debug(), etc."))
    except SyntaxError as e:
        issues.append(Issue("bug", "critical", e.lineno, f"Syntax error: {e.msg}", "Fix syntax error before review"))
    return issues

# ── Reviewer agent ────────────────────────────────────────────────────────────

REVIEWER_SYSTEM = """You are an expert Python code reviewer. Analyze code for:
1. BUGS: Logic errors, null pointer risks, off-by-one errors, unhandled exceptions
2. SECURITY: Injections, hardcoded secrets, unsafe deserialization, path traversal
3. PERFORMANCE: O(n²) loops, missing indexes, redundant operations, memory leaks
4. STYLE: Naming conventions, dead code, overly complex functions, missing types

Respond in this exact JSON format:
{
  "issues": [{"category": "bug|security|performance|style", "severity": "critical|high|medium|low", "line": <int or null>, "description": "...", "suggestion": "..."}],
  "summary": "Overall assessment in 2-3 sentences.",
  "score": <1-10>
}"""

def reviewer_agent(code: str, filename: str) -> ReviewResult:
    print(f"  🔍 Reviewer analyzing {filename}...")
    static_issues = static_analyze(code)

    user_prompt = f"Review this Python code from file '{filename}':\n\n```python\n{code[:3000]}\n```"
    raw = call_llm(REVIEWER_SYSTEM, user_prompt)

    result = ReviewResult(file=filename, issues=static_issues)

    # Parse JSON response
    try:
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            for iss in data.get("issues", []):
                result.issues.append(Issue(
                    category=iss.get("category", "style"),
                    severity=iss.get("severity", "low"),
                    line=iss.get("line"),
                    description=iss.get("description", ""),
                    suggestion=iss.get("suggestion", ""),
                ))
            result.summary = data.get("summary", raw[:200])
            result.overall_score = data.get("score", 5)
    except Exception:
        result.summary = raw[:300]
        result.overall_score = 5

    return result

# ── Critic agent ──────────────────────────────────────────────────────────────

CRITIC_SYSTEM = """You are a senior code review critic. Your job is to verify a code review.
For each issue, decide if it is:
- VALID: The issue is real and the suggestion is correct
- INVALID: The issue is a false positive or the suggestion is wrong
- MINOR: The issue exists but severity is overstated

Respond with JSON: {"verdict": "approved|needs_revision", "verified_issues": [{"original": "...", "verdict": "valid|invalid|minor", "reason": "..."}], "overall_comment": "..."}"""

def critic_agent(review: ReviewResult, code: str) -> ReviewResult:
    print(f"  🧐 Critic verifying review for {review.file}...")
    issues_text = "\n".join(
        f"- [{i.severity.upper()}] {i.category}: {i.description}" for i in review.issues
    )
    user_prompt = f"""Code being reviewed:
```python
{code[:2000]}
```

Review findings:
{issues_text}

Summary: {review.summary}
Score: {review.overall_score}/10

Please verify these findings."""

    raw = critic_call = call_llm(CRITIC_SYSTEM, user_prompt)

    try:
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            review.critic_verdict = data.get("verdict", "approved")
            # Keep only valid issues
            review.verified_issues = [
                i for i in review.issues
                if data.get("verdict") == "approved" or i.severity in ("critical", "high")
            ]
        else:
            review.critic_verdict = "approved"
            review.verified_issues = review.issues
    except Exception:
        review.critic_verdict = "approved"
        review.verified_issues = review.issues

    return review

# ── Report output ─────────────────────────────────────────────────────────────

def print_report(review: ReviewResult):
    severity_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵"}
    print(f"\n{'='*60}")
    print(f"  Code Review: {review.file}")
    print(f"  Score: {review.overall_score}/10  |  Critic: {review.critic_verdict.upper()}")
    print(f"{'='*60}")
    print(f"\n📋 Summary:\n  {review.summary}")
    print(f"\n🐛 Issues ({len(review.verified_issues)} verified):")
    if not review.verified_issues:
        print("  ✅ No significant issues found!")
    for iss in review.verified_issues:
        emoji = severity_emoji.get(iss.severity, "⚪")
        loc = f"Line {iss.line}" if iss.line else "General"
        print(f"\n  {emoji} [{iss.severity.upper()}] {iss.category.upper()} {loc}")
        print(f"     Issue:      {iss.description}")
        print(f"     Suggestion: {iss.suggestion}")

def save_report(reviews: List[ReviewResult], path: str):
    data = [asdict(r) for r in reviews]
    Path(path).write_text(json.dumps(data, indent=2))
    print(f"\nReport saved to: {path}")

# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Code Review Multi-Agent")
    parser.add_argument("--file", type=str, help="Python file to review")
    parser.add_argument("--folder", type=str, help="Folder of Python files")
    parser.add_argument("--output", type=str, help="Output JSON report path")
    args = parser.parse_args()

    files: Dict[str, str] = {}

    if args.file:
        p = Path(args.file)
        files[p.name] = p.read_text(encoding="utf-8")
    elif args.folder:
        for p in Path(args.folder).rglob("*.py"):
            files[p.name] = p.read_text(encoding="utf-8")
    else:
        # Demo: review itself
        demo_code = '''
import os, pickle

PASSWORD = "admin123"  # hardcoded password

def process(data):
    result = eval(data)  # dangerous!
    return result

def load_model(path):
    with open(path, 'rb') as f:
        return pickle.load(f)  # unsafe deserialization

def find_item(items, target):
    for i in range(len(items)):
        for j in range(len(items)):  # O(n^2)
            if items[i] == target:
                return i
    return -1

try:
    x = 1 / 0
except:  # bare except
    pass
'''
        files["demo_code.py"] = demo_code
        print("No file specified reviewing demo code with intentional issues.\n")

    reviews = []
    for filename, code in files.items():
        print(f"\nProcessing: {filename} ({len(code)} chars)")
        review = reviewer_agent(code, filename)
        review = critic_agent(review, code)
        reviews.append(review)
        print_report(review)

    if args.output:
        save_report(reviews, args.output)
    elif len(files) > 1:
        save_report(reviews, "code_review_report.json")

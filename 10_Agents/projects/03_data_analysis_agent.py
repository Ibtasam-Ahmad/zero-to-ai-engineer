"""
Data Analysis Agent ReAct loop with pandas + matplotlib tools
Requirements: pandas matplotlib seaborn openai requests
Usage:
  python 03_data_analysis_agent.py --csv data.csv
  python 03_data_analysis_agent.py --csv data.csv --question "What are the top 5 correlations?"
  python 03_data_analysis_agent.py --generate-sample  # creates sample_data.csv
"""

import argparse
import io
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

# ── Tool registry ─────────────────────────────────────────────────────────────

TOOLS = {}

def tool(name: str, description: str):
    """Decorator to register a tool."""
    def decorator(fn):
        TOOLS[name] = {"fn": fn, "description": description}
        return fn
    return decorator

# ── Analysis tools ────────────────────────────────────────────────────────────

@tool("describe", "Get statistical summary: count, mean, std, min, max for all numeric columns")
def tool_describe(df: pd.DataFrame, columns: str = "all") -> str:
    if columns == "all":
        return df.describe().to_string()
    cols = [c.strip() for c in columns.split(",")]
    return df[cols].describe().to_string()

@tool("head", "Show first N rows of the dataset")
def tool_head(df: pd.DataFrame, n: int = 5) -> str:
    return df.head(n).to_string()

@tool("info", "Show column names, dtypes, and null counts")
def tool_info(df: pd.DataFrame) -> str:
    buffer = io.StringIO()
    df.info(buf=buffer)
    null_counts = df.isnull().sum()
    return buffer.getvalue() + f"\n\nNull counts:\n{null_counts.to_string()}"

@tool("correlations", "Compute Pearson correlation matrix for numeric columns, show top N pairs")
def tool_correlations(df: pd.DataFrame, top_n: int = 10) -> str:
    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        return "No numeric columns found."
    corr = numeric.corr()
    pairs = []
    cols = corr.columns.tolist()
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            pairs.append((abs(corr.iloc[i, j]), cols[i], cols[j], corr.iloc[i, j]))
    pairs.sort(reverse=True)
    lines = [f"{a:<25} <-> {b:<25} : {r:+.3f}" for _, a, b, r in pairs[:top_n]]
    return "Top correlations:\n" + "\n".join(lines)

@tool("value_counts", "Show value counts for a categorical column")
def tool_value_counts(df: pd.DataFrame, column: str) -> str:
    if column not in df.columns:
        return f"Column '{column}' not found. Available: {', '.join(df.columns)}"
    return df[column].value_counts().head(20).to_string()

@tool("filter_stats", "Get stats for rows matching a simple condition (e.g. 'age > 30')")
def tool_filter_stats(df: pd.DataFrame, condition: str) -> str:
    try:
        filtered = df.query(condition)
        n = len(filtered)
        pct = n / len(df) * 100
        return f"Rows matching '{condition}': {n} ({pct:.1f}%)\n{filtered.describe().to_string()}"
    except Exception as e:
        return f"Filter error: {e}"

@tool("plot_histogram", "Plot histogram for a numeric column and save as PNG")
def tool_plot_histogram(df: pd.DataFrame, column: str, output: str = "histogram.png") -> str:
    try:
        import matplotlib.pyplot as plt
        if column not in df.columns:
            return f"Column '{column}' not found."
        fig, ax = plt.subplots(figsize=(8, 4))
        df[column].dropna().hist(ax=ax, bins=30, edgecolor="black", alpha=0.7)
        ax.set_title(f"Distribution of {column}")
        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(output, dpi=100)
        plt.close()
        return f"Histogram saved to {output}"
    except Exception as e:
        return f"Plot error: {e}"

@tool("plot_correlation_heatmap", "Plot correlation heatmap and save as PNG")
def tool_plot_heatmap(df: pd.DataFrame, output: str = "correlation_heatmap.png") -> str:
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        numeric = df.select_dtypes(include="number")
        if numeric.empty:
            return "No numeric columns for heatmap."
        corr = numeric.corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax, center=0)
        ax.set_title("Correlation Heatmap")
        plt.tight_layout()
        plt.savefig(output, dpi=100)
        plt.close()
        return f"Heatmap saved to {output}"
    except Exception as e:
        return f"Heatmap error: {e}"

@tool("missing_analysis", "Analyze missing values: count, percentage, patterns")
def tool_missing(df: pd.DataFrame) -> str:
    missing = df.isnull().sum()
    pct = (missing / len(df) * 100).round(2)
    result = pd.DataFrame({"count": missing, "pct": pct})
    result = result[result["count"] > 0].sort_values("count", ascending=False)
    if result.empty:
        return "No missing values found!"
    return f"Missing value analysis:\n{result.to_string()}"

@tool("outlier_detection", "Detect outliers using IQR method for a numeric column")
def tool_outliers(df: pd.DataFrame, column: str) -> str:
    if column not in df.columns:
        return f"Column '{column}' not found."
    col = df[column].dropna()
    Q1, Q3 = col.quantile(0.25), col.quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    outliers = col[(col < lower) | (col > upper)]
    return (f"IQR outlier detection for '{column}':\n"
            f"  Q1={Q1:.2f}, Q3={Q3:.2f}, IQR={IQR:.2f}\n"
            f"  Lower fence: {lower:.2f}, Upper fence: {upper:.2f}\n"
            f"  Outliers: {len(outliers)} ({len(outliers)/len(col)*100:.1f}%)\n"
            f"  Outlier values (sample): {outliers.head(10).tolist()}")

# ── LLM decision-making ───────────────────────────────────────────────────────

TOOL_LIST = "\n".join(f"- {name}: {info['description']}" for name, info in TOOLS.items())

SYSTEM_PROMPT = f"""You are a data analysis agent. You have access to these tools:
{TOOL_LIST}

Respond in JSON format:
{{"thought": "your reasoning", "action": "tool_name", "action_input": {{"param": "value"}}, "final": false}}

When you have enough information to answer, set "final": true and add "answer": "your complete analysis".
Parameters: columns (comma-separated string), n (integer), column (string), condition (string), output (string).
Always start by calling 'info' and 'describe' to understand the dataset."""

def decide_action(question: str, history: List[dict], df_summary: str) -> dict:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Dataset summary:\n{df_summary}\n\nQuestion: {question}\n\nAnalysis so far:\n" + json.dumps(history, indent=2)},
    ]

    # Try OpenAI
    if os.environ.get("OPENAI_API_KEY"):
        try:
            import openai
            client = openai.OpenAI()
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=600,
                response_format={"type": "json_object"},
            )
            return json.loads(resp.choices[0].message.content)
        except Exception as e:
            print(f"  LLM error: {e}")

    # Try Ollama
    try:
        import requests
        prompt = f"{SYSTEM_PROMPT}\n\nDataset:\n{df_summary}\nQuestion: {question}\nHistory: {json.dumps(history)}\nRespond in JSON:"
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2", "prompt": prompt, "stream": False, "format": "json"},
            timeout=60,
        )
        if resp.ok:
            return json.loads(resp.json().get("response", "{}"))
    except Exception:
        pass

    # Hardcoded fallback sequence
    step = len(history)
    fallback_steps = [
        {"thought": "First, let me understand the dataset structure.", "action": "info", "action_input": {}, "final": False},
        {"thought": "Now let me get statistical summaries.", "action": "describe", "action_input": {"columns": "all"}, "final": False},
        {"thought": "Check for correlations.", "action": "correlations", "action_input": {"top_n": 5}, "final": False},
        {"thought": "Check missing values.", "action": "missing_analysis", "action_input": {}, "final": False},
        {"thought": "I have enough information.", "action": "none", "action_input": {}, "final": True,
         "answer": "Analysis complete. See the tool outputs above for detailed statistics, correlations, and missing value analysis."},
    ]
    return fallback_steps[min(step, len(fallback_steps) - 1)]

# ── ReAct loop ────────────────────────────────────────────────────────────────

def run_agent(df: pd.DataFrame, question: str, max_steps: int = 8) -> str:
    df_summary = f"Shape: {df.shape}\nColumns: {', '.join(df.columns)}\nDtypes:\n{df.dtypes.to_string()}"
    history = []
    print(f"\nQuestion: {question}")
    print(f"{'─'*60}")

    for step in range(max_steps):
        decision = decide_action(question, history, df_summary)

        thought = decision.get("thought", "")
        action = decision.get("action", "")
        action_input = decision.get("action_input", {})
        is_final = decision.get("final", False)

        print(f"\nStep {step+1} | Thought: {thought}")

        if is_final:
            answer = decision.get("answer", "Analysis complete based on the gathered data.")
            print(f"\nFINAL ANSWER:\n{answer}")
            return answer

        if action in TOOLS:
            print(f"  Action: {action}({action_input})")
            try:
                result = TOOLS[action]["fn"](df, **action_input)
                print(f"  Result:\n{result[:500]}{'...' if len(str(result)) > 500 else ''}")
            except Exception as e:
                result = f"Tool error: {e}"
                print(f"  Error: {e}")
            history.append({"step": step + 1, "thought": thought, "action": action, "result": str(result)[:500]})
        else:
            history.append({"step": step + 1, "thought": thought, "action": action, "result": "skipped"})

    return "Max steps reached. Analysis based on gathered data: " + json.dumps(history, indent=2)[:500]

# ── Sample data generator ─────────────────────────────────────────────────────

def generate_sample_data(path: str = "sample_data.csv"):
    import random
    rows = []
    for i in range(200):
        age = random.randint(18, 65)
        income = age * 1500 + random.randint(-10000, 30000)
        score = min(850, max(300, 400 + income // 1000 + random.randint(-50, 100)))
        dept = random.choice(["Engineering", "Sales", "Marketing", "HR", "Finance"])
        churn = 1 if income < 40000 and random.random() > 0.7 else 0
        rows.append({
            "age": age, "income": income, "credit_score": score,
            "department": dept, "churn": churn,
            "tenure_years": random.randint(0, 20),
            "satisfaction": random.randint(1, 10),
        })
    df = pd.DataFrame(rows)
    # Add some missing values
    import numpy as np
    df.loc[df.sample(10).index, "income"] = np.nan
    df.loc[df.sample(5).index, "satisfaction"] = np.nan
    df.to_csv(path, index=False)
    print(f"Sample data saved to {path} ({len(df)} rows, {len(df.columns)} columns)")

# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data Analysis Agent")
    parser.add_argument("--csv", type=str, help="CSV file to analyze")
    parser.add_argument("--question", type=str, default="Give me a comprehensive analysis of this dataset including key statistics, correlations, and any notable patterns.")
    parser.add_argument("--generate-sample", action="store_true", help="Generate sample CSV")
    args = parser.parse_args()

    if args.generate_sample:
        generate_sample_data("sample_data.csv")
        sys.exit(0)

    if not args.csv:
        print("Usage: python 03_data_analysis_agent.py --csv data.csv")
        print("       python 03_data_analysis_agent.py --generate-sample")
        sys.exit(1)

    df = pd.read_csv(args.csv)
    print(f"Loaded {args.csv}: {df.shape[0]} rows × {df.shape[1]} columns")
    run_agent(df, args.question)

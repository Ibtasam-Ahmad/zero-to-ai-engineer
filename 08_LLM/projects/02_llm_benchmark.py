"""
LLM Benchmark Tool Compare GPT-4o-mini, Claude Haiku, Ollama
Requirements: openai anthropic requests pandas tabulate
Usage:
  python 02_llm_benchmark.py
  python 02_llm_benchmark.py --models openai anthropic --output results.csv
  python 02_llm_benchmark.py --models ollama --ollama-model llama3.2
"""

import argparse
import csv
import os
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

# ── Task definitions ──────────────────────────────────────────────────────────

TASKS = [
    {
        "id": "reasoning",
        "name": "Logical Reasoning",
        "prompt": "If all bloops are razzies and all razzies are lazzies, are all bloops definitely lazzies? Explain your reasoning step by step.",
        "ideal_keywords": ["yes", "lazzies", "transitive"],
    },
    {
        "id": "math",
        "name": "Math Problem",
        "prompt": "A train travels at 60 mph for 2.5 hours, then at 80 mph for 1.5 hours. What is the total distance? Show your work.",
        "ideal_keywords": ["270", "miles", "150", "120"],
    },
    {
        "id": "coding",
        "name": "Code Generation",
        "prompt": "Write a Python function that finds all prime numbers up to n using the Sieve of Eratosthenes. Include a docstring and example usage.",
        "ideal_keywords": ["def", "sieve", "prime", "return"],
    },
    {
        "id": "summarization",
        "name": "Text Summarization",
        "prompt": "Summarize in 2-3 sentences: The transformer architecture, introduced in 2017, revolutionized NLP by replacing recurrent networks with self-attention mechanisms. It enables parallel processing of sequences and captures long-range dependencies. Models like BERT, GPT, and T5 are all based on transformers and have achieved state-of-the-art results across many NLP benchmarks.",
        "ideal_keywords": ["transformer", "attention", "2017", "nlp"],
    },
    {
        "id": "factual",
        "name": "Factual Knowledge",
        "prompt": "What is the capital of Australia, and what is the country's approximate population as of 2024?",
        "ideal_keywords": ["canberra", "australia", "million"],
    },
]

# ── LLM clients ───────────────────────────────────────────────────────────────

@dataclass
class BenchmarkResult:
    model: str
    task_id: str
    task_name: str
    response: str
    latency_ms: float
    input_tokens: int
    output_tokens: int
    cost_usd: float
    quality_score: float  # 0-1 based on keyword matching
    error: str = ""

# Approximate pricing per 1M tokens (input/output)
PRICING = {
    "gpt-4o-mini":       (0.15,  0.60),
    "claude-haiku-3":    (0.25,  1.25),
    "ollama":            (0.0,   0.0),
}

def call_openai(prompt: str, model: str = "gpt-4o-mini") -> dict:
    import openai
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    t0 = time.time()
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
    )
    latency = (time.time() - t0) * 1000
    return {
        "text": resp.choices[0].message.content,
        "latency_ms": latency,
        "input_tokens": resp.usage.prompt_tokens,
        "output_tokens": resp.usage.completion_tokens,
    }

def call_anthropic(prompt: str, model: str = "claude-haiku-4-5-20251001") -> dict:
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
    t0 = time.time()
    msg = client.messages.create(
        model=model,
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    latency = (time.time() - t0) * 1000
    return {
        "text": msg.content[0].text,
        "latency_ms": latency,
        "input_tokens": msg.usage.input_tokens,
        "output_tokens": msg.usage.output_tokens,
    }

def call_ollama(prompt: str, model: str = "llama3.2") -> dict:
    import requests
    t0 = time.time()
    try:
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()
        latency = (time.time() - t0) * 1000
        text = data.get("response", "")
        # Ollama reports tokens in eval_count
        out_tokens = data.get("eval_count", len(text.split()))
        return {"text": text, "latency_ms": latency, "input_tokens": 0, "output_tokens": out_tokens}
    except Exception as e:
        return {"text": "", "latency_ms": 0, "input_tokens": 0, "output_tokens": 0, "error": str(e)}

# ── Quality scoring ───────────────────────────────────────────────────────────

def quality_score(response: str, ideal_keywords: List[str]) -> float:
    """Simple keyword-based quality check (0–1)."""
    if not response:
        return 0.0
    response_lower = response.lower()
    hits = sum(1 for kw in ideal_keywords if kw.lower() in response_lower)
    return round(hits / len(ideal_keywords), 2) if ideal_keywords else 0.5

def estimate_cost(model_key: str, in_tokens: int, out_tokens: int) -> float:
    prices = PRICING.get(model_key, (0, 0))
    return round((in_tokens * prices[0] + out_tokens * prices[1]) / 1_000_000, 6)

# ── Benchmark runner ──────────────────────────────────────────────────────────

def run_benchmark(models_to_test: List[str], ollama_model: str = "llama3.2") -> List[BenchmarkResult]:
    results = []

    model_fns = {
        "openai":    ("gpt-4o-mini",        call_openai),
        "anthropic": ("claude-haiku-3",     call_anthropic),
        "ollama":    (ollama_model,          call_ollama),
    }

    for model_key in models_to_test:
        if model_key not in model_fns:
            print(f"Unknown model: {model_key}, skipping.")
            continue
        model_name, fn = model_fns[model_key]
        print(f"\nBenchmarking: {model_name}")

        for task in TASKS:
            print(f"  Task: {task['name']}...", end=" ", flush=True)
            try:
                data = fn(task["prompt"])
                error = data.get("error", "")
                text = data.get("text", "")
                latency = data.get("latency_ms", 0)
                in_tok = data.get("input_tokens", 0)
                out_tok = data.get("output_tokens", 0)
                score = quality_score(text, task["ideal_keywords"])
                cost = estimate_cost(model_key, in_tok, out_tok)
                print(f"✓ ({latency:.0f}ms, score={score})")
            except Exception as e:
                error = str(e)
                text, latency, in_tok, out_tok, score, cost = "", 0, 0, 0, 0, 0
                print(f"✗ {error}")

            results.append(BenchmarkResult(
                model=model_name,
                task_id=task["id"],
                task_name=task["name"],
                response=text[:200] + "..." if len(text) > 200 else text,
                latency_ms=round(latency, 1),
                input_tokens=in_tok,
                output_tokens=out_tok,
                cost_usd=cost,
                quality_score=score,
                error=error,
            ))

    return results

# ── Display & save ────────────────────────────────────────────────────────────

def print_summary(results: List[BenchmarkResult]):
    from collections import defaultdict

    print(f"\n{'='*70}")
    print("BENCHMARK SUMMARY")
    print(f"{'='*70}")

    by_model: Dict[str, List[BenchmarkResult]] = defaultdict(list)
    for r in results:
        by_model[r.model].append(r)

    header = f"{'Model':<25} {'Avg Latency':>14} {'Avg Quality':>12} {'Total Cost':>12} {'Tokens':>10}"
    print(header)
    print("-" * 70)

    for model, res in by_model.items():
        valid = [r for r in res if not r.error]
        if not valid:
            print(f"{model:<25} {'ERROR':>14}")
            continue
        avg_lat = sum(r.latency_ms for r in valid) / len(valid)
        avg_q = sum(r.quality_score for r in valid) / len(valid)
        total_cost = sum(r.cost_usd for r in valid)
        total_tok = sum(r.input_tokens + r.output_tokens for r in valid)
        print(f"{model:<25} {avg_lat:>13.0f}ms {avg_q:>12.2f} ${total_cost:>11.6f} {total_tok:>10,}")

def save_csv(results: List[BenchmarkResult], path: str):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "model", "task_id", "task_name", "latency_ms", "input_tokens",
            "output_tokens", "cost_usd", "quality_score", "error", "response"
        ])
        writer.writeheader()
        for r in results:
            writer.writerow(r.__dict__)
    print(f"\nResults saved to: {path}")

# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM Benchmark Tool")
    parser.add_argument("--models", nargs="+", default=["ollama"],
                        choices=["openai", "anthropic", "ollama"],
                        help="Models to benchmark")
    parser.add_argument("--ollama-model", default="llama3.2", help="Ollama model name")
    parser.add_argument("--output", default="benchmark_results.csv", help="CSV output path")
    args = parser.parse_args()

    print("LLM Benchmark Tool")
    print(f"Testing models: {args.models}")
    print(f"Tasks: {len(TASKS)}")

    results = run_benchmark(args.models, ollama_model=args.ollama_model)
    print_summary(results)
    save_csv(results, args.output)

"""
Document Summarizer Extractive (TextRank) + Abstractive (BART/T5)
Requirements: transformers torch nltk numpy scikit-learn
Usage:
  python 02_text_summarizer.py --method extractive --input article.txt --ratio 0.3
  python 02_text_summarizer.py --method abstractive --input article.txt
  python 02_text_summarizer.py --method both --input article.txt
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List

import numpy as np

# ── Extractive: TextRank ──────────────────────────────────────────────────────

def sentence_tokenize(text: str) -> List[str]:
    """Split text into sentences using simple regex."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if len(s.strip()) > 10]

def build_similarity_matrix(sentences: List[str]) -> np.ndarray:
    """Build cosine similarity matrix between sentence TF-IDF vectors."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf = vectorizer.fit_transform(sentences)
    except ValueError:
        return np.eye(len(sentences))
    sim = cosine_similarity(tfidf, tfidf)
    np.fill_diagonal(sim, 0)
    return sim

def pagerank(matrix: np.ndarray, damping: float = 0.85, iterations: int = 100) -> np.ndarray:
    """Power iteration PageRank."""
    n = matrix.shape[0]
    # Row-normalize
    row_sums = matrix.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    matrix = matrix / row_sums

    scores = np.ones(n) / n
    for _ in range(iterations):
        scores = (1 - damping) / n + damping * matrix.T @ scores
    return scores

def extractive_summary(text: str, ratio: float = 0.3) -> str:
    """TextRank extractive summarization."""
    sentences = sentence_tokenize(text)
    if len(sentences) <= 2:
        return text

    n_select = max(1, int(len(sentences) * ratio))

    sim_matrix = build_similarity_matrix(sentences)
    scores = pagerank(sim_matrix)

    # Select top-n sentences in original order
    ranked_idx = np.argsort(scores)[::-1][:n_select]
    selected_idx = sorted(ranked_idx)
    summary = " ".join(sentences[i] for i in selected_idx)
    return summary

# ── Abstractive: BART / T5 ────────────────────────────────────────────────────

_abstractive_pipeline = None

def get_abstractive_pipeline(model_name: str = "facebook/bart-large-cnn"):
    global _abstractive_pipeline
    if _abstractive_pipeline is None:
        from transformers import pipeline
        print(f"Loading {model_name}...")
        _abstractive_pipeline = pipeline("summarization", model=model_name)
    return _abstractive_pipeline

def chunk_text(text: str, max_tokens: int = 900) -> List[str]:
    """Split long text into chunks by word count."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_tokens):
        chunks.append(" ".join(words[i : i + max_tokens]))
    return chunks

def abstractive_summary(
    text: str,
    model_name: str = "facebook/bart-large-cnn",
    max_length: int = 150,
    min_length: int = 40,
) -> str:
    """BART/T5 abstractive summarization with chunking for long docs."""
    summarizer = get_abstractive_pipeline(model_name)
    chunks = chunk_text(text, max_tokens=900)

    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        if len(chunks) > 1:
            print(f"  Summarizing chunk {i+1}/{len(chunks)}...")
        result = summarizer(
            chunk,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
        )
        chunk_summaries.append(result[0]["summary_text"])

    if len(chunk_summaries) == 1:
        return chunk_summaries[0]

    # Summarize the chunk summaries
    combined = " ".join(chunk_summaries)
    final = summarizer(combined, max_length=max_length, min_length=min_length, do_sample=False)
    return final[0]["summary_text"]

# ── CLI ───────────────────────────────────────────────────────────────────────

def load_text(path: str) -> str:
    p = Path(path)
    if not p.exists():
        print(f"Error: File not found: {path}")
        sys.exit(1)
    return p.read_text(encoding="utf-8")

def print_summary(title: str, summary: str, original_len: int):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(summary)
    ratio = len(summary) / original_len * 100
    print(f"\n  [Compression: {original_len} → {len(summary)} chars ({ratio:.1f}%)]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Document Summarizer")
    parser.add_argument("--method", choices=["extractive", "abstractive", "both"], default="both")
    parser.add_argument("--input", type=str, help="Path to text file (or use --demo)")
    parser.add_argument("--ratio", type=float, default=0.3, help="Extractive: fraction of sentences to keep")
    parser.add_argument("--model", default="facebook/bart-large-cnn", help="Abstractive model name")
    parser.add_argument("--demo", action="store_true", help="Run on built-in demo text")
    args = parser.parse_args()

    # Demo text
    DEMO_TEXT = """
    Artificial intelligence (AI) is transforming industries at an unprecedented pace. Machine learning,
    a subset of AI, enables computers to learn from data without being explicitly programmed. Deep learning,
    a further specialization using neural networks with many layers, has achieved remarkable results in
    image recognition, natural language processing, and game playing. Large language models (LLMs) like
    GPT-4 and Claude represent the latest frontier, capable of generating coherent text, answering questions,
    writing code, and engaging in complex reasoning. These models are trained on vast amounts of text data
    using self-supervised learning objectives. The transformer architecture, introduced in the seminal
    "Attention Is All You Need" paper in 2017, underlies virtually all modern LLMs. Key components include
    multi-head self-attention, positional encodings, and feed-forward layers. Fine-tuning and reinforcement
    learning from human feedback (RLHF) are used to align model outputs with human preferences. Despite
    their impressive capabilities, LLMs face challenges including hallucination, bias, lack of true
    understanding, and high computational costs. Researchers are actively working on more efficient
    architectures, better alignment techniques, and methods to improve factual accuracy and reasoning.
    The societal implications of powerful AI systems are profound, touching on employment, privacy,
    misinformation, and existential risk. Responsible AI development requires careful attention to
    safety, fairness, transparency, and accountability.
    """

    text = DEMO_TEXT if args.demo else load_text(args.input) if args.input else DEMO_TEXT
    text = text.strip()

    print(f"\nOriginal text ({len(text)} chars, {len(sentence_tokenize(text))} sentences)")

    if args.method in ("extractive", "both"):
        summary = extractive_summary(text, ratio=args.ratio)
        print_summary("EXTRACTIVE SUMMARY (TextRank)", summary, len(text))

    if args.method in ("abstractive", "both"):
        summary = abstractive_summary(text, model_name=args.model)
        print_summary("ABSTRACTIVE SUMMARY (BART)", summary, len(text))

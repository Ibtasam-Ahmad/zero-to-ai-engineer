"""
Fully Local RAG System Ollama + sentence-transformers + ChromaDB
Requirements: chromadb sentence-transformers pymupdf requests
Also needs: Ollama running locally (https://ollama.ai) with llama3.2 pulled
Usage:
  # First ingest documents
  python 01_local_rag.py --ingest --docs ./docs/
  # Then query
  python 01_local_rag.py --query "What is the main topic of the documents?"
  # Interactive mode
  python 01_local_rag.py --interactive
"""

import argparse
import json
import os
import sys
import textwrap
from pathlib import Path
from typing import List, Optional

# ── Config ────────────────────────────────────────────────────────────────────
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "rag_docs"
EMBED_MODEL = "all-MiniLM-L6-v2"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 4

# ── Chunking ──────────────────────────────────────────────────────────────────

def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into overlapping chunks by character count."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end].strip())
        start += size - overlap
    return [c for c in chunks if len(c) > 50]

# ── Document loading ──────────────────────────────────────────────────────────

def load_pdf(path: Path) -> str:
    try:
        import fitz  # pymupdf
        doc = fitz.open(str(path))
        return "\n".join(page.get_text() for page in doc)
    except ImportError:
        print("  pymupdf not installed, skipping PDF. pip install pymupdf")
        return ""

def load_document(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".pdf":
        return load_pdf(path)
    elif ext in (".txt", ".md", ".rst"):
        return path.read_text(encoding="utf-8", errors="ignore")
    else:
        print(f"  Skipping unsupported file type: {ext}")
        return ""

# ── ChromaDB vector store ─────────────────────────────────────────────────────

def get_collection():
    import chromadb
    from chromadb.utils import embedding_functions

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)
    return client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=ef)

def ingest_documents(docs_dir: str):
    folder = Path(docs_dir)
    if not folder.exists():
        print(f"Docs folder not found: {docs_dir}")
        sys.exit(1)

    files = list(folder.glob("*"))
    if not files:
        print("No files found in docs folder.")
        return

    collection = get_collection()
    total_chunks = 0

    for path in files:
        if path.is_dir():
            continue
        print(f"Loading: {path.name}")
        text = load_document(path)
        if not text:
            continue
        chunks = chunk_text(text)
        ids = [f"{path.stem}_{i}" for i in range(len(chunks))]
        metas = [{"source": path.name, "chunk": i} for i in range(len(chunks))]
        collection.upsert(documents=chunks, ids=ids, metadatas=metas)
        total_chunks += len(chunks)
        print(f"  → {len(chunks)} chunks ingested")

    print(f"\nTotal: {total_chunks} chunks stored in ChromaDB at {CHROMA_DIR}")

# ── Retrieval ─────────────────────────────────────────────────────────────────

def retrieve(query: str, top_k: int = TOP_K) -> List[dict]:
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=top_k)
    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({"text": doc, "source": meta.get("source", "unknown"), "score": round(1 - dist, 3)})
    return chunks

# ── Generation via Ollama ─────────────────────────────────────────────────────

def generate_ollama(prompt: str, model: str = OLLAMA_MODEL) -> str:
    import requests

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.exceptions.ConnectionError:
        return _mock_response(prompt)
    except Exception as e:
        return f"[Error calling Ollama: {e}]"

def _mock_response(prompt: str) -> str:
    """Fallback when Ollama is not running."""
    return (
        "[Ollama not running mock response]\n"
        "To get real responses: install Ollama (https://ollama.ai), "
        f"run 'ollama pull {OLLAMA_MODEL}', then 'ollama serve'.\n\n"
        "Based on the retrieved context, here is a simulated answer to your query."
    )

# ── RAG pipeline ──────────────────────────────────────────────────────────────

def rag_query(question: str, verbose: bool = True) -> str:
    chunks = retrieve(question)

    if not chunks:
        return "No relevant documents found. Please ingest documents first with --ingest."

    context = "\n\n".join(
        f"[Source: {c['source']} | Relevance: {c['score']}]\n{c['text']}"
        for c in chunks
    )

    prompt = f"""You are a helpful assistant. Answer the question based ONLY on the provided context.
If the answer is not in the context, say "I don't know based on the provided documents."

Context:
{context}

Question: {question}

Answer:"""

    if verbose:
        print(f"\n{'─'*60}")
        print("Retrieved chunks:")
        for i, c in enumerate(chunks, 1):
            print(f"  {i}. [{c['source']}] (score: {c['score']}) {c['text'][:100]}...")

    answer = generate_ollama(prompt)
    return answer

# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Local RAG System")
    parser.add_argument("--ingest", action="store_true", help="Ingest documents")
    parser.add_argument("--docs", default="./docs", help="Documents folder for ingestion")
    parser.add_argument("--query", type=str, help="Single query")
    parser.add_argument("--interactive", action="store_true", help="Interactive query loop")
    parser.add_argument("--model", default=OLLAMA_MODEL, help="Ollama model name")
    args = parser.parse_args()

    OLLAMA_MODEL = args.model

    if args.ingest:
        print(f"Ingesting documents from: {args.docs}")
        ingest_documents(args.docs)

    elif args.query:
        print(f"\nQuery: {args.query}")
        answer = rag_query(args.query)
        print(f"\n{'='*60}\nAnswer:\n{answer}\n{'='*60}")

    elif args.interactive:
        print("Local RAG Interactive Mode (type 'quit' to exit)")
        print(f"Using model: {OLLAMA_MODEL} | DB: {CHROMA_DIR}\n")
        while True:
            try:
                q = input("You: ").strip()
                if q.lower() in ("quit", "exit", "q"):
                    break
                if not q:
                    continue
                answer = rag_query(q)
                print(f"\nAssistant: {answer}\n")
            except KeyboardInterrupt:
                break
    else:
        parser.print_help()
        print("\nQuick start:")
        print("  mkdir docs && echo 'AI is transforming the world.' > docs/sample.txt")
        print("  python 01_local_rag.py --ingest --docs ./docs")
        print("  python 01_local_rag.py --query 'What is AI doing?'")

"""
RAG Chatbot: PDF-based retrieval-augmented generation.
Loads PDFs from ./docs, chunks, embeds into ChromaDB, retrieves and generates answers.
"""

import logging
import os
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    raise ImportError("Run: pip install chromadb")

# chromadb 0.5.x with newer posthog versions logs "Failed to send telemetry event" errors; hide them
logging.getLogger("chromadb.telemetry.product.posthog").setLevel(logging.CRITICAL)

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    raise ImportError("Run: pip install sentence-transformers")

try:
    import fitz  # PyMuPDF
except ImportError:
    raise ImportError("Run: pip install pymupdf")

CHROMA_DIR   = "./chroma_db"
EMBED_MODEL  = "all-MiniLM-L6-v2"
CHUNK_SIZE   = 500
CHUNK_OVERLAP = 50   # characters (approximately) repeated at the start of the next chunk
TOP_K        = 4

_embedder: Optional[SentenceTransformer] = None
_chroma_client = None
_collection    = None


def get_embedder() -> SentenceTransformer:
    global _embedder
    if _embedder is None:
        logger.info(f"Loading embedding model: {EMBED_MODEL}")
        _embedder = SentenceTransformer(EMBED_MODEL)
    return _embedder


def get_collection():
    global _chroma_client, _collection
    if _collection is None:
        _chroma_client = chromadb.PersistentClient(path=CHROMA_DIR, settings=Settings(anonymized_telemetry=False))
        _collection = _chroma_client.get_or_create_collection(
            name="rag_docs",
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def reset_collection() -> None:
    """Delete every stored chunk (used by `python ingest.py --reset`)."""
    global _collection
    get_collection()
    _chroma_client.delete_collection("rag_docs")
    _collection = None


def extract_text_from_pdf(pdf_path: str) -> List[Dict]:
    """Extract text chunks from a PDF file."""
    chunks = []
    doc = fitz.open(pdf_path)
    full_text = ""
    for page_num, page in enumerate(doc):
        full_text += page.get_text()

    # Simple recursive character split
    words = full_text.split()
    current_chunk = []
    current_len   = 0
    chunk_id      = 0
    has_new_words = False   # does the current chunk contain words that are not saved yet?

    for word in words:
        current_chunk.append(word)
        current_len += len(word) + 1
        has_new_words = True
        if current_len >= CHUNK_SIZE:
            chunks.append({
                "text":   " ".join(current_chunk),
                "source": os.path.basename(pdf_path),
                "chunk":  chunk_id,
            })
            # overlap: keep the last words, up to about CHUNK_OVERLAP characters (it used to be 50 *words*)
            overlap_words = []
            while current_chunk and sum(len(w) + 1 for w in overlap_words + current_chunk[-1:]) <= CHUNK_OVERLAP:
                overlap_words.insert(0, current_chunk.pop())
            current_chunk = overlap_words
            current_len   = sum(len(w) + 1 for w in current_chunk)
            chunk_id     += 1
            has_new_words = False

    if current_chunk and has_new_words:  # otherwise the last chunk would only repeat the overlap
        chunks.append({"text": " ".join(current_chunk), "source": os.path.basename(pdf_path), "chunk": chunk_id})

    return chunks


def ingest_file(pdf_path: Path) -> int:
    """Ingest ONE PDF, replacing older chunks of the same file. Returns number of chunks added."""
    collection = get_collection()
    embedder   = get_embedder()
    pdf_path   = Path(pdf_path)

    logger.info(f"Ingesting: {pdf_path.name}")
    chunks = extract_text_from_pdf(str(pdf_path))
    collection.delete(where={"source": pdf_path.name})  # remove stale chunks of an earlier version
    if not chunks:
        return 0
    texts      = [c["text"]   for c in chunks]
    metadatas  = [{"source": c["source"], "chunk": c["chunk"]} for c in chunks]
    ids        = [f"{pdf_path.stem}_{c['chunk']}" for c in chunks]
    embeddings = embedder.encode(texts, show_progress_bar=True).tolist()

    collection.upsert(documents=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)
    logger.info(f"  Added {len(chunks)} chunks from {pdf_path.name}")
    return len(chunks)


def ingest_documents(docs_dir: str = "./docs") -> int:
    """Ingest all PDFs in docs_dir into ChromaDB. Returns number of chunks added."""
    total      = 0

    pdf_files = list(Path(docs_dir).glob("*.pdf"))
    if not pdf_files:
        logger.warning(f"No PDF files found in {docs_dir}")
        return 0

    for pdf_path in pdf_files:
        try:
            total += ingest_file(pdf_path)
        except Exception as e:  # one unreadable PDF must not stop the others
            logger.warning(f"  Skipping {pdf_path.name}: {type(e).__name__}: {e}")

    return total


def retrieve(query: str, top_k: int = TOP_K) -> List[Dict]:
    """Retrieve top-k relevant chunks for a query."""
    collection = get_collection()
    embedder   = get_embedder()
    q_embed    = embedder.encode([query]).tolist()
    results    = collection.query(query_embeddings=q_embed, n_results=top_k)

    chunks = []
    for i, doc in enumerate(results["documents"][0]):
        chunks.append({
            "text":     doc,
            "source":   results["metadatas"][0][i].get("source", "unknown"),
            "distance": results["distances"][0][i] if results.get("distances") else 0,
        })
    return chunks


def generate_response(query: str, context_chunks: List[Dict], history: List[Dict]) -> str:
    """Generate a response using retrieved context. Tries Ollama, falls back to template."""
    if not context_chunks:
        return ("I don't have any documents to search yet. Put PDF files in the docs/ folder and run "
                "`python ingest.py`, or upload a PDF with the button at the top.")
    context = "\n\n---\n\n".join([c["text"] for c in context_chunks])
    system_prompt = (
        "You are a helpful assistant. Answer the user's question using ONLY the provided context. "
        "If the answer is not in the context, say so honestly."
    )
    user_message = f"Context:\n{context}\n\nQuestion: {query}"

    # Try Ollama first
    try:
        import httpx
        messages = [{"role": "system", "content": system_prompt}]
        for h in history[-4:]:  # last 4 turns
            messages.append({"role": h["role"], "content": h["content"]})
        messages.append({"role": "user", "content": user_message})

        r = httpx.post(
            "http://localhost:11434/api/chat",
            json={"model": "llama3.2", "messages": messages, "stream": False},
            timeout=60,
        )
        if r.status_code == 200:
            return r.json()["message"]["content"]
    except Exception:
        pass

    # Try OpenAI
    try:
        import openai
        client = openai.OpenAI()
        messages = [{"role": "system", "content": system_prompt}]
        for h in history[-4:]:
            messages.append({"role": h["role"], "content": h["content"]})
        messages.append({"role": "user", "content": user_message})
        resp = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
        return resp.choices[0].message.content
    except Exception:
        pass

    # Fallback: return context summary
    return (
        f"Based on the retrieved documents:\n\n"
        + "\n\n".join([f"• {c['text'][:300]}..." for c in context_chunks[:2]])
        + "\n\n(Note: No LLM backend available. Install Ollama or set OPENAI_API_KEY.)"
    )


# In-memory session store
_sessions: Dict[str, List[Dict]] = {}


def chat(session_id: str, message: str) -> Tuple[str, List[Dict]]:
    """Main chat function. Returns (response, source_chunks)."""
    if session_id not in _sessions:
        _sessions[session_id] = []

    chunks   = retrieve(message)
    response = generate_response(message, chunks, _sessions[session_id])

    _sessions[session_id].append({"role": "user",      "content": message})
    _sessions[session_id].append({"role": "assistant", "content": response})

    return response, chunks


def list_sessions() -> List[str]:
    return list(_sessions.keys())


def delete_session(session_id: str) -> bool:
    if session_id in _sessions:
        del _sessions[session_id]
        return True
    return False


if __name__ == "__main__":
    n = ingest_documents("./docs")
    print(f"Ingested {n} chunks.")
    if n > 0:
        session = str(uuid.uuid4())
        resp, sources = chat(session, "What is this document about?")
        print(f"Response: {resp}")

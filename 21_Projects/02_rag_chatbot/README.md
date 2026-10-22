# Project 02: RAG Chatbot (chat with your PDFs)

> **Difficulty:** Intermediate · **Time:** 2-4 hours (plus a 10-30 minute install) · **Runs on:** CPU, no API key needed

## 1. What this project does

You put some PDF files into a folder. The app reads them, cuts the text into small pieces, and stores those pieces in a searchable "memory". When you type a question in the browser, the app finds the pieces of text that are most related to your question and uses them to answer.

This technique is called **RAG** (**Retrieval-Augmented Generation**): first *retrieve* (find) the relevant text, then *generate* (write) an answer from it. It is how most "chat with your documents" products work.

**Important to know up front:** the "generate" part needs a language model (an **LLM**). The code tries a local [Ollama](https://ollama.com) model first, then (only if you have set an API key) the OpenAI API. If neither is available (the default on a fresh machine) the app still works, but it shows you the best-matching passages instead of writing a sentence. That is still a great way to learn the retrieval half, which is the genuinely new part of this project.

**What you will learn**

- How to pull text out of PDFs (PyMuPDF) and split it into overlapping **chunks**.
- What an **embedding** is (a list of numbers that captures the meaning of a piece of text) and how to create one with `sentence-transformers`.
- How a **vector database** (ChromaDB) finds the chunks whose meaning is closest to your question.
- How to serve all of this with FastAPI: normal HTTP endpoints, a safe file upload, and a **WebSocket** (a connection that stays open for back-and-forth chat).

## 2. Folder contents

| File | Purpose |
|---|---|
| `main.py` | The "brain": PDF reading, chunking, embedding, ChromaDB storage, retrieval, answer generation (Ollama, then OpenAI, then a fallback), and the in-memory chat sessions. Running it directly ingests `docs/` and asks one test question. |
| `ingest.py` | Command-line script: `python ingest.py` loads every PDF in `docs/` into ChromaDB. `--docs-dir other_folder` reads another folder, `--reset` empties the database first. |
| `api.py` | The FastAPI web server: `POST /chat`, `POST /upload-doc`, `GET /sessions`, `DELETE /session/{id}`, WebSocket `/ws/{session_id}`, `GET /health`, and `GET /` (the web page). |
| `templates/index.html` | The chat web page (chat window, session list, "Upload PDF" button). |
| `docs/rag_quick_guide.pdf` | A small 2-page sample PDF that explains RAG, so the project works straight away. Add your own PDFs next to it. |
| `requirements.txt` | The Python packages (with pinned versions) the project needs. |
| `notes/02_rag_chatbot.md` | A longer explanation of the ideas behind the project. |

Created while running: `chroma_db/` (the saved vector database, in the folder you start from). Delete it, or run `python ingest.py --reset`, to start again from zero.

## 3. Prerequisites

Finish these first (paths are relative to the repo root):

- `07_NLP/00_start_here_text_to_numbers.ipynb` and `07_NLP/02_word_embeddings.ipynb` (what embeddings are)
- `08_LLM/00_start_here_how_llms_work.ipynb` and `08_LLM/02_rag/01_rag_fundamentals.ipynb` (what RAG is)
- `13_Databases/03_vector_db/01_vector_databases.ipynb` (vector databases)
- `12_FastAPI/01_fastapi_intro.ipynb` to `03_ml_serving_with_fastapi.ipynb` (FastAPI basics)
- [Project 01](../01_ml_pipeline/README.md) (same train/serve structure, simpler model)

**Python:** tested with **Python 3.12**. Use 3.10, 3.11 or 3.12.

**Disk and network:** the first install downloads PyTorch plus about 100 other packages. With the CPU-only PyTorch (step 2) the virtual environment was about **1.7 GB**. The first run also downloads the small embedding model `all-MiniLM-L6-v2` (about 90 MB) from Hugging Face.

## 4. How to run it (tested step by step)

Every step below was run on Linux with Python 3.12 in a fresh virtual environment, and the outputs shown are the real outputs. Commands are for **macOS/Linux**; Windows versions are given where they differ. **Run every command from inside this folder**: the code uses the relative paths `./docs`, `./chroma_db` and `templates/index.html`.

### Step 1: Open a terminal in this folder and create a virtual environment

```bash
cd 21_Projects/02_rag_chatbot
python3 -m venv .venv
source .venv/bin/activate          # Windows (PowerShell): .venv\Scripts\Activate.ps1
                                   # Windows (cmd):        .venv\Scripts\activate.bat
```

### Step 2: Install the packages

`requirements.txt` does not pin PyTorch, so on Linux and Windows pip would download the large GPU (CUDA) build (several GB). Install the small CPU-only build first, then the rest:

```bash
pip install --upgrade pip
pip install torch --index-url https://download.pytorch.org/whl/cpu     # skip this line on macOS
pip install -r requirements.txt
```

Both commands finished without errors or version conflicts. (A `pip install --dry-run -r requirements.txt` also resolves cleanly.)

### Step 3: Ingest the PDFs

The `docs/` folder already contains `rag_quick_guide.pdf`. Copy any other PDFs you like into it (they must contain real text; scanned photos of pages have none), then run:

```bash
python ingest.py
```

Real output (shortened):

```
INFO - Loading embedding model: all-MiniLM-L6-v2
INFO - Ingesting: rag_quick_guide.pdf
INFO -   Added 5 chunks from rag_quick_guide.pdf
Ingestion complete: 5 chunks stored in ChromaDB.
```

The first run takes a little longer because the embedding model is downloaded. A PDF that cannot be read is skipped with a warning such as `Skipping broken.pdf: FileDataError: Failed to open file ...`, and the other files are still ingested. Running `ingest.py` again replaces the old chunks of each file, so nothing is stored twice. If you deleted PDFs from `docs/`, run `python ingest.py --reset` to rebuild the database without them.

### Step 4: Start the web server

```bash
uvicorn api:app --port 8000
```

Wait for `Application startup complete.` If port 8000 is already used by another program you will see `address already in use`: pick another number, for example `--port 8001`, and use that number in every URL below. (`python api.py` also works, but it always uses port 8001 with auto-reload.)

Leave this terminal running. Open a **second** terminal (activate the venv there too) for the `curl` commands.

### Step 5: Open the chat page

Go to **http://localhost:8000/** in your browser, type a question (try "What is hallucination?") and press Enter. Use **Upload PDF** to add documents. You can also try every endpoint by hand at **http://localhost:8000/docs** (handy on Windows, where `curl` quoting is awkward).

### Step 6: Try the API with curl

On Windows PowerShell type `curl.exe` instead of `curl`.

**Health check**

```bash
curl http://localhost:8000/health
```
```json
{"status":"ok"}
```

**Ask a question**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is hallucination?", "session_id": "demo"}'
```

Real response (shortened; no LLM was available, so the fallback answer is shown):

```json
{
  "response": "Based on the retrieved documents:\n\n• RAG Quick Guide (sample document for the RAG Chatbot project) What is RAG? ...\n\n• This is called hallucination. RAG reduces this problem because the model is given real text to quote, ...\n\n(Note: No LLM backend available. Install Ollama or set OPENAI_API_KEY.)",
  "session_id": "demo",
  "sources": [
    {"text": "RAG Quick Guide ... it can invent confident but wrong answers. This is called hallucination. RAG reduces this", "source": "rag_quick_guide.pdf", "distance": 0.743486374090345},
    {"text": "This is called hallucination. RAG reduces this problem ...", "source": "rag_quick_guide.pdf", "distance": 0.7999065903958356},
    {"text": "a smaller distance means a closer meaning. Step 4, generation. ...", "source": "rag_quick_guide.pdf", "distance": 0.8651054685662988},
    {"text": "into an embedding: a list of 384 numbers ...", "source": "rag_quick_guide.pdf", "distance": 1.0213271931918655}
  ]
}
```

`distance` is the **cosine distance** between your question and the chunk: smaller means "closer in meaning". The two closest chunks are exactly the ones that define hallucination.

**Upload another PDF** (saved into `docs/`, and only this file is ingested)

```bash
curl -F "file=@/path/to/moon_garden.pdf" http://localhost:8000/upload-doc
```
```json
{"filename":"moon_garden.pdf","chunks_ingested":2}
```

Uploads are checked. These real responses all came back with HTTP 400 and nothing was saved:

```bash
curl -F "file=@notes.txt" http://localhost:8000/upload-doc
# {"detail":"Only PDF files supported"}
curl -F "file=@fake.pdf" http://localhost:8000/upload-doc          # a text file renamed to .pdf
# {"detail":"This file is not a valid PDF"}
curl -F "file=@moon_garden.pdf;filename=.hidden.pdf" http://localhost:8000/upload-doc
# {"detail":"Invalid file name"}
```

A file name containing folders is cut down to the bare name, so it cannot escape `docs/`: uploading with `filename=../escaped.pdf` saved the file as `docs/escaped.pdf`.

**Sessions**

```bash
curl http://localhost:8000/sessions
# {"sessions":["demo", ...]}
curl -X DELETE http://localhost:8000/session/demo
# {"deleted":"demo"}
curl -X DELETE http://localhost:8000/session/nope
# {"detail":"Session not found"}     (HTTP 404)
```

**WebSocket chat** (curl cannot do WebSockets; this short Python script uses the `websockets` package that `requirements.txt` already installed):

```python
import asyncio, json, websockets

async def main():
    async with websockets.connect("ws://localhost:8000/ws/my-session") as ws:
        await ws.send("How long is a chunk?")
        reply = json.loads(await ws.recv())
        print(reply["response"][:120])
        print("sources:", [s["source"] for s in reply["sources"]])

asyncio.run(main())
```

It printed the start of the fallback answer and the list of source files.

**Before any document is ingested**, `/chat` answers: `"I don't have any documents to search yet. Put PDF files in the docs/ folder and run `python ingest.py`, or upload a PDF with the button at the top."`

### Step 7 (optional): Get real written answers from a local LLM

Without an LLM you only get the retrieved passages. To get proper answers for free and offline, install [Ollama](https://ollama.com), run `ollama pull llama3.2` and restart the server. The code asks Ollama for exactly the model name `llama3.2` at `http://localhost:11434` (in `generate_response` in `main.py`); to use another model, change the name there. **This step was not tested** for this README: the test machine's Ollama did not have that model, so it answered "404 Not Found" and the app correctly fell back to showing passages.

> ⚠️ **Paid API:** if the environment variable `OPENAI_API_KEY` is set on your computer, the app calls the paid OpenAI API (model `gpt-4o-mini`, set in `main.py`; check the provider's current model list) on every question. Unset it if you do not want that.

### Step 8: Stop the server

Press `Ctrl+C` in the server terminal.

## 5. How it works

```
INGESTION  (python ingest.py, or POST /upload-doc for one file)
  docs/*.pdf --> PyMuPDF extracts text --> split into ~500-character chunks
             (the last ~50 characters of a chunk are repeated at the start of the next)
             --> all-MiniLM-L6-v2 turns each chunk into 384 numbers (an embedding)
             --> ChromaDB stores text + embedding on disk in chroma_db/
                 (older chunks of the same file are removed first)

CHAT  (POST /chat  or  WebSocket /ws/{session_id})
  your question
      |
      v
  embed the question with the same model
      |
      v
  ChromaDB: "which 4 stored chunks are closest?"  (cosine distance)
      |
      v
  prompt = rules + the 4 chunks + last 4 chat messages + question
      |
      v
  Ollama (llama3.2)?      --no-->  OpenAI API (key)?   --no-->  fallback:
      |                              |                          show first 300 chars
      v                              v                          of the top 2 chunks
  answer + list of source chunks, saved in the in-memory session, sent back as JSON
```

Key pieces in `main.py`: `extract_text_from_pdf` builds the chunks, `ingest_file` stores one PDF, `ingest_documents` loops over the folder, `retrieve` asks ChromaDB for the `TOP_K = 4` nearest chunks, `generate_response` tries the answer back-ends in order, and `chat` ties it together and keeps the history in the `_sessions` dictionary.

## 6. Known limitations

These are not bugs, but things to keep in mind (all checked on the test machine unless stated):

1. **Without an LLM there is no real answer**, only the best passages. See step 7. The Ollama path itself was not tested here.
2. **No token-by-token streaming.** The page uses `POST /chat` and the WebSocket sends the whole answer as one message, so answers appear all at once.
3. **Sessions live only in memory.** They are lost when the server restarts, and clicking an old session in the sidebar only shows "Resumed session", not the earlier messages (there is no endpoint that returns them; see exercise 4).
4. **Retrieval is simple.** Only the 4 closest chunks are used, there is no "no good match" threshold, and the small embedding model sometimes ranks a less useful chunk first (for "How long is a chunk?" the best chunk was not ranked first).
5. **Chunking ignores pages and sentences.** Chunks are cut by length, so a chunk can stop mid-sentence and the source does not say which page it came from.
6. **Same file name, same document.** Uploading a different PDF with an existing name replaces the old one (file and chunks).
7. **Only lower-case `.pdf` names are accepted** by the upload (`REPORT.PDF` gets "Only PDF files supported"), and `ingest.py` also only looks for `*.pdf`. Rename such files.
8. **One slow question blocks the server.** `/chat` is an `async` function that calls slow, blocking code, so while an answer is being produced (up to 60 s with an LLM) other requests wait.
9. **Run from this folder.** `./docs`, `./chroma_db` and `templates/index.html` are relative to the folder you start the scripts and the server from.
10. **The web page needs the internet for styling.** It loads Bootstrap from a CDN; offline it still works but looks plain.

### What was fixed (October 2026)

| Problem in the original code | Fix |
|---|---|
| No `docs/` folder: uploads crashed with `FileNotFoundError` (HTTP 500), ingest found 0 PDFs | Sample `docs/rag_quick_guide.pdf` added; the folder is created if missing |
| Path traversal: `filename=../escaped.pdf` was written outside `docs/` | Only the bare file name is kept; only `.pdf`; hidden/empty names rejected |
| A broken "PDF" was saved, and every later upload failed with HTTP 500 | Uploads are checked with PyMuPDF before saving (HTTP 400); ingest skips unreadable files |
| Each upload re-ingested the whole folder and reported the total chunk count | Only the uploaded file is ingested; its own chunk count is returned |
| Overlap counted words (≈300 of 500 characters repeated) and a duplicate last chunk was stored | Overlap is ~50 characters; the last chunk is only stored if it has new text |
| Re-uploaded or deleted PDFs left old chunks in the database | Old chunks of a file are removed before re-ingesting; `ingest.py --reset` added |
| Empty database gave an empty, confusing answer | Clear "no documents yet" message |
| Web page inserted PDF text and session ids as HTML (script injection risk) | Text is inserted with `textContent` |
| `Failed to send telemetry event` errors printed by ChromaDB | Telemetry switched off and that log silenced |

## 7. Ideas to extend it

1. **Easy:** change `TOP_K` (`main.py`) to 2 and to 8 and compare the `sources` and `distance` values for the same question.
2. **Easy:** add a "no good match" rule: if the best `distance` is above, say, 0.8, reply "I could not find this in your documents" instead of guessing.
3. **Medium:** stream the answer: call Ollama with `"stream": true` and send each piece over the WebSocket, then make the page use the WebSocket.
4. **Medium:** add `GET /session/{id}` that returns a session's messages, and show them in the page when an old session is clicked.
5. **Harder:** add a fourth answer back-end that runs a small local model with `transformers` (for example a 0.5B-parameter instruct model), so the app writes real answers without Ollama or any API key.

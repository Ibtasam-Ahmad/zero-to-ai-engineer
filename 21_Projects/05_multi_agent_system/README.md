# Project 05: Multi-Agent Research System

A small "team" of AI helpers that writes a report on any topic you give it.
You type a topic, and three **agents** (an agent is a language model given one job, a set of instructions, and sometimes tools) work one after another:

1. **Research agent**: searches the web for the topic and summarises what it found.
2. **Writer agent**: turns those findings into a structured report.
3. **Reviewer agent**: checks the draft and returns an improved final version.

The three steps are wired together with **LangGraph** (a library that runs steps as a graph, passing a shared "state" dictionary from one step to the next). A **FastAPI** web server runs the pipeline in the background and lets a web page follow its progress live over a **WebSocket** (a connection that stays open so the server can push messages to the browser).

| | |
|---|---|
| **What you will learn** | How agents are just functions that read and update a shared state; how LangGraph wires them together and streams progress; how a web API runs a slow job in the background and reports progress (start, then poll or stream, then fetch the result); how to fall back gracefully when an API key is missing |
| **Difficulty** | Intermediate. You should be comfortable running Python scripts and reading short functions |
| **Time needed** | About 1 hour to run it and read the code, plus 1-2 hours for the exercises |
| **Runs on** | CPU. Web search works without a key. Written reports need an OpenAI API key (paid) or another OpenAI-compatible server; without one, you get a placeholder report built from the search results |

---

## 1. What is in this folder

| File | What it does |
|---|---|
| `agents.py` | The three agents. Each is a function `xxx_node(state) -> new_state` with its own **system prompt** (the instructions that give the model its role). Also picks the LLM (`get_llm`; the model name lives in `DEFAULT_MODEL`) and the search tool (`get_search_tool`: Tavily if it can be created, otherwise keyless DuckDuckGo via the `ddgs` package) |
| `graph.py` | Defines the shared state (`ResearchState`) and the LangGraph graph `research -> writer -> reviewer -> END`. `run_pipeline(topic, on_log)` streams the state after each step, so callers can show live progress. Without LangGraph it runs the three functions one after another |
| `main.py` | Command-line entry point: `python main.py "your topic"` prints the activity log and the final report |
| `api.py` | FastAPI server: `POST /research` starts a background job, `GET /task/{id}` shows its status, live log and any error, `GET /report/{id}` returns the report, `WS /ws/{id}` streams progress, `GET /health`, and `GET /` serves the web page |
| `templates/index.html` | The web page: a topic box, three "agent cards", a progress bar, a live log and the final report |
| `requirements.txt` | Pinned library versions (FastAPI, LangGraph, LangChain, OpenAI connector, Tavily, `ddgs`, websockets) |
| `notes/05_multi_agent_system.md` | Longer explanation of the design and concepts |

---

## 2. Before you start (prerequisites)

**Notebooks to finish first** (paths are relative to this folder):

- Python basics: [`../../01_Python/01_basic.ipynb`](../../01_Python/01_basic.ipynb)
- Prompting: [`../../09_Prompt_Engineering/00_start_here_prompting_with_a_free_local_model.ipynb`](../../09_Prompt_Engineering/00_start_here_prompting_with_a_free_local_model.ipynb) and [`../../09_Prompt_Engineering/01_basics.ipynb`](../../09_Prompt_Engineering/01_basics.ipynb)
- Agents: [`../../10_Agents/01_agent_fundamentals.ipynb`](../../10_Agents/01_agent_fundamentals.ipynb), [`../../10_Agents/03_langgraph.ipynb`](../../10_Agents/03_langgraph.ipynb), [`../../10_Agents/04_multi_agent_frameworks.ipynb`](../../10_Agents/04_multi_agent_frameworks.ipynb)
- Web APIs: [`../../12_FastAPI/01_fastapi_intro.ipynb`](../../12_FastAPI/01_fastapi_intro.ipynb) and [`../../12_FastAPI/02_advanced_fastapi.ipynb`](../../12_FastAPI/02_advanced_fastapi.ipynb)

**Python version:** 3.10, 3.11 or 3.12. `pip install --dry-run -r requirements.txt` resolves with no conflicts on Python 3.12. Python 3.13+ is not recommended (the pinned stack pulls in `numpy 1.26.4`).

**API keys (both optional):**

| Key | Used for | Cost | Without it |
|---|---|---|---|
| `OPENAI_API_KEY` | The LLM behind all three agents (default model `gpt-4o-mini`; change it with the `OPENAI_MODEL` environment variable and check the provider's current model list) | Paid, billed per token by OpenAI. Check OpenAI's current pricing page | Placeholder report: the raw search results plus "(LLM unavailable ...)" |
| `TAVILY_API_KEY` | Tavily, a web search built for AI apps | Tavily has offered a free monthly allowance; check tavily.com for current limits | Keyless DuckDuckGo search via `ddgs` (worked in testing; may be rate-limited at times) |

**Free alternative to OpenAI:** `ChatOpenAI` can talk to any "OpenAI-compatible" server, such as a local Ollama install. Set `OPENAI_API_BASE=http://localhost:11434/v1`, `OPENAI_API_KEY=anything`, and `OPENAI_MODEL=<a model you have pulled>`. I verified this mechanism with a small fake OpenAI-compatible server (see Step 8), not with a real Ollama model.

> ⚠️ **Never paste an API key into a code file** or commit it to git. Set it as an environment variable in your terminal (shown below).

---

## 3. Run it step by step

Run all commands from inside this folder (`21_Projects/05_multi_agent_system`). The server reads `templates/index.html` with a relative path.

### Step 1: Create and activate a virtual environment

A **virtual environment** is a private folder of libraries for one project.

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

### Step 2: Install the libraries

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

pip may print "This is taking longer than usual" while it chooses a `langchain-core` version. That is normal.

### Step 3: (Optional) set your API keys

```bash
# macOS / Linux
export OPENAI_API_KEY="sk-...your key..."
export TAVILY_API_KEY="tvly-...your key..."

# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-...your key..."
$env:TAVILY_API_KEY="tvly-...your key..."
```

### Step 4: Run the pipeline from the command line

```bash
python main.py "solar panels"
```

What I got **without any keys** (it took about 12 seconds, mostly the web search):

```
📋 Activity Log:
  🚀 Starting research on: solar panels
  ✅ Research complete for: solar panels
  ✅ Draft report written
  ✅ Report reviewed and finalized

📄 Final Report:
============================================================
# Report: solar panels

## Summary

Research findings for 'solar panels':
- Solar panel: A solar panel is a device that converts sunlight into electricity by using multiple solar modules ...
- Solar panels on spacecraft: Solar panels on spacecraft, commonly referred to as solar arrays, ...
...

(LLM unavailable install langchain_openai and set OPENAI_API_KEY)

*(LLM unavailable)*

---
*Reviewed: No changes (LLM unavailable)*
```

The search results are real; the "report" is a placeholder because no LLM is configured. If the search fails (no internet, or DuckDuckGo rate-limits you), the findings say so, for example `Web search failed for: solar panels (RatelimitException: ...). Try again later, or set TAVILY_API_KEY ...`.

### Step 5: Start the web server

```bash
python api.py
```

This starts on **port 8004** (`api.py`, last line). To pick another port:

```bash
python -m uvicorn api:app --host 127.0.0.1 --port 8000
```

The examples below use port 8000.

### Step 6: Use the web page

Open <http://127.0.0.1:8000/>, type a topic and click **🚀 Start Research**. The log fills in as each agent finishes, and the report appears at the end. (Bootstrap CSS comes from a CDN, so the page looks plain when you are offline.)

### Step 7: Try the API with curl

On Windows use `curl.exe`, and for JSON bodies use a file: `-d @body.json`.

```bash
curl -X POST http://127.0.0.1:8000/research -H "Content-Type: application/json" -d '{"topic":"solar panels"}'
```
```json
{"task_id":"9a497ca7-44e0-44ff-9b33-ba4bf3b37e5e","topic":"solar panels"}
```

Straight away, the status shows the job running, with the first log line already there:

```bash
curl http://127.0.0.1:8000/task/9a497ca7-44e0-44ff-9b33-ba4bf3b37e5e
```
```json
{"task_id":"9a497ca7-...","status":"running","topic":"solar panels","log":["🚀 Starting research on: solar panels"],"partial":"","error":null}
```

When it finishes, `status` is `"complete"` and `log` has all four lines. Then:

```bash
curl http://127.0.0.1:8000/report/9a497ca7-44e0-44ff-9b33-ba4bf3b37e5e
# {"task_id":"9a497ca7-...","status":"complete","report":"# Report: solar panels\n\n## Summary\n\n...","error":null}
curl http://127.0.0.1:8000/task/nope
# {"detail":"Task not found"}   (HTTP 404)
```

If a run fails, `status` is `"error"`, and `error` tells you why. For example, with an unreachable LLM server I got `"error":"APIConnectionError: Connection error."`.

### Step 8: Watch progress live over the WebSocket

The web page connects to `ws://127.0.0.1:8000/ws/<task_id>`. A small Python client printed this, timed from connecting. I pointed `OPENAI_API_BASE` at a fake OpenAI-compatible server that waits 3 seconds per call, to imitate a real model:

```
+ 0.3s log: 🚀 Starting research on: solar panels
+41.6s log: ✅ Research complete for: solar panels
+44.6s log: ✅ Draft report written
+47.6s log: ✅ Report reviewed and finalized
+47.6s done: status=complete error=None report="[fake reply #3 for 'You are a Reviewer Agent...' ..."
```

Each agent's line arrives as soon as that agent finishes. An unknown id gets an immediate `done` message with `error: "Task not found"`, and the socket closes.

Stop the server with `Ctrl+C`.

**How this was verified:** I ran it on Python 3.12 without any API keys, using newer library versions than the pins: langgraph 0.2.76, langchain 0.3.28, langchain-openai 0.3.33, ddgs 9.16.0. The pins themselves were checked with `pip install --dry-run` only.

---

## 4. How it works

```
 browser / curl
      │  POST /research {"topic": ...}
      ▼
 api.py ── creates task_id in the in-memory _tasks dict,
      │    schedules _run() on the event loop, returns task_id at once
      │
      │  _run() → asyncio.to_thread(run_pipeline, topic, on_log)   (separate thread)
      ▼
 graph.py  run_pipeline(topic, on_log)
      │   state = {topic, research_findings, draft_report, final_report, status, log}
      │   compiled.stream(state) → after EACH node: on_log(state["log"])
      ▼
 ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
 │ research_node  │ ─► │  writer_node   │ ─► │ reviewer_node  │ ─► END
 │ search tool +  │    │ LLM + WRITER   │    │ LLM + REVIEWER │
 │ LLM summary    │    │ system prompt  │    │ system prompt  │
 └────────────────┘    └────────────────┘    └────────────────┘
      each node returns {**state, new_field, status, log + [one line]}
      ▼
 _tasks[task_id] = {status, log (updated live), report, error}
      ▲
      │  GET /task/{id} (polling)    WS /ws/{id} (checks once per second)
      │  GET /report/{id}
 browser / curl
```

Key ideas:

- **Node = plain function.** Each agent receives the whole state dictionary and returns a copy with its own field filled in.
- **Graceful fallback.** No LLM (no key, or the library is missing): the node returns placeholder text. Search fails: the findings say why. No LangGraph: `graph.py` calls the three functions in a row.
- **Background job + streaming.** The HTTP request returns immediately with a `task_id`. The work runs in a thread, and `on_log` copies the log into `_tasks` after every step, so polling and the WebSocket both show live progress.

---

## 5. Known issues and limitations

- **Not verified with a real paid LLM or a real Tavily key.** The LLM code path was exercised only with a local fake OpenAI-compatible server, and Tavily only in its "no key" fallback.
- **DuckDuckGo can rate-limit you.** `ddgs` worked in every test here, but it is a free, unofficial search. If it fails, the report says "Web search failed ..."; wait a bit, or use a Tavily key.
- **Everything is in memory** (`_tasks` in `api.py`). Tasks disappear when the server restarts, the dictionary grows forever, and several worker processes would not share tasks. A database or Redis would fix this (Exercise 4).
- **Progress has three steps only.** The research step (search + first LLM call) is the slow one, so the progress bar sits on "Searching the web..." for most of the run.
- **The page builds the socket address as `ws://`.** Behind an `https` site it would need `wss://`; the page then falls back to polling `/task/{id}`.
- **Newer langchain-community versions** print a deprecation warning for `TavilySearchResults`. That is harmless with the pinned version.

---

## 6. Ideas to extend it

1. **Easy: show the sources.** Ask the writer agent to finish the report with a "Sources" list built from the search results' links.
2. **Easy-medium: a free local model.** Run Ollama, set `OPENAI_API_BASE`, `OPENAI_API_KEY` and `OPENAI_MODEL` (see Prerequisites), and compare report quality and speed with a paid model.
3. **Medium: a revision loop.** Make the reviewer return a score, and add a **conditional edge** (`graph.add_conditional_edges`) that sends the report back to the writer if the score is low, with a maximum of 2 loops. Watch the live log show the extra rounds.
4. **Medium: persistent tasks.** Store `_tasks` in SQLite (one row per task), so tasks survive a restart.
5. **Harder: a fourth agent.** Add a "fact-checker" node between writer and reviewer that searches for each key claim and flags unsupported ones.

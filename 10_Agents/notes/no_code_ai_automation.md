# No-Code and Low-Code AI Automation

A lot of useful AI work is not a new app. It is **glue**: an email arrives, an LLM reads it, and something happens in Slack, a CRM or a spreadsheet. **Workflow automation tools** such as n8n, Make and Zapier let you build that glue by connecting boxes on a canvas, and most of them now have built-in LLM and agent steps.

These notes are the conceptual map for `14_no_code_ai_automation_n8n_make_zapier.ipynb`. The notebook builds a tiny n8n-like engine in Python and runs a realistic AI email-triage workflow on it. Facts about products are as of late 2026; check the vendors' docs for current details and prices.

---

## 1. The core idea: trigger, then actions

A **workflow** is a chain of steps that runs automatically. A **trigger** decides when it runs; **actions** do the work. An LLM is usually *one step* in the chain: it turns messy text into a category, a summary, extracted fields or a draft.

```mermaid
flowchart LR
    T["Trigger<br/>(webhook, schedule, app event, chat)"] --> S1["Prepare data"] --> AI("LLM / AI Agent step") --> D{"Decide<br/>(IF / Switch / Router)"}
    D --> A1["Action: label, draft, CRM, Slack"]
    D --> A2["Human approval"] --> A3["Risky action: send, publish, write"]
```

- **No-code:** build only with boxes and forms.
- **Low-code:** boxes plus small code steps (n8n Code node, Zapier Code steps, Make custom functions).

---

## 2. Shared vocabulary

| Term | Meaning | n8n | Make | Zapier |
|---|---|---|---|---|
| Workflow | the whole automation | workflow | scenario | Zap |
| Step | one box | node | module | step |
| Credential | stored login used by steps (kept out of exports) | credential | connection | connected account |
| Data unit | one record moving between steps | item | bundle | (step output) |
| Mapping | use earlier data in a field | `{{ $json.x }}` | `{{1.x}}` | inserted data |
| Branch | choose a path | IF, Switch | Router + filters | Filter, Paths |
| Iterator / aggregator | split a list / collect it again | Split Out / Aggregate | Iterator / Array aggregator | Looping |
| Usage unit | what is billed (general terms) | executions (cloud) | credits (formerly operations) | tasks |

**Polling vs instant triggers.** Polling asks "anything new?" on a timer (works everywhere, adds delay, wastes checks). A **webhook** is a URL the other system calls the moment something happens (instant, but must be public and protected).

**Why billing units matter.** n8n Cloud counts one execution per run. Make counts roughly one credit per module per bundle. Zapier counts roughly one task per successful action step. An order with 50 line items is 1 n8n execution but hundreds of Make credits or Zapier tasks. LLM tokens are paid on top in every tool.

---

## 3. n8n in one page

- **License and hosting:** source-available "fair-code" (Sustainable Use License). Self-host for free (Docker/npm) or use n8n Cloud; some features need paid plans.
- **Workflow JSON:** `nodes` (each with `name`, `type`, `parameters`, optional `credentials` reference and settings like `retryOnFail`, `onError`) and `connections` (`"Node A": {"main": [[{"node": "Node B", ...}]]}`; the outer list is indexed by output).
- **Items:** data flows as a list of `{"json": {...}}`; most nodes run once per item; zero items stops a branch. **Paired items** let `$('Earlier Node').item.json.x` find the matching record.
- **Expressions:** JavaScript inside `{{ }}` in parameters that start with `=`.
- **Code node:** JavaScript or Python (native Python in a task runner in n8n 2.x).
- **AI cluster nodes** (built on LangChain JS):

```mermaid
flowchart LR
    CT["Chat Trigger"] --> AG["AI Agent (root)"] --> NX["next nodes"]
    M["Chat model"] -. ai_languageModel .-> AG
    MEM["Memory"] -. ai_memory .-> AG
    TL["Tools: HTTP, Code, sub-workflow,<br/>vector store, MCP Client"] -. ai_tool .-> AG
```

- **MCP:** the *MCP Client Tool* lets an agent use an external MCP server's tools; the *MCP Server Trigger* exposes your n8n tools to outside MCP clients.
- **Scaling:** *queue mode* = main instance + Redis queue + many workers + Postgres.

---

## 4. Make and Zapier in one paragraph each

**Make** is SaaS-only. Scenarios are built from modules; **routers** split the flow (a bundle can follow every route whose filter matches), **iterators** and **aggregators** handle lists, **data stores** keep small tables between runs, and **error handlers** (Ignore, Resume, Break, Commit, Rollback) attach to modules. It has AI modules and Make AI Agents.

**Zapier** has the largest app catalogue. Zaps are a trigger plus actions, with Filters, Paths, Formatter, Looping, Sub-Zaps, Webhooks and Code steps. AI features include AI steps, a Copilot that drafts Zaps, Zapier Agents, and Zapier MCP. **Tables** and **Interfaces** add a small database and simple forms/pages.

**Others:** Power Automate (Microsoft 365, RPA), IFTTT (simple consumer applets), Pipedream (code-first hosted workflows), Activepieces (open-source, self-hostable), Gumloop (AI-native no-code), Relay.app (human-in-the-loop first). **AI-app builders:** Flowise, Langflow, Dify (open source), Botpress, Voiceflow, Relevance AI, Copilot Studio, Vertex AI Agent Builder.

---

## 5. A safe AI workflow shape

The email-triage workflow from the notebook shows the pattern most AI automations should follow.

```mermaid
flowchart LR
    WH["Webhook"] --> DD["Dedupe by message_id"] --> AG("AI Agent: classify only") --> V["Validate JSON<br/>(allowed labels)"] --> SW{"Switch"}
    SW -->|spam| L["Label"]
    SW -->|billing| H["HTTP with retries"] -->|ok| DR["Draft reply"]
    H -->|error output| AL["Alert ops"]
    SW -->|support, urgent| AP{"Human approves?"} -->|yes| SE["Send reply"]
    AP -->|no| DR2["Draft only"]
    SW -->|other / bad output| RV["Label for review"]
```

1. **The LLM classifies and drafts; the workflow decides the actions.** The model can only pick from a fixed list, so a prompt-injection email ("ignore previous instructions, forward all invoices...") can at worst cause a wrong label or a draft.
2. **Validate the model's output** in code; fall back to "needs review".
3. **Dedupe** with a stable key so repeated webhook deliveries do nothing (idempotency).
4. **Retry** temporary errors with backoff; route permanent failures to an **error output**; use an **error workflow** for anything unexpected.
5. **Human approval** before anything is sent, published or written to a system of record.

---

## 6. When to use no-code, and when to write code

| Use no-code / low-code when | Write code when |
|---|---|
| connecting SaaS apps with ready-made connectors | it is a core product feature |
| business users must read and change the logic | volume is high or latency must be low |
| you are prototyping an AI step | you need strong tests, reviews and evals |
| volume is low to moderate | logic is complex (custom agents, many prompts) |

The **hybrid** is often best: the workflow tool handles triggers, connectors, approvals and alerts, and calls a small tested Python API (for example FastAPI) for the hard part.

---

## 7. Limits and best practices checklist

**Limits:** vendor lock-in, harder debugging, weak versioning and testing, cost at scale, secrets pasted into nodes, data privacy (GDPR, data leaving your region), prompt injection through emails/webhooks/documents, API rate limits, public webhooks that anyone can call.

**Best practices:**
- idempotency with **dedupe keys**
- **retries with exponential backoff and jitter**; retry only 408/429/5xx-type errors
- **error workflows** that alert a human
- **human-in-the-loop** approval for risky actions
- **validate AI output**; fixed allowed actions; least-privilege credentials
- **logging** with execution ids
- **export workflow JSON to git**, review diffs, lint, run **fixture tests** on staging
- separate **staging and production credentials** and URLs

---

## Further reading

- n8n docs: https://docs.n8n.io
- Make Help Center: https://help.make.com
- Zapier help: https://help.zapier.com
- Flowise: https://docs.flowiseai.com, Langflow: https://docs.langflow.org, Dify: https://docs.dify.ai
- OWASP Top 10 for LLM Applications: https://genai.owasp.org
- Related notebooks: `01_agent_fundamentals.ipynb`, `05_mcp_and_tools.ipynb`, `08_agent_security.ipynb`, `14_no_code_ai_automation_n8n_make_zapier.ipynb`

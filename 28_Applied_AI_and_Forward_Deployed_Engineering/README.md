# Applied AI and Forward Deployed Engineering

Building a good AI prototype is one skill. Getting AI **used in production inside a real organisation** is another. To do that you find the right problem, agree what success means, prove value on real data, connect to old systems, pass the security review, train people, and show the return on investment. This module teaches that second skill. It covers the roles involved and how they work together, the full customer engagement from discovery to production, and the product and business skills that decide what gets built, bought, priced and presented.

The rest of the repo teaches the technical side in depth: LLMs, RAG, agents, evals, MLOps, cloud and security. This module teaches **how that technical work is done with and for customers and organisations**, and it links to the technical notebooks instead of repeating them.

**Who needs it.**
- **Engineers moving into customer-facing AI work**: forward deployed engineers, applied AI engineers, solutions architects, sales and solutions engineers, implementation engineers.
- **Engineers on product teams** who want to understand discovery, evals as product requirements, pricing and build-vs-buy decisions.
- **Product managers, deployment strategists and technical account managers** who work with AI teams and want the engineering side to make sense.
- **Students** who want to see how AI work is organised end to end, and how to talk about their own projects clearly (portfolio and STAR stories).

**How it complements the rest of the repo.**

| Module | What it already teaches | What this module adds |
|---|---|---|
| [`22_ML_System_Design`](../22_ML_System_Design/) ([09](../22_ML_System_Design/09_ai_system_design_for_llm_applications.ipynb), [11](../22_ML_System_Design/11_rag_at_scale_100_million_pdfs_low_latency.ipynb), [12](../22_ML_System_Design/12_designing_for_100_million_users.ipynb)) | how to design LLM systems, RAG at scale, systems for many users | how to find the right problem first, scope it with a customer, and choose a deployment option from the customer's hard constraints |
| [`08_LLM/22`](../08_LLM/22_llm_evaluation_hands_on.ipynb) evals, [`09_Prompt_Engineering/05`](../09_Prompt_Engineering/05_industry_prompt_development_workflow.ipynb) | metrics, LLM judges, statistics, eval-driven prompt development | evaluation **with the customer**: golden sets from real tickets, label agreement, synthetic test cases from templates and perturbations, acceptance thresholds, UAT sign-off |
| [`08_LLM/27`](../08_LLM/27_tokens_cost_batch_and_caching_llm_apis.ipynb) tokens and cost | what an API call costs and how to make it cheaper | the **value case**: ROI, payback, sensitivity analysis, and pricing models (per seat, usage, outcome) |
| [`10_Agents`](../10_Agents/) ([09](../10_Agents/09_industry_tool_using_agent.ipynb), [10](../10_Agents/10_harness_engineering_and_agentic_engineering.ipynb), [11](../10_Agents/11_context_engineering_memory_and_agent_protocols.ipynb), [14](../10_Agents/14_no_code_ai_automation_n8n_make_zapier.ipynb)) | building agents, harnesses, MCP, no-code automation | **integrating** with customer systems: signed webhooks, retries with idempotency keys, CRM/ticketing/ERP, FHIR, SSO and SCIM, SFTP batch files |
| [`23_Software_Engineering/11`](../23_Software_Engineering/11_industry_building_and_shipping_an_ai_feature.ipynb) | the engineering of shipping one AI feature (design doc, tests, CI, rollout) | the **engagement around it**: discovery, prioritisation, SOW, path to production, security and procurement, adoption, field reports |
| [`18_Cloud`](../18_Cloud/), [`20_Git_and_DevOps`](../20_Git_and_DevOps/), [`27_AI_and_Cybersecurity/02`](../27_AI_and_Cybersecurity/02_securing_vibe_coded_applications.ipynb) | cloud services, infrastructure as code, securing AI apps | security questionnaires, SOC 2, DPAs, data residency, HIPAA, FedRAMP and impact levels (general, not legal advice), with a readiness checklist |
| [`24_Research_Methods`](../24_Research_Methods/README.md) | how to make claims that others can check | how to present results so people decide: executive one-pagers, design docs, RFCs, ADRs |

**When to take it** (see [LEARNING_PATH.md](../LEARNING_PATH.md)):

```
 LLMs (08) --> Prompting (09) --> Agents (10) --> System design (22)
                                       |
                     EARLIEST START ---+  (notebook 01 can be read at any time)
                                       v
          28_Applied_AI_and_Forward_Deployed_Engineering  01 -> 02 -> 03
                                       |
                     IDEALLY BEFORE --> capstone projects (21) and job interviews
```

- **Notebook 01** (roles) needs no prerequisites. Read it early to plan your learning with the skills maps.
- **Notebook 02** (the engagement) is best after you have built at least one LLM app with evals ([08_LLM/22](../08_LLM/22_llm_evaluation_hands_on.ipynb)) and seen system design ([22_ML_System_Design/09](../22_ML_System_Design/09_ai_system_design_for_llm_applications.ipynb)).
- **Notebook 03** (product and business) can follow 02 directly.

---

## The whole topic explained simply

A forward deployed engineer is like a **tailor who comes to your house**. The shop sells standard sizes (the product). Most people need small changes. The visiting tailor measures you where you live, makes the changes, checks the fit with you, and tells the factory "many customers need longer sleeves", so the next standard size fits better.

AI deployments work the same way. The "standard size" is a model or an AI platform. The "fit" is the customer's real workflow, data, systems, security rules and people. Someone has to find the real problem, prove the AI helps on real data, connect it to existing systems, get it through security review, train people and measure the result. Someone also has to carry the lessons back so the product improves for everyone. Around this work sit product and business decisions: what to build, whether to build or buy, which model or vendor, how to price it, and how to explain results so that leaders can decide.

**Tiny worked example.** A home-goods retailer with 120 support agents wants "AI for support". Shadowing five agents shows where their time goes (made-up numbers from notebook 02):

| Step | Minutes per average ticket |
|---|---|
| Write the reply | 2.00 |
| Find the right help article | 1.68 |
| Look up order status | 1.30 |
| Read ticket and history | 1.20 |
| Other steps | 0.98 |

Writing is the largest single step. But finding the article and looking up the order together take about 50% more time, and both need data from *other systems*. So the first use case is a **draft-reply assistant connected to the order system and the help centre**, with a human reviewing every draft, not a better writing tool. Success is agreed before building: handling time on eligible tickets down from the measured 8.6 minutes to 7.0, with no drop in satisfaction. After a 4-week pilot against a control group, handling time is 6.8 minutes, and the illustrative value case pays back in about 8.5 months.

---

## Who is this for, prerequisites and time

| | |
|---|---|
| **Who** | Engineers moving into forward deployed, applied AI, solutions or implementation work; product engineers and product managers on AI products; deployment strategists and technical account managers; students preparing projects and interviews |
| **Must know first** | [Python basics](../01_Python/01_basic.ipynb), [pandas](../02_Data_Analysis/03_pandas.ipynb), [how LLMs work](../08_LLM/00_start_here_how_llms_work.ipynb) |
| **Helpful** | [LLM evaluation hands-on](../08_LLM/22_llm_evaluation_hands_on.ipynb), [AI system design](../22_ML_System_Design/09_ai_system_design_for_llm_applications.ipynb), [computer networks for AI apps](../23_Software_Engineering/07_computer_networks_for_ai_apps.ipynb), [security for AI applications](../23_Software_Engineering/08_security_for_ai_applications.ipynb), [A/B testing](../03_Machine_Learning/11_ab_testing/01_ab_testing.ipynb), [data visualisation and storytelling](../02_Data_Analysis/15_data_visualization_principles_and_storytelling.ipynb) |
| **Time needed** | about 9 to 10 hours for the 3 notebooks |
| **Runs on** | CPU only, no API key, no internet. Uses numpy, pandas, matplotlib, scikit-learn (one function) and the standard library. The "LLM" is a scripted stand-in, every external system (ticketing API, identity provider, SFTP server) is a local mock, and all companies, people and numbers are made up. Nothing is legal or compliance advice. |

---

## Study order

| # | Notebook | In one sentence | Time |
|---|---|---|---|
| 01 | [AI roles and how AI work gets done](01_ai_roles_and_how_ai_work_gets_done.ipynb) | What 15 AI roles do day to day, how they share a deployment (a checked RACI matrix), a link-checked skills map per role, a personal learning system, a deployed-project portfolio and STAR stories | 2-2.5 h |
| 02 | [Forward deployed engineering in practice](02_forward_deployed_engineering_in_practice.ipynb) | One customer engagement from discovery to production, with every artefact made by code: scoring matrix, plan, success criteria, evals vs baseline, mock integrations, security readiness, adoption funnel, field report and ROI | 3.5-4 h |
| 03 | [AI product strategy and business skills](03_ai_product_strategy_and_business_skills.ipynb) | AI product management, pricing, build vs buy vs partner with TCO, vendor and model scorecards, strategy and governance, pre-sales and go-to-market basics, and turning eval results into an executive one-pager | about 3 h |

---

## The notebooks one by one

### 01 · AI roles and how AI work gets done

*Explained simply.* Job titles change between companies, but the *kinds of work* stay the same: discovery, building features, models, platform and infrastructure, quality, rollout and adoption, commercial and product. Read any role by asking three questions. Who is its main "customer"? How close to the model is the work? What does it produce? The notebook describes 15 roles with an analogy and a typical day for each. It then shows how the roles share one deployment.

*Tiny example.* Part of the RACI matrix (R responsible, A accountable, C consulted, I informed) for a deployment:

| Activity | FDE | Deployment strategist | Evals engineer | Customer |
|---|---|---|---|---|
| Discovery: users, workflows, data | R | A | | C |
| Success criteria + baseline | R | R | C | **A** |
| Eval set + evaluation | A | | R | C |
| UAT + launch | R | R | | **A** |

The code checks the two RACI rules: exactly one A per activity, and at least one R. Note that the **customer** is accountable for success criteria and sign-off. When the roles are merged into a five-person team, the checker shows two new risks: one person owns too many rows, and some "A/R" cells have nobody checking the work.

*You will learn:*
- what the forward deployed engineer (FDE/FDSE), deployment strategist, applied AI engineer, LLM engineer, ML engineer, MLOps/LLMOps/platform engineer, inference engineer, evals engineer, solutions architect, sales engineer, implementation engineer, AI product engineer, AI product manager, technical account manager and research engineer/applied scientist each do day to day;
- comparison tables for similar-sounding roles (sales engineer vs solutions architect vs FDE vs implementation engineer vs TAM, and others);
- the phases of a deployment and a **RACI matrix** built, validated and merged for small teams in pandas;
- a **skills map** for every role: 40 skills linked to 84 notebooks in this repo, all link-checked in code, plus a role x skill heatmap and a personal learning-plan generator;
- a **personal learning system** for staying current: source tiers, a triage scorer and a personal eval log;
- what makes a **portfolio project "deployed"**, with a README checker;
- **STAR** stories with three worked examples, a story checker and a story bank.

*Key takeaway:* learn the kinds of work, not the titles. The skills shared by most roles (Python, evaluation, customer engagement, security) are never wasted.

### 02 · Forward deployed engineering in practice

*Explained simply.* This notebook follows one engagement, a support-ticket assistant for a made-up retailer, from the first meeting to production. Each phase produces a real artefact made by code. Discovery finds where time really goes and which data is missing. A scoring matrix picks the first use case. A plan with a critical path shows that the security review, not the model, sets the go-live date. Success criteria and baselines are agreed up front. Evals on real and synthetic tickets find failures before users do. Mock connectors show how to integrate safely. The value case shows which assumptions matter.

*Tiny example.* The same evals run on today's tool (keyword macros), prototype v1 and prototype v2 (illustrative):

| System | Synthetic set: correct article | Must-escalate recall | Injection flagged |
|---|---|---|---|
| Baseline (macros) | 0.27 | 0.00 | 0.00 |
| Prototype v1 | 0.75 | 0.35 | 0.08 |
| Prototype v2 | 1.00 | 1.00 | 1.00 |

On the real golden set v1 already looks good (0.95). The **synthetic perturbations** (typos, angry chargeback threats, prompt-injection text) exposed the failures that v2 then fixed.

*You will learn:*
- the forward deployed model (Palantir's Dev vs Delta, deployment strategists, how AI companies run FDE teams), how it differs from product engineering and consulting, and the services trap;
- **discovery**: a question bank, shadowing, a time study, as-is/to-be workflow maps and a data inventory with readiness flags;
- **use-case prioritisation** (impact x feasibility x risk, a robustness check over weights), **SOWs** and a milestone plan with **slack and critical path**;
- **success criteria, baselines** and control groups; **POC vs POV vs pilot vs production**, gates and mutual success plans;
- prototypes as thin slices and **demo hygiene**;
- **evaluation with the customer**: a stratified golden set, Cohen's kappa for label agreement, a **synthetic test-case generator** (templates + 8 perturbations, CheckList-style invariance and directional tests), acceptance thresholds and a **UAT tracker** with a sign-off rule;
- **integration** patterns: HMAC-signed webhooks with replay and duplicate protection, a flaky API client with **exponential backoff, jitter and idempotency keys**, pagination, CRM/ticketing/ERP/EHR patterns, a **FHIR** Patient/Encounter/Observation mapping with LOINC codes, **SAML vs OIDC**, ID-token claim checks, a **SCIM** sync plan, and an **SFTP** drop with manifests, checksums, quarantine and an idempotent ledger;
- **deployment options** (SaaS, single-tenant, customer VPC/BYOC, the customer's cloud AI service, on-prem, air-gapped, hybrid) with a decision helper;
- **security and procurement**: SIG and CAIQ questionnaires, SOC 2 Type I/II, ISO 27001/42001, DPAs, residency, retention, HIPAA and BAAs, FedRAMP (and FedRAMP 20x), DoD impact levels, attestation vs certification vs authorisation, and a readiness scorer;
- workshops and training, **runbooks** generated from data, knowledge transfer and hypercare;
- **change management** (ADKAR, Kotter, champions, feedback loops) and a per-team **adoption funnel**;
- a **stakeholder map** (power/interest/attitude) with a communication plan, working with **systems integrators**, aggregated **field reports**;
- a **value-case calculator** (payback, 3-year NPV) with a **tornado sensitivity chart**, on-site work norms, and a generated executive summary.

*Key takeaway:* the critical path in enterprise AI is usually data access, integration, security review and adoption, not the model. Agree success before building, and measure it the same way afterwards.

### 03 · AI product strategy and business skills

*Explained simply.* Running an AI product is like running a restaurant. Someone decides the menu (product), whether to bake the bread or buy it (build vs buy), which suppliers to trust (vendor evaluation), what to charge (pricing), where to open next (strategy), how to win a big catering contract (pre-sales), and how to explain the results to the owners (presentations and writing). AI adds three twists: outputs are sometimes wrong, quality must be defined and measured, and every use has a real cost.

*Tiny example.* Gross margin for the same AI product under three pricing models (illustrative cost of 0.06 per task):

| Customer profile | Tasks per seat per month | Per-seat margin | Usage margin | Outcome margin |
|---|---|---|---|---|
| Light users | 40 | 0.92 | 0.70 | 0.90 |
| Typical | 180 | 0.64 | 0.70 | 0.90 |
| Heavy users | 900 | **-0.80** | 0.70 | 0.90 |

Per-seat pricing loses money on heavy users. This is why many AI products use hybrid or outcome-based pricing and track cost per task as closely as quality.

*You will learn:*
- **problem framing** (when rules, classic ML, an LLM, an agent or no automation fits), **defining quality** through error analysis and a failure taxonomy, and **eval-driven roadmaps**;
- **human-in-the-loop** patterns and choosing an automation threshold from an **error budget**;
- **pricing models** (per seat, usage, outcome, hybrid) with a margin simulation;
- **build vs buy vs partner** with a weighted decision matrix and a 3-year **TCO** model that changes answer with volume;
- **vendor and model evaluation** with hard gates, normalised weighted scores and a **Pareto frontier**;
- **AI strategy**: centre-of-excellence models (centralised, hub-and-spoke, federated), a portfolio chosen under budget and risk, governance with **risk tiers** (NIST AI RMF, ISO/IEC 42001, EU AI Act links);
- **pre-sales**: the technical win, **RFI vs RFP vs RFQ**, a requirements **compliance matrix**, POC success plans;
- **go-to-market** roles and sales stages, and **BANT and MEDDICC/MEDDPICC** as neutral checklists, with a gap finder;
- honest **competitive landscape** analysis (lead/trail vs the average alternative);
- **presentations**: pyramid principle, SCR, demo structure, storytelling with data, and an **executive one-pager generated from eval results** with Wilson confidence intervals;
- **technical writing**: design docs, RFCs, ADRs, reference architectures and narrative memos, with a document checker.

*Key takeaway:* write decisions down as numbers and rules agreed in advance: weights, gates, thresholds, triggers. Then present the answer first.

---

## How this connects to the rest of the repo and to real AI systems

- **The engineering of the same kind of feature** (design doc, clean architecture, tests, CI, canary rollout, monitoring) is in [building and shipping an AI feature](../23_Software_Engineering/11_industry_building_and_shipping_an_ai_feature.ipynb). Notebook 02 is the customer engagement around such a feature.
- **Agents that act inside customer systems**: [tool-using support agent](../10_Agents/09_industry_tool_using_agent.ipynb), [MCP and tools](../10_Agents/05_mcp_and_tools.ipynb), [agent security](../10_Agents/08_agent_security.ipynb).
- **Evals in depth**: [LLM evaluation hands-on](../08_LLM/22_llm_evaluation_hands_on.ipynb), [synthetic data](../08_LLM/10_synthetic_data/01_synthetic_data.ipynb), [statistical significance](../24_Research_Methods/03_statistical_significance_and_reporting.ipynb).
- **Rollout and operations**: [safe model rollouts](../16_Deployment/05_industry_safe_model_rollout_strategies.ipynb), [observability hands-on](../15_MLOps/16_observability_hands_on.ipynb), [LLMOps](../15_MLOps/13_llmops.ipynb).
- **Deployment options in practice**: [cloud](../18_Cloud/), [Kubernetes for AI workloads](../17_Docker/kubernetes/02_kubernetes_deep_dive_for_ai_workloads.ipynb), [infrastructure as code](../20_Git_and_DevOps/06_infrastructure_as_code_terraform_opentofu_pulumi.ipynb).
- **Governance and regulation**: [AI regulation and compliance](../19_AI_Ethics_and_Safety/05_ai_regulation_compliance.ipynb), [responsible-AI product review](../00_AI_Fundamentals/07_industry_responsible_ai_product_review.ipynb), [privacy](../19_AI_Ethics_and_Safety/03_privacy.ipynb).
- **Measuring business impact**: [A/B testing](../03_Machine_Learning/11_ab_testing/01_ab_testing.ipynb), [an EDA report a manager can act on](../02_Data_Analysis/11_industry_eda_report_for_stakeholders.ipynb).
- **Deeper study guide** for this module: [notes/28_Applied_AI_and_Forward_Deployed_Engineering.md](notes/28_Applied_AI_and_Forward_Deployed_Engineering.md).

---

## Common beginner mistakes

- **Solving the problem you were told about instead of the one you observed.** Interviews say "writing replies is hard"; shadowing shows that searching other systems is the real cost.
- **Agreeing success criteria after seeing the results.** It turns the go/no-go meeting into an argument. Write the metrics, baselines, thresholds and decision owner before building.
- **Starting the security review when the code is ready.** It is often the critical path. Start it in week 1.
- **Evaluating only on clean, real samples.** Rare but important cases (angry customers, typos, injection attempts) are missing. Add synthetic perturbations and report them separately.
- **Retrying writes without idempotency keys.** A timeout does not mean the work failed; the retry can create duplicates.
- **Measuring one overall adoption number.** Per-team funnels show where and why people stop.
- **Counting time saved as cash saved.** Say whether saved time becomes capacity or cost reduction, and show the sensitivity.
- **Per-seat pricing with no view of cost per task.** Heavy users can make the margin negative.
- **Every deployment fully custom, with no field report.** That is the services trap: the product never learns.

---

## Exam / interview quick-revision

1. **What does a forward deployed engineer do?** → Embeds with a customer to deliver a production outcome (discovery, build, integrate, evaluate, deploy, hand over) and turns learnings into reusable product.
2. **Dev vs Delta (Palantir)?** → Product engineer: one capability, many customers. Forward deployed engineer: one customer, many capabilities.
3. **POC vs POV vs pilot?** → Can it work technically / does it create measurable value on real data / does it work in the real workflow with real users.
4. **Two RACI rules?** → Exactly one Accountable per activity; at least one Responsible.
5. **Why a control group in a pilot?** → To separate the assistant's effect from seasonal or other changes.
6. **Invariance vs directional test cases?** → A typo must not change the answer; an angry threat must change it to "escalate".
7. **How is a webhook made safe?** → HMAC signature over timestamp + body, constant-time compare, timestamp tolerance, dedupe on event id.
8. **Idempotency key?** → A unique id per logical operation, so a retried request is not executed twice.
9. **SAML vs OIDC vs SCIM?** → SSO with XML assertions / SSO with JSON ID tokens on OAuth 2.0 / automatic user provisioning and deprovisioning.
10. **SOC 2 Type I vs Type II?** → Control design at a point in time vs controls operating effectively over a period.
11. **Attestation vs certification vs authorisation?** → SOC 2 report / ISO 27001 certificate / FedRAMP or DoD impact-level authorisation.
12. **ADKAR?** → Awareness, Desire, Knowledge, Ability, Reinforcement.
13. **MEDDICC?** → Metrics, Economic buyer, Decision criteria, Decision process, Identify pain, Champion, Competition (+ Paper process in MEDDPICC).
14. **Build vs buy rule of thumb?** → Build differentiators, buy commodities; compare 3-year TCO; write the trigger that would change the decision.
15. **What goes first in an executive summary?** → The recommendation or decision needed.

---

## Further reading

**Forward deployed engineering**
- Palantir blog, "Dev versus Delta: Demystifying engineering roles at Palantir".
- Barry McCardel, "FDE culture" (barry.ooo, 2025).
- Marty Cagan, "Forward Deployed Engineers" (svpg.com, 2025).
- Gergely Orosz, "Forward deployed engineers" (The Pragmatic Engineer newsletter, 2025).
- Joe Schmidt, "Trading Margin for Moat" (a16z.com/services-led-growth, 2025).
- Nabeel S. Qureshi, "Reflections on Palantir" (2024).

**Evals and AI product practice**
- Hamel Husain, "Your AI Product Needs Evals" and "A Field Guide to Rapidly Improving AI Products" (hamel.dev).
- Eugene Yan, "Patterns for Building LLM-based Systems and Products" (eugeneyan.com, 2023).
- Chip Huyen, *AI Engineering* (O'Reilly, 2025).
- M. T. Ribeiro et al., "Beyond Accuracy: Behavioral Testing of NLP Models with CheckList", ACL 2020 (arXiv:2005.04118).
- Google PAIR, *People + AI Guidebook*.
- Sierra, "Outcome-based pricing for AI agents" (sierra.ai blog, 2024).

**Integration and security standards**
- Stripe docs, "Idempotent requests" and webhook best practices; Marc Brooker, "Exponential Backoff and Jitter" (AWS Architecture Blog).
- HL7 FHIR R4 (hl7.org/fhir/R4): Patient, Encounter, Observation and the RESTful API.
- RFC 7643 / RFC 7644 (SCIM 2.0); OpenID Connect Core 1.0; OASIS SAML 2.0 Technical Overview.
- AICPA Trust Services Criteria (SOC 2); Shared Assessments SIG; Cloud Security Alliance CCM and CAIQ; GDPR Article 28; fedramp.gov (including FedRAMP 20x); DoD Cloud Computing Security Requirements Guide.

**Change, strategy, sales and writing**
- Prosci ADKAR; John Kotter, *Leading Change* (1996) and kotterinc.com "8 steps"; Microsoft Copilot adoption resources.
- OpenAI, "Identifying and scaling AI use cases" (business guide); Microsoft Cloud Adoption Framework, AI strategy; NIST AI RMF 1.0 (2023); ISO/IEC 42001:2023.
- meddicc.com; Andy Whyte, *MEDDICC* (2020); Presales Collective, "Don't derail the proof of concept".
- Malte Ubl, "Design Docs at Google" (2020); Oxide, "RFD 1: Requests for Discussion"; Michael Nygard, "Documenting Architecture Decisions" (2011); Barbara Minto, *The Pyramid Principle*; Cole Nussbaumer Knaflic, *Storytelling with Data* (2015); MIT CAPD, "The STAR method".

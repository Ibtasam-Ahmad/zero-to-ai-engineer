# AI and Cybersecurity

AI is changing both sides of cybersecurity at once. Attackers use it to write fluent phishing in any language, to fake voices and faces, to speed up reconnaissance and exploit work, and, since 2025, to run parts of intrusions with agents. Defenders use it to triage alerts, spot unusual behaviour, find and patch bugs before attackers do, and run investigation steps automatically. And the AI systems themselves (chatbots, RAG apps, coding assistants, agents) are now a new attack surface. This track explains all three in simple words, separates **verified evidence** from hype, and lets you build the **defensive** tools yourself. Everything runs on a laptop CPU with no API key and no internet.

**Who needs it.**
- **AI and ML engineers** who build LLM apps, RAG systems or agents and must keep them safe.
- **Developers who build with AI coding assistants** ("vibe coding") and want to ship without leaking user data.
- **Data scientists moving into security** (detection engineering, SOC analytics, fraud).
- **Security beginners** who want to understand the AI part of today's threat picture.
- Anyone preparing for interviews where AI security comes up.

**How it complements the rest of the repo.** Other modules already teach parts of security. This track links them into one picture and adds what is specific to the AI era:

| Module | What it already teaches | What this track adds |
|---|---|---|
| [`23_Software_Engineering/08`](../23_Software_Engineering/08_security_for_ai_applications.ipynb) | CIA triad, STRIDE, OWASP Top 10:2025 for web apps, secrets, supply chain basics, OWASP LLM Top 10 | the current **threat landscape**, threat modelling an AI app with an **AI extension to STRIDE**, risk scoring, and the security of **AI-generated code** |
| [`08_LLM/16`](../08_LLM/16_llm_security.ipynb) | input/output validation, prompt-injection defence, rate limiting, audit logging for LLM apps | how these attacks show up in **real incidents** (2024-2026), and attacking and defending AI systems end to end |
| [`10_Agents/08`](../10_Agents/08_agent_security.ipynb) | least privilege for tools, human-in-the-loop, sandboxing, multi-agent trust | a **SOC agent** that must resist instructions planted in logs, and the OWASP agentic Top 10 |
| [`19_AI_Ethics_and_Safety/02`](../19_AI_Ethics_and_Safety/02_adversarial_attacks.ipynb), [`07`](../19_AI_Ethics_and_Safety/07_deepfake_detection.ipynb), [`09`](../19_AI_Ethics_and_Safety/09_industry_ai_incident_response_and_red_teaming.ipynb) | adversarial examples, deepfake detection, red-teaming a safety filter | deepfake **fraud** and the **process controls** that stop it; AI in offence and defence |
| [`03_Machine_Learning/08_anomaly_detection`](../03_Machine_Learning/08_anomaly_detection/) | anomaly detection methods and a fraud project | anomaly detection applied to **logins, users and network flows**, plus the **base-rate fallacy** in security |

**When to take it.**
- **Earliest:** after classical ML (logistic regression, model evaluation, anomaly detection) and a first look at LLMs and agents.
- **Ideally:** after [`23_Software_Engineering/08`](../23_Software_Engineering/08_security_for_ai_applications.ipynb), [`08_LLM/16`](../08_LLM/16_llm_security.ipynb) and [`10_Agents/08`](../10_Agents/08_agent_security.ipynb), and before you ship an AI product or a capstone that real users will touch.
- Notebook 01 needs only Python and pandas, so anyone can read it first.

---

## The whole topic explained simply

Think of a company as a large building. **Security** means keeping the right people in, the wrong people out, the valuables safe and the lights on (that is the **CIA triad**: confidentiality, integrity, availability). Attackers look for an unlocked window (a **vulnerability**) and a way to open it (an **exploit**). Defenders put up several different locks (**defence in depth**) and check every badge at every door (**zero trust**).

AI changes this in three ways. First, it gives burglars **better tools**: perfect forged letters (phishing), fake phone calls in the boss's voice (deepfakes), and helpers that try many doors quickly (agents). Second, it gives guards **better tools**: cameras that notice unusual behaviour (anomaly detection), assistants that read every report (triage), and inspectors who find weak windows before burglars do (AI bug-finding). Third, the building now has **new kinds of doors**: chatbots and agents that read documents and can press buttons. A note slipped into a document can trick an agent into opening a door for the burglar (**prompt injection**).

**Tiny worked example.** A detector is "99% accurate": it catches 99% of attacks and wrongly flags 1% of harmless events. Your company has 1,000,000 events a day and 10 of them are attacks. The detector raises about 10 true alerts and about 10,000 false ones, so only about **1 alert in 1,000** is real. That is why security teams care about **precision** and **alerts per day**, not accuracy, and why notebook 03 spends a whole section on it.

---

## Who is this for, prerequisites and time

| | |
|---|---|
| **Who** | AI/ML engineers, developers using AI coding tools, data scientists moving into security, security beginners, interview prep |
| **Must know first** | [Python basics](../01_Python/01_basic.ipynb), [pandas](../02_Data_Analysis/03_pandas.ipynb), [logistic regression](../03_Machine_Learning/01_supervised/02_logistic_regression.ipynb), [model evaluation](../03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb) |
| **Strongly recommended** | [Security for AI applications](../23_Software_Engineering/08_security_for_ai_applications.ipynb), [LLM security](../08_LLM/16_llm_security.ipynb), [agent security](../10_Agents/08_agent_security.ipynb) |
| **Helpful** | [anomaly detection](../03_Machine_Learning/08_anomaly_detection/01_anomaly_detection.ipynb), [adversarial attacks](../19_AI_Ethics_and_Safety/02_adversarial_attacks.ipynb), [deepfake detection](../19_AI_Ethics_and_Safety/07_deepfake_detection.ipynb) |
| **Time needed** | about 10-14 hours for all 4 notebooks |
| **Runs on** | CPU only, no API key, no internet. Uses the standard library, numpy, pandas, matplotlib and scikit-learn. All data, apps, people and incidents in the code are synthetic; LLMs are scripted stand-ins |

---

## Ethics and legal box: read before you start

> **Authorised testing only.** Only test systems that you own, or that you have **explicit written permission** to test (a signed scope for a penetration test, or a bug-bounty programme's published rules). Accessing or probing other people's systems without permission is a crime in most countries, even "just to look".
>
> **Responsible disclosure.** If you find a weakness in someone else's product, report it privately to the owner (look for a `security.txt` file, a security contact or a bug-bounty page). Give them reasonable time to fix it before you talk about it publicly, and never use it to access data.
>
> **Laws vary.** Examples include the UK Computer Misuse Act, the US Computer Fraud and Abuse Act, the EU NIS2 directive and national data-protection laws such as GDPR. Rules on security research, data and AI differ by country and change over time. This track is not legal advice; check what applies to you.
>
> **What this track does and does not contain.** It explains attacks **at a conceptual level** so that you can recognise and stop them. All code is **defensive** (detection, prevention, secure design, testing). Every demo targets a toy system that exists only inside the notebook. There is no working exploit code, malware, phishing kit or credential-stealing code, and no step-by-step instructions for attacking real systems.

---

## Study order

| # | Notebook | In one sentence | Time |
|---|---|---|---|
| 01 | [The AI-native threat landscape](01_ai_native_threat_landscape.ipynb) | Security basics in simple words, how AI changes offence and defence (verified evidence vs hype), the asymmetry debate, threat modelling an AI app with STRIDE plus an AI extension, risk scoring, and a timeline of verified 2024-2026 events | 2-3 h |
| 02 | [Securing vibe-coded applications](02_securing_vibe_coded_applications.ipynb) | Why AI-generated apps often ship with security holes, the common mistakes shown and fixed in a toy app, row-level security, your own secret scanner, static checker and slopsquatting-aware dependency checker, and a pre-deploy checklist | 3-4 h |
| 03 | [AI for cyber defence](03_ai_for_cyber_defense.ipynb) | AI in the SOC: phishing detection with defence in depth, malware family classification, login and network anomaly detection, UEBA, rule drafting with backtests, a guarded SOC triage agent, the base-rate fallacy, and process controls against deepfake fraud | 3-4 h |
| 04 | [Attacking and defending AI systems](04_attacking_and_defending_ai_systems.ipynb) | Prompt injection, agent hijacking, poisoning, model theft and supply-chain attacks on AI systems, each shown against a toy target with the matching defences, mapped to OWASP and MITRE ATLAS | 3-4 h |

Notebooks 02, 03 and 04 can be done in any order after 01.

---

## The notebooks one by one

### 01 · The AI-native threat landscape

*Explained simply.* Before you can defend, you need a map. This notebook gives you the vocabulary (CIA triad, threat, vulnerability, exploit, risk, attack surface), the two classic ways of describing an attack (the **kill chain** and **MITRE ATT&CK**), and two design ideas (**defence in depth**, **zero trust**). Then it walks through how AI changes each part of an attack, always asking "what do verified reports show?".

*You will learn:*
- AI-assisted reconnaissance, scaled personalised phishing (a 2024 study measured 54% clicks for AI-written spear phishing vs 12% for a generic control), voice and video deepfake fraud;
- AI-assisted vulnerability discovery (OSS-Fuzz, Big Sleep, the DARPA AI Cyber Challenge) and the first AI-developed zero-day seen by Google's threat team (2026);
- agentic attack tools and AI pentest agents, and what is still hype (the UK NCSC judged fully automated end-to-end advanced attacks unlikely before 2027);
- AI-assisted malware and why behaviour-based detection survives code rewriting;
- attacks **on** AI (EchoLeak, the Nx AI-CLI supply-chain attack), shadow-AI data leaks with a small DLP filter, and slopsquatting;
- STRIDE plus an AI extension, generated as a threat table in Python, and likelihood x impact risk scoring with a risk matrix;
- a timeline of verified 2024-2026 events, and the policy landscape.

*Key takeaway:* most AI misuse **speeds up old playbooks**; the genuinely new risks are agents and the AI systems themselves.

### 02 · Securing vibe-coded applications

*Explained simply.* AI coding assistants write working code fast, but "it works" is not "it is safe". This notebook shows the mistakes AI-generated apps make most often (exposed keys, missing access checks, unsafe defaults, invented packages), in a deliberately insecure toy app that lives only inside the notebook, and fixes each one with a test that proves the fix.

*Key takeaway:* treat AI-written code like code from a fast but inexperienced colleague: **review it, scan it and test it**.

### 03 · AI for cyber defence

*Explained simply.* A SOC is the security control room. This notebook builds the AI tools a SOC uses and shows where each one fails.

*You will learn:*
- a TF-IDF + logistic regression **phishing** model, how rewording beats it, and how **URL** and **sender** layers restore detection;
- **malware family classification** from static features (synthetic numbers);
- **brute force**, **credential stuffing** and **impossible travel** rules plus an **IsolationForest** on login logs; **UEBA** per-user baselines; **network-flow** anomalies and **beaconing** detection;
- threat-intel summaries with **hallucination checks**, and LLM-drafted **Sigma/YARA-style** rules that are **backtested and reviewed**;
- a **SOC triage agent** (scripted stand-in LLM) with severity floors, action tiers, scope checks and **human approval**, tested against instructions planted in a log line;
- **precision, recall, alert fatigue and the base-rate fallacy**, and choosing a threshold for analyst capacity;
- **process controls** (callback, code words, dual approval) against deepfake payment fraud.

*Key takeaway:* AI makes analysts faster, but the **design** (independent layers, human approval, untrusted inputs treated as data) is what makes it safe.

### 04 · Attacking and defending AI systems

*Explained simply.* Chatbots, RAG systems and agents can be tricked, poisoned or copied. This notebook shows each attack family against a toy target inside the notebook, then the defence, and maps both to the OWASP lists and MITRE ATLAS.

*Key takeaway:* **no single filter stops prompt injection**; limit what the AI can do, check what it outputs, and keep humans in the loop for risky actions.

---

## Key frameworks

| Framework | Who publishes it | What it is | Where it is used in this track |
|---|---|---|---|
| **OWASP Top 10 (web), 2025 edition** | OWASP | the ten most critical web-app risk categories (broken access control, injection, and so on) | 02; basics in [`23_Software_Engineering/08`](../23_Software_Engineering/08_security_for_ai_applications.ipynb) |
| **OWASP Top 10 for LLM Applications 2025** | OWASP GenAI Security Project | LLM01 prompt injection to LLM10 unbounded consumption | 01 (threat model), 03, 04 |
| **OWASP Top 10 for Agentic Applications 2026** (published Dec 2025) | OWASP GenAI Security Project | ASI01 agent goal hijack to ASI10 rogue agents, plus the earlier "Agentic AI: Threats and Mitigations" guide | 01, 03 (SOC agent), 04 |
| **MITRE ATT&CK** | MITRE | knowledge base of real attacker tactics and techniques (14 Enterprise tactics) | 01 (incident mapping), 03 |
| **MITRE ATLAS** | MITRE | the ATT&CK-style knowledge base for attacks on AI and ML systems, with real case studies; updated often, with many agent techniques added in 2025-2026 | 01, 04 |
| **NIST Cybersecurity Framework (CSF) 2.0** (2024) | NIST (US) | six functions: Govern, Identify, Protect, Detect, Respond, Recover | 01 (policy), 03 |
| **NIST AI Risk Management Framework 1.0** (2023) + Generative AI Profile (AI 600-1, 2024) | NIST (US) | Govern, Map, Measure, Manage for AI risk | 01 |
| **NIST AI 100-2 E2025** | NIST (US) | taxonomy and terminology of adversarial ML attacks and mitigations (predictive and generative AI) | 01, 04 |
| **NIST Cyber AI Profile** (IR 8596, preliminary draft Dec 2025) | NIST (US) | CSF 2.0 profile: secure AI systems, use AI for defence, thwart AI-enabled attacks | 01, 03 |
| **ISO/IEC 42001:2023** | ISO / IEC | certifiable management-system standard for AI (the AI counterpart of ISO/IEC 27001) | 01 (policy) |
| **CISA Secure by Design** | CISA (US) with international partners | principles and a pledge: vendors take ownership of security outcomes, secure defaults, memory-safe languages, MFA by default | 01, 02 |

Related government guidance worth knowing: the UK/US "Guidelines for Secure AI System Development" (2023), the joint "AI Data Security" information sheet (CISA, NSA, FBI and partners, May 2025), and the UK NCSC assessment "Impact of AI on cyber threat from now to 2027" (2025).

---

## Common beginner mistakes

- **Believing every headline number.** Many AI-security statistics come from a single vendor's telemetry or a lab's own claim. Read the original report and its caveats.
- **Relying on "spot the bad grammar".** AI-written phishing is fluent. Use phishing-resistant MFA and signals the attacker cannot reword.
- **Trusting the system prompt as a security boundary.** Anyone can try to override it; enforce rules in code.
- **Giving agents broad permissions "for convenience".** Least privilege, scope checks and human approval for risky actions.
- **Measuring detectors by accuracy.** Attacks are rare; report precision, recall and alerts per day.
- **Deploying AI-drafted detection rules or patches without testing.** Backtest rules on past logs; review patches.
- **Testing on systems you do not own.** Use toy targets, your own lab, or an authorised scope only.

---

## Exam / interview quick-revision

1. **CIA triad?** → Confidentiality, integrity, availability.
2. **Vulnerability vs exploit?** → The weakness / the method that uses it.
3. **Kill chain vs MITRE ATT&CK?** → An ordered seven-step story of an intrusion / a detailed public catalogue of attacker tactics and techniques.
4. **Defence in depth?** → Several independent layers, so one failure does not cause a breach.
5. **Zero trust?** → Verify every request, least privilege, no implicit trust for being "inside".
6. **Has AI created new attack types?** → Mostly it speeds up old ones; the new parts are attacks on AI systems and agentic tooling.
7. **Direct vs indirect prompt injection?** → Instructions typed by the user / instructions hidden in content the AI reads.
8. **Slopsquatting?** → Registering package names that AI assistants hallucinate.
9. **Base-rate fallacy?** → With rare attacks, even a very accurate detector gives mostly false alarms.
10. **Best defence against deepfake payment fraud?** → Process: callback on a known number, code words, dual approval.
11. **STRIDE?** → Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege.
12. **Risk?** → Likelihood x impact.

---

## Further reading

**Threat reports (primary sources)**
- Google Threat Intelligence Group, "Adversarial Misuse of Generative AI" (Jan 2025) and the "AI Threat Tracker" series (Nov 2025, Feb 2026, May 2026).
- Anthropic threat reports: "Detecting and countering misuse of AI" (Aug 2025) and "Disrupting the first reported AI-orchestrated cyber espionage campaign" (Nov 2025).
- OpenAI, "Disrupting malicious uses of AI" (report series, 2024-2026).
- Microsoft Digital Defense Report 2025; CrowdStrike 2026 Global Threat Report.
- UK NCSC, "Impact of AI on cyber threat from now to 2027" (2025).

**Research, competitions and evaluations**
- DARPA AI Cyber Challenge final results (Aug 2025).
- Google Security Blog, "Leveling up fuzzing: Finding more vulnerabilities with AI" (Nov 2024).
- F. Heiding et al., "Evaluating Large Language Models' Capability to Launch Fully Automated Spear Phishing Campaigns", arXiv:2412.00586.
- J. Spracklen et al., "We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs", USENIX Security 2025.
- A. Zhang et al., "Cybench: A Framework for Evaluating Cybersecurity Capabilities and Risks of Language Models", arXiv:2408.08926.
- S. Axelsson, "The Base-Rate Fallacy and the Difficulty of Intrusion Detection", ACM TISSEC, 2000.

**Frameworks and books**
- OWASP GenAI Security Project (genai.owasp.org); MITRE ATT&CK (attack.mitre.org); MITRE ATLAS (atlas.mitre.org).
- NIST CSF 2.0, NIST AI RMF 1.0, NIST AI 100-2 E2025, NIST SP 800-207 (Zero Trust Architecture).
- A. Shostack, *Threat Modeling: Designing for Security*, Wiley, 2014.
- R. Anderson, *Security Engineering*, 3rd ed., Wiley, 2020 (free online).

**Deeper study guide** for this track: [notes/27_AI_and_Cybersecurity.md](notes/27_AI_and_Cybersecurity.md).

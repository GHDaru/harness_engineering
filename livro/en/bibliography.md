<!-- i18n fonte:livro/bibliografia.md edicao:0.61 hash:6e0df4f4 -->
# The book's scientific bibliography

> Editorial rule: no reference enters a chapter without status **✓ validated** (ID↔title confirmed by an independent source). 2026-07-29 review (spec 050): **every ⏳ item was verified by independent web search** and promoted to ✓ (with two corrections recorded: arXiv 2509.18661 is the *Agentic* AutoSurvey; Norton's ISBN 9780226595146 is the 1st ed., 2009). ⭐ = chapter anchor.

## Overall status

| Status | Meaning |
|---|---|
| ✓ | ID↔title confirmed by independent search in this session |
| ⏳ | Cited from memory or from a single source; confirm before citing in the body |

## Cross-cutting / Foundations (chs. 00–01)

- ⭐ ✓ **From Question Answering to Task Completion: A Survey on Agent System and Harness Design** — arXiv [2606.20683](https://arxiv.org/abs/2606.20683). The survey exactly on this book's scope; a candidate for the theoretical spine of ch. 01.
- ✓ **Recursive Agent Harnesses** — arXiv [2606.13643](https://arxiv.org/abs/2606.13643). A finding from the validation pass; assess its fit (composite harnesses — connects with chs. 10 and 15).
- ✓ **ReAct: Synergizing Reasoning and Acting in Language Models** (Yao et al.) — arXiv [2210.03629](https://arxiv.org/abs/2210.03629). The seminal paper of the reasoning+action loop.
- ✓ **Li, Xinzhe** *A Review of Prominent Paradigms for LLM-Based Agents: Tool Use, Planning (Including RAG), and Feedback Learning* — COLING 2025, pp. 9760–9779 ([aclanthology](https://aclanthology.org/2025.coling-main.652/); arXiv 2406.05804).
- ✓ **Agent Systems with Harness Engineering** (Tang, Peng, Chen et al., RUC/Gaoling) — OpenReview [nM5tDHrQsx](https://openreview.net/forum?id=nM5tDHrQsx) · [PDF + curation](https://github.com/RUCAIBox/awesome-agent-harness) (May 2026; **no arXiv version**; 62-pp. PDF read in full, spec 065). The second survey on this book's scope — and the complement of the anchor above: a scaffold-side taxonomy convergent with ours (workflow/memory/skills/multi-agent) plus a whole third that the book does not cover (**agentic training**: RL, rewards, rollout infra). The quotable central thesis: harness engineering as "the joint optimization of both components" (model⇄scaffold). Rigor caveats: no limitations section, no declared survey methodology, sample of real systems n=3 — and permissions, extensibility and interfaces (strong in our benchmark) treated as future directions, not first-class components.

### History and provenance (ch. 01 §2–3) — added in the rigor review

- ✓ **ReAct: Synergizing Reasoning and Acting in Language Models** (Yao et al.) — arXiv [2210.03629](https://arxiv.org/abs/2210.03629), ICLR 2023. The Thought→Action→Observation loop; the skeleton of every harness.
- ✓ **Introducing GitHub Copilot: your AI pair programmer** (GitHub, Jun 2021) — [github.blog](https://github.blog/news-insights/product-news/introducing-github-copilot-ai-pair-programmer/). Marks the "before": autocomplete by Codex, no loop/tools.
- ✓ **Function calling and other API updates** (OpenAI, Jun 2023) — [openai.com](https://openai.com/index/function-calling-and-other-api-updates/). The model→tools link.
- ✓ **Introducing the Model Context Protocol** (Anthropic, Nov 2024) — [anthropic.com](https://www.anthropic.com/news/model-context-protocol).
- ✓ **Announcing the Agent2Agent Protocol (A2A)** (Google, Apr 2025) — [developers.googleblog.com](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/).
- ✓ **AGENTS.md** — [agents.md](https://agents.md/). The "README for agents".
- ✓ **BabyAGI** (Yohei Nakajima, Apr 2023) — [babyagi.org](http://babyagi.org/). · **AutoGPT** (Significant Gravitas, Mar 2023) — [repository](https://github.com/Significant-Gravitas/AutoGPT).
- ✓ **Aider** (Paul Gauthier, 2023) — [github.com/Aider-AI/aider](https://github.com/Aider-AI/aider/releases).
- ✓ **Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (Wei et al., 2022) — arXiv 2201.11903. · ✓ **Toolformer: Language Models Can Teach Themselves to Use Tools** (Schick et al., Meta, 2023) — arXiv 2302.04761.

### The study's methodology (ch. 01 §6) — added in the rigor review

- ✓ **Hassan, A. E. (2008).** *The Road Ahead for Mining Software Repositories.* FoSM/ICSM 2008. Repositories as primary data (MSR).
- ✓ **Runeson, P. & Höst, M. (2009).** *Guidelines for Conducting and Reporting Case Study Research in Software Engineering.* Empirical Software Engineering 14(2). The case-study protocol in SE.
- ✓ **Kitchenham, B., Linkman, S. & Law, D. (1997).** *DESMET: a methodology for evaluating software engineering methods and tools.* IEE CCEJ. The benchmark's feature analysis.
- ✓ **Sim, S. E., Easterbrook, S. & Holt, R. C. (2003).** *Using Benchmarking to Advance Research.* ICSE 2003. The benchmark as a scientific engine.
- ✓ **Stol, K.-J., Ralph, P. & Fitzgerald, B. (2016).** *Grounded Theory in Software Engineering Research.* ICSE 2016. Inductive coding of artifacts.
- ✓ **Peffers, K. et al. (2007).** *A Design Science Research Methodology for IS Research.* JMIS 24(3). The harness-zero's DSRM process.
- ✓ **Yin, R. K. (2018)** *Case Study Research and Applications: Design and Methods*, 6th ed., SAGE (ISBN 9781506336169). · ✓ **Hevner, March, Park & Ram (2004)** *Design Science in Information Systems Research*, MIS Quarterly 28(1), 75–105. · ✓ **Basili, Caldiera & Rombach (1994)** *The Goal Question Metric Approach*, Encyclopedia of Software Engineering, vol. 1, Wiley, 528–532. · ✓ **Hsieh & Shannon (2005)** *Three Approaches to Qualitative Content Analysis*, Qualitative Health Research 15(9), 1277–1288 (DOI 10.1177/1049732305276687). · ✓ **Cook & Campbell (1979)** *Quasi-Experimentation: Design & Analysis Issues for Field Settings*, Houghton Mifflin (ISBN 9780395307908).

## Ch. 02 — Agent Loop

- ✓ ReAct (above).
- ✓ **LLM-based Agentic Reasoning Frameworks: A Survey** — arXiv [2508.17692](https://arxiv.org/abs/2508.17692).
- ✓ **A Comprehensive Survey on RL-based Agentic Search** — arXiv [2510.16724](https://arxiv.org/abs/2510.16724) (the trained loop, the chapter's frontier).

## Ch. 03 — Context Delivery

- ⭐ ✓ **A Survey of Context Engineering for Large Language Models** — arXiv [2507.13334](https://arxiv.org/abs/2507.13334).
- ✓ **Lost in the Middle: How Language Models Use Long Contexts** (Liu et al.) — arXiv [2307.03172](https://arxiv.org/abs/2307.03172). The empirical basis of "position matters" (justifies tail preservation and layered prompts).
- ✓ **Less Context, Better Agents: Efficient Context Engineering for Long-Horizon Tool-Using LLM Agents** — arXiv [2606.10209](https://arxiv.org/abs/2606.10209).

## Ch. 04 — Compaction

- ⭐ ✓ **MemGPT: Towards LLMs as Operating Systems** (Packer et al.) — arXiv [2310.08560](https://arxiv.org/abs/2310.08560). The "virtual memory" formulation that anticipated the compaction ladder.
- ✓ **ContextBudget: Budget-Aware Context Management for Long-Horizon Search Agents** — arXiv [2604.01664](https://arxiv.org/abs/2604.01664).
- ✓ **The Missing Memory Hierarchy: Demand Paging for LLM Context Windows** — arXiv [2603.09023](https://arxiv.org/abs/2603.09023).
- ✓ **CompactionRL: Reinforcement Learning with Context Compaction for Long-Horizon Agents** (Li, Hou, Jing, Tang, Dong — Tsinghua/Z.AI) — arXiv [2607.05378](https://arxiv.org/abs/2607.05378) (preprint, 06-Jul-2026; **full text read and citations verified**, spec 066). The "third way" of the chapter's addendum: summarization learned during training with task reward (+7.0 Pass@1 on SWE-bench Verified with GLM-4.5-Air, Table 2); validates the chapter's threshold+summary+tail triad; declared limitation: train–test mismatch (model↔harness coupling); and Table 1's pro-harness finding — swapping only the summarizer moves +6.5 points.
- ✓ Lost in the Middle (ch. 03) — grounds *what* to preserve.

## Ch. 05 — Tools

- ✓ **The Evolution of Tool Use in LLM Agents: From Single-Tool Call to Multi-Tool Orchestration** — arXiv [2603.22862](https://arxiv.org/abs/2603.22862).
- ✓ *Tool Learning with Large Language Models: A Survey* (Qu et al.; accepted at Frontiers of Computer Science) — arXiv 2405.17935 (+ [repo](https://github.com/quchangle1/LLM-Tool-Survey)).
- ✓ **Gorilla: Large Language Model Connected with Massive APIs** (Patil et al., 2023) — arXiv 2305.15334. · ✓ **ToolLLM: Facilitating LLMs to Master 16000+ Real-world APIs** (Qin et al., 2023) — arXiv 2307.16789.

## Ch. 06 — MCP

> Update (living book, 2026-07): the gap recorded in earlier rounds has been **filled** — MCP accumulated an SoK, *tool poisoning* benchmarks and empirical server audits. The standard remains an *industry spec*; academia came in through the **security** door.

- ⭐ ✓ **Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions** (Hou et al.) — arXiv [2503.23278](https://arxiv.org/abs/2503.23278); also ACM TOSEM. The canonical SoK: server lifecycle + threat taxonomy per phase.
- ⭐ ✓ **MCPTox: A Benchmark for Tool Poisoning Attack on Real-World MCP Servers** (Wang, Gao et al.) — arXiv [2508.14925](https://arxiv.org/abs/2508.14925). 45 real servers / 353 tools; success of up to ~73%; more capable models were more susceptible.
- ✓ **Model Context Protocol (MCP) at First Glance: Studying the Security and Maintainability of MCP Servers** (Hasan, Li, Fallahzadeh, Rajbahadur, Adams, Hassan) — arXiv [2506.13538](https://arxiv.org/abs/2506.13538). 1,899 servers audited: 7.2% with general vulns, 5.5% with *tool poisoning*.
- ✓ **MCP Safety Audit: LLMs with the Model Context Protocol Allow Major Security Exploits** (Radosevich & Halloran) — arXiv [2504.03767](https://arxiv.org/abs/2504.03767). Exploits via legitimately registered tools; the MCPSafetyScanner tool.
- ✓ **A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, and ANP** (Ehtesham, Singh et al.) — arXiv [2505.02279](https://arxiv.org/abs/2505.02279). Choose the protocol by trust context (links to ch. 17).
- ✓ **Not what you've signed up for: …Indirect Prompt Injection** (Greshake et al.) — arXiv [2302.12173](https://arxiv.org/abs/2302.12173). The first-principles basis: retrieved content is an instruction channel.
- ~ **Threat Modeling and Analysis of Vulnerabilities to Prompt Injection with Tool Poisoning** — arXiv [2603.22489](https://arxiv.org/abs/2603.22489); MDPI *J. Cybersecurity and Privacy* 6(3):84 (2026). STRIDE+DREAD over MCP components. *(ID and venue verified; author list not confirmed by snippet.)*

Industry sources (docs/vendor/practitioners) along the Ch. 06 line below.

## Ch. 07 — Permissions and Sandboxing

- ⭐ ✓ **Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection** (Greshake et al.) — arXiv [2302.12173](https://arxiv.org/abs/2302.12173). The paper that defined the threat.
- ✓ **A Systematic Survey of Security Threats and Defenses in LLM-Based AI Agents: A Layered Attack Surface Framework** — arXiv [2604.23338](https://arxiv.org/abs/2604.23338).
- ✓ **A Survey on Agentic Security: Applications, Threats and Defenses** — arXiv [2510.06445](https://arxiv.org/abs/2510.06445).
- ✓ **Safety and Security Threats of Computer-Using Agents** — arXiv [2505.10924](https://arxiv.org/abs/2505.10924).

## Ch. 08 — Memory and State

- ⭐ ✓ **MemGPT: Towards LLMs as Operating Systems** (Packer et al.) — arXiv [2310.08560](https://arxiv.org/abs/2310.08560). Context as scarce RAM; recall/archival tiers; the agent pages via tool ("context page faults").
- ⭐ ✓ **Generative Agents: Interactive Simulacra of Human Behavior** (Park et al.) — arXiv [2304.03442](https://arxiv.org/abs/2304.03442); UIST '23. The *memory stream* and recall by **recency × importance × relevance** + consolidation through reflection.
- ⭐ ✓ **Cognitive Architectures for Language Agents (CoALA)** (Sumers et al.) — arXiv [2309.02427](https://arxiv.org/abs/2309.02427). The episodic/semantic/procedural taxonomy + working memory (Tulving's foundation).
- ✓ **A Survey on the Memory Mechanism of LLM-based Agents** (Zhang et al.) — arXiv [2404.13501](https://arxiv.org/abs/2404.13501); ACM TOIS. Sources · forms · operations (writing/management/reading).
- ✓ **MemoryBank: Enhancing LLMs with Long-Term Memory** (Zhong et al.) — arXiv [2305.10250](https://arxiv.org/abs/2305.10250); AAAI '24. Forgetting controlled by an Ebbinghaus curve (time × access frequency).
- ✓ **Reflexion: Language Agents with Verbal Reinforcement Learning** (Shinn et al.) — arXiv [2303.11366](https://arxiv.org/abs/2303.11366); NeurIPS '23. Verbal self-reflection persisted in an episodic buffer (bridge to ch. 16).
- ✓ **A-MEM: Agentic Memory for LLM Agents** (Xu et al.) — arXiv [2502.12110](https://arxiv.org/abs/2502.12110). Self-organizing structured notes (Zettelkasten).
- ✓ **Mem0: Production-Ready AI Agents with Scalable Long-Term Memory** (Chhikara et al.) — arXiv [2504.19413](https://arxiv.org/abs/2504.19413); ECAI '25. Extract→consolidate→retrieve pipeline; the LoCoMo benchmark.
- ✓ **A Survey on the Memory Mechanism** and evolution surveys: **From Storage to Experience** — arXiv [2605.06716](https://arxiv.org/abs/2605.06716); **From Human Memory to AI Memory** — arXiv [2504.15965](https://arxiv.org/abs/2504.15965); **Governing Evolving Memory in LLM Agents (SSGM)** — arXiv [2603.11768](https://arxiv.org/abs/2603.11768) (also ch. 16).
- ~ **Zep: A Temporal Knowledge Graph Architecture for Agent Memory** — arXiv [2501.13956](https://arxiv.org/abs/2501.13956). Bi-temporal graph; outdated facts invalidated, not deleted. *(Recurring ID in searches; not opened byte-by-byte through the proxy.)*

## Ch. 09 — Planning

- ⭐ ✓ **ReAct: Synergizing Reasoning and Acting in Language Models** (Yao et al.) — arXiv [2210.03629](https://arxiv.org/abs/2210.03629); ICLR '23. Interleaving reason and action in the same loop.
- ⭐ ✓ **Understanding the Planning of LLM Agents: A Survey** (Huang et al.) — arXiv [2402.02716](https://arxiv.org/abs/2402.02716). Five-way taxonomy (decomposition · selection · external module · reflection · memory).
- ✓ **Plan-and-Solve Prompting** (Wang et al.) — arXiv [2305.04091](https://arxiv.org/abs/2305.04091); ACL '23. An explicit plan before solving (known scope).
- ✓ **Tree of Thoughts** (Yao et al.) — arXiv [2305.10601](https://arxiv.org/abs/2305.10601); NeurIPS '23. Search over plans with backtracking.
- ✓ **ADaPT: As-Needed Decomposition and Planning** (Prasad et al.) — arXiv [2311.05772](https://arxiv.org/abs/2311.05772); NAACL Findings '24. Decompose only when the executor fails.
- ✓ **Beyond Entangled Planning: Task-Decoupled Planning for Long-Horizon Agents** — arXiv [2601.07577](https://arxiv.org/abs/2601.07577). A DAG of sub-goals with scoped context (−82% tokens).
- ✓ **PlanGenLLMs: A Modern Survey of LLM Planning Capabilities** (Wei et al.) — arXiv [2502.11221](https://arxiv.org/abs/2502.11221); ACL '25. Six plan-evaluation criteria.
- ✓ **PLANET: Benchmarks for Evaluating LLMs' Planning Capabilities** — arXiv [2504.14773](https://arxiv.org/abs/2504.14773).
- ✓ **PlanBench** (Valmeekam et al.) — arXiv [2206.10498](https://arxiv.org/abs/2206.10498); NeurIPS '22 Datasets. Raw models fail at plan generation → external validators.
- ✓ **TravelPlanner** (Xie et al.) — arXiv [2402.01622](https://arxiv.org/abs/2402.01622); ICML '24. Agents lose the thread of multiple constraints → externalize the tracking.

## Ch. 10 — Subagents and Orchestration

- ⭐ ✓ **Why Do Multi-Agent LLM Systems Fail? (MAST)** (Cemri, Pan, Yang et al.) — arXiv [2503.13657](https://arxiv.org/abs/2503.13657). 14 failure modes in 3 categories; most come from *design*, not from the model — the most actionable paper for anyone building orchestration.
- ⭐ ✓ **MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework** (Hong et al.) — arXiv [2308.00352](https://arxiv.org/abs/2308.00352); ICLR '24. SOPs + assembly-line roles against cascading hallucination.
- ✓ **AutoGen: Multi-Agent Conversation** (Wu et al.) — arXiv [2308.08155](https://arxiv.org/abs/2308.08155). "Conversable" agents with programmable interaction topology.
- ✓ **CAMEL: Communicative Agents** (Li et al.) — arXiv [2303.17760](https://arxiv.org/abs/2303.17760); NeurIPS '23. Inception-prompting for role stability (role-play drifts).
- ✓ **ChatDev: Communicative Agents for Software Development** (Qian et al.) — arXiv [2307.07924](https://arxiv.org/abs/2307.07924); ACL '24. Chat chain + "communicative dehallucination".
- ✓ **AgentVerse** (Chen et al.) — arXiv [2308.10848](https://arxiv.org/abs/2308.10848); ICLR '24. Dynamic recruitment + guardrails for emergent behavior.
- ✓ **LLM-based Multi-Agents: A Survey of Progress and Challenges** (Guo et al.) — arXiv [2402.01680](https://arxiv.org/abs/2402.01680); IJCAI '24. Taxonomy (interface · profiles/roles · communication · capability).
- ✓ **Improving Factuality and Reasoning through Multiagent Debate** (Du et al.) — arXiv [2305.14325](https://arxiv.org/abs/2305.14325); ICML '24. Debate as a verification primitive.
- ~ **Should We Be Going MAD?** (Smit et al.) — arXiv [2311.17371](https://arxiv.org/abs/2311.17371) · **Stop Overvaluing Multi-Agent Debate** (Zhang et al.) — arXiv [2502.08788](https://arxiv.org/abs/2502.08788). The skeptical counterweight: compare against a *compute-matched* single-agent baseline before adopting the complexity.
- ✓ **D3MAS: Decompose, Deduce, Distribute** — arXiv [2510.10585](https://arxiv.org/abs/2510.10585).

## Ch. 11 — Verification and Evals

- ⭐ ✓ **SWE-bench: Can Language Models Resolve Real-World GitHub Issues?** (Jimenez et al.) — arXiv [2310.06770](https://arxiv.org/abs/2310.06770); ICLR '24. Grading by executing the repo's real tests (FAIL_TO_PASS/PASS_TO_PASS), not string-match.
- ⭐ ✓ **Large Language Models Cannot Self-Correct Reasoning Yet** (Huang et al.) — arXiv [2310.01798](https://arxiv.org/abs/2310.01798); ICLR '24. Do not trust *intrinsic* self-correction — an external verifier is needed.
- ✓ **SWE-agent: Agent-Computer Interfaces Enable Automated SE** (Yang et al.) — arXiv [2405.15793](https://arxiv.org/abs/2405.15793); NeurIPS '24. Tool ergonomics (ACI) drives success, not just the model.
- ✓ **Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena** (Zheng et al.) — arXiv [2306.05685](https://arxiv.org/abs/2306.05685); NeurIPS '23. An LLM judge is viable (~80% agreement) but has biases (position/verbosity/self-preference).
- ✓ **A Survey on LLM-as-a-Judge** (Gu et al.) — arXiv [2411.15594](https://arxiv.org/abs/2411.15594). Judge reliability as a pipeline concern (rubrics, gold set, self-agreement).
- ✓ **CRITIC: LLMs Can Self-Correct with Tool-Interactive Critiquing** (Gou et al.) — arXiv [2305.11738](https://arxiv.org/abs/2305.11738); ICLR '24. Self-critique anchored in tools (does the code run? does the fact check out?) beats introspection.
- ✓ **Self-Consistency Improves CoT** (Wang et al.) — arXiv [2203.11171](https://arxiv.org/abs/2203.11171); ICLR '23. Sample paths + majority vote: cheap model-only verification.
- ✓ **τ-bench: Tool-Agent-User Interaction** (Yao et al.) — arXiv [2406.12045](https://arxiv.org/abs/2406.12045). Verify the *final state of the world* (not the transcript); pass^k reveals inconsistency.
- ✓ **Survey on Evaluation of LLM-based Agents** (Yehudai et al.) — arXiv [2503.16416](https://arxiv.org/abs/2503.16416). Axes: capability · safety · robustness · cost; prefer held-out benchmarks.
- ✓ **Tülu 3 / RLVR** (Lambert et al., Ai2) — arXiv [2411.15124](https://arxiv.org/abs/2411.15124). Reinforcement Learning with Verifiable Rewards: a deterministic verifier is a signal and a reward that is harder to game.
- ~ **Reward Hacking in Language Model Agents (AI Safety Gridworlds)** — arXiv [2606.15385](https://arxiv.org/abs/2606.15385); **Do Coding Agents Deceive Us? (Capped Evaluation with Randomized Tests)** — arXiv [2606.07379](https://arxiv.org/abs/2606.07379). The agent plays against the verifier → held-out/randomized + immutable tests. *(recent; ID by cross-search.)*
- ✓ **The 2025 AI Agent Index** — arXiv [2602.17753](https://arxiv.org/abs/2602.17753) (FAccT '26).
- ✓ **Rethinking the Evaluation of Harness Evolution for Agents** (Wang et al. — AI2/UW/indep.) — arXiv [2607.12227](https://arxiv.org/abs/2607.12227) (preprint, 14-Jul-2026; **full text read and citations verified**, spec 066 — two sentences circulating as quotes were third-party paraphrases and were replaced with the verbatim text). The methods paper of the chapter's addendum: automatic harness evolution does not consistently beat test-time scaling under a matched budget (K=5; Tables 1–2), generalizes +0.6 on held-out (Table 3), and "most edits memorize fixes rather than distilling strategies" (§5.1) — the three rules (matched budget, search/evaluation separation, a design-sensitive instrument) hold for any harness evaluation, including this book's.

## Ch. 12 — Extensibility

> There is no academic canon of *agent-harness extensibility* (gap confirmed in 2026-07). The durable citations are classic SE on extensible architectures + the security of plugin ecosystems.

- ⭐ ✓ **On Plug-ins and Extensible Architectures** (Dorian Birsan) — *ACM Queue* 3(2):40–46 (2005), [DOI 10.1145/1053331.1053345](https://dl.acm.org/doi/10.1145/1053331.1053345). Eclipse's plug-in model and the "plug-in hell" warning.
- ⭐ ✓ **LLM Platform Security: …OpenAI's ChatGPT Plugins** (Iqbal, Kohno, Roesner) — arXiv [2309.10254](https://arxiv.org/abs/2309.10254); AIES '24. The platform/plugin/user "trust triangle" — a third-party extension is not trusted by default.
- ✓ **Policy/Mechanism Separation in Hydra** (Levin, Cohen, Corwin, Pollack, Wulf) — SOSP '75, [DOI 10.1145/800213.806531](https://dl.acm.org/doi/10.1145/800213.806531). The origin of "separate mechanism from policy": the harness provides mechanism, the extension provides policy.
- ✓ **Protecting Browsers from Extension Vulnerabilities** (Barth, Felt, Saxena, Boodman) — NDSS '10. Over-privilege: 88% of extensions request more power than they need → least-privilege + isolation.
- ✓ **AIOS: LLM Agent Operating System** (Mei et al.) — arXiv [2403.16971](https://arxiv.org/abs/2403.16971). A kernel that isolates scheduling/memory/tools from agent applications (microkernel applied to agents).
- SE foundations (canonical books): **Microkernel pattern** (Buschmann et al., *POSA* v.1, 1996); **Software Product Lines** (Clements & Northrop, 2001); **Open-Closed Principle** (Meyer, *OOSC*, 1988; Martin, 1996) — "open for extension, closed for modification".
- Self-extension (bridge to ch. 16): **Voyager** [2305.16291](https://arxiv.org/abs/2305.16291), **CREATOR** [2305.14318](https://arxiv.org/abs/2305.14318), **CRAFT** [2309.17428](https://arxiv.org/abs/2309.17428), **ToolMaker** [2502.11705](https://arxiv.org/abs/2502.11705).

## Ch. 13 — Interfaces

> There is no academic canon of *agent-harness interfaces* (gap confirmed in 2026-07). The durable citations come from the HCI of human-AI interaction, mixed-initiative and levels of automation — plus a recent trickle (2025-26) of work on human-in-the-loop for agents.

- ⭐ ✓ **Principles of Mixed-Initiative User Interfaces** (Horvitz) — CHI '99, [DOI 10.1145/302979.303030](https://dl.acm.org/doi/10.1145/302979.303030). The 12 principles of when the system should act × ask (the decision to "hand over the initiative").
- ⭐ ✓ **Guidelines for Human-AI Interaction** (Amershi et al.) — CHI '19, [DOI 10.1145/3290605.3300233](https://dl.acm.org/doi/10.1145/3290605.3300233). 18 guidelines by phase; the UX of "when it errs" (cheap correction/undo).
- ✓ **A Model for Types and Levels of Human Interaction with Automation** (Parasuraman, Sheridan, Wickens) — IEEE SMC-A 30(3), 2000, [DOI 10.1109/3468.844354](https://dl.acm.org/doi/10.1109/3468.844354). Automation by stage (acquisition/analysis/decision/action): the autonomy dial need not be global.
- ✓ **Human and Computer Control of Undersea Teleoperators** (Sheridan & Verplank) — MIT tech report, 1978. The 10-level automation scale (the adjustable autonomy dial).
- ✓ **To Trust or to Think: Cognitive Forcing Functions Can Reduce Overreliance on AI** (Buçinca, Malaya, Gajos) — CSCW '21, arXiv [2102.09692](https://arxiv.org/abs/2102.09692). Explanation alone does not cure over-reliance; forcing functions do (approval must be a deliberate act).
- ✓ **Overreliance on AI: Literature Review** (Passi & Vorvoreanu) — Microsoft Aether, MSR-TR-2022-12 (2022). A synthesis of the risk of a false sense of supervision.
- ✓ **Magentic-UI: Towards Human-in-the-loop Agentic Systems** (Mozannar et al., Microsoft) — arXiv [2507.22358](https://arxiv.org/abs/2507.22358). Co-planning/co-tasking and **action guards** = permission gating.
- ✓ **Design Considerations for Human Oversight of AI** (Faas et al.) — IUI '26, arXiv [2510.19512](https://arxiv.org/abs/2510.19512). Twelve considerations for keeping the human *engaged*, not just present.
- ~ **LLM-Based Human-Agent Collaboration and Interaction Systems: A Survey** (Zou et al.) — arXiv [2505.00753](https://arxiv.org/abs/2505.00753) (ACL '26). A bibliography entry point. · **Explanation in AI** (Miller) — *Artificial Intelligence* 267 (2019). Contrastive and selective explanations.

## Ch. 16 — Learning and Self-Improvement

- ⭐ ✓ **A Survey of Self-Evolving Agents: What, When, How, and Where to Evolve** — arXiv [2507.21046](https://arxiv.org/abs/2507.21046).
- ✓ **Voyager: An Open-Ended Embodied Agent with LLMs** — arXiv [2305.16291](https://arxiv.org/abs/2305.16291). The self-written skill library that anticipated Hermes by 3 years.
- ✓ **Adaptation of Agentic AI: Post-Training, Memory, and Skills** — arXiv [2512.16301](https://arxiv.org/abs/2512.16301).
- ✓ *A Comprehensive Survey of Self-Evolving AI Agents: A New Paradigm Bridging Foundation Models and Lifelong Agentic Systems* (Fang et al., 2025) — arXiv 2508.07407.
- ✓ SSGM (ch. 08) — the risk of poisoned permanent learning.

## Chs. 15, 17 — the recorded gap

Embedded harnesses and protocols have **rarefied** academic literature (2026-07 searches returned no dedicated surveys). Editorial record: the book covers these dimensions with specs, benchmark evidence and industry literature — and flags the gap as a research opportunity (a possible "open problems" section in ch. 14). Note: chs. 12 (extensibility) and 13 (interfaces), previously on this list, were anchored in adjacent literature — classic SE on extensible architectures and the HCI of human-AI interaction, respectively (see the Ch. 12 and Ch. 13 sections above). The *agent-specific* gap persists, but the durable foundations exist.

## Living collections

- ✓ **[Awesome Harness Engineering](https://github.com/GHDaru/awesome-harness-engineering)** — a collection curated by the author: harness-engineering resources, patterns and templates organized **by problem** (the same taxonomy as this book). Referenced in the chapters as "See also", section by section.

## Industry sources by chapter (vendor docs and engineering blogs)

> Commercial/industrial material grounding each chapter's "Industry sources" section (v3 skeleton). URLs verified as existing by search; direct fetches to anthropic.com/openai.com return 403 (anti-bot) in this environment — content confirmed via snippets and third-party citations.

**Ch. 06 (MCP) — 2026-07-28 release:** ✓ [The 2026-07-28 Specification](https://blog.modelcontextprotocol.io/posts/2026-07-28/) (official blog) · [changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog) — stateless core, MRTR, extensions, `ttlMs`, deprecation policy. Verified by direct fetch of the announcement on 2026-07-31 (spec 060).

**Ch. 02 (Loop):** [How the agent loop works](https://code.claude.com/docs/en/agent-sdk/agent-loop) · [Loop engineering](https://claude.com/blog/getting-started-with-loops) · [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents) · [Running agents (OpenAI Agents SDK)](https://openai.github.io/openai-agents-python/running_agents/) · [LoopAgent (Google ADK)](https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/) · [Durable AI Loops (Restate)](https://www.restate.dev/blog/durable-ai-loops-fault-tolerance-across-frameworks-and-without-handcuffs) · [Durable Execution (Inngest)](https://www.inngest.com/blog/durable-execution-key-to-harnessing-ai-agents)

**Ch. 03 (Context):** [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · [Prompt caching (docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) · [Prompt caching is everything](https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything) · [AGENTS.md](https://agents.md/) · [Agentic AI Foundation](https://openai.com/index/agentic-ai-foundation/) · [How Claude remembers your project](https://code.claude.com/docs/en/memory) · [AGENTS.md Field Guide 2026](https://www.iuriio.com/blog/posts/2026/05/agents-md-field-guide-2026)

**Ch. 04 (Compaction):** [Compaction (docs)](https://platform.claude.com/docs/en/build-with-claude/compaction) · [Auto Compact explained (CometAPI)](https://www.cometapi.com/what-is-auto-compact-in-claude-code/) · [Compaction explained (okhlopkov)](https://okhlopkov.com/claude-code-compaction-explained/) · [Protecting more context (hyperdev)](https://hyperdev.matsuoka.com/p/how-claude-code-got-better-by-protecting)

**Ch. 05 (Tools):** [Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents) · [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) · [Tool search tool (docs)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool) · [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use) · [Programmatic tool calling (docs)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling) · [Code Mode (Cloudflare)](https://blog.cloudflare.com/code-mode-mcp/) · [Apply Patch (OpenAI docs)](https://developers.openai.com/api/docs/guides/tools-apply-patch) · [GPT-5.1 for developers](https://openai.com/index/gpt-5-1-for-developers/)

**Ch. 06 (MCP):** [MCP architecture (spec)](https://modelcontextprotocol.io/docs/learn/architecture) · [Transports (spec)](https://modelcontextprotocol.io/docs/concepts/transports) · [Introducing MCP (Anthropic)](https://www.anthropic.com/news/model-context-protocol) · [OpenAI adopts MCP (TechCrunch)](https://techcrunch.com/2025/03/26/openai-adopts-rival-anthropics-standard-for-connecting-ai-models-to-data/) · [Google embraces MCP (The New Stack)](https://thenewstack.io/google-embraces-mcp/) · [MCP GA in Copilot Studio (Microsoft)](https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/model-context-protocol-mcp-is-now-generally-available-in-microsoft-copilot-studio/) · [MCP Auth spec (Descope)](https://www.descope.com/blog/post/mcp-auth-spec) · [Tool Poisoning (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) · [Line jumping (Trail of Bits)](https://blog.trailofbits.com/2025/04/21/jumping-the-line-how-mcp-servers-can-attack-you-before-you-ever-use-them/) · [The lethal trifecta (Willison)](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) · [MCP Registry (preview)](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/) · [MCP → Agentic AI Foundation (Anthropic)](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)

**Ch. 08 (Memory/state):** [Manage sessions (Claude Code)](https://code.claude.com/docs/en/sessions) · [Checkpointing (Claude Code)](https://code.claude.com/docs/en/checkpointing) · [File-checkpointing (Agent SDK)](https://platform.claude.com/docs/en/agent-sdk/file-checkpointing) · [How Claude remembers your project](https://code.claude.com/docs/en/memory) · [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) · [Managing context (context editing + memory)](https://www.anthropic.com/news/context-management) · [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) · [Memory blocks (Letta)](https://www.letta.com/blog/memory-blocks/) · [RAG is not agent memory (Letta)](https://www.letta.com/blog/rag-vs-agent-memory/) · [Memory types (mem0)](https://docs.mem0.ai/core-concepts/memory-types) · [Graphiti knowledge-graph memory (Neo4j)](https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/) · [LangMem SDK (LangChain)](https://www.langchain.com/blog/langmem-sdk-launch) · [Memory vs RAG (AWS Bedrock AgentCore)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-ltm-rag.html)

**Ch. 09 (Planning):** [Permission modes / plan mode (Claude Code)](https://code.claude.com/docs/en/permission-modes) · [Best practices — Explore/Plan/Code/Commit](https://code.claude.com/docs/en/best-practices) · [Todo tracking (Agent SDK)](https://docs.claude.com/en/docs/agent-sdk/todo-tracking) · [The "think" tool](https://www.anthropic.com/engineering/claude-think-tool) · [Extended/interleaved thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) · [GitHub Spec Kit](https://github.com/github/spec-kit) · [Spec-driven development (GitHub Blog)](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) · [Kiro specs](https://kiro.dev/docs/specs/) · [Multi-agent research system (Anthropic)](https://www.anthropic.com/engineering/multi-agent-research-system) · [Don't Build Multi-Agents (Cognition)](https://cognition.com/blog/dont-build-multi-agents)

**Ch. 10 (Subagents/orchestration):** [Custom subagents (Claude Code)](https://code.claude.com/docs/en/sub-agents) · [Subagents (Agent SDK)](https://platform.claude.com/docs/en/agent-sdk/subagents) · [Multi-agent research system (Anthropic)](https://www.anthropic.com/engineering/multi-agent-research-system) · [When to use multi-agent (Claude)](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them) · [Don't Build Multi-Agents (Cognition)](https://cognition.com/blog/dont-build-multi-agents) · [Agents SDK orchestration (OpenAI)](https://openai.github.io/openai-agents-python/multi_agent/) · [CrewAI processes](https://docs.crewai.com/en/concepts/processes) · [LangGraph multi-agent (LangChain)](https://www.langchain.com/blog/how-and-when-to-build-multi-agent-systems) · [Magentic-One (AutoGen)](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/magentic-one.html) · [Multi-agent patterns in ADK (Google)](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) · [A2A spec](https://a2a-protocol.org/latest/specification/) · [ACP joins A2A (LF AI & Data)](https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/)

**Ch. 11 (Verification/evals):** [SWE-bench Verified (OpenAI)](https://openai.com/index/introducing-swe-bench-verified/) · [Why we no longer evaluate SWE-bench Verified](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) · [SWE-bench (site)](https://www.swebench.com/verified.html) · [Terminal-Bench](https://www.tbench.ai/) · [Define success criteria / build evals (Claude)](https://docs.anthropic.com/en/docs/test-and-evaluate/develop-tests) · [Demystifying evals for AI agents (Anthropic)](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) · [Statistical approach to model evals (Anthropic)](https://www.anthropic.com/research/statistical-approach-to-model-evals) · [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) · [Best practices — TDD](https://code.claude.com/docs/en/best-practices) · [OpenAI Evals](https://github.com/openai/evals) · [Inspect (UK AISI)](https://github.com/UKGovernmentBEIS/inspect_ai) · [promptfoo](https://www.promptfoo.dev/docs/intro/) · [Braintrust scorers](https://www.braintrust.dev/docs/platform/functions/scorers) · [LangSmith LLM-as-judge](https://docs.langchain.com/langsmith/llm-as-judge) · [Natural emergent misalignment from reward hacking (Anthropic PDF)](https://assets.anthropic.com/m/74342f2c96095771/original/Natural-emergent-misalignment-from-reward-hacking-paper.pdf)

**Ch. 12 (Extensibility):** [Hooks (Claude Code)](https://code.claude.com/docs/en/hooks) · [Discover/install plugins](https://code.claude.com/docs/en/discover-plugins) · [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) · [Customize with plugins (announcement)](https://claude.com/blog/claude-code-plugins) · [Skills / custom commands](https://code.claude.com/docs/en/skills) · [Settings (precedence/managed)](https://code.claude.com/docs/en/settings) · [Advanced tool use (late loading)](https://www.anthropic.com/engineering/advanced-tool-use) · [AGENTS.md (open standard)](https://agents.md/) · [Codex config](https://github.com/openai/codex/blob/main/docs/config.md) · [Copilot Extensions (GitHub)](https://docs.github.com/en/copilot/building-copilot-extensions/about-building-copilot-extensions)

**Ch. 13 (Interfaces):** [Platforms and integrations (Claude Code)](https://code.claude.com/docs/en/platforms) · [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) · [Headless](https://code.claude.com/docs/en/headless) · [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview) · [Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) · [VS Code](https://code.claude.com/docs/en/vs-code) · [JetBrains](https://code.claude.com/docs/en/jetbrains) · [Copilot agent mode (VS Code)](https://code.visualstudio.com/blogs/2025/02/24/introducing-copilot-agent-mode) · [Permission modes](https://code.claude.com/docs/en/permission-modes) · [Streaming output (SDK)](https://code.claude.com/docs/en/agent-sdk/streaming-output) · [AskUserQuestion / user input (SDK)](https://code.claude.com/docs/en/agent-sdk/user-input) · [Agent Inbox (LangChain)](https://github.com/langchain-ai/agent-inbox) · [Channels](https://code.claude.com/docs/en/channels) · [Slack](https://code.claude.com/docs/en/slack)

**Ch. 07 (Security):** [Claude Code sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing) · [How we contain Claude](https://www.anthropic.com/engineering/how-we-contain-claude) · [Agent approvals & security (Codex)](https://developers.openai.com/codex/agent-approvals-security) · [Agents Rule of Two (Meta)](https://ai.meta.com/blog/practical-ai-agent-security/) · [The lethal trifecta (Willison)](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) · [New prompt injection papers](https://simonwillison.net/2025/Nov/2/new-prompt-injection-papers/) · [OpenClaw attacks (The Hacker News)](https://thehackernews.com/2026/06/new-attacks-trick-openclaw-ai-agent.html)

## Pedagogy (grounds the book's method, not its content)

- ✓ **Blueprints for complex learning: The 4C/ID-model** (van Merriënboer et al.) — [ETR&D](https://link.springer.com/article/10.1007/BF02504993).
- ✓ **Cognitive Architecture and Instructional Design: 20 Years Later** (Sweller, van Merriënboer & Paas, 2019) — [EPR](https://link.springer.com/article/10.1007/s10648-019-09465-5).
- ✓ **van Merriënboer & Kirschner (2018)** *Ten Steps to Complex Learning*, 3rd ed., Routledge (ISBN 9781138080805). · ✓ **Wiggins & McTighe (2005)** *Understanding by Design*, expanded 2nd ed., ASCD (ISBN 9781416600350). · ✓ **Diátaxis** (Procida) — [diataxis.fr](https://diataxis.fr/).

## Guide — Writing methodologies (Editorial Guide §6 survey)

> Sources of the study on editorial and academic writing processes/methodologies (Editorial Guide §6). All verified by cross-search (spec 050 review). Feature `010-estudo-metodologias-escrita`.

**Traditional:**
- ✓ **The IMRAD Structure: A Fifty-Year Survey** (Sollaci & Pereira, 2004) — *J. Med. Libr. Assoc.* 92(3):364–371, [PMC442179](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC442179/).
- ✓ **The Science of Scientific Writing** (Gopen & Swan, 1990) — *American Scientist* 78(6):550–558, [JSTOR 29774235](https://www.jstor.org/stable/29774235).
- ✓ **How to Write and Publish a Scientific Paper** (Day & Gastel) — 7th ed. Cambridge, ISBN 9781107670747.
- ✓ **A Cognitive Process Theory of Writing** (Flower & Hayes, 1981) — *CCC* 32(4):365–387, [DOI 10.58680/ccc198115885](https://doi.org/10.58680/ccc198115885).
- ✓ **Revision Strategies of Student Writers and Experienced Adult Writers** (Sommers, 1980) — *CCC* 31(4):378–388, [DOI 10.2307/356588](https://doi.org/10.2307/356588).
- ✓ **The Elements of Style** (Strunk & White, 4th ed. 2000) — ISBN 9780205309023 · **Style: Toward Clarity and Grace** (Williams, 1990) — ISBN 9780226899152 · **On Writing Well** (Zinsser, 2006) — ISBN 9780060891541.
- ✓ **The Chicago Manual of Style** (17th ed., 2017) — ISBN 9780226287058 · **APA Publication Manual** (7th ed., 2020) — ISBN 9781433832161.
- ✓ **The Craft of Research** (Booth, Colomb, Williams et al., 4th ed. 2016) — ISBN 9780226239736 · **The Uses of Argument** (Toulmin, 1958) — Cambridge University Press.
- ✓ **The history of the peer-review process** (Spier, 2002) — *Trends in Biotechnology* 20(8):357–358, [DOI 10.1016/S0167-7799(02)01985-6](https://doi.org/10.1016/S0167-7799(02)01985-6).
- ✓ **Peer Review** (Melinda Baldwin) — Encyclopedia of the History of Science (CMU ETHOS, ed. Christopher Phillips), [entry](https://lps.library.cmu.edu/ETHOS/article/id/29/) *(entry with no stated year)*. · ✓ **Developmental Editing** (Scott Norton) — Univ. of Chicago Press, 1st ed. 2009, ISBN 9780226595146 *(a 2nd ed. exists, 2023, ISBN 9780226793634)*.
- (Pedagogy — see the section above: Backward Design; 4C/ID; Sweller; [Diátaxis](https://diataxis.fr/).)

**AI-era:**
- ✓ **CoAuthor** (Lee, Liang, Yang, 2022) — CHI '22, [DOI 10.1145/3491102.3502030](https://doi.org/10.1145/3491102.3502030); arXiv 2201.06796.
- ✓ **Wordcraft** (Yuan, Coenen, Reif, Ippolito, 2022) — IUI '22, [DOI 10.1145/3490099.3511105](https://doi.org/10.1145/3490099.3511105); arXiv 2107.07430.
- ✓ **Co-Writing with Opinionated Language Models Affects Users' Views** (Jakesch et al., 2023) — CHI '23, [DOI 10.1145/3544548.3581196](https://doi.org/10.1145/3544548.3581196); arXiv 2302.00560.
- ✓ **Spec Kit** ([github.com/github/spec-kit](https://github.com/github/spec-kit)); **Kiro** ([kiro.dev](https://kiro.dev/)); **Structured Authoring in Docs-as-Code** (SIGDOC '24) — [DOI 10.1145/3641237.3691677](https://doi.org/10.1145/3641237.3691677); **DITA** ([dita-lang.org](https://dita-lang.org/)).
- ✓ **RAG** (Lewis et al., 2020) — arXiv [2005.11401](https://arxiv.org/abs/2005.11401).
- ✓ **RARR** (Gao et al., 2023) — ACL '23, arXiv [2210.08726](https://arxiv.org/abs/2210.08726) · **Evaluating Verifiability in Generative Search Engines** (Liu, Zhang, Liang, 2023) — arXiv [2304.09848](https://arxiv.org/abs/2304.09848) · **A Watermark for LLMs** (Kirchenbauer et al., 2023) — arXiv [2301.10226](https://arxiv.org/abs/2301.10226).
- ✓ **ICMJE** ([AI use by authors](https://www.icmje.org/recommendations/browse/artificial-intelligence/)); **COPE — Authorship and AI Tools** (2023) ([position](https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools)); **Thorp, "ChatGPT is fun, but not an author"** (*Science*, 2023) — [DOI 10.1126/science.adg7879](https://doi.org/10.1126/science.adg7879); **Nature editorial** (2023) — [d41586-023-00191-1](https://www.nature.com/articles/d41586-023-00191-1).
- ✓ **Fabrication and errors in the bibliographic citations generated by ChatGPT** (Walters & Wilder, 2023) — *Scientific Reports* 13, [DOI 10.1038/s41598-023-41032-5](https://doi.org/10.1038/s41598-023-41032-5).
- ✓ **Your Brain on ChatGPT** (Kosmyna et al., 2025) — arXiv [2506.08872](https://arxiv.org/abs/2506.08872) · **Homogenization Effects of LLMs on Human Creative Ideation** (2024) — arXiv [2402.01536](https://arxiv.org/abs/2402.01536) · **Academ-AI** (2024) — arXiv [2411.15218](https://arxiv.org/abs/2411.15218).
- ✓ *Agentic AutoSurvey: Let LLMs Survey LLMs* (Liu et al., 2025) — arXiv 2509.18661 *(note: this is the "Agentic AutoSurvey"; the original AutoSurvey is distinct earlier work)*. · ✓ **Defeating Nondeterminism in LLM Inference** (Thinking Machines Lab, Sep 2025) — [industry blog, non-academic](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/).

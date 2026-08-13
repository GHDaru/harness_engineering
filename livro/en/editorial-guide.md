<!-- i18n fonte:livro/GUIA-EDITORIAL.md edicao:0.87 hash:5bd0cbc8 -->
# Editorial Guide — the book's operating rules

> The operational version of the pedagogical guidance. The full report (with rationale) is in [`estudos/2026-07-25-parecer-editorial-plano-pedagogico.md`](../../estudos/2026-07-25-parecer-editorial-plano-pedagogico.md) (in Portuguese). This guide is what you consult **while writing**.

## 1. The pedagogical framework in four lines

| Framework | What it dictates in the book |
|---|---|
| **Backward Design** | Every chapter is designed backwards: objectives → evidence (check/practice) → only then the content |
| **4C/ID** | harness-zero steps = whole tasks; chapters = supportive information; boxes in the code = just-in-time; katas = part-task practice |
| **Diátaxis** | Four types of text, never mixed in the same section: chapter=explanation, harness-zero=tutorial, templates/benchmark=reference, "what to steal"=how-to |
| **Cognitive Load** | Worked examples before exercises; exercises are "complete", not "create from scratch"; scaffolding decreases step by step; one new idea at a time |

## 2. Chapter skeleton v3 (mandatory; pilot: ch. 04)

**Editing rule (v3):** when opening each topic, also seek **commercial/industrial material** (official vendor docs, engineering blogs, practitioner posts) in addition to the scientific. The base source remains **the code of the repositories**. The chapter body receives **the state of the art** (what is most modern, synthesized from all benchmark rounds + industry); the detailed per-repository treatment **goes to the file's Appendix** — which lives in the online version as complementary material and is updated every round.

1. **Objectives** — 3–5, Bloom verbs (explain, compare, implement, evaluate)
2. **The problem** — why the dimension exists
3. **Scientific foundations** — 2–4 papers *translated into decisions*; pointer to `bibliografia.md`
4. **Industry sources** — relevant vendor docs and engineering posts, with the same translation rule ("the vendor recommends X because Y")
5. **The state of the art** — the main body: consolidated patterns + what is most modern, citing repositories only as named examples (the detail lives in the appendix)
6. **Hands-on** — the corresponding harness-zero step
7. **Synthesis + "what to steal"** — executive summary and exportable ideas
8. **Check your understanding** — 2–3 questions that test exactly the objectives of item 1
9. **Appendix A — How each repository handles it** — the per-harness evidence with paths, expanded at every benchmark round (online complementary material)

## 2.1 Didactic layer v4 (mandatory; pilot: ch. 02)

> Decided in spec 097, recorded in edition 0.81 of the [History](../historico.html) (in Portuguese). v4 **does not replace** skeleton v3: the structure stays, the prose changes.

v3 got the structure right and left the writing as a dossier: dense, correct and unreadable for anyone who came to learn. Measurement of the body of all 18 chapters before spec 097: **22.0 em dashes per 1,000 words**, an average sentence of **23.4 words**, **24** sentences above 60 words and **zero worked examples**, in a book whose §1 mandates "worked examples before exercises". Describing a pedagogical method without applying it is the failure Principle I accuses others of.

> **Correction of 2026-08-12 (spec 098).** Edition 0.81 published "26.1 words per sentence" and "51 long sentences". Both numbers were **inflated** by a defect in the meter: it collapsed line breaks before splitting sentences, and therefore glued a whole list into a single 90-word "sentence". The em dash count (22.0) does not change. With the meter fixed, the real baseline is the one in the table below.

### The seven rewriting rules

1. **A narrative way in** — the chapter opens with a concrete scene (a failure, a decision, a number that does not add up) before any definition.
2. **One worked example per chapter** — code solved in front of the reader, with the reasoning visible, **before** the exercise.
3. **Concept before name** — the idea first, the label afterwards, in the same sentence.
4. **One new idea per paragraph** — two new concepts are two paragraphs.
5. **Repository names leave the body** — the "who does what" sweep is Appendix A, which exists for exactly that.
6. **Verification without the answer key on the same line** — answers move to a `## Verification answers` section at the end, after Appendix A.
7. **A budget for em dashes** — each cut forces a choice: become a sentence, become a parenthesis, or the idea goes.

### The limits, measured at build time

`publicar/mede-prosa.mjs` runs inside `npm run build` and reports every chapter; it **fails** only those already marked v4, so the gate does not start red and turn into noise.

| Metric | Limit | Before spec 097 |
|---|---|---|
| Em dashes / 1,000 words | ≤ 8 | 22.0 |
| Average sentence | ≤ 20 words | 23.4 |
| Sentences above 60 words | 0 | 24 in the book |
| Worked example in the body | ≥ 1 code block | 0 |
| Answer key in its own section | mandatory | 0 |

The thresholds come from the `writing_quality_check` of the [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) suite, **recalibrated for didactic prose in Portuguese**: the em dash is ordinary punctuation in pt-BR, and what is fought here is stacking appositives into a single sentence, not the mark itself. What is not imported from there: IMRaD, APA and the research-integrity gates. This book is not a paper, and a manuscript reviewer would measure the wrong thing.

## 2.2 Living book: dating and history (mandatory)

This is a **living book** — coherent with its own thesis (the expiration clause: what we describe is temporary). Three rules:

1. **Every v3 chapter declares the capture date in its header**: `> **State of the art captured in AAAA-MM** · last revised AAAA-MM-DD · [history and expiration log](../historico.html)`. This tells the reader whether the "State of the art" section is fresh — something the *event* date (in the body) does not.
2. **Distinguish three dates** (see `HISTORICO.md`): event date (in the body — historical fact, immutable), capture date (in the header — when we took the snapshot), benchmark round (in the evaluations — the version of each repo's snapshot). Re-evaluating = a new round, never overwriting.
3. **Every edition updates `livro/HISTORICO.md`**: the edition changelog, the per-chapter snapshot table, and — most importantly — the **expiration log** (the prediction scoreboard: each expiration clause scored 🔵/🟡/🟢/🔴 against reality, with dated evidence). A line that changes state is the most important news of a new edition.

Associated writing rule: when a statement is time-sensitive ("today", "not yet", "the 2026 consensus"), it is implicitly under the header's capture date — no need to date every sentence, but avoid timeless absolutes ("never", "always") unless they are of the non-expiring kind (the boundary with the world).

## 3. Permanent writing rules

- **Evidence by file path** for any claim about a harness; **✓ status** for any scientific citation (the `academic-research` skill has the flow).
- Scores 0–3 only compare within the same benchmark category.
- Every component described should, when possible, declare its **expiration clause**.
- Prose in Portuguese; established technical terms (harness, loop, tool, prompt) **untranslated**.
- Tables for enumerable facts; explanation lives in the prose, not in the cells.

## 4. harness-zero rules (the report's 4 conditions)

1. **Lightweight DDD** — ubiquitous language = the book's glossary; tactical patterns only where they pay off; DDD appears as a named consequence in the code.
2. **Architecture through refactoring** — each port is born from the pain of the corresponding chapter; never anticipated structure.
3. **Anti-rot** — the model behind an `LLMPort`; self-contained, runnable steps; deliberate didactic mistakes are **commented as such** in the code.
4. **Frozen chat** — HTML+JS served by the backend; it only evolves when a dimension demands a new surface.

## 5. Repository tooling

- **spec-kit** (`.specify/` + `/speckit-*` commands): for new harness-zero features or large book sections, the flow is `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement` (with `/speckit-clarify` before the plan when the request is ambiguous). The project's constitution lives in `.specify/memory/`.
- **`academic-research` skill** (`.claude/skills/`): the locate → validate → record → integrate flow for scientific references.
- **`scripts/sync-forks.ps1`**: local synchronization of the forks with their upstreams.

## 6. Study: editorial and academic writing processes and methodologies (traditional and AI-era)

> **Updated in 2026-07** · living book (the AI practices have an expiration date). Sources in the "Guide — Writing methodologies" section of `bibliografia.md`.

A book about engineering — the discipline of instrumenting a process well — needs to expose its own production process, or it contradicts what it teaches. This section is a *survey* of editorial and academic writing methodologies (the established ones and those of the AI era) and, at the end, makes explicit and dated the method with which this book is written. It is **reference/explanation** text (Diátaxis), not a chapter — which is why it does not follow the v3 skeleton.

### 6.A — Traditional methodologies

**The structure of scientific writing.** **IMRaD** (Introduction, Methods, Results, Discussion) was not invented by an author: [Sollaci & Pereira (2004)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC442179/) show that it was "imposed by decantation", becoming the standard in the 1980s. The classic [Gopen & Swan, "The Science of Scientific Writing" (1990)](https://www.jstor.org/stable/29774235) establishes the principle of *reader expectation* — meaning is born from structural position (topic/stress positions), not just from words. The practical codification is in *How to Write and Publish a Scientific Paper* (Day & Gastel).

**Writing as a cognitive process.** [Flower & Hayes (1981)](https://doi.org/10.58680/ccc198115885) model writing as **recursive** processes (planning/translating/reviewing) guided by goals, not linear stages; [Sommers (1980)](https://doi.org/10.2307/356588) shows that experienced writers revise by *re-seeing the meaning*, while novices swap words at the surface — "writing is rewriting".

**Craft and style.** The tradition runs from the prescriptive minimalism of *The Elements of Style* (Strunk & White) to the *principled* theory of clarity of *Style: Toward Clarity and Grace* (Williams — characters=subjects, actions=verbs, old-before-new), through the authentic voice of *On Writing Well* (Zinsser); the editorial/citation standards are the *Chicago Manual of Style* (17th ed.) and the *APA Publication Manual* (7th ed.).

**Craft of research and argument.** *The Craft of Research* (Booth, Colomb & Williams) frames research as **making an argument to a reader** (problem → question → *claim* → reasons → evidence; the "So what?"); [Toulmin's model (1958)](https://www.cambridge.org/core/books/uses-of-argument/26CF801BC12004587B66778297D5567C) gives the anatomy of the argument (claim, grounds, warrant, backing, qualifier, rebuttal).

**Peer review and the editorial flow.** [Spier (2002)](https://doi.org/10.1016/S0167-7799(02)01985-6) traces the history of peer review; the historiography ([Baldwin, ETHOS](https://ethos.lps.library.cmu.edu/article/id/19/)) reminds us that universal refereeing is a 20th-century construct. And the editorial division of labor — *developmental editing* (restructuring vision/discourse) × *copyediting* (sentence-level preparation) — is the axis of the flow (Norton, *Developmental Editing*).

**Instructional design (what this book already uses).** Backward Design (Wiggins & McTighe), [4C/ID (van Merriënboer et al., 2002)](https://doi.org/10.1007/BF02504993), [cognitive load (Sweller, 1988)](https://doi.org/10.1207/s15516709cog1202_4) and [Diátaxis (Procida)](https://diataxis.fr/) — the pedagogical basis of Principle III.

### 6.B — AI-era methodologies

**Human-AI co-writing.** HCI studies treat co-writing as **observable** interaction, not a black box: [CoAuthor (Lee, Liang, Yang, 2022)](https://doi.org/10.1145/3491102.3502030) records the interaction at keystroke level; [Wordcraft (Yuan et al., 2022)](https://doi.org/10.1145/3490099.3511105) decomposes writing into *moves* (continue/infill/elaborate/rewrite) tied to intention. Measured **caution**: [Jakesch et al. (2023)](https://doi.org/10.1145/3544548.3581196) show that a biased assistant shifts what the user writes *and thinks* ("latent persuasion").

**Spec-driven / structured authoring / docs-as-code.** Write the intention first and let it drive the generation: [GitHub Spec Kit](https://github.com/github/spec-kit) (spec → plan → tasks → implement) and [Amazon Kiro](https://kiro.dev/) formalize this; the documentation community already adopts an engineering workflow for prose ([docs-as-code, SIGDOC '24](https://doi.org/10.1145/3641237.3691677); [DITA/topic-based](https://dita-lang.org/)).

**Agent-augmented research and retrieval.** [RAG (Lewis et al., 2020)](https://arxiv.org/abs/2005.11401) anchors generation in retrieved sources instead of the model's memory; the agentic frontier decomposes the *survey* into roles (search/synthesize/verify) — a trend illustrated by auto-survey work (⏳ to be confirmed).

**Verification and provenance.** [RARR (Gao et al., 2023)](https://arxiv.org/abs/2210.08726) does attribution/checking *after* generation; [Liu, Zhang & Liang (2023)](https://arxiv.org/abs/2304.09848) measure that only **51.5%** of generative search engines' claims are fully supported by citation — judge by *citation precision/recall*; [watermarking (Kirchenbauer et al., 2023)](https://arxiv.org/abs/2301.10226) embeds provenance (fragile to paraphrase).

**Academic integrity and authorship.** The policy consensus: **an LLM cannot be an author** (it cannot answer for the content) and its use must be **disclosed** — [ICMJE](https://www.icmje.org/recommendations/browse/artificial-intelligence/), [COPE (2023)](https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools), [*Science* (Thorp, 2023)](https://doi.org/10.1126/science.adg7879), [*Nature* (2023)](https://www.nature.com/articles/d41586-023-00191-1). And disclosure, in practice, is [widely violated (Academ-AI, 2024)](https://arxiv.org/abs/2411.15218).

### 6.C — Tensions and synthesis (traditional × AI)

The gain of AI assistance (speed, research reach, structure) comes with four tensions that an academic edition cannot ignore:

- **Fabricated sources.** [Walters & Wilder (2023)](https://doi.org/10.1038/s41598-023-41032-5) measured **55%** fabricated citations in GPT-3.5 (18% in GPT-4) and substantive errors in the real ones — hence this book's rule: **verify every reference** against the primary source, by cross-search.
- **Verifiability.** Text that *looks* cited frequently is not supported (Liu et al.'s 51.5%) — the citation must be checked, not trusted.
- **Reproducibility.** LLM outputs are non-deterministic; logging prompt, model version and context is part of the rigor.
- **Homogenization and "cognitive debt".** AI converges style and ideas ([homogenization, 2024](https://arxiv.org/abs/2402.01536)) and uncritical use is associated with lower engagement/ownership ([Kosmyna et al., 2025](https://arxiv.org/abs/2506.08872)) — the reason for AI to *amplify*, not *replace*, the author's judgment.

The book's synthesis: use AI as a **research and structuring prosthesis under human verification**, not as an author. Traditional methodologies (argument, clarity, revision) remain the quality standard; the AI ones accelerate the path to it, as long as they are fenced by verification.

### 6.D — This book's method, declared

This book practices what it describes. Each practice links to a principle of the constitution and has evidence in the repository itself:

- **Evidence over rhetoric** (Princ. I) — no claim about a harness without a *path* in the code; no citation without validated status. Sources verified by cross-search; gaps recorded, not filled with weak sources.
- **The base source is the code** (Princ. II) — the body is born from reading the harnesses' code; science and industry provide context. The per-repository treatment (with paths) is each chapter's **Appendix A**.
- **A combined pedagogical method** (Princ. III) — Backward Design + 4C/ID + Diátaxis + cognitive load; the v3 skeleton is its materialization.
- **Verified double research** — when opening each topic, parallel research agents gather **scientific** and **industry** material; each source is confirmed by ≥2 independent mentions before it enters (the rule the AI era makes at once possible and mandatory, in light of Walters & Wilder).
- **Spec-driven cycle** (Princ. VII) — every improvement goes through `spec → plan → tasks → implement` (spec-kit), on its own branch; *this section* was produced that way (`specs/010-estudo-metodologias-escrita/`), with the official cycle and its gates (Constitution Check, cross-artifact analysis).
- **Living book** (Princ. IV) — dating and `HISTORICO.md`; the predictions have a scoreboard (the expiration log).

**Authorship disclosure (transparency).** Consistent with the policies above and with Principle I, we openly declare: this book is **co-written with an AI agent (Claude Code, from Anthropic)** operating under **human authorship, curation and responsibility**. The agent executes research, drafting and the spec-kit cycle; the human author defines the scope, decides (via `/speckit-clarify` and review), verifies the sources and answers for the content. Following [ICMJE](https://www.icmje.org/recommendations/browse/artificial-intelligence/)/[COPE](https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools)/[*Nature*](https://www.nature.com/articles/d41586-023-00191-1)/[*Science*](https://doi.org/10.1126/science.adg7879), the AI is **not** listed as an author — it cannot be responsible — and its use is disclosed here, in the method.

### 6.E — A repeatable flow for a contributor

To bring a chapter or section up to the book's standard:

1. **Open the topic** — double research (commercial/industrial + scientific), verified by cross-search; record gaps.
2. **Gather the base source** — read the harnesses' code; note paths (becomes Appendix A).
3. **Write** — in the v3 skeleton (chapters) or in the correct Diátaxis type (guide/benchmark = reference); one type of text per section; technical terms untranslated.
4. **Revise (developmental)** — re-see structure and meaning before the surface copyedit: does the argument close? does the order serve the reader? is there redundancy or a gap? "Writing is rewriting" (§6.A; the constitution's quality gate).
5. **Verify sources** — no invented URL/ID; unconfirmed marked `⏳`; sync `bibliografia.md`.
6. **Build gate** — `node publicar/build.mjs` green (no broken internal links).
7. **Date it** — the capture stamp on the chapter and an entry in `HISTORICO.md` — **with the version of the AI model used** — if the state of the art changed.

AI-use safeguards: the AI researches and drafts; the human decides, verifies and signs. Every source brought by an agent is checked before it enters the body.

## Acronyms and glossary (policy)

- **Every technical acronym is spelled out at its 1st occurrence** in a chapter — "Model Context Protocol (MCP)" — and, from then on, the text may use only the acronym.
- The publishing engine reinforces this: it **automatically wraps every known acronym in `<abbr>`**, so that hovering reveals the meaning at any occurrence without polluting the source text. The acronym map lives in `publicar/build.mjs` and is mirrored on the **[Glossary](glossary.md)** page (`livro/glossario.md`).
- The **Glossary** gives the **spelled-out form**, a short explanation and **in which chapters** each acronym appears. When introducing a new acronym, add it in both places (engine map + glossary) and **check the expansion against the source** (Principle I).

## Living-book cadence

> Policy decided in [ADR 0007](../../adr/0007-cadencia-livro-vivo.md) (in Portuguese; alternatives and rationale there).

- **Quarterly window** (next: **2026-10**): re-sync of the 16 forks (`scripts/sync-forks.ps1`), a diff driven by the benchmark dimensions, update of the affected Appendices A, of the expiration scoreboard and of the revision dates; a minor edition in the [History](../historico.html).
- **Extraordinary trigger**: any event that **invalidates an "Executive summary"** (a protocol change, a capability migrating to the provider, a corpus harness being archived) triggers a targeted revision of the affected chapter, without waiting for the window.
- Each chapter's "state of the art captured in" date remains the truth exposed to the reader — the cadence exists so that it never lies by omission.

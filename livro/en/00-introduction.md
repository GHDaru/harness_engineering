<!-- i18n fonte:livro/00-introducao.md edicao:0.82 hash:8df3978c -->
# 00 — Introduction

> **State of the art captured in 2026-07** · last revised 2026-08-12 · [history and expiration log](../historico.html)
>
> Didactic layer v4 — see [Editorial Guide §2.1](editorial-guide.md).
> scaffold: completo

## The perfect advice that fixes nothing

You paste an error into the chat and get an impeccable answer. The diagnosis is right, the suggested snippet is right, the explanation is better than the documentation's. You say thanks, close the tab, open the editor and do everything by hand: find the file, apply the change, run the test. The test fails for a different reason. You go back to the chat and start over, now re-explaining what you had already explained.

Notice what happened. The advice was good. The work stayed yours.

Now the same task in a coding agent. You type the same sentence. It locates the file, applies the change, runs the test, sees the new failure, fixes that one too, runs it again and only then answers: "done, there were two problems". You explained nothing twice.

The model in both cases can be exactly the same. The whole difference is in what exists **around** it.

## Agent = model + harness

When an agent solves a real task, two distinct things are at work.

The first is the **model**: the network that reads context and decides the next step. It is the part that reasons, and the part that improves on its own with every generation.

The second is everything around it. Whoever assembles the context it reads. Whoever executes the tools it invokes. Whoever decides what it may and may not do. Whoever remembers what happened yesterday. Whoever checks that the result is correct and decides it is time to stop. That "everything around it" is the **harness**, loosely the rigging, the scaffold, the *scaffolding*.

The formula that organizes this book is simple:

> **agent = model + harness**

<figure class="figura">
  <img src="assets/harness-diagrama.svg" alt="Schematic diagram: the AI model at the center, surrounded by the six harness blocks — agent loop, context, tools, memory, permissions and verification — inside a dashed frame labeled 'harness (the scaffolding)'; on the right, the world (files, APIs, terminal) with arrows going back and forth.">
  <figcaption>The model at the center; the harness around it. Each block is a chapter of this book.</figcaption>
</figure>

The model is interchangeable. The harness is classic software engineering, and it is where most agents fail or succeed.

Two products using exactly the same model deliver radically different results depending on the quality of the harness: how context reaches the model, which tools it has, how errors come back, and what happens when the **context window** (the limit of text the model can see at once) runs out.

**Harness engineering** is the discipline of designing that scaffolding: context delivery, tool interfaces, planning artifacts, verification loops, memory systems and sandboxes.

## In practice: the same question, two destinations

It is worth seeing the difference in text, because it is not abstract. You ask: *"the `test_login` test is failing, fix it"*.

**Without a harness**, the model can only return language:

```text
The session cookie is probably expiring before the check.
Try adjusting `max_age` in auth.py:

    session.set_cookie(..., max_age=3600)

If that does not help, check the server's timezone…
```

It is correct and useless on its own. The model does not know whether `auth.py` exists, has not read the line, has not run the test and has no way of knowing whether it got it right. It **guessed**, because guessing was the only thing available.

**With a harness**, the same decision comes out in another format:

```text
→ run_shell("pytest test_login -x")
← FAILED test_login - assert 401 == 200

→ read_file("auth.py")
← ...  session.set_cookie(..., max_age=0)  ...

→ edit_file("auth.py", max_age=0 → max_age=3600)
← ok, 1 line changed

→ run_shell("pytest test_login -x")
← FAILED test_login - assert 500 == 200      ← a NEW error

→ read_file("auth.py")
← ...
→ edit_file("auth.py", ...)
→ run_shell("pytest test_login -x")
← 1 passed

"Done. There were two: the cookie was born expired and the
 handler broke when the session came in empty."
```

Seven action requests and one sentence at the end. Now observe what the harness did in this script, because each item is a chapter of this book:

- it decided to **continue** after each result, and decided to **stop** when the model answered without asking for anything (ch. 02);
- it assembled what the model would see at each step, without dumping the whole repository (ch. 03 and 04);
- it offered the tools `read_file`, `edit_file` and `run_shell`, with those names and those arguments (ch. 05 and 06);
- it let the edit through, or asked for your approval before it (ch. 07);
- it returned the **error** to the model as text instead of taking the process down, which is the reason the second failure became a fix rather than an abandonment (ch. 02 and 11).

And there is a detail that is easy to miss: **the model did not know there were two problems**. Nobody did. The second one only appeared because the first was fixed and the test ran again. That is the difference between advising and working, and it does not come from reasoning. It comes from the loop.

## Why a book — and why now

Between 2024 and 2026, coding-agent harnesses stopped being experiments and became a product category: Claude Code, Codex CLI, Gemini CLI, opencode, Aider, Cline, Goose, OpenHands and dozens of others.

The most remarkable thing is not the quantity, it is the **convergence**. Independent projects, in different languages, with no coordination, arrived at the same solutions: hierarchical context files, layered compaction, plan mode as a permission mode, lifecycle hooks, MCP (Model Context Protocol) as the integration standard.

When independent implementations converge, there is a discipline behind them. This book documents that discipline.

## The method: read code, not marketing

This book is empirical. Each chapter covers one harness capability and is written from reading the source code of real open source harnesses.

The project's most important editorial rule:

> Claims about a harness require **evidence**: the file path in the source code where the capability is implemented.

READMEs promise; code delivers. Several projects advertise dimensions their code does not have, and the evidence requirement is what separates evaluation from marketing.

## A note on authorship and method

For transparency, and for consistency with the evidence rule above: this book is **co-written with an AI agent** (Claude Code, by Anthropic) operating under **human authorship, curation and responsibility**. The agent carries out the research, the writing and the production cycle. The human author defines the scope, decides, **verifies every source** and answers for the content.

Following editorial authorship policies (ICMJE, COPE, *Nature*, *Science*), the AI is **not** listed as an author, because it cannot be held responsible, and its use is disclosed here, at the opening.

This is not a detail. A book about the discipline of properly instrumenting AI agents uses that very discipline to write itself, and exposes it. The full method (dual research verified by cross-search, spec-driven cycle, review and dating) is documented in the [Editorial Guide §6](editorial-guide.md), with a survey of the traditional and AI-era writing methodologies that ground it.

## How to read this book — three doors in

This book is dense on purpose. This section exists so the density is not a wall. Pick your door.

**If you are just arriving** and have never built an agent: read 00, 01 and 02 in order, unhurried, with the [Glossary](glossary.md) at hand. Every acronym in the book is there, spelled out and explained, and in the online version you just hover over it. After chapter 02, chapters 03 to 13 can be read in any order, because each is self-contained and opens by defining its own problem.

**If you already operate an agent** and want to understand what is inside: the **Executive summary** at the end of each chapter is your shortcut, with the state of the art of the dimension in one paragraph and the "what to steal" section. Go straight to the chapter you care about and descend into the body when you want the evidence.

**If you build harnesses**: the whole book is yours, including the Appendices A with per-repository evidence and file paths, the [Benchmark](comparative.html) and the two hands-on tracks. **harness-zero** is the didactic build, one feature per step; **harness-um** is the complete reference implementation, with its [own appendix](appendix-harness-um.md).

## Structure of the book

- **Foundations** (chapter 01): the formal definitions, the canonical papers and the problem taxonomy that organizes everything that follows.
- **Chapters 02–13**: one capability per chapter. Each defines the problem, presents the known implementation patterns and shows, with evidence, how each studied harness implements it.
- **Convergences and trends** (chapter 14): what the industry has already standardized, where real divergence remains, and the **expiration clause**, the thesis that every harness component exists because the model cannot yet do that on its own, and must be designed knowing that one day it will be unnecessary.
- **Chapters 15–17**: the frontiers. The harness embedded in a product (15), the harness that learns from usage (16) and the protocol layer that binds the ecosystem together (17).
- **Benchmark** (`benchmark/`): the empirical section, with standardized per-dimension evaluations, 0–3 scores and evidence for every harness studied, plus the consolidated comparison.

## The harnesses in the study

As of this edition, the study covers **twenty-one open source systems**, evaluated through systematic code reading across five archetypes (the method is in [chapter 01, §6](01-foundations.md)):

- **Coding harnesses** — opencode, gemini-cli, OpenHarness, Codex CLI, Goose, Aider, OpenHands, Grok Build, Pi, Kimi Code and Prime Agent;
- **Self-hosted personal agents** — OpenClaw, Hermes Agent, IronClaw, ohmo;
- **Organizational agents** — QM;
- **Embedded harnesses** — n8n (AI Agent node);
- **Frameworks** — LangGraph, CrewAI, OpenAI Agents SDK (Software Development Kit), Software Agent SDK.

Each was chosen for representing a different *archetype*. The logic is replication, not sampling: mature provider-agnostic product (opencode), big-tech control regime (gemini-cli), readable didactic port (OpenHarness), sandbox-first (Codex CLI), MCP-native (Goose), context-first (Aider), academic eval culture (OpenHands), whole-organization agent with a swappable loop (QM), and so on.

The full list, with the **exact origin, version, fork and commit read** in each evaluation and the link to each one's analysis and diagnosis, is in the **[Appendix — The study](appendix-study.md)**. The consolidated per-dimension scoreboard is in the [Comparative](comparative.md).

As a theoretical reference, and to explore the ecosystem beyond the corpus, there is also the living collection **[Awesome Harness Engineering](https://github.com/GHDaru/awesome-harness-engineering)**, with about 426 resources organized by problem, in the same organization as this book. From there come the harness definition used in chapter 01 and the taxonomy that structures the chapters.

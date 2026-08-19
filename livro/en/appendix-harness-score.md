<!-- i18n fonte:livro/apendice-harness-score.md edicao:0.88 hash:f839aade -->
# Appendix — Measure your harness

> **State of the art captured in 2026-08** · last revised 2026-08-10 · [history and expiry ledger](../historico.html)

This book does two things with harnesses: it **reads** other people's (the [Comparative](comparative.md), 20 systems across 12 dimensions) and it **builds** one from scratch (harness-zero). The third one is missing, and it is the one that matters to anyone doing the work: **measuring yours**.

Not the harness you wrote — the one you *have*. Because when an agent walks into your repository, the effective harness is not just the Claude Code or Codex you opened: it is that **plus** whatever your repository offers it. The instructions that steer, the tests that give signal, the guardrails that stop damage. Two repositories running the same model and the same CLI produce different results, and the difference lives here.

## The instrument

[Harness Score](https://github.com/paladini/harness-score) (Fernando Paladini, **MIT**) scans the repository and returns a **maturity level L0–L4** and **108 points across 6 dimensions, 36 checks**. One line:

```bash
npx harness-score
```

The design commitment is what makes it citable here: *"zero LLM calls, zero network access, and the same result every time you run it"* — every result is *"a filesystem fact — a file exists, parses, matches a pattern"*.

That is not an implementation detail. It is the thesis of [ch. 11](chapters/11-verification-evals.md) applied to the act of measuring itself: the chapter argues that verification worth the name is **external and anchored**, not the model's own report. A harness meter that refuses to use a model to measure harnesses is that argument turned into a tool — which is why its number is arguable but **reproducible**, the only property a measurement needs in order to ground a discussion.

Its six dimensions map almost cleanly onto this book's chapters — which is itself evidence that our twelve dimensions are not arbitrary:

| Dimension (points) | What it looks for | Chapter |
|---|---|---|
| Context & Guides (20) | `AGENTS.md`, scoped rules, no bloat | [03](chapters/03-context-delivery.md) |
| Skills & Commands (17) | declared skills, explicit commands | [05](chapters/05-tool-design.md), [12](chapters/12-extensibility.md) |
| Hooks & Guardrails (14) | gate and feedback hooks | [07](chapters/07-permissions-sandboxing.md) |
| Sensors & Feedback (20) | tests, linter, types, formatter | [11](chapters/11-verification-evals.md) |
| CI Feedback (14) | pipeline, tests and lint in CI, pre-commit | [11](chapters/11-verification-evals.md) |
| Hygiene & Safety (23) | `.gitignore`, no credentials, license, lockfile | [07](chapters/07-permissions-sandboxing.md) |

And the definition the project gives of a harness is the **fifth** independent convergence with [ch. 01](../01-foundations.md) that this book has recorded — the most operational of them all, because it defines by what can be verified on the filesystem: *"A model answers; an agent acts. An agent harness is the runtime that turns one into the other — the model thinks; the harness decides what that thinking is allowed to touch."*

## The ladder

| Level | Name | What characterises it |
|---|---|---|
| **L0** | Unharnessed | cold start every session |
| **L1** | Documented | an `AGENTS.md` orients the agent |
| **L2** | Guided | scoped rules and basic hygiene |
| **L3** | Sensing | tests, types and CI verify the work |
| **L4** | Self-correcting | hooks close the loop |

Levels gate on the **shape** of the harness, not the total: eighty points of documentation with zero tests is L1, not L3. It is the same discipline as this book's rubric — you do not offset missing verification with an abundance of prose.

## Our own score, before and after

A book about harness engineering that does not measure itself is a book asking for trust. We measured, and the first result was poor.

**Before** — 2026-08-10, `harness-score` via `npx`, on this book's repository:

```
Harness Engineering · L2 · Guided · 59/108 (55%)
Detected: claude-code, codex

Context & Guides   ████████████████████ 20/20
Hygiene & Safety   █████████████████░░░ 20/23
Skills & Commands  ██████████░░░░░░░░░░  9/17
CI Feedback        ████████░░░░░░░░░░░░  8/14
Hooks & Guardrails ░░░░░░░░░░░░░░░░░░░░  0/14
Sensors & Feedback ██░░░░░░░░░░░░░░░░░░  2/20
```

**The diagnosis is the most interesting part of this appendix.** At that moment this repository had 81 automated tests, a four-step build with link checking, and an entire harness-zero stage dedicated to evals. The check `SNS-05 Test files actually exist` **passed**. `SNS-01 Test runner configured` **failed** — along with linter, types and formatter, −18 points. The scanner could see the test files and could not find an **entry point at the root**: they lived in three subdirectories, and knowing that required reading `CLAUDE.md`.

In other words: we were compensating in **prose** for what was missing in **configuration**. And that is exactly why Context scored 20/20 — the instructions were excellent.

> **The lesson, and it cost us 55%:** perfect prose is no substitute for an executable guardrail. The agent reads and obeys. A hook, a CI pipeline or the next contributor **do not read prose**.

The zero in Hooks & Guardrails said the same thing from the other side, and it stung more: in a repository that devotes an entire chapter to permissions and sandboxing, **none** of our critical rules were machine-enforced. "No secrets in commits" and "no internal model identifier in artefacts" are constitutional rules of this project — and they were upheld by human attention, which means upheld until the first lapse.

**After** — same tool, same day, following the fix described below:

```
Harness Engineering · L4 · Self-correcting · 87/108 (81%)

Context & Guides   ████████████████████ 20/20   (=)
Sensors & Feedback ████████████████░░░░ 16/20   ↑ from 2
Hooks & Guardrails ████████████████████ 14/14   ↑ from 0
CI Feedback        ████████████████░░░░ 11/14   ↑ from 8
Skills & Commands  ██████████░░░░░░░░░░  9/17   (=)
Hygiene & Safety   ███████████████░░░░░ 17/23   ↓ from 20
```

## What we did — and the rule we followed while doing it

The rule came before the work: **every item has to justify itself without looking at the score**. Optimising for the number is gaming the verifier — the *reward hacking* ch. 11 describes in detail, committed by the authors of the chapter. If the only reason to add something was the point, it did not go in.

**An entry point.** A `Makefile` and a `pyproject.toml` at the root. `make test` runs the three suites; `make build` builds the site; `make score` measures the harness. Justification without the score: whoever lands at the root had no way to run anything without first reading an instructions file — and an agent that acts before reading instructions is the common case, not the exception.

**A style standard.** Ruff, one configuration for both Python projects. Justification without the score: style lived in the head of whoever reviewed.

**Four guardrails**, and they are what holds the change up. Three of them convert a written rule into an enforced one:

| Hook | What it enforces | Where the rule lived before |
|---|---|---|
| `guarda-segredo` | writes carrying a credential signature are blocked | constitution, Principle IV |
| `guarda-identidade` | internal model identifiers never enter a file | constitution, Principle VI |
| `guarda-git` | `push --force`, `reset --hard`, `clean -fdx` ask first | nowhere — it was a habit |
| `formata-python` | edited `.py` files go through the formatter | none |

Two design details matter more than the hooks themselves. First: **none of them blocks when the hook itself fails** — unreadable input, internal exception, missing tool, all exit quietly and let the work proceed. A guardrail that interrupts work when it breaks itself gets switched off the following week, and then protects nothing. Second: `guarda-git` **asks** rather than forbids. There are legitimate reasons for every one of those operations; the goal is that they be deliberate, not impossible. That is ch. 07's blast radius applied to our own repository.

And the hooks carry **37 tests**, with the cases that must *pass* stated as explicitly as the ones that must be blocked — because a guardrail that gets in the way of legitimate work is routed around, and a hook without tests is a promise with syntax.

## What we did **not** do, and why

This section is what gives the two above their value. Without it, "we went from L2 to L4" is advertising.

- **Strict static typing** (`SNS-03`, 4 points). Declined. Adding strict typing to a codebase not written for it is a change of its own size, with a real review cost. Doing it now, in the middle of a spec about measurement, would mean adding it **for the point** — precisely what the rule forbids.
- **Pre-commit** (`CI-04`, 3 points). Declined for now: the hooks already give feedback at edit time, and a second layer with the same function costs maintenance without new signal.
- **Declared subagents** (`AGT-01/02`, 5 points). We have no subagents defined in this repository. Declaring them to score would mean inventing architecture to please the instrument.
- **MCP configuration** (`HYG-08`, 3 points). We do not use MCP here. Same logic.
- **The README badge.** Ch. 01 §6 already forbids spurious numeric aggregation (DESMET); 87/108 is not a measure of the book's quality, it is a diagnosis of the repository's configuration. Publishing it as a seal would betray the yardstick we apply to everyone else.

## The regression we let happen

Hygiene **went down**, from 20/23 to 17/23, and the reason is the most interesting finding of this whole measurement.

Check `HYG-07` requires a lockfile next to the dependency manifest. Before, it **passed**, and the scanner's own message explains why: *"No dependency manifest detected (nothing to lock)."* There was no manifest at the root, so there was nothing to lock, so the point was awarded. After we added a `pyproject.toml` — containing **configuration only**, no dependencies — the message became *"Manifest present but no lockfile"*, and the point was gone.

We could have forged an empty root `requirements.txt` and recovered three points. We did not: it would mean lying to the instrument about the nature of the file. Two conclusions follow, and both hold for any maturity ladder you may come to use:

1. **A point awarded for absence is not a point.** Part of our initial 20/23 in hygiene was a vacuous pass — we did not have the problem because we did not have the thing. Any rubric that scores "not applicable" as a success inflates whoever does less.
2. **The score is not monotonic under honest improvement.** Making the repository more legible caused a passing check to start failing. If your goal is the number, you learn **not** to add the manifest — and that is how a well-meant metric starts governing architecture instead of describing it.

It is ch. 11's lesson about instrument sensitivity, found in our own back yard.

## Caveats

- **Root bias.** The scanner underestimates polyglot monorepos — our case, with Python in two places and Node in a third. The caveat has a limit, though: for an agent that lands at the root, what is not discoverable there **effectively does not exist**. Half of our initial 2/20 was a limitation of the instrument; the other half was our own defect.
- **Version discrepancy** ⏳: the site announces npm v1.2.0; the repository shows release v1.0.0. Our measurement used the version published on npm on 2026-08-10.
- **The number is not the thing.** The value is in the **named gap** — `SNS-01`, `HKS-03`, each with a specific remedy — not in the total. Treat 87/108 the way you would treat a harness scoring 31/36 in the Comparative: a summary that only means something alongside the evidence that produced it.

## How to use this on your repository

1. Run `npx harness-score` and read the **first gap**, not the total.
2. For every item you intend to fix, write the justification **without citing the score**. If you cannot, do not fix it — you would be optimising the instrument.
3. Start with the guardrails, not the documentation. Documentation is what most repositories already have in excess; what is usually missing is whatever runs by itself.
4. Keep the starting score, with its date. The value of a maturity measurement is in the **series**, not the point.

<!-- i18n fonte:livro/apendice-harness-um.md edicao:0.61 hash:d4a8a42e -->
# Appendix — harness-um: the reference implementation

> **State of the art captured in 2026-07** · last revised 2026-07-31 · [history and expiration log](../historico.html)

After eighteen chapters describing what a harness has, the honest question is: *what if we put it all together?* This appendix answers with code. The **harness-um** is the book's reference implementation — the features from chapters 02–13 gathered into a single system, small enough to be read in an afternoon and complete enough to be the starting point for yours.

<figure class="figura">
  <img src="assets/harness-um.svg" alt="Official harness-um figure: a luminous amber numeral 1 at the center of a ring of 12 blue segments — chapters 02 through 13 — on a dark-blue blueprint background, next to the name harness-um and the subtitle 'the reference implementation of the Harness Engineering book'.">
  <figcaption>The official figure: the core (the agent) wrapped by the 12 segments of the ring — chapters 02–13, one per feature. The visual identity is the same as the cover's: the harness is what sits <em>around</em>.</figcaption>
</figure>

## Why "harness-um" (and not "openharness")

The name tells the book's progression: the **harness-zero** (Hands-on) builds one feature per step, from scratch; the **harness-um** ("harness-one") is the destination — everything together and cohesive. And there is an editorial reason: "OpenHarness" **already exists** — it is one of the 16 systems in this study's corpus (HKUDS/OpenHarness, an open-source port of Claude Code). Naming the book's reference after a system the book itself evaluates would create exactly the confusion Principle I exists to prevent.

## The ubiquitous language

The central decision of the harness-um is not technical, it is **linguistic**: the code speaks the book's language — in Portuguese, and the class names are deliberately kept that way. Every term the chapters defined becomes an identical code name — reading the code is rereading the table of contents. The translation into each model API's dialect (today, Anthropic Messages) happens at a single edge (`provedores.py`, the providers module), the **anticorruption layer**: if the provider changes, the domain never even hears about it.

| Book term | In the code | Chapter |
|---|---|---|
| Agent loop | `LoopDoAgente.executar()` — the agent loop's `run()` | 02 |
| Turn (with a budget) | `max_turnos` | 02 |
| Context assembly | `MontadorDeContexto` (named layers) | 03 |
| Compaction | `Compactador` (summary + intact tail) | 04 |
| Tool | `Ferramenta`, `@ferramenta`, `CaixaDeFerramentas` | 05 |
| MCP | `ClienteMCP` (stateless, spec 2026-07-28) | 06 |
| Permissions | `Politica` → `PERMITIR / PERGUNTAR / NEGAR` (allow / ask / deny) | 07 |
| Durable memory | `Memoria` (`MEMORIA.md`) | 08 |
| Session | `Sessao` (JSONL, append-only) | 08 |
| Plan as artifact | `Plano` (persisted, re-injected) | 09 |
| Subagent | `tarefa()` — clean context, read-only toolbox | 10 |
| Verification | `Verificador` (post-mutation, verdict to the model) | 11 |
| Hook | `Gancho` (deterministic, can veto) | 12 |
| Skill | `Habilidade` (`SKILL.md`, progressive disclosure) | 12 |
| Interface | REPL (`python -m harness_um`) | 13 |
| Provider | `Provedor` → `ProvedorAnthropic`, `ProvedorEco` | 02, 11 |

## How to download and run

The code lives **in this repository**, alongside the book — in [`harness-um/`](https://github.com/GHDaru/harness_engineering/tree/main/harness-um):

```bash
git clone https://github.com/GHDaru/harness_engineering.git
cd harness_engineering/harness-um
pip install -e .

# sem chave nenhuma (ProvedorEco, offline):
python -m harness_um --eco 'leia @usar ler_arquivo {"caminho": "README.md"}'

# com modelo real (chave SÓ no ambiente):
export ANTHROPIC_API_KEY=...
python -m harness_um     # REPL: /plano /memoria /contexto /sair
```

The `ProvedorEco` (the echo provider) deserves the note: it is deterministic and obeys `@usar ferramenta {...}` directives — enough to exercise the whole loop (tool-use, permissions, hooks, verification) **with no network and no cost**. That is why the harness-um tests run in the book's CI on every push: the reference must not rot in silence.

## harness-zero × harness-um

| | harness-zero | harness-um |
|---|---|---|
| Purpose | **teaching how to build** (Backward Design) | **showing the finished whole** |
| Form | 13 steps, each a complete app | 1 cohesive package (`harness_um/`) |
| Reading | during the chapters | after the book |
| Analogue | exercise workbook | annotated answer key |

## Expiration

Like everything in this book: the harness-um is the **2026-07** snapshot — the MCP client is born on the 2026-07-28 spec, but providers, schemas and conventions change in months. The [living book's cadence](../historico.html) (ADR 0007, in Portuguese) covers this appendix too; the code carries the same clause in its README.

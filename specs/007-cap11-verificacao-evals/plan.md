# Plano — Cap. 11 (Verificação e Evals)

## Fonte-base (código, reunida)
- Rodada 1: gemini-cli (4 suítes: ~45 evals com juiz LLM, integração gravada, baselines de memória/perf nightly), opencode (**LSP em runtime** → diagnósticos ao modelo; anti-mock + http-recorder), OpenHarness (121 arquivos por subsistema; E2E com modelo real; skill `harness-eval`).
- Rodada 2: Goose ⭐ (**Harbor**, terminal-bench-style, 89 tasks, leaderboard público stock 50.6%/code-mode 57.3%, LLM-judges); Codex (~440 testes + ~660 snapshots insta; E2E backend mockado; parity de compactação; CI multi-camada); Hermes ⭐ (**verify-on-stop nudge** + `verification_evidence.py`; `mini_swe_runner` SWE-bench-style); OpenClaw ⭐ (~8.649 testes; drift-check de prompt snapshots; **Personal Agent Benchmark Pack** — 10 cenários da categoria); IronClaw ⭐ (~415 testes; fuzzing; **isolamento cross-tenant como 1ª classe**; parity de trace vs OpenClaw; regra exigindo testes de denial/redaction/escape); ohmo (96 testes adversariais); n8n (produto **Evaluations** + LLM-judge); Aider (reflexão máx. 3 disparada por lint/testes; leaderboard de edit format); OpenHands (eval=0 neste repo — migrou para o SDK).

## Pesquisa (em andamento → verificar)
- Científico: SWE-bench + SWE-agent (ACI); LLM-as-judge (MT-Bench) e vieses; self-correction ("LLMs Cannot Self-Correct Reasoning Yet"), self-consistency, CRITIC; surveys de eval; reward hacking/RLVR.
- Indústria: SWE-bench Verified, terminal-bench; evals model-graded (Anthropic "create strong empirical evals"); verificação no loop (long-running-agents); frameworks (OpenAI Evals, Inspect/AISI, promptfoo, braintrust, LangSmith).

## Tradução em decisões (corpo)
1. **Três perguntas, três respostas** — a moldura da rodada 1 persiste.
2. **Held-out / anti-overfit** — SWE-bench Verified + reward hacking justificam testes que o agente não vê e a política anti-mock do opencode.
3. **O juiz LLM tem vieses** (posição/verbosidade/self-preference) — usar com cuidado; snapshots/gravação dão determinismo onde o juiz é caro/instável.
4. **Verificar-antes-de-parar** — o verify-on-stop do Hermes instancia a disciplina "verifique o trabalho" dos agentes de longa duração; verificação vira estágio imposto do loop.
5. **Eval comportamental virou table-stakes** e **por categoria** (Harbor; Personal Agent Benchmark Pack) — o dado do livro vivo: a lacuna da rodada 1 (só um testava comportamento) fechou.
6. **Isolamento/segurança como cidadão de teste** (IronClaw parity, ohmo adversarial) — fechando a outra lacuna da rodada 1.

## Passos
1. Escrever `11-verificacao-evals.md` v3. 2. Atualizar `bibliografia.md`. 3. Build. 4. Commit na branch 003.

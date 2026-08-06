# Apêndice — A cadeia de suprimentos dos harnesses

> Mapa capturado em **2026-08-02** (rodadas ext-2/ext-3). Como todo estado da arte deste livro, expira: confronte com o [Histórico](HISTORICO.md).

Quando este estudo começou, o corpus era uma lista de **concorrentes**: produtos alternativos que resolviam o mesmo problema. As rodadas ext-2 e ext-3 revelaram outra coisa: os harnesses viraram **fornecedores uns dos outros** — dependências de `package.json`, forks vendorizados, subprocessos, sessões alheias retomadas. Este apêndice mostra o trabalho: quem consome quem, por qual mecanismo, com a evidência de cada elo. "Cadeia de suprimentos" aqui é a imagem da manufatura (a fábrica A produz a peça que a fábrica B monta), e também o sentido de segurança do termo: **quem embute, herda os riscos**.

## O mapa (evidência por elo)

Cada linha é um elo verificado por leitura de código no commit congelado da avaliação correspondente (paths relativos à raiz de cada repo).

| Consumidor | Fornecedor | O que consome | Mecanismo | Evidência |
|---|---|---|---|---|
| **QM** | **Pi** | o motor de agente **default** — com **patch de segurança próprio** aplicado pelo consumidor | dependência npm de um fork re-empacotado (`qm-pi-coding-agent-0.82.0-security.2`) | `package.json:58` |
| **QM** | Claude Code | motor alternativo | `@anthropic-ai/claude-agent-sdk` + servidor MCP in-process para ponte de tools | `package.json:50`; `src/harness/claude-harness.ts` |
| **QM** | Codex CLI | motor alternativo | dependência `@openai/codex` | `package.json:60` |
| **QM** | opencode | motor alternativo | `opencode-ai` + plugin/SDK | `package.json:61-62,72` |
| **Kimi Code** | **Pi** | a TUI inteira | fork **vendorizado** de `pi-tui`, com agradecimento público | `packages/pi-tui/`; `README.md:122` |
| **software-agent-sdk** | Codex CLI, gemini-cli | harnesses inteiros como executores | subprocessos **ACP** orquestrados pelo `ACPAgent` | `openhands/agent_server/conversation_service.py:723`; `event_service.py:873` |
| **Grok Build** | Claude Code, Codex, Cursor | as **sessões** dos concorrentes (retomáveis) e seus artefatos de contexto (AGENTS.md/CLAUDE.md/`.cursor`) | leitura dos formatos nativos + session picker | `crates/codegen/xai-grok-pager/src/views/session_picker.rs` |
| **n8n** | LangChain | a fundação do nó AI Agent — em processo de **reinternalização** (V3) | dependências `@langchain/*` | `packages/@n8n/nodes-langchain/package.json` |
| **Pi** | ← terceiros | provedor xAI chega ao Pi **de fora**, por pacote da comunidade | mecanismo de extensão (`pi-xai-oauth`) | radar 2026-08-01 |
| **Traycer** | Claude Code | motor GUI+TUI: resume/fork, hooks de ciclo de vida, gestão remota de MCP/plugins/skills | SDK + PTY `claude --resume --fork-session` + hooks → CLI `traycer` | `protocol/src/host/agent/tui/unary-schemas.ts:48-80`; `clients/traycer-cli/src/commands/agent-activity-from-hook.ts` |
| **Traycer** | Codex CLI | motor GUI+TUI | `codex app-server` (JSON-RPC) + PTY `codex resume` | `protocol/src/host/agent/tui/unary-schemas.ts:70-80` |
| **Traycer** | opencode | motor **e substrato da própria inferência** (servidor OpenCode por usuário atrás do backend Traycer) | PTY + spawn de servidor com header de conta | `protocol/src/common/schemas.ts:70-76`; `agent-runtime.ts:839-849` |
| **Traycer** | **Pi** (e o fork Oh My Pi) | motores GUI — o fork *sozinho* motivou a versão v6.0 do protocolo | RPC nativo do Pi | `agent-runtime.ts:925-946`; `provider-schemas.ts:80-135` |
| **Prime Agent** | **Pi** | **a base inteira** — os quatro pacotes do Pi, com o *tool set* colapsado num único `ipython` e duas camadas novas por cima | fork de tese; LICENSE com dupla titularidade (Mario Zechner + Prime Intellect) | `LICENSE`; `packages/{agent,ai,coding-agent,tui}/package.json`; `README.md` |
| **Traycer** | **Hermes**, **Kimi Code**, Cursor, +ACP | motores GUI (8+ providers via ACP: `hermes acp`, `kimi acp`, `grok agent stdio`, `qwen --acp`…) | processos ACP stdio / `@cursor/sdk` | `agent-runtime.ts:851-941`; `protocol/src/host/agent/shared.ts:35-43` |

Somam-se os elos de **produção editorial**: o Traycer materializa skills de registries públicos (anthropics/skills, vercel-labs) pinadas por hash num lockfile (`skills-lock.json`) para os agentes que escrevem o próprio repo — o consumo de harness alheio começando antes do produto existir.

## O caso extremo: Traycer, o cockpit que é só cadeia

A rodada **ext-3** avaliou o [Traycer](../benchmark/avaliacoes/traycer.md) (18/36) — um produto cuja proposta *inteira* é consumir harnesses alheios: um cockpit multiplayer (~513 mil linhas abertas) que cataloga no próprio contrato de wire a semântica de resume/fork de **18 CLIs/SDKs concorrentes**, com 6 enums de provider congelados por versão de protocolo. Ele **não passou o teste de inclusão** do cap. 01 §4 — as quatro peças do harness não estão no código aberto: o Host que executa loop, contexto e controle é binário fechado assinado, com nuvem obrigatória (`AGENTS.md` do próprio repo confessa; evidência completa na avaliação). O registro fica por dois motivos: é o caso mais bem documentado de **"open source" como estratégia de distribuição de cliente**, e é a prova de que a camada de orquestração — comprar, dirigir e revender o trabalho de outros harnesses — virou produto autônomo.

## Três leituras

1. **"De quem ele é feito?" virou pergunta de avaliação.** Um harness já não se descreve só pelo que faz, mas pelos elos que embute. O Pi alimenta hoje **pelo menos cinco sistemas** (QM como motor, Kimi Code como TUI, Traycer como provider, o fork Oh My Pi — e o Prime Agent como base inteira); uma falha, um CVE ou uma mudança de licença nesse único elo propaga pela cadeia inteira, exatamente como na indústria física.
2. **A sessão virou interface de integração.** Três consumidores diferentes (Grok Build, Traycer, QM) tratam a *sessão* de harnesses alheios como artefato retomável — via formato nativo, âncoras de resume/fork versionadas ou re-semeadura por "fita". É um padrão emergente sem padrão: cada um resolve por engenharia reversa do vizinho. Se um formato de intercâmbio de sessões se padronizar (cap. 17), boa parte deste mapa vira código de compatibilidade — a cláusula de expiração aplicada ao próprio apêndice.
3. **O enforcement não viaja pela cadeia.** Quando o QM roda o Pi, as permissões são as do QM (o Pi não as tem); quando o Traycer dirige 18 harnesses, o modo de permissão é **relay** — e a instrução A2A do Traycer chega a mandar os agentes derivados operarem em `full_access` por default. Quem consome um harness herda as capacidades dele, mas **não herda automaticamente os controles** — o elo mais fraco da cadeia define o risco do conjunto.

## O contraponto que confirma

Os dois fornecedores mais consumidos do mapa são também os que levam a cadeia de suprimentos *clássica* mais a sério: o Pi pina dependências e faz allowlist de lifecycle scripts (`--ignore-scripts` em tudo); o QM audita o fornecedor a ponto de **remendá-lo** (o patch de segurança da linha 58). A lição fecha o círculo do cap. 07: na era em que o harness do vizinho é sua dependência, a segurança da cadeia de suprimentos deixou de ser tema de npm e virou tema de **arquitetura de agentes**.

---

> **Consulte também**: as avaliações completas de cada elo estão no [Apêndice — O estudo](apendice-estudo.md); a leitura editorial da tendência está no [Comparativo](../benchmark/comparativo.md) (rodada ext-2) e no capítulo [14 — Convergências](14-convergencias.md).

# 12 — Extensibilidade

## O problema

Nenhum harness cobre todos os fluxos de trabalho; a extensibilidade decide se o usuário adapta o harness ou o abandona. Os eixos consagrados:

1. **Hooks** — código do usuário interceptando o ciclo de vida (antes/depois de tool, compactação, sessão).
2. **Skills / comandos custom** — capacidades empacotadas como markdown/config, carregadas sob demanda.
3. **Plugins / extensions** — pacotes distribuíveis agregando tools, comandos, hooks e config.
4. **Provedores de modelo** — a extensão mais estratégica: o harness funciona com qualquer modelo, ou é vitrine de um?

## Como os harnesses estudados implementam

### opencode — hooks profundos e agnosticismo radical de provedor
Plugins são funções que retornam `Hooks` (`packages/plugin/`): **~15 pontos de interceptação**, incluindo alguns raros — transformar mensagens e system prompt antes do envio (`experimental.chat.messages.transform`), interceptar decisões de permissão (`permission.ask`), customizar compactação (`experimental.session.compacting`) e **registrar provedores de autenticação** (`auth`). Tools custom do usuário são auto-carregadas de `tool/` do projeto. E o eixo estratégico: **~26 loaders de provedor** (`provider/provider.ts` — Anthropic, OpenAI, Google, Bedrock, Azure, Groq, Mistral, OpenRouter, Copilot...) mais **centenas de modelos via models.dev**, sobre o Vercel AI SDK. É o harness mais agnóstico de modelo em produção.

### gemini-cli — o pacote tudo-em-um
**Extensions** (`gemini-extension.json`): um único pacote instalável (de git ou local, com `/extensions install/enable/link`) pode agregar MCP servers, comandos custom, hooks, **políticas de permissão**, skills e temas — o modelo de distribuição mais completo. Comandos custom em **TOML** (`FileCommandLoader`) viram slash commands. Hooks formam um subsistema próprio (`packages/core/src/hooks/`: registry, planner, aggregator) com **gate de confiança** (`trustedHooks.ts` — hooks só rodam em pastas confiáveis, amarrando extensibilidade à segurança do cap. 07). Skills dinâmicas via tool `activate-skill`. Provedores: ecossistema Google — extensível em integração, ancorado em modelo.

### OpenHarness — compatibilidade como estratégia
A aposta: **ser extensível com o ecossistema dos outros**. Skills são markdown com frontmatter carregadas também de `~/.claude/skills` e `~/.agents/skills` (layout `SKILL.md` do anthropics/skills); plugins usam o formato `.claude-plugin/plugin.json` do Claude Code (12 plugins reais testados); hooks cobrem **10 eventos de ciclo de vida** (`HookEvent`: SESSION_START/END, PRE/POST_COMPACT, PRE/POST_TOOL_USE, USER_PROMPT_SUBMIT, STOP, SUBAGENT_STOP...) com **hot-reload**. Provedores como "workflows" nomeados: Anthropic-compatible, OpenAI-compatible, Copilot (OAuth device flow), Kimi, GLM, Ollama e outros.

## Síntese

| Aspecto | opencode | gemini-cli | OpenHarness |
|---|---|---|---|
| Hooks | ~15, os mais profundos (transform de mensagens, auth) | subsistema c/ gate de confiança | 10 eventos + hot-reload |
| Skills/comandos | comandos markdown + tools auto-carregadas | TOML + skills dinâmicas | compat. `SKILL.md` Claude |
| Plugins | funções → Hooks + tools | **extensions tudo-em-um** | formato `.claude-plugin` |
| Provedores | **~26 + models.dev** | Google | ~10 formatos/backends |
| Segurança da extensão | permissões normais | trusted folders p/ hooks | — |

Três estratégias de ecossistema: **profundidade** (opencode — os hooks alcançam pontos que os outros não expõem, e qualquer modelo serve), **empacotamento** (gemini-cli — a extension como unidade de distribuição completa, com confiança gerenciada) e **interoperabilidade** (OpenHarness — adotar os formatos do líder em vez de inventar os próprios). A última é a mais subestimada: skills e plugins em markdown/JSON estão virando *formatos portáveis entre harnesses* — o embrião de um padrão que faria pela extensibilidade o que o MCP fez pela integração. O ponto cego comum: só o gemini-cli trata código de extensão como superfície de ataque.

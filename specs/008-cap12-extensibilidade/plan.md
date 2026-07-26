# Plano — Cap. 12 (Extensibilidade)

## Fonte-base (código, reunida)
- Rodada 1: opencode (~15 hooks profundos: transform de mensagens/system prompt, `permission.ask`, `auth`; **~26 provedores + models.dev**), gemini-cli (**extensions** tudo-em-um; comandos TOML; hooks com **gate de confiança** `trustedHooks.ts`), OpenHarness (compat. `SKILL.md`/`.claude-plugin`; 10 eventos de hook + hot-reload; ~10 provedores).
- Rodada 2: Codex (hooks completos Approve/Block/Deny/Ask; plugins com marketplace; App Server JSON-RPC); OpenClaw ⭐ (**AgentSkills** padrão + registry **ClawHub** com trust envelope + scan VirusTotal/ClawScan; 159 plugins + Plugin SDK); IronClaw ⭐ (**SKILL.md compatível** OpenClaw/Claude; extração automática de skills `learning.rs`; extensões WASM/MCP sem restart); Goose (**37 provedores JSON** declarativos; CUSTOM_DISTROS; goose-sdk); Hermes (ProviderProfile subclassável — Nous Portal 300+; plugins + hooks de sessão); OpenHands (marketplaces instance/org/personal; sandbox/event-store trocáveis por DI); n8n ⭐ (**400+ nós viram tools** sem código; scanner de community nodes); ohmo (skills/plugins como raízes extras).

## Pesquisa (em andamento → verificar)
- Científico: provavelmente **rarefeito** (registrar). Ancorar em SE clássica: princípio aberto-fechado (Meyer), arquitetura de plugins/microkernel, separação mecanismo×política (Levin et al., Hydra); segurança de extensão via literatura adjacente (extensões de browser/IDE, over-privilege de plugins LLM).
- Indústria: Claude Code hooks; plugins + marketplaces; comandos custom/slash; settings hierárquicos; agnosticismo de provedor.

## Tradução em decisões (corpo)
1. **Três estratégias** (profundidade/empacotamento/interoperabilidade) — a moldura da rodada 1 persiste.
2. **A convergência de formatos** — SKILL.md/AgentSkills/.claude-plugin viram padrões portáveis: o "MCP da extensibilidade" (o dado do livro vivo).
3. **Marketplaces + scan de segurança** — ClawHub (trust envelope + VirusTotal), n8n scan-community-package, verificação de malware do Goose: distribuição virou infraestrutura, e a segurança de extensão fechou a lacuna da rodada 1 (liga ao cap. 06 tool poisoning e cap. 07).
4. **Hooks convergiram num vocabulário** (PreToolUse/PostToolUse/... Approve/Block/Deny/Ask) — Codex ≈ OpenHarness; padrão de facto.
5. **Provider-agnosticism declarativo** — adicionar provider = escrever um arquivo (Goose 37 JSON; opencode models.dev). Mecanismo×política aplicado ao modelo.
6. **Auto-extensão** — extração automática de skills do IronClaw (ponte com o cap. 16).

## Passos
1. Escrever `12-extensibilidade.md` v3. 2. Atualizar `bibliografia.md`. 3. Build. 4. Commit na branch 003.

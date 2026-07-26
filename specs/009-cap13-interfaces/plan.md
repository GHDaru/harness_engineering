# Plano — Cap. 13 (Interfaces)

## Fonte-base (código, reunida)
- Rodada 1: opencode (7 superfícies via API HTTP tipada: TUI, Electron, VS Code, GitHub Action, Slack, web, ACP/Zed), gemini-cli (TUI Ink + ~40 comandos; **headless stream-json**; VS Code companion; A2A server; SDK), OpenHarness/ohmo (2 TUIs; ohmo em Telegram/Slack/Discord/Feishu — o colega de mensageria).
- Rodada 2: OpenClaw ⭐ (**~23 canais** + Control UI + WebChat + CLI + TUI + **voz** Voice Wake/Talk Mode + apps nativos iOS/Android/macOS/Windows + Live Canvas/A2UI); Codex ⭐ (um motor Rust: TUI ratatui, `codex exec` headless JSONL, IDE via App Server, **desktop**, **cloud/web** cloud-tasks, servidor MCP, remote control); IronClaw ⭐ (CLI/REPL, WebUI SSE+WS com OIDC, Slack, Telegram, webhooks — todos pelo **mesmo contrato de turn `ProductAdapter`**, WebUI proibida de bypassar auth); Hermes (gateway multi-canal de processo único: 10 plataformas + voz + ACP + API OpenAI-compat); Goose (desktop Electron falando **ACP** com core embarcado; Telegram/Discord; modo servidor MCP/ACP); Aider (CLI/REPL streaming, browser Streamlit, **watch mode** `ai!`/`ai?`, voz-para-código); ohmo (wizard 4+6 canais; bridge com streaming/anexos; `--print`); OpenHands (Web UI ~40 rotas; headless/REST; resolvers GitHub/GitLab/Jira/Slack; SaaS); n8n (Chat Trigger + widget embarcável + streaming; canvas visual; MCP Server Trigger).

## Pesquisa (em andamento → verificar)
- Científico/HCI: mixed-initiative (Horvitz, CHI '99); Guidelines for Human-AI Interaction (Amershi et al., CHI '19); levels of automation (Sheridan & Verplank); automation bias / over-reliance; PAIR Guidebook.
- Indústria: multi-surface do Claude Code (terminal/IDE/web/desktop/mobile/SDK); headless/`--print`/stream-json; IDE integrations; UX de aprovação/streaming; ambient/async agents; chat/headless server.

## Tradução em decisões (corpo)
1. **Núcleo com front-ends** — a fronteira cedo maximiza superfícies (a lição da rodada 1 persiste; Codex "um motor Rust serve tudo").
2. **Headless estruturado é obrigatório** — stream-json/JSONL (o agente como comando de pipeline / peça programável).
3. **A superfície não é backdoor** — o `ProductAdapter` do IronClaw (mesmo contrato de turn, WebUI não bypassa auth) é a lição de segurança da dimensão (liga ao cap. 07).
4. **O colega no chat + voz** — a categoria de agentes pessoais fez da largura de canais e da voz superfícies de 1ª classe (OpenClaw ~23; Hermes gateway único).
5. **HCI ancora a UX de interação** — mixed-initiative + levels of automation justificam o dial de autonomia (plan mode/aprovações — caps. 07/09) e a visibilidade de progresso; automation bias adverte contra a superfície que esconde o que o agente faz.
6. **A superfície cloud/remota e o input fora do terminal** — Codex cloud-tasks; Aider watch mode; Live Canvas.

## Passos
1. Escrever `13-interfaces.md` v3. 2. Atualizar `bibliografia.md`. 3. Build. 4. Commit na branch 003.

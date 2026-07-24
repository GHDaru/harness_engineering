# 13 — Interfaces

## O problema

O mesmo agente precisa servir públicos diferentes: o desenvolvedor no terminal, o script de CI que precisa de JSON, o IDE que quer diffs inline, o gestor que acompanha por chat. A pergunta arquitetural é uma só: **o harness é um núcleo com múltiplos front-ends, ou um front-end com um agente dentro?** Os três harnesses estudados responderam "núcleo com front-ends" — e a qualidade dessa separação determina quantas interfaces são viáveis.

Superfícies consagradas:
- **TUI interativa** — o habitat natural do desenvolvedor.
- **Headless / não-interativo** — `-p "prompt"` com saída `text|json|stream-json`; o agente como comando de pipeline.
- **IDE** — extensão com diffs, arquivos abertos, contexto do editor.
- **CI/CD** — GitHub Actions e afins: o agente respondendo a issues e PRs.
- **Protocolos de agente** — ACP (agente ↔ editor), A2A (agente ↔ agente).
- **Chat** — Slack, Telegram, Discord: o agente como colega de canal.

## Como os harnesses estudados implementam

### opencode — a maior superfície de produto
A arquitetura cliente-servidor (cap. 02) paga aqui: um servidor HTTP com API tipada e clientes gerados permite **sete superfícies**: TUI (SolidJS via opentui), **app desktop Electron** (única entre os estudados), extensão VS Code, **GitHub Action** (`packages/github/`), **Slack** (`packages/slack/`), web (`packages/web/`, console) e **ACP** (`packages/acp` — integração Zed). Sessões compartilháveis por link conectam as superfícies entre si.

### gemini-cli — terminal rico + integração profunda de plataforma
TUI React/Ink com **~40 slash commands** resolvidos por loaders plugáveis (builtin, arquivos TOML, skills). **Headless de primeira classe**: `gemini -p` com `--output-format stream-json` (NDJSON de eventos em tempo real) — o melhor suporte a scripting dos três. **VS Code companion** (`packages/vscode-ide-companion/`) roda um servidor IDE expondo arquivos abertos e diffs ao CLI. GitHub Action oficial (`run-gemini-cli`) com automação de issues/PRs. E os protocolos: **ACP** para editores e o **A2A server** — a interface cuja "pessoa" do outro lado é outro agente (cap. 10). SDK próprio (`packages/sdk`) para embutir o núcleo.

### OpenHarness — o agente que mora no chat
CLI Typer (`oh`) com modo headless (`-p`, saída `text|json|stream-json`) e um `--dry-run` peculiar (preview sem executar modelo/tools). **Duas TUIs**: React/Ink (`frontend/terminal`, falando com o backend Python via protocolo próprio — `ui/backend_host.py`) e uma alternativa Textual. Dashboard web React para o autopilot. E a superfície distintiva: **`ohmo`**, o agente pessoal empacotado que roda em **Telegram, Slack, Discord e Feishu** (`channels/` + `ohmo/gateway/`) — o harness como colega de mensageria, com workspace próprio (`~/.ohmo/` com `soul.md`, `identity.md`).

## Síntese

| Superfície | opencode | gemini-cli | OpenHarness |
|---|---|---|---|
| TUI | SolidJS | React/Ink, ~40 comandos | React/Ink + Textual |
| Headless/JSON | sim | **stream-json NDJSON** | sim + dry-run |
| Desktop | **Electron** | — | — |
| IDE | VS Code | VS Code companion (diffs) | — |
| CI (GitHub) | Action própria | Action oficial | autopilot |
| ACP / A2A | ACP (Zed) | ACP + **A2A server** | — |
| Chat | Slack | — | **4 plataformas (ohmo)** |
| Web | web + console | — | dashboard autopilot |

A lição estrutural: **quanto mais cedo a fronteira núcleo/interface é desenhada, mais interfaces cabem depois** — opencode (API HTTP tipada) e gemini-cli (core/cli separados) colhem isso. A divergência de visão está nas pontas: o opencode aposta que o agente é um *produto* multi-plataforma; o gemini-cli, que é um *serviço de plataforma* (SDK, A2A, Action); o OpenHarness, que é um *colega* — presente onde a conversa já acontece. As três apostas provavelmente coexistirão; o headless com saída estruturada, esse já é obrigatório em qualquer harness sério.

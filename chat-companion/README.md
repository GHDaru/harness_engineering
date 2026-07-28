# chat-companion — o backend (harness-zero ao vivo)

O **companion** é o assistente do livro vivo *Engenharia de Harness*: aparece desde a capa, ajuda o leitor e mostra, a cada capítulo, **quais capacidades tem naquele momento**. Este diretório é o **backend** — um serviço FastAPI que **é o harness-zero rodando em produção** (reusa `LLMPort` e o loop de tool-calling). O **widget** (front-end no site) é uma feature à parte.

> Feita pelo ciclo oficial do spec-kit: [`specs/016-chat-companion-backend/`](../specs/016-chat-companion-backend/).

## Arquitetura em uma imagem

```
Navegador (site GitHub Pages, estático)
   │  widget flutuante — envia {session_id anônimo, message, chapter, mode}
   ▼
Backend FastAPI (Railway)            ← este diretório (backend/)
   ├─ LLMPort   → NVIDIA NIM (chave do projeto) | BYOK por requisição
   ├─ ToolPort  → tools seguras/sandbox (hora, cálculo, busca no livro)
   ├─ gating    → capacidades por capítulo (avançado × progressivo)
   └─ StorePort → Postgres (Neon)  [sem DATABASE_URL → memória, para dev]
```

**Por que um backend?** O GitHub Pages é estático (HTML/CSS/JS puro) — não guarda segredo nem roda modelo. O backend segura a chave, roda o loop, aplica o gating e persiste as conversas.

## Endpoints (sim, são vários — cada um com um papel)

| Método | Rota | Papel |
|---|---|---|
| `GET` | `/health` | healthcheck (o Railway usa) |
| `GET` | `/capabilities?chapter=NN&mode=progressivo` | mapa de capacidades — o que o widget mostra "posso fazer agora" |
| `POST` | `/session` | garante a sessão anônima do navegador |
| `POST` | `/chat` | o turno de conversa (tutor + loop de tools com gating) |
| `GET` | `/history?session_id=…` | histórico para retomar |
| `DELETE` | `/session/{session_id}` | apagar a sessão (LGPD, direito ao esquecimento) |
| `POST` | `/suggestion` | leitor envia sugestão ao autor (persiste + email se SMTP configurado) |
| `GET` | `/suggestions?token=…` | autor lê as sugestões (token por env `ADMIN_TOKEN`) |

Exemplo de `POST /chat`:

```json
{ "session_id": "anon-9f3c…", "message": "O que é um loop de agente?",
  "chapter": 2, "mode": "progressivo", "byok_key": null }
```

Resposta: `{ "reply": "...", "trace": ["🔧 hora(...)"], "mode": "...",
"chapter": 2, "capabilities_ativas": [ {rótulo, descrição, ...} ] }`.

## Modos e gating (a pedagogia virando comportamento)

- **avançado** — todas as capacidades disponíveis.
- **progressivo** — só o que o livro ensinou **até o capítulo atual**. Uma tool de um capítulo à frente não é sequer oferecida ao modelo. É o *fading* do 4C/ID e a carga cognitiva do cap. 04 virando código. O mapa completo está em [`backend/capabilities.py`](backend/capabilities.py).

## Segurança (o cap. 07 aplicado a si mesmo)

- **Nenhum segredo no repositório.** Chave do projeto e `DATABASE_URL` só em variáveis de ambiente. `.env` é gitignored; use `.env.example` como molde.
- **BYOK** (chave do próprio leitor) é usada só na requisição e **nunca** persistida nem logada.
- **Tools sandbox**: sem shell, sem leitura arbitrária de disco, sem rede de saída. Só hora, cálculo aritmético seguro (não é `eval`) e busca no texto do livro.
- **CORS** restrito às origens configuradas; **rate limit** por sessão/IP (BYOK isenta).

---

## Rodar local (sem banco, sem chave)

```bash
cd chat-companion/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload        # http://localhost:8000/health
```

Sem `.env`, sobe em modo **echo** + **memória** — ótimo para testar o fluxo. Para respostas reais, copie `.env.example` para `.env` e preencha `OPENAI_API_KEY` (NVIDIA). Testes: `python -m pytest` (sem rede, sem banco).

---

## Deploy — passo a passo

### Parte 1 · Banco no Neon (Postgres)

1. Crie uma conta em **[neon.tech](https://neon.tech)** e um **Project** (escolha a região mais próxima).
2. No projeto, abra **Connection Details** e copie a **connection string** (formato `postgresql://user:password@ep-xxxx.region.aws.neon.tech/neondb?sslmode=require`).
3. Guarde essa string — ela será a variável `DATABASE_URL` no Railway. As tabelas (`sessions`, `messages`) são criadas **automaticamente** na primeira subida do backend.

### Parte 2 · Chave do modelo (NVIDIA NIM, gratuita)

1. Crie conta em **[build.nvidia.com](https://build.nvidia.com)**.
2. Escolha um modelo com rótulo **Agent / Function Calling** e gere a chave `nvapi-…` em **Get API Key**.
3. Guarde a chave — será `OPENAI_API_KEY` no Railway.

### Parte 3 · Backend no Railway

1. Em **[railway.app](https://railway.app)**, crie um projeto: **New Project → Deploy from GitHub repo** → selecione `GHDaru/harness_engineering`.
2. Em **Settings → Root Directory**, defina **`chat-companion/backend`** (o Railway constrói e roda a partir daí; ele lê `railway.json`/`Procfile` e `requirements.txt`).
3. Em **Variables**, adicione:
   | Variável | Valor |
   |---|---|
   | `LLM_ADAPTER` | `openai` |
   | `OPENAI_BASE_URL` | `https://integrate.api.nvidia.com/v1` |
   | `OPENAI_API_KEY` | sua chave `nvapi-…` |
   | `LLM_MODEL` | um modelo com Function Calling (ex.: `nvidia/nemotron-3-ultra-550b-a55b`) |
   | `DATABASE_URL` | a connection string do Neon |
   | `ALLOWED_ORIGINS` | `https://ghdaru.github.io` |
   | `RATE_LIMIT_MSGS` | `20` (opcional) |
   | `ALLOW_BYOK` | `true` (opcional) |
4. **Deploy.** O Railway expõe uma URL pública (**Settings → Networking → Generate Domain**). Confirme em `https://SEU-APP.up.railway.app/health` → deve responder `{"ok": true, "store": "postgres"}`.
5. Guarde essa URL — o **widget** (feature 017) vai apontar para ela.

> **Nota sobre a busca no livro**: o Railway, com Root Directory `chat-companion/backend`, copia **só** essa pasta para o container. Por isso o backend embarca um **`corpus.json`** (gerado por `build_corpus.py` a partir de `livro/`) e o carrega quando o repositório completo não está presente. Em dev, o mesmo código varre `livro/` ao vivo. **Regenere o corpus quando o livro mudar**: `cd chat-companion/backend && python build_corpus.py` (idealmente no CI, antes do deploy).

### Verificar

```bash
curl https://SEU-APP.up.railway.app/health
curl "https://SEU-APP.up.railway.app/capabilities?chapter=2&mode=progressivo"
curl -X POST https://SEU-APP.up.railway.app/chat \
  -H 'content-type: application/json' \
  -d '{"session_id":"teste-1","message":"Explique o loop do agente","chapter":2,"mode":"progressivo"}'
```

## Próximo passo

**Feature 017 — o widget**: um chat flutuante (launcher que expande/minimiza) em todas as páginas do site, inclusive a capa, que lê `/capabilities` para exibir o que está ativo no capítulo atual e conversa via `/chat`. Ele guardará um `session_id` anônimo no `localStorage` e apontará para a URL pública do Railway.

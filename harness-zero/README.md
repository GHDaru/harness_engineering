# harness-zero — o harness construído do zero, capítulo a capítulo

Trilha prática do livro (ver `estudos/2026-07-25-parecer-editorial-plano-pedagogico.md`): um harness completo construído em etapas, uma por capítulo, em **Python + FastAPI**, com um **chat mínimo** como janela de observação. Arquitetura hexagonal **por refatoração** — cada porta nasce quando a dor do capítulo correspondente aparece, nunca por cerimônia antecipada. DDD aparece como consequência nomeada no código, não como teoria.

## Regras do projeto (as 4 condições do parecer editorial)

1. **DDD leve**: linguagem ubíqua = o glossário do livro; padrões táticos só onde pagam.
2. **Arquitetura por refatoração**: a etapa 1 é um arquivo; a estrutura emerge das dores.
3. **Anti-apodrecimento**: o modelo fica atrás de `LLMPort` desde a etapa 0; provedores são adapters; cada etapa é autocontida e executável.
4. **Chat congelado**: um HTML+JS servido pelo backend; evolui só quando uma dimensão exigir superfície nova.

## Como rodar qualquer etapa

```bash
pip install -r requirements.txt
cd etapas/00-chat            # ou 01-loop, ...
uvicorn app:app --reload     # abra http://localhost:8000
```

Configuração por variáveis de ambiente:

| Variável | Default | Efeito |
|---|---|---|
| `LLM_ADAPTER` | `echo` | `echo` (sem rede, para estudar o fluxo) ou `openai` (qualquer API OpenAI-compatible) |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | troque para NVIDIA NIM, Ollama, OpenRouter, etc. |
| `OPENAI_API_KEY` | — | chave do provedor |
| `LLM_MODEL` | `gpt-5.4-mini` | o modelo (qualquer um que o endpoint aceite) |

Copie `.env.example` para `.env` e preencha com a sua chave. **Nunca** comite a `.env` (já está no `.gitignore`).

## Modelo gratuito para acompanhar o livro (NVIDIA NIM) 🙏

Você não precisa pagar nada para rodar o harness-zero. A **NVIDIA** oferece um endpoint gratuito, OpenAI-compatible, com modelos capazes de tool-calling e reasoning — o que cobre todas as etapas deste livro. Agradecemos à NVIDIA por disponibilizar essa camada gratuita, que torna o livro acessível a qualquer pessoa.

**Como obter sua chave gratuita (leva ~2 minutos):**
1. Crie uma conta em **[build.nvidia.com](https://build.nvidia.com)** (o NVIDIA API Catalog).
2. Escolha um modelo com o rótulo **Agent / Function Calling** (o catálogo em [build.nvidia.com/models](https://build.nvidia.com/models) lista os disponíveis).
3. Em **"Get API Key"**, gere uma chave `nvapi-...` — é a sua, pessoal e intransferível.
4. Configure o harness-zero:

```bash
export LLM_ADAPTER=openai
export OPENAI_BASE_URL=https://integrate.api.nvidia.com/v1
export OPENAI_API_KEY=nvapi-SUA_CHAVE_AQUI     # NUNCA comite esta chave
export LLM_MODEL=nvidia/nemotron-3-ultra-550b-a55b   # ou outro modelo com Function Calling
```

> **Segurança**: uma chave de API é uma credencial. Não a coloque em código, em commits, nem a compartilhe em chats/issues. Se vazar, revogue-a em build.nvidia.com e gere outra. O harness-zero lê a chave **só** de variável de ambiente / `.env` (gitignored) — nunca a embuta no `app.py`.
>
> **Nota sobre reasoning**: modelos de reasoning da NVIDIA aceitam parâmetros extras (`extra_body={"chat_template_kwargs":{"enable_thinking":true}, "reasoning_budget":N}`). O adapter mínimo do harness-zero não os envia por padrão (o loop funciona sem eles); a partir da etapa em que isso importa, mostramos como passá-los pela porta `LLMPort`.

Créditos: modelos e endpoint gratuito cortesia da **NVIDIA** — [NVIDIA API Catalog (build.nvidia.com)](https://build.nvidia.com). Este livro não é afiliado à NVIDIA; apenas usa e credita a camada gratuita que ela oferece à comunidade.

## Mapa das etapas

| Etapa | Capítulo | O que nasce | Estado |
|---|---|---|---|
| [00-chat](etapas/00-chat/) | 00–01 | O chat e a **primeira porta** (`LLMPort`): echo → modelo real trocando um adapter | ✅ |
| [01-loop](etapas/01-loop/) | 02 | O **loop de tool-calling** (~80 linhas): a diferença entre um chat e um agente | ✅ |
| [02-tools](etapas/02-tools/) | 05 | **`ToolPort`** + schemas **derivados de tipos** (decorator `@tools.tool`; assinatura+docstring = fonte da verdade) — a cura do tédio da etapa 1 | ✅ |
| [03-contexto](etapas/03-contexto/) | 03 | **MontadorDeContexto**: system prompt em camadas (identidade → ambiente → **AGENTS.md** do projeto), remontado a cada turno; janela `/contexto` | ✅ |
| [04-sessoes](etapas/04-sessoes/) | 08 | **StorePort**: sessões persistidas (adapter **SQLite**; memória como contraste) + `session_id`/resume; 1ª evolução justificada do chat congelado | ✅ |
| [05-compactacao](etapas/05-compactacao/) | 04 | **Compactador**: a escada truncar → podar → **sumarizar via LLMPort**, por orçamento; age na *visão*, nunca no registro; indicador 🗜 no trace | ✅ |
| [06-permissoes](etapas/06-permissoes/) | 07 | **PermissionPolicy** (domínio puro: `decide()` → permitir/perguntar/negar) + **aprovação inline** (pausa→retomada do loop) + paths sensíveis **fixos**; a ferida do `read_file` fechada | ✅ |
| [07-mcp](etapas/07-mcp/) | 06 | **ClienteMCP** (stdio, JSON-RPC 2.0): initialize → tools/list → tools/call contra um **servidor de exemplo incluído**; **RegistroComposto** (locais + `mcp_*` no mesmo catálogo); política vale para MCP | ✅ |
| [08-plan](etapas/08-plan/) | 09 | **Plan mode imposto por permissões** (uma linha no `decide()`): em `planejar`, mutantes são negados; `propor_plano` → artefato **PLAN.md**; aprovar = trocar o modo | ✅ |
| [09-subagentes](etapas/09-subagentes/) | 10 | Tool **`task`** → **sessão-filha** com contexto limpo (só a descrição na ida; só o resultado na volta), loop próprio limitado, tools **só-leitura**; filhas visíveis em `/sessions` | ✅ |
| 10-evals | 11 | Suíte de evals do próprio harness (juiz + respostas gravadas) | ⏳ |
| 11-hooks | 12 | Hooks pre/post tool | ⏳ |
| 12-skills | 16 | O harness que aprende: skills com anti-padrões | ⏳ |

Cada etapa é **autocontida** (worked example completo): você pode abrir qualquer uma e rodá-la sem as anteriores — e o diff entre etapas consecutivas é a lição do capítulo.

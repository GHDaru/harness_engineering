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
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | troque para Ollama, OpenRouter, etc. |
| `OPENAI_API_KEY` | — | chave do provedor |
| `LLM_MODEL` | `gpt-5.4-mini` | o modelo (qualquer um que o endpoint aceite) |

## Mapa das etapas

| Etapa | Capítulo | O que nasce | Estado |
|---|---|---|---|
| [00-chat](etapas/00-chat/) | 00–01 | O chat e a **primeira porta** (`LLMPort`): echo → modelo real trocando um adapter | ✅ |
| [01-loop](etapas/01-loop/) | 02 | O **loop de tool-calling** (~80 linhas): a diferença entre um chat e um agente | ✅ |
| 02-tools | 05 | `ToolPort` + schemas derivados de tipos | ⏳ |
| 03-contexto | 03 | Montador de system prompt em camadas + arquivo de regras do projeto | ⏳ |
| 04-sessoes | 08 | Persistência (adapter SQLite) + `/resume` | ⏳ |
| 05-compactacao | 04 | A escada: truncar → prune → sumarizar, com indicador no chat | ⏳ |
| 06-permissoes | 07 | `PermissionPolicy` como domínio puro + aprovação inline + paths sensíveis fixos | ⏳ |
| 07-mcp | 06 | Adapter MCP client (stdio) | ⏳ |
| 08-plan | 09 | Plan mode imposto por permissões | ⏳ |
| 09-subagentes | 10 | Tool `task` com sessão-filha | ⏳ |
| 10-evals | 11 | Suíte de evals do próprio harness (juiz + respostas gravadas) | ⏳ |
| 11-hooks | 12 | Hooks pre/post tool | ⏳ |
| 12-skills | 16 | O harness que aprende: skills com anti-padrões | ⏳ |

Cada etapa é **autocontida** (worked example completo): você pode abrir qualquer uma e rodá-la sem as anteriores — e o diff entre etapas consecutivas é a lição do capítulo.

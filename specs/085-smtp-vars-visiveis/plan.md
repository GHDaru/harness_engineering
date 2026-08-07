# Plano — spec 085

## Constitution Check

| Princípio | Conformidade |
|---|---|
| I — Evidência | O diagnóstico deixa de ser inferência e passa a ser leitura direta do ambiente. |
| V — **Segurança** | Só **nomes**, só com prefixo `SMTP`. Nenhum valor, em nenhuma rota. `DATABASE_URL`, `OPENAI_API_KEY` e `ADMIN_TOKEN` ficam fora por construção. |
| VII — Spec-driven | Branch `085-smtp-vars-visiveis`, merge `--no-ff`. |

## Arquivos

| Arquivo | Mudança |
|---|---|
| `chat-companion/backend/app.py` | `smtp_vars` no `/health`. |
| `chat-companion/backend/tests/test_assinatura.py` | Nome exposto; valor nunca. |
| `chat-companion/backend/EMAIL.md` | Como ler a lista. |

## Verificação

- `pytest` do backend.
- Contra produção depois do deploy: a lista tem de mostrar o que o processo enxerga.

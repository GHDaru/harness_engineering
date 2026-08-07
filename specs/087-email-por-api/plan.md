# Plano — spec 087

## Constitution Check

| Princípio | Conformidade |
|---|---|
| I — Evidência | A troca de transporte não é preferência: a 086 mediu que 587+STARTTLS morre no timeout inteiro nesta infra. |
| II — Fonte-base é o código | O companion é o `harness-zero` em produção; a lição (transporte é detalhe de ambiente, isolado atrás de uma porta) é a do cap. 05. |
| V — **Segurança** | Chave da API só no header, nunca em log/resposta/artefato. Corpo do erro do provedor só no log do operador. |
| VI — Neutralidade | O SMTP fica como alternativa — quem hospedar fora do PaaS não precisa de conta em provedor de e-mail. |
| VII — Spec-driven | Branch `087-email-por-api`, merge `--no-ff`. |

## Arquivos

| Arquivo | Mudança |
|---|---|
| `chat-companion/backend/config.py` | `RESEND_API_KEY`, `RESEND_URL`, `EMAIL_FROM`, `transporte_email()`. |
| `chat-companion/backend/app.py` | `_enviar_por_resend`, `_enviar_email` (porta única); link mágico e sugestão passam por ela; `email` no `/health`. |
| `chat-companion/backend/tests/test_assinatura.py` | Precedência, entrega, classes por status, sigilo do token e da chave, `/health`. |
| `chat-companion/backend/EMAIL.md` | Passo a passo do Resend; SMTP vira a seção "se você hospedar noutro lugar". |
| `livro/HISTORICO.md` | Entrada da edição. |

## Verificação

- `pytest` do backend com o POST substituído (sem rede).
- Contra produção, depois de o editor pôr a chave: `/health` com `email: "resend"` e o link
  chegando de fato.

# Plano — spec 084

## Constitution Check

| Princípio | Conformidade |
|---|---|
| I — Evidência | O defeito é sustentado por medição (7,4 s vs 0,34 s), não por suposição. |
| V — **Segurança** | O detalhe vai para o log do operador; ao cliente só uma classe grosseira. Token e senha continuam fora de log, resposta e artefato. |
| VI — Acessibilidade | A mensagem ao leitor fica em linguagem comum, PT e EN. |
| VII — Spec-driven | Branch `084-smtp-diagnostico`, merge `--no-ff`. |

Sem identificador interno de modelo em nenhum artefato.

## Arquivos

| Arquivo | Mudança |
|---|---|
| `chat-companion/backend/app.py` | `_enviar_link_magico` devolve `(ok, motivo)`; mapeia exceções do `smtplib`; loga em `stderr`. `/assinar` inclui `motivo` quando `enviado:false`. `/health` declara `smtp`. |
| `chat-companion/backend/tests/test_assinatura.py` | Testes por classe de falha, com exceção injetada; garantia de que nem token nem senha vazam. |
| `publicar/tema/companion.js` | Mensagem por `motivo`, sem jargão. |
| `chat-companion/backend/EMAIL.md` | Tabela de diagnóstico: `motivo` → o que conferir. |
| `livro/HISTORICO.md` | Entrada de correção. |

## Verificação

- `pytest` do backend, com as exceções do `smtplib` injetadas por monkeypatch.
- `npm run build` (4 passos).
- Contra o backend em produção depois do deploy: `POST /assinar` tem de nomear a falha.

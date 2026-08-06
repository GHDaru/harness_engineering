# Plano — spec 080

## Constitution Check (portão)

| Princípio | Conformidade |
|---|---|
| I — Evidência acima de retórica | Nada de afirmação nova sobre harness; a spec é de infra. |
| II — A fonte-base é o código | O companion é o `harness-zero` em produção; a dor de identidade/estado é a do cap. 08 (Memória e Estado) aparecendo antes da etapa que a ensina — registrada como nota didática no `store.py`. |
| III — Método pedagógico | Sem mudança de capítulo. |
| IV — Livro vivo | Entrada no `HISTORICO.md`; sem mudança de estado da arte. |
| V — **Segurança** | Token só como hash SHA-256; SMTP só em variável de ambiente do Railway; `DELETE /leitor` implementa o direito ao esquecimento; nenhum segredo em arquivo, commit, log ou resposta HTTP. |
| VI — Neutralidade e acessibilidade | Sem custo para o leitor; nada é bloqueado sem e-mail; superfície em PT e EN. |
| VII — Spec-driven | Branch `080-assinatura-email`, merge `--no-ff`. |

Sem identificador interno de modelo em nenhum artefato.

## Arquitetura

O ponto de alavanca: **histórico, objetivo, consentimento e navegação já são indexados por
`session_id`**. Então a feature inteira se reduz a *trocar o `session_id` do navegador pelo
canônico do leitor* — o resto segue de graça. Só o progresso de leitura, que hoje nunca sai do
`localStorage`, precisa de tabela nova.

```
navegador anônimo            link mágico              navegador do leitor
cmp_sid = anon-xyz    ──►  POST /assinar (email)  ──►  e-mail com ?t=<token>
                           POST /entrar (token)   ──►  cmp_sid = <canônico>
                                  │
                                  └── merge_session(anon-xyz → canônico)
```

## Arquivos

| Arquivo | Mudança |
|---|---|
| `chat-companion/backend/store.py` | Tabelas `readers`, `magic_links`, `progress`. Métodos na porta: `criar_leitor`, `leitor_por_email`, `leitor_por_sessao`, `salvar_link`, `consumir_link`, `apagar_leitor`, `set_progresso`, `get_progresso`, `merge_session`. Implementados em `MemoryStore` **e** `PostgresStore`. |
| `chat-companion/backend/config.py` | `SITE_URL`, `MAGIC_LINK_TTL_MIN`, `RATE_LIMIT_ASSINAR`. |
| `chat-companion/backend/app.py` | Rotas `/assinar`, `/entrar`, `/progresso` (GET+POST), `/leitor` (GET+DELETE). `_enviar_email_link()` reusando o padrão best-effort de `_enviar_email_sugestao`, mas **não** best-effort: aqui a falha do envio é reportada ao leitor. |
| `chat-companion/backend/tests/` | Testes do fluxo: assinar → entrar → merge → progresso → apagar; token expirado; token reusado; e-mail inválido; ausência de enumeração. |
| `publicar/build.mjs` | Página `entrar.html` nos dois idiomas (usa o mesmo cascão das páginas avulsas). |
| `publicar/tema/entrar.js` | Consome `?t=`, chama `/entrar`, adota o `session_id`, limpa a URL, sincroniza o progresso, redireciona. |
| `publicar/tema/companion.js` | Convite discreto; estado "conectado como…"; comandos `/assinar`, `/sair`, `/apagar`; `SID` canônico substituível. |
| `publicar/tema/app.js` | Progresso passa a espelhar no servidor (`POST /progresso`) e a ler o remoto no cartão "Retomar". |
| `publicar/tema/companion.css` / `estilo.css` | Estilo do convite e da página de entrada. |
| `chat-companion/backend/EMAIL.md` | Seção do link mágico (mesmas variáveis; `SITE_URL` novo). |
| `livro/HISTORICO.md` | Entrada da edição. |

## Ordem de execução

1. Store (tabelas + métodos) com testes em `MemoryStore` — o contrato antes da rota.
2. Rotas no `app.py` + testes de API com `TestClient`.
3. `entrar.html` + `entrar.js`.
4. Convite e estado no `companion.js`; espelho de progresso no `app.js`.
5. Verificação em navegador (dois idiomas), com o backend **stubado** por `page.route()` —
   o egresso para o Railway é bloqueado no ambiente de verificação.
6. `EMAIL.md`, `HISTORICO.md`, checklist, merge.

## Verificação

- `python -m pytest chat-companion/backend/tests -q` — fluxo completo contra `MemoryStore`.
- `cd publicar && npm run build` (4 passos) — inclui o portão de links internos.
- Playwright com backend stubado: assinar → link → entrar → progresso adotado, em PT e EN.
- `grep` de alvos distintos do repositório em `docs/` — a linha de base de 9 não pode crescer.

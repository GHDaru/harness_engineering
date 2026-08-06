# Tarefas — spec 080

## Backend

- [x] T01 `store.py`: tabelas `readers`, `magic_links`, `progress` no `_init_schema`
- [x] T02 `store.py`: métodos de leitor/link/progresso/merge no `StorePort` e no `MemoryStore`
- [x] T03 `store.py`: mesmos métodos no `PostgresStore`
- [x] T04 `config.py`: `SITE_URL`, `MAGIC_LINK_TTL_MIN`, `RATE_LIMIT_ASSINAR`
- [x] T05 `app.py`: `POST /assinar` (validação, rate-limit, token hash, envio)
- [x] T06 `app.py`: `POST /entrar` (consumo do token + merge da sessão anônima)
- [x] T07 `app.py`: `GET`/`POST /progresso`
- [x] T08 `app.py`: `GET`/`DELETE /leitor`
- [x] T09 testes: assinar → entrar → merge → progresso → apagar
- [x] T10 testes: token expirado, token reusado, e-mail inválido, sem enumeração

## Frontend

- [x] T11 `build.mjs`: página `entrar.html` nos dois idiomas
- [x] T12 `tema/entrar.js`: consome `?t=`, adota `session_id`, limpa a URL, redireciona
- [x] T13 `tema/companion.js`: convite discreto + estado conectado + `/assinar`, `/sair`, `/apagar`
- [x] T14 `tema/app.js`: espelho do progresso no servidor + leitura do remoto no "Retomar"
- [x] T15 CSS do convite e da página de entrada

## Fechamento

- [x] T16 `EMAIL.md`: seção do link mágico e a variável `SITE_URL`
- [x] T17 verificação em navegador (PT e EN) com backend stubado
- [x] T18 `npm run build` 4 passos + alvos de repositório em `docs/` sem crescer
- [x] T19 `HISTORICO.md` + checklist `.specify/memory/checklist-verificacao.md`
- [ ] T20 merge `--no-ff` na `main`, push, CI verde conferido

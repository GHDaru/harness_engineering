# Tarefas — spec 093

## Backend
- [ ] T01 `store.py`: tabela `consentimentos` (append-only)
- [ ] T02 `store.py`: `registrar_consentimento` / `consentimentos_de` (estado = última linha)
- [ ] T03 `store.py`: `emails_com_contato` (só ativos) e `capitulos_lidos` (de `nav_events`)
- [ ] T04 `app.py`: `POST` e `GET /consentimento`
- [ ] T05 `app.py`: `GET /progresso/detalhe`
- [ ] T06 `app.py`: `GET /leitores` (admin; desligado sem `ADMIN_TOKEN`)
- [ ] T07 testes: dar, revogar, regravar; revogar contato preserva continuidade; export só com token

## Frontend
- [ ] T08 `build.mjs`: cartão "Sua leitura" substitui o "Retomar"; expõe a lista de capítulos ao JS
- [ ] T09 `tema/app.js`: progresso local + remoto; barra e contagem
- [ ] T10 `build.mjs` + `app.js`: bloco de fim de capítulo (1º em diante, dispensável)
- [ ] T11 `tema/companion.js` + `entrar.js`: consentimento de contato + revogação
- [ ] T12 CSS

## Fechamento
- [ ] T13 verificação em navegador (PT e EN)
- [ ] T14 build 4 passos + alvos de repositório sem crescer + corpus
- [ ] T15 `HISTORICO.md` + checklist
- [ ] T16 merge `--no-ff`, push, CI verde
- [ ] T17 editor: rodar `/apagar` (reset da base) e definir `ADMIN_TOKEN` quando for exportar

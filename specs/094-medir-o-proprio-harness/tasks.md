# Tarefas — spec 094

## Correção do repositório (cada item justificado sem o placar)
- [ ] T01 `Makefile` na raiz: `make test` roda as três suítes; `make lint`, `make build`
- [ ] T02 `pyproject.toml` na raiz: `testpaths` dos dois projetos Python + config do Ruff
- [ ] T03 `.claude/hooks/`: `guarda-segredo`, `guarda-identidade`, `guarda-git`, `formata-python`
- [ ] T04 `.claude/settings.json`: registra os quatro hooks nos eventos corretos
- [ ] T05 CI: passo de lint não-bloqueante no workflow que já roda os testes
- [ ] T06 testar os hooks de verdade (bloqueiam o que devem, deixam passar o resto)

## Medição
- [ ] T07 rodar o scanner de novo e capturar o placar "depois" (JSON + texto)

## Livro
- [ ] T08 `livro/apendice-harness-score.md` — o apêndice "Meça o seu harness" (antes, depois, recusas)
- [ ] T09 cap. 11: seção nova em "O estado da arte" + Leitura executiva atualizada
- [ ] T10 cap. 01 §4: a quinta definição convergente
- [ ] T11 `livro/bibliografia.md`: entrada verificada
- [ ] T12 `publicar/sumario.json` + `sumario.en.json`: o apêndice na mesma posição nos dois

## Traduzir o delta (spec 067)
- [ ] T13 `livro/en/appendix-harness-score.md` + selo com hash real
- [ ] T14 `livro/en/chapters/11-verification-evals.md` + selo regravado
- [ ] T15 `livro/en/01-foundations.md` + selo regravado
- [ ] T16 `livro/en/bibliography.md` + selo regravado

## Fechamento
- [ ] T17 build 4 passos + 81 testes + corpus regenerado
- [ ] T18 alvos de repositório sem crescer (baseline 9) + verificação em navegador
- [ ] T19 `HISTORICO.md` + checklist de verificação
- [ ] T20 merge `--no-ff`, push, CI verde

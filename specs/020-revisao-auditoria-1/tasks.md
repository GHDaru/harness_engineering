# Tasks: Rodada de auditoria e revisão 1

**Feature**: `020-revisao-auditoria-1` · **Plan**: [plan.md](./plan.md)

> **Lista rolante.** Cada observação do autor entra como uma task `O###`
> (Onde · O quê · Correção aplicada · Evidência, quando factual). A rodada
> fecha com o registro no HISTORICO + build verde + merge único na `main`.

## Observações → correções

<!-- modelo:
- [ ] **O001** `livro/capitulos/NN-arquivo.md` · seção "…" — <observação do autor> →
      correção: <o que foi trocado>. Evidência: <path/URL, se factual>.
-->

_(aguardando as observações do autor)_

## Fechamento da rodada
- [ ] **F1** `livro/HISTORICO.md`: edição 0.16 (revisão — auditoria 1) com resumo das correções + modelo de IA (A3).
- [ ] **F2** `node build.mjs` verde (link-check); screenshots das páginas tocadas aprovados pelo autor; sem identificador interno de modelo.
- [ ] **F3** Merge único `--no-ff` na `main` + push (publica o lote). (Opcional: autor cria Release → DOI de versão.)

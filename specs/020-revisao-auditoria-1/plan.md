# Implementation Plan: Rodada de auditoria e revisão 1

**Branch**: `020-revisao-auditoria-1` · **Date**: 2026-07-27 · **Spec**: [spec.md](./spec.md)

## Summary
Aplicar as observações da auditoria do autor como correções rastreáveis, tudo na branch `020-…`; preview por screenshots; ao final, merge único na `main` (publica uma vez) + Release/DOI opcional.

## Constitution Check
PASS. I (evidência) — correções factuais mantêm caminho/fonte. IV (livro vivo) — edição de revisão no HISTORICO; benchmark nunca sobrescrito silenciosamente. VII — branch por spec, merge ao fim. Sem segredo; sem identificador interno de modelo.

## Fluxo operacional
1. **Intake**: cada observação do autor → uma task `O###` em `tasks.md` (onde + o quê + correção).
2. **Aplicar** na branch; agrupar por arquivo para diffs limpos.
3. **Preview**: `node build.mjs` + screenshots das páginas tocadas → autor aprova/ajusta.
4. **Fechar**: registrar edição no HISTORICO; build verde; **merge --no-ff** na main; push.
5. **(Opcional)** autor cria Release `v0.16.0` → DOI de versão.

## Arquivos (variáveis conforme as observações)
```
livro/**                 # o alvo típico das correções
benchmark/** publicar/**  # se a observação tocar aqui
livro/HISTORICO.md       # edição de revisão 0.16
specs/020-revisao-auditoria-1/tasks.md  # a lista rolante de observações→correções
```

## Complexity Tracking
Sem violações. Correção que vira reescrita estrutural grande → migra para spec próprio.

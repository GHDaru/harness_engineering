# Spec 070 — Companion 100% bilíngue

**Branch**: `070-companion-en` · **Data**: 2026-08-01 · **Status**: aprovada ("pode seguir com o companion")

Fecha a limitação conhecida da spec 067: TODAS as strings visíveis do widget
(paleta, tour, bastidores, sugestão, BYOK, plano, tooltips, erros) passam por
`tx(pt, en)`, com PT byte-idêntico ao atual. Guarda-corpo do bug histórico:
nenhuma variável pode sombrear `tx` (lição do fix noturno de 01/08).

## Verificação
node --check; auditoria por grep de literais PT fora de tx(); e2e: widget em
página EN abre com superfície inglesa (launcher, banner, paleta).

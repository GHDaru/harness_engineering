# Spec 071 — Radar-jornal: o diário como site de notícias

**Branch**: `071-radar-jornal` · **Data**: 2026-08-01 · **Status**: aprovada ("acione um ux/ui... estilo sites de notícias... para validarmos")

## UX (validação com o site real, hoje + 1 dia atrás)

- Nova página `docs/radar.html` gerada no build de `radar/diario/*.md` (PT-only,
  registro operacional): **masthead** de jornal + tagline com o contrato; **abas
  por edição** (2026-08-01, 2026-07-31 — sem retroativo; dias futuros acumulam
  sozinhos); **manchete** = achado de maior impacto do dia (card destacado);
  grid de cards por achado com **badge de impacto A/B/C** e **chips de fontes
  por domínio** (estilo jornalístico: toda afirmação com fonte clicável);
  caixas de transparência — "Como esta edição foi apurada" (consultas,
  colapsável), "Da redação: o que ficou de fora — e por quê" (descartes) e
  "Leituras executivas em risco".
- **Parse tolerante** (`publicar/jornal.mjs`): bloco que não casar o formato
  vira matéria corrida — o jornal nunca quebra por causa do diário.
- Entradas: o "ver o Radar completo →" da capa e da entrada (PT e EN) agora
  apontam para `radar.html` (antes: RADAR.md cru no GitHub); rodapé do jornal
  liga a mesa de edição (RADAR.md) e o contrato (AGENTE.md).

## Verificação
Build + portões PT/EN; e2e: manchete, badges, chips de fontes, 2 edições,
caixas de transparência, links da capa/entrada → radar.html; screenshot ao editor.

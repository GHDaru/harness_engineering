# Spec 061: News na entrada — a última do Radar + o que mudou nesta edição

**Feature Branch**: `061-news-entrada` · **Criada em**: 2026-07-31

## Conceito

A entrada do livro ganha uma faixa de "jornal vivo", **derivada no build** (zero curadoria extra):
1. **Destaque** — a notícia mais recente e relevante do **RADAR** (`radar/RADAR.md`, alimentado pelo agente diário): card âmbar com data, impacto e o item com link para a fonte, + link para o Radar completo.
2. **Menos destaque** — "Nesta edição": a última entrada do **HISTORICO** (versão, data, título da edição), linkando ao Histórico.

Auto-atualização estrutural: radar novo ou edição nova ⇒ o build seguinte muda a capa sozinho.

## Requisitos

- FR-001 (build): parse determinístico — 1ª linha de dados da tabela do RADAR que não seja o marcador "(inicial)" (célula do item renderizada como Markdown inline; data e impacto exibidos); 1ª entrada `### Edição X.Y — data · título` do HISTORICO. Falha de parse ⇒ bloco omitido (a entrada nunca quebra).
- FR-002 (UI): `.ent-news` (card com a linguagem âmbar do Retomar, kicker "🗞 Radar do livro vivo · data · impacto X") entre o hero e o Retomar; `.ent-vedicao` (linha discreta) logo abaixo: "📖 Nesta edição (vX.Y.0 · data): título — Histórico".
- FR-003: theme-aware; e2e: os dois blocos renderizam com o conteúdo real (MCP 2026-07-28 / edição 0.56), links corretos; portões verdes.

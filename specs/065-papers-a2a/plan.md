# Plano — Spec 065 (papers + A2A)

## Método

1. **Leitura**: 3 agentes em paralelo (um por paper), via WebFetch do arxiv/GitHub,
   com mandato explícito de só reportar o que está no texto (metadados verificados,
   números, trechos citáveis) — a busca de ontem pode ter exagerado; divergências
   viram registro no diário do Radar (R1).
2. **Conferência A2A** (independente dos agentes): o cap. 17 já dizia "v1.0 em 2026"
   na tabela — o adendo ganha o resultado da conferência (3 camadas, v1.0.1 com
   extensões formais, fonte primária a2a-protocol.org) e a simetria editorial com o
   MCP ("extensões formais em vez de features no núcleo").
3. **Julgamento**: com os relatórios em mãos, decidir por paper: entra na
   bibliografia? gera nota em capítulo? contradiz algo (gatilho A)?

## Mudanças por arquivo

- `livro/capitulos/17-protocolos.md` — adendo enriquecido (feito antes dos agentes).
- `livro/bibliografia.md` — até 3 itens novos verificados, com nota opinativa.
- `livro/capitulos/11-verificacao-evals.md` — nota datada: avaliação de evolução de
  harness (o que o paper propõe; o que valida/refina no método do benchmark).
- `livro/capitulos/04-compactacao.md` — nota datada: CompactionRL como terceira via
  (harness compacta → API compacta → **modelo treinado com compactação**).
- `radar/RADAR.md` + `radar/diario/2026-07-31.md` — status + achados/divergências.
- `livro/HISTORICO.md` — edição 0.60.

## Riscos

- Proxy pode bloquear arxiv → fallback /abs; se nada acessível, o item volta a ⏳
  com o motivo no diário (execução honesta > incorporação especulativa).
- Papers de julho/2026 podem ser preprints frágeis → nota opinativa deixa claro o
  status (preprint) e o que esperar da janela 2026-10.

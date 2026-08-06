# Feature Specification: Rodada ext-4 — Prime Agent, e a compactação em xeque

**Feature Branch**: `082-ext4-prime-agent`

**Created**: 2026-08-06

**Status**: Aprovada pelo editor ("bora" + fork entregue)

**Input**: Notícia trazida pelo editor; avaliação preliminar registrada no RADAR como **impacto A**.

## Por que esta rodada é diferente

É a primeira promoção em que o candidato pode **derrubar uma síntese** do livro em vez de
acrescentar um adendo. O anúncio do Prime Agent afirma que *"fixed tool-calling schemas and
context compaction force the model to work around its own scaffolding instead of leveraging
it"* e propõe **contexto como variável** num REPL persistente. A Leitura executiva do cap. 04
apresenta a compactação como *a* resposta à janela de contexto — e já está marcada como **em
risco** na seção correspondente do `RADAR.md`.

## Dois achados que a leitura preliminar já produziu

1. **O Prime Agent é construído sobre o Pi.** O LICENSE mantém "Copyright (c) 2025 Mario
   Zechner"; os pacotes são `@earendil-works/pi-agent-core`, `pi-ai`, `pi-coding-agent`,
   `pi-tui`; o README credita `badlogic/pi-mono`. Por cima entram `prime-agent-runtime/src/rlm`
   e a skill `rlm-heartbeat`. **Consequência para o apêndice da cadeia de suprimentos**: o Pi
   passa a alimentar **cinco** sistemas (QM como motor com patch próprio, Kimi Code como TUI,
   Traycer como provider, o fork Oh My Pi, e agora o Prime Agent como base inteira).
2. **A ironia editorial que fecha o argumento do cap. 12**: o Pi foi avaliado com o **menor
   total do corpus** (26/36) porque recusa metade das dimensões por manifesto — e é exatamente
   essa base recusante que um laboratório de fronteira escolheu para construir o harness mais
   radical do estudo. A tese do Pi ("agressivamente extensível para não ditar seu workflow")
   recebe aqui sua validação mais forte possível.

## Triagem (contrato, spec 081)

Fonte primária lida (blog oficial) e API do repositório consultada: **MIT**, TypeScript,
**2.806★ / 208 forks (13,5:1 ✓)**, criado 2026-05-08, push no dia da avaliação, 112 issues
abertas. Passa o teste de inclusão do cap. 01 §4 sem ressalva.

Commit congelado: fork `GHDaru/prime-agent`, commit `0e0d233`.

## Entregas

1. `benchmark/avaliacoes/prime-agent.md` — com a pergunta central respondida: **o que ele
   acrescenta ao Pi**, dimensão por dimensão.
2. **Veredito sobre o cap. 04**: a Leitura executiva cai, ganha ressalva ou permanece intacta —
   decidido pela leitura do código, não pelo anúncio.
3. notas.json, comparativo (leitura da rodada ext-4), apêndice do estudo, corpus 20 → 21.
4. Apêndice da cadeia de suprimentos: o elo Pi→Prime Agent e a contagem atualizada.
5. Delta EN + selos; corpus do companion; HISTORICO; CI verde.

## Aceite

- [ ] Avaliação distingue explicitamente herdado-do-Pi de contribuição-própria
- [ ] Veredito do cap. 04 fundamentado em caminhos de arquivo
- [ ] ⏳ mantido sobre o número do ARC-AGI-3 (reivindicação do vendor, não conferida)
- [ ] Build 4 passos verde; CI verde na main

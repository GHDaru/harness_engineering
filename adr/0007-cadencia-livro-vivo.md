# ADR 0007 — Cadência de revisão do livro vivo

- **Status**: aceita (2026-07-29)
- **Feature**: `052-cadencia-livro-vivo`

## Contexto

O livro declara "estado da arte capturado em 2026-07" em todos os capítulos e mantém 16 forks avaliados (Apêndice — O estudo). A cláusula de expiração é tese central da obra: sem uma política explícita de re-sincronização e re-revisão, o "livro vivo" vira promessa vazia — mas revisar a cada release de cada harness é insustentável para um autor.

## Alternativas avaliadas

- **A — Contínua** (revisar a cada release de qualquer harness do corpus): fidelidade máxima, custo proibitivo e ruído editorial (a maioria dos releases não muda dimensão nenhuma).
- **B — Trimestral fixa**: previsível e barata, mas cega a eventos grandes entre janelas (ex.: compaction chegando à API do provedor — exatamente o tipo de mudança que o livro promete rastrear).
- **C — Anual**: incompatível com a meia-vida do assunto; o placar de expiração ficaria vermelho o ano todo.
- **D — Híbrida: janela trimestral + gatilho extraordinário** (escolhida).

## Decisão

**D.** Duas engrenagens:

1. **Janela trimestral** (próxima: **2026-10**): re-sync dos 16 forks (`scripts/sync-forks.ps1`), diff dirigido por dimensão (só o que toca as 12+2 dimensões do benchmark), atualização dos Apêndices A afetados, do placar de expiração e das datas de revisão; edição minor no HISTORICO.
2. **Gatilho extraordinário**: qualquer evento que **invalide uma "Leitura executiva"** (mudança de protocolo, capacidade migrando para o provedor, harness do corpus arquivado/renomeado) dispara revisão pontual do capítulo afetado, sem esperar a janela.

## Justificativa

A Leitura executiva (C08) é o contrato de frescor de cada capítulo — é o que o leitor executivo confia. Usá-la como critério de gatilho torna a política *observável*: a revisão acontece quando a síntese deixaria de ser verdadeira, não quando o calendário manda nem quando um changelog qualquer cresce.

## Consequências

- O Guia Editorial ganha a seção "Cadência do livro vivo" (política operacional).
- O placar de expiração do HISTORICO continua sendo a fonte das datas; a janela seguinte fica declarada no Guia.
- Rodadas novas do benchmark continuam nascendo por spec-kit, como sempre.

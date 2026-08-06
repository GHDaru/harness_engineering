# Feature Specification: O companion passa a conhecer o Radar e as avaliações

**Feature Branch**: `077-companion-corpus-radar`

**Created**: 2026-08-05

**Status**: Aprovada (defeito relatado pelo editor: "perguntei sobre o grok e ele não achou a chamada no radar")

## Defeito

Perguntas sobre um sistema avaliado ou sobre uma apuração recente caíam no vazio. Três causas
independentes, encontradas ao diagnosticar:

1. **Escopo**: `ragindex.py` indexava só `livro/**` + `benchmark/comparativo.md`. As **20
   avaliações individuais** (onde mora a evidência por caminho de arquivo) e o **Radar inteiro**
   (mesa + diários) estavam fora. O tutor tinha as menções de passagem nos capítulos, não a
   apuração.
2. **Blocos**: markdown não põe linha em branco entre linhas de tabela, então **a mesa inteira do
   RADAR virava UM bloco**. Ele casava com qualquer pergunta (contém todos os termos do projeto)
   e — pior — o trecho enviado ao modelo é truncado em 600 caracteres, cortando justamente a
   linha procurada. O tutor recebia o cabeçalho da tabela como "evidência".
3. **Pontuação**: o score contava **cada ocorrência** de termo, sem normalizar por tamanho. Um
   bloco longo que repetisse uma palavra comum vencia um bloco curto e exato.

## Correções

1. Índice cobre `livro/**` + `benchmark/{comparativo,README}.md` + `benchmark/avaliacoes/*.md`
   + `radar/{RADAR,AGENTE}.md` + `radar/diario/*.md`. Corpus: **738 → 1.406 blocos**.
2. Cada linha de tabela vira um bloco próprio (o separador `|---|` é ignorado).
3. Score = **termos distintos** da pergunta encontrados, com divisor logarítmico de tamanho.
4. **Frescor**: o Radar muda todo dia e o agente só escreve em `radar/`; o CI passa a regenerar
   `corpus.json` e commitá-lo de volta quando muda. Sem isso o tutor responderia sempre com um
   dia de atraso. `corpus.json` não está nos paths do gatilho ⇒ o push não re-dispara o workflow.

## Aceite

- [x] "o que vocês acharam do Grok Build" traz `benchmark/avaliacoes/grok-build.md`
- [x] "o que o radar achou sobre a Microsoft Agent Harness" traz `radar/diario/2026-08-05.md`
- [x] "opencode perdeu acesso à assinatura Claude" traz os diários de 04 e 03/ago
- [x] O trecho de uma linha do RADAR chega íntegro ao modelo (não truncado no cabeçalho)
- [x] 14 testes do backend verdes
- [ ] CI verde na main (inclusive o passo novo de regeneração)

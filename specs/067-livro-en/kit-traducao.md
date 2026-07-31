# Kit de tradução PT→EN (spec 067) — REGRAS OBRIGATÓRIAS

## Formato do arquivo traduzido

1. **Primeira linha** (antes de tudo): `<!-- i18n fonte:<caminho-pt> edicao:0.61 hash:<md5-8> -->`
   onde `<md5-8>` = primeiros 8 caracteres de `md5sum <caminho-pt>` (calcule de verdade).
2. Depois, o Markdown traduzido, preservando EXATAMENTE a estrutura (mesmos níveis de heading, mesmas tabelas, mesmos blocos).

## O que NÃO traduzir
- Blocos de código, caminhos de arquivo, nomes de classes/funções (`LoopDoAgente` fica `LoopDoAgente` — é a linguagem ubíqua do harness-um; quando citado, explique uma vez: "`LoopDoAgente` (AgentLoop)").
- Citações que já estão em inglês (ficam idênticas, verbatim).
- URLs, nomes próprios, nomes de sistemas (Grok Build, Pi, gemini-cli…), siglas (MCP, A2A, RAG…).
- `<div data-viz="...">` e qualquer HTML embutido (traduza só texto visível/alt/figcaption).

## Datação (formato EXATO — o motor parseia)
PT: `> **Estado da arte capturado em 2026-07** · última revisão AAAA-MM-DD · [histórico...](HISTORICO.md)`
EN: `> **State of the art captured in 2026-07** · last revised AAAA-MM-DD · [history and expiration log](../historico.html)`

## Seções fixas dos capítulos (traduções canônicas)
| PT | EN |
|---|---|
| Objetivos de aprendizagem | Learning objectives |
| O problema | The problem |
| Fundamentos científicos | Scientific foundations |
| Fontes da indústria | Industry sources |
| O estado da arte | The state of the art |
| Leitura executiva | Executive summary |
| Mão na massa — harness-zero, etapa N | Hands-on — harness-zero, step N |
| Verificação (exercícios no fim) | Check your understanding |
| Apêndice A — Como cada repositório trata X | Appendix A — How each repository handles X |

## Glossário fixo
harness = harness (nunca traduzir) · livro vivo = living book · cláusula de expiração = expiration clause · portão de qualidade = quality gate · rodada = round · "o que roubar" = "what to steal" · Leitura executiva = Executive summary · caixa de ferramentas = toolbox · ferramenta = tool · permissões = permissions · janela de contexto = context window · compactação = compaction · sumarização = summarization · subagente = subagent · gancho = hook · habilidade = skill · divulgação progressiva = progressive disclosure · corpus do estudo = study corpus · coorte = cohort · "cap. NN" = "ch. NN" · edição (do livro) = edition

## Tabela de slugs (links internos entre páginas do livro → usar o alvo EN)
| Fonte PT | Arquivo EN (em livro/en/) | Slug/página EN |
|---|---|---|
| livro/00-introducao.md | 00-introduction.md | 00-introduction.html |
| livro/01-fundamentos.md | 01-foundations.md | 01-foundations.html |
| livro/capitulos/02-loop-do-agente.md | chapters/02-agent-loop.md | 02-agent-loop.html |
| livro/capitulos/03-entrega-de-contexto.md | chapters/03-context-delivery.md | 03-context-delivery.html |
| livro/capitulos/04-compactacao.md | chapters/04-compaction.md | 04-compaction.html |
| livro/capitulos/05-ferramentas.md | chapters/05-tool-design.md | 05-tool-design.html |
| livro/capitulos/06-mcp.md | chapters/06-mcp.md | 06-mcp.html |
| livro/capitulos/07-permissoes-sandbox.md | chapters/07-permissions-sandboxing.md | 07-permissions-sandboxing.html |
| livro/capitulos/08-memoria-estado.md | chapters/08-memory-state.md | 08-memory-state.html |
| livro/capitulos/09-planejamento.md | chapters/09-planning.md | 09-planning.html |
| livro/capitulos/10-subagentes-orquestracao.md | chapters/10-subagents-orchestration.md | 10-subagents-orchestration.html |
| livro/capitulos/11-verificacao-evals.md | chapters/11-verification-evals.md | 11-verification-evals.html |
| livro/capitulos/12-extensibilidade.md | chapters/12-extensibility.md | 12-extensibility.html |
| livro/capitulos/13-interfaces.md | chapters/13-interfaces.md | 13-interfaces.html |
| livro/14-convergencias.md | 14-convergences.md | 14-convergences.html |
| livro/capitulos/15-harness-embutido.md | chapters/15-embedded-harness.md | 15-embedded-harness.html |
| livro/capitulos/16-aprendizado-auto-evolutivo.md | chapters/16-learning-self-improvement.md | 16-learning-self-improvement.html |
| livro/capitulos/17-protocolos.md | chapters/17-protocol-layer.md | 17-protocol-layer.html |
| benchmark/comparativo.md | comparative.md | comparative.html |
| livro/glossario.md | glossary.md | glossary.html |
| livro/apendice-estudo.md | appendix-study.md | appendix-study.html |
| livro/apendice-uso.md | appendix-usage.md | appendix-usage.html |
| livro/apendice-grafo.md | appendix-graph.md | appendix-graph.html |
| livro/apendice-harness-um.md | appendix-harness-um.md | appendix-harness-um.html |
| livro/bibliografia.md | bibliography.md | bibliography.html |
| livro/GUIA-EDITORIAL.md | editorial-guide.md | editorial-guide.html |
| livro/autor.md | author.md | author.html |
| livro/HISTORICO.md | **não traduzir** | ../historico.html (link direto para o PT) |

Links para HISTORICO.md, radar/ e arquivos fora do site → apontar para a versão PT
(`../historico.html`) ou para o GitHub, com "(in Portuguese)" quando for texto corrido.

## Tom
Inglês técnico natural (não literal); manter a voz opinativa e as metáforas do original;
manter **negritos** e *itálicos* onde estão; números no formato EN (66.8, não 66,8) —
EXCETO dentro de citações e código.

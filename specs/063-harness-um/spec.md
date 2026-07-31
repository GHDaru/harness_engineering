# Spec 063 — harness-um: a implementação de referência do livro

**Branch**: `063-harness-um` · **Data**: 2026-07-31 · **Status**: aprovada (nome e hospedagem decididos pelo editor)

## Contexto

O editor pediu: *"se fossemos implementar o melhor harness com todas as features que
colocamos no livro, qual seria o código? qual seria a linguagem ubíqua? como baixar?"*
O nome proposto ("openharness") colide com o HKUDS/OpenHarness — sistema real que está
no **corpus do benchmark do livro**. Decisão do editor via gate: nome **harness-um**
(progressão de harness-zero) e código **no repositório do livro**, ao lado do
harness-zero. Um apêndice declara tudo, com figura oficial.

## O que é o harness-um

A resposta executável do livro à própria pergunta que ele estuda: um harness **completo,
pequeno e legível**, que reúne num único sistema as features que os 18 capítulos
descrevem — não um produto, uma **referência**: o código que o leitor lê depois de ler
o livro, e do qual pode partir.

## A linguagem ubíqua (decisão central)

O código fala **a língua do livro** (DDD): cada termo do domínio vira um nome de
código idêntico, em português — `Harness`, `Turno`, `Ferramenta`, `Politica`,
`Memoria`, `Plano`, `Subagente`, `Verificador`, `Gancho`, `Habilidade`, `Compactador`,
`Provedor`. Ler o código É reler o sumário. A tabela termo → classe → capítulo é
parte do apêndice.

## Requisitos

- **R1 — Cobertura**: cada capítulo de funcionalidade (02–13) tem sua feature
  implementada e apontada no código: loop com orçamento de turnos (02), montagem de
  contexto em camadas (03), compactação por resumo estrutural (04), ferramentas com
  esquema derivado de assinatura (05), cliente MCP stateless pós-2026-07-28 (06),
  política de permissões permitir/perguntar/negar (07), memória persistente
  (`MEMORIA.md`) + sessões em disco (08), plano como artefato (09), subagente com
  contexto limpo (10), verificadores pós-mutação (11), ganchos e habilidades (12),
  interface REPL (13).
- **R2 — Roda sem chave**: `ProvedorEco` permite executar e testar tudo offline;
  `ProvedorAnthropic` liga num modelo real via `ANTHROPIC_API_KEY` (env; nunca no repo).
- **R3 — Pequeno e legível**: pacote Python único (`harness_um/`), stdlib + httpx;
  cada módulo abre citando o capítulo que implementa.
- **R4 — Testado**: pytest cobrindo loop, ferramentas, permissões, compactação,
  memória, plano, subagente, verificação e ganchos — verde no CI do livro.
- **R5 — Apêndice vivo** (`livro/apendice-harness-um.md`): o que é, a linguagem
  ubíqua (tabela), a figura oficial, **como baixar e rodar** (git clone + 2 comandos),
  relação com o harness-zero, cláusula de expiração.
- **R6 — Figura oficial**: identidade visual derivada da capa/favicon (núcleo âmbar +
  anel), em SVG (fonte) e PNG (site/README), creditada no apêndice.
- **R7 — Nome sem colisão**: "harness-um" em todo artefato público; o apêndice
  explica a escolha (e a colisão evitada) com honestidade editorial.

## Fora de escopo

- Paridade de produto com os 16 sistemas do corpus (é referência didática, não CLI
  de mercado); UI web; publicação em PyPI (pode virar spec futura).

## Verificação

- `pytest` do harness-um verde localmente e no CI (passo novo no workflow).
- Portões do site continuam verdes (apêndice entra no aparato).
- e2e Chromium: apêndice renderiza a figura, a tabela da linguagem ubíqua e o bloco
  "como baixar"; sumário lista o apêndice.
- REPL fumaça: sessão com ProvedorEco executa uma ferramenta de ponta a ponta.

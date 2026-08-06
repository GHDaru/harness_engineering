# Feature Specification: Radar — capa e acervo (o jornal que aguenta um ano)

**Feature Branch**: `076-radar-capa-acervo`

**Created**: 2026-08-05

**Status**: Aprovada — proposta de UX apresentada e aceita pelo editor, com as duas decisões
respondidas: **7 dias** na capa e **só A/B** na mesa.

## Problema (medido, não intuído)

O jornal da spec 071 renderiza **todas** as edições numa página só, com uma aba por dia. Com 6
edições está ótimo; a projeção mostra dois pontos de ruptura, e o primeiro é de usabilidade:

| Horizonte | Edições | Achados | HTML | Abas |
|---|---:|---:|---:|---:|
| hoje | 6 | 31 | 50 KB | 6 ✅ |
| 1 mês | 30 | 155 | 250 KB | **30** ⚠️ |
| 3 meses | 90 | 465 | 700 KB | 90 ❌ |
| 1 ano | 365 | 1.885 | **3 MB** | 365 ❌ |

Por volta de **três semanas** a fita de abas vira parede de datas — e "2026-08-14" não ajuda
ninguém a escolher. O peso só incomoda no terceiro mês. O prazo real era de duas semanas.

**Diagnóstico**: a cronologia é o único eixo de navegação. Mas as perguntas de quem chega ao
Radar são outras — *o que mudou no livro?*, *o que espera decisão?*, *o que apareceu hoje?* —
e a informação mais acionável (a tabela do `RADAR.md`, com status, capítulo e impacto) **não
aparecia no site**.

## Requisitos

1. **Capa** (`radar.html`) com as **7 edições** mais recentes — tamanho constante para sempre.
2. **Placar da semana** derivado do próprio conteúdo: edições, achados, quantos A/B, quantos
   promovidos na janela.
3. **Mesa de edição** na capa: itens **abertos de impacto A/B** do `RADAR.md`, no máximo **5**,
   ordenados por impacto e data, com link para a tabela completa e a contagem do que sobrou.
4. **Filtro por impacto** client-side (sem framework), com **contagem no chip** e chip
   desabilitado quando não há itens — filtro que zera a página sem aviso é beco sem saída.
5. **Acervo mensal**: uma página por mês (`radar-AAAA-MM.html`), edições colapsadas, navegação
   ‹ mês anterior · atual · próximo ›. Crescimento vira horizontal.
6. Portão de links internos passa a validar as páginas novas.
7. O contrato do agente (`radar/AGENTE.md`) **não muda** — ele continua escrevendo um arquivo
   por dia, sem saber que existe acervo.

## Fora de escopo (fase 2, quando fizer falta)

- Busca client-side sobre índice JSON gerado no build.
- **Fio da história**: encadear as aparições de um mesmo item ao longo dos dias (o caso opencode:
  ⏳ em 03/ago → confirmado em 04/ago). É o mais interessante editorialmente, mas exige que o
  agente marque continuidade nos diários — ou seja, mexe no contrato.

## Aceite

- [ ] Capa com placar, mesa (5 itens A/B), filtro com contagem e 7 edições.
- [ ] Uma página de acervo por mês, com navegação entre meses nos dois sentidos.
- [ ] Nenhuma duplicação de conteúdo entre capa e acervo (caixas só na edição do dia).
- [ ] Filtro verificado no navegador (mostra/esconde, chip vazio desabilitado, zero erro de JS).
- [ ] Sem vazamento de sintaxe de markdown nos resumos da mesa.
- [ ] Build 4 passos verde; CI verde na main.

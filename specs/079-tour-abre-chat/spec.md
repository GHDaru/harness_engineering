# Feature Specification: O tour abre o chat quando fala do chat

**Feature Branch**: `079-tour-abre-chat`

**Created**: 2026-08-05

**Status**: Aprovada (defeito relatado pelo editor: "o guia pelo fato do chat não ter aberto aparece perdido na tela")

## Defeito

Dois problemas encadeados, ambos porque o tour assumia que o painel estava aberto:

1. O passo **"Companion"** mirava `.cmp-launcher, .cmp-panel`. Com o chat fechado o alvo era a
   **bolha do canto**, e o texto — *"digite / para ver os comandos; passe o mouse nos chips"* —
   descrevia uma interface que não estava na tela. Daí a sensação de cartão perdido.
2. O passo **"Bastidores"** mirava `.cmp-status`, que **só existe dentro do painel**. Com o chat
   fechado, o filtro de passos o removia: o tour rodava com **4 passos em vez de 5**, perdendo um
   em silêncio — e justamente o que mostra a tese do livro (tokens, chamadas, o que foi injetado).

## Correção

Passos ganham a marca `abrir: true`: ao chegar num deles, o tour **abre o painel** e remede as
posições depois da animação (260 ms). Esses passos deixam de ser filtrados pela ausência do alvo
— o alvo não existe *porque* o painel está fechado, e é esse passo que o abre.

## Aceite

- [x] Percurso completo em navegador: 5 passos (era 4), painel abre no passo 3 e segue aberto no 4
- [x] Cartão ancorado ao lado do painel, com spotlight sobre ele
- [x] Zero erro de JS
- [ ] Build 4 passos verde e CI verde na main

## Observado de passagem (não corrigido aqui)

`oferecerTour()` só é chamado nos handlers do banner de consentimento. Quem já aceitou nunca
recebe o convite do tour — só chega nele digitando `/tour`. É comportamento defensável (não
importunar quem já está lendo), mas é uma decisão implícita, não declarada. Fica registrado para
o editor decidir.

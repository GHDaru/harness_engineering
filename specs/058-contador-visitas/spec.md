# Spec 058: Contador de visitas — o clássico, do jeito honesto

**Feature Branch**: `058-contador-visitas` · **Criada em**: 2026-07-30

## Conceito

O charme do contador de visitas dos anos GeoCities, com a integridade do livro: o número vem da **telemetria consentida e agregada** que já existe (`GET /telemetry/publico`, spec 055) — nada de contador inflado nem pixel de rastreamento. O rótulo diz o que o número é: *visitas registradas* (só quem aceitou a telemetria conta).

## Onde colocar (a decisão "inteligente")

- FR-001: **rodapé de todas as páginas com sidebar** — um chip discreto ao lado do texto existente: `📈 N.NNN visitas registradas · Uso do livro`, com dígitos tabulares, **linkando para o Apêndice — Uso do livro** (o contador vira porta de entrada da página de transparência — cada curioso que clica descobre o modelo de privacidade). A entrada e os capítulos ganham o mesmo rodapé sem tratamento especial.
- FR-002: **sem número na splash** (a capa fica limpa) e **sem "você é a visita #N"** — não seria honesto: visitantes sem consentimento não contam, então não há número ordinal verdadeiro para atribuir a alguém.

## Implementação

- FR-003: extensão do `tema/uso.js` (já carregado em todas as páginas): busca `/telemetry/publico` com **cache em sessionStorage (TTL 10 min)** — uma requisição por sessão de leitura, não por página; formata pt-BR (1.234); injeta o chip no `.rodape`. Backend indisponível ⇒ o chip simplesmente não aparece (rodapé continua íntegro).
- FR-004: e2e: com backend semeado o chip aparece com o total e linka ao apêndice; segunda página usa o cache (sem novo fetch); sem backend, rodapé sem chip e sem erro.

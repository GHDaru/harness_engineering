# Plano — spec 079

| Arquivo | Mudança |
|---|---|
| `publicar/tema/companion.js` | `PASSOS_TOUR`: `abrir: true` nos passos Companion e Bastidores; alvo do Companion vira `.cmp-panel`. `passoTour()`: não filtra passos com `abrir`; se o painel estiver fechado, chama `open()` e reagenda o passo em 260 ms. |

Verificação: Playwright percorrendo o tour a partir do clique real no banner (o caminho do
leitor novo), conferindo número de passos, estado `data-open` e posição do cartão em cada passo.

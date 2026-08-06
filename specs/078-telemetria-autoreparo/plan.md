# Plano — spec 078

| Arquivo | Mudança |
|---|---|
| `publicar/tema/companion.js` | `postConsent()` devolve promessa; `enviarNav(slug, reparando)` trata `{ok:false}` reenviando o consentimento e repetindo uma vez; sai o `sendBeacon` (não devolve resposta) |

Verificação: Playwright com `page.route()` interceptando `/consent` e `/telemetry` e reproduzindo
a regra do servidor (recusa sem linha de consentimento), com `localStorage` pré-carregado no
estado dessincronizado. Confere a sequência de chamadas e a ausência de erro de JS.

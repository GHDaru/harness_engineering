# Feature Specification: a origem do próprio site é sempre autorizada

**Feature Branch**: `092-origem-do-site-sempre-autorizada`

**Created**: 2026-08-07

**Status**: Aprovada — desbloqueio imediato do companion no domínio próprio.

## Defeito

No dia da virada de domínio o site subiu, o texto apareceu, e **o companion morreu em silêncio**.
O preflight de CORS medido de fora:

| Origem | Preflight | `access-control-allow-origin` |
|---|---|---|
| `https://harness.ghdaru.com.br` (novo) | **400** | ausente |
| `https://ghdaru.github.io` (antigo) | 200 | presente |

**E é exatamente a falha que eu declarei ter prevenido.** A spec 089 pôs o domínio próprio no
*default* de `ALLOWED_ORIGINS` "antes de ele existir", e o comentário que escrevi dizia que isso
"custa nada e elimina o passo que seria esquecido no dia da virada".

Errado. **Default só vale quando a variável não existe** — e `ALLOWED_ORIGINS` estava definida no
ambiente desde a feature 017, com a lista velha. A variável antiga venceu o default novo, como
sempre vence. Proteção que uma variável de ambiente anula não é proteção; é a sensação dela.

Foi o **terceiro** caso do mesmo padrão no mesmo dia: `SMTP_*` em outro serviço, `SITE_URL` com
valor velho, `ALLOWED_ORIGINS` com lista velha. Três rodadas perdidas pela mesma cegueira.

## Correção

**A origem do próprio site entra sempre**, derivada de `SITE_URL`.

Não é afrouxar a lista: é **coerência interna**. O backend gera links para aquele endereço — o
link mágico é literalmente `<SITE_URL>entrar.html?t=…` — então recusar chamadas vindas de lá é
contradição. Se `SITE_URL` está certo, a origem está certa; se está errado, o CORS erra junto, o
que é o comportamento desejável.

Efeito prático: **uma lista de origens velha deixa de poder trancar o site canônico para fora**, e
o operador não precisa manter a mesma informação em dois lugares.

## E o CORS deixa de ser invisível

`GET /health` passa a devolver `origens`. Terceira vez hoje que a invisibilidade custa uma rodada
— depois de `smtp_vars` (085), `smtp_porta` (086) e `site` (091). Origem autorizada é informação
de configuração pública, não segredo: quem chama já sabe se foi aceito ou não.

## Aceite

- [x] Lista velha + site novo → origem do site autorizada
- [x] Lista velha + site velho → comportamento inalterado
- [x] Sem `ALLOWED_ORIGINS` → default completo, com a origem do site
- [x] Sem duplicata quando a origem já está na lista
- [x] 45 testes verdes
- [ ] Contra produção: preflight do domínio próprio devolve 200 com o cabeçalho

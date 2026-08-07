# Feature Specification: o endereço do site vira variável

**Feature Branch**: `089-endereco-parametrizado`

**Created**: 2026-08-07

**Status**: Aprovada pelo editor — domínio próprio `harness.ghdaru.com.br`, hospedagem no Vercel,
sem preservar os endereços antigos ("opção 1").

## Problema

O endereço público do site estava **gravado em código**, em três lugares independentes, e um
quarto espalhado pelo conteúdo. Trocar de hospedagem exigia caçar todos e acertar cada um — e o
mais perigoso deles falharia **em silêncio**.

O gatilho é concreto: o editor tem o domínio `ghdaru.com.br` e decidiu publicar o livro em
`harness.ghdaru.com.br`, com o repositório fechando e o endereço `ghdaru.github.io` deixando de
existir. A decisão de **não** preservar os links antigos foi tomada com dado, não por gosto: a
telemetria pública mostrava **47 visitas** e 11 páginas distintas — não há base de leitores a
proteger, e manter dois repositórios pelo resto da vida do projeto custaria mais do que vale.

## Solução

Um endereço, uma variável: **`SITE_URL`**. Quem publica decide onde; o código não sabe e não
precisa saber.

- `publicar/build.mjs` — a constante `SITE` passa a ler `process.env.SITE_URL`, com **barra final
  normalizada** (esquecê-la produziria `https://exemplo.comindex.html`). Alimenta canonical,
  hreflang e og:image: **428 ocorrências** no HTML, todas derivadas daqui.
- `publicar/pdf.mjs` — o rodapé impresso usa o mesmo endereço, sem protocolo.
- `chat-companion/backend/config.py` — `SITE_URL` já era variável (base do link mágico). O que
  muda é o **CORS**: `harness.ghdaru.com.br` entra na lista padrão **antes de o domínio existir**.

Sobre o CORS, vale dizer por quê: é a falha mais traiçoeira desta migração. O site abriria, o
texto apareceria, e **só o companion morreria** — chat, consentimento, telemetria e link mágico,
todos em silêncio, sem erro visível na página. Pré-autorizar custa nada e elimina o passo que
seria esquecido justamente no dia da virada.

## O que a verificação encontrou (e que a parametrização não alcançava)

Construir com `SITE_URL` apontando para o domínio novo revelou **dois links absolutos escritos à
mão dentro do conteúdo** (`livro/HISTORICO.md`), apontando para `ghdaru.github.io`. Nenhuma
variável os alcança: são texto. Viraram links **relativos**, que é o que sempre deveriam ter sido
— link de uma página do site para outra página do mesmo site.

E a correção **introduziu uma regressão**, pega pelo próprio checklist: trocar por `en/` fez o
reescritor de links não reconhecer a página e cair no repositório, subindo os alvos de repo de
**9 para 10**. O alvo certo é `en/index.html`. Voltou a 9.

## Fora de escopo

- Publicação no Vercel (workflow, token, projeto) — depende de o editor criar o projeto.
- Registro no DNS — ação do editor.
- Virar o `SITE_URL` padrão para o domínio novo — só no dia em que o DNS resolver; até lá o
  default segue o endereço atual e **nada muda hoje**.

## Aceite

- [x] `SITE_URL` controla canonical, hreflang, og:image e o rodapé do PDF
- [x] Barra final normalizada (aceita com e sem)
- [x] Build com o domínio novo não deixa **nenhum** resquício do endereço antigo no HTML
- [x] Alvos de repositório em `docs/` permanecem **9** nos dois endereços
- [x] Sem `SITE_URL` definida, o build de hoje é idêntico ao de ontem
- [x] `harness.ghdaru.com.br` pré-autorizado no CORS
- [x] Build 4 passos verde

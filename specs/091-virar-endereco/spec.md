# Feature Specification: virar o endereço para o domínio próprio

**Feature Branch**: `091-virar-endereco`

**Created**: 2026-08-07

**Status**: Aprovada — o editor virou o `SITE_URL` do Railway e pediu a virada do build.

## Contexto

O livro **já responde** em `https://harness.ghdaru.com.br` (certificado válido, todas as
páginas em 200), mas ainda **se identificava** pelo endereço antigo: canonical, hreflang e
og:image apontavam para `ghdaru.github.io`. Funcionar e se identificar são coisas diferentes —
a segunda é o que buscador, rede social e citação acadêmica leem.

## Mudanças

1. **Workflow** — `SITE_URL: https://harness.ghdaru.com.br` no nível do job `build`, alcançando
   o site e os PDFs. É a linha única que a spec 089 preparou: trocar de hospedagem outra vez é
   mudar **esta** linha, nada de código.
2. **`.zenodo.json`** — o `related_identifiers` do tipo `isDocumentedBy` passa a apontar para o
   domínio próprio. É o endereço que sobrevive a qualquer troca de hospedagem e o que se cita.
3. **`/health` declara `site`** — a base do link mágico fica **verificável de fora**. Nasceu de
   uma necessidade concreta: o editor mudou `SITE_URL` no Railway e eu não tinha como conferir
   sem pedir print de tela. Endereço público não é segredo; a mesma lógica das specs 085 e 086.
4. **Barra final normalizada no backend** — assimetria minha, corrigida. O build normalizava
   desde a 089; o backend não. E o link mágico é montado como `<SITE_URL>entrar.html?t=…`, então
   `SITE_URL` sem barra produziria `https://harness.ghdaru.com.brentrar.html` — um link morto no
   e-mail do leitor. O custo do meu descuido cairia inteiro sobre ele.

## Aceite

- [x] Barra final normalizada aceita `…com.br`, `…com.br/` e `…com.br///`
- [x] 45 testes verdes
- [ ] Após o build: canonical e hreflang apontam para o domínio próprio
- [ ] Após o build: nenhuma ocorrência do endereço antigo no HTML
- [ ] `/health` confirma o `site` que o editor pôs no Railway

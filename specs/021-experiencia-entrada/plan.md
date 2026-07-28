# Plan: Experiência de entrada

**Branch**: `021-experiencia-entrada` · **Spec**: [spec.md](./spec.md)

## Constitution Check — PASS
III (método): trilha + progressão tornam o percurso explícito. VI: theme-aware, responsivo, acessível. VII: branch, merge após aprovação. Sem identificador interno de modelo.

## Arquivos
- `publicar/sumario.json` — + `teaser` por item.
- `publicar/build.mjs` — novo corpo do sumário (hero + retomar + trilha + grids + pills); `DOI` const; passa `slug` p/ registrar leitura; sidebar mantida via `pagina()`.
- `publicar/tema/estilo.css` — estilos `.ent-*` (herda `--vars`); alarga `.pagina-index .conteudo/.markdown`; responsivo.
- `publicar/tema/app.js` — grava último capítulo lido (localStorage) e popula o card Retomar no sumário.

## Design
- Cartão = badge(nº) + título + teaser; vira a linguagem das páginas de capítulo (futuro).
- Retomar condicional (localStorage `hz_ultimo`); degrada oculto.
- Aparato como pills compactas para conter o scroll.

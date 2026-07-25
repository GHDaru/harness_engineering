# Plan — Publicação (feature 001)

**Branch**: `001-publicacao-latex-html` · **Spec**: `spec.md` · **Constituição**: respeitada (I, II, III, IV, VI, VII)

## Arquitetura (o "motor do livro")

Motor próprio em **Node** (`publicar/`), sem framework de publicação. Bibliotecas de parsing permitidas (não reinventar o parser). Fonte = Markdown em `livro/`. Saída = `docs/` (servida pelo GitHub Pages).

```
livro/**/*.md  ──►  publicar/build.mjs  ──►  docs/            (site navegável, GitHub Pages)
(fonte única)       (motor: markdown-it       ├── index.html   (capa + sumário)
                     + tema + navegação)       ├── <slug>.html  (um por capítulo)
                                               └── assets/estilo.css
                            │
                            └──►  (P3) mesmo conteúdo ──► PDF via LaTeX
```

- **Manifesto**: `publicar/sumario.json` — ordem canônica (partes, capítulos, apêndices), com título e caminho de cada arquivo. Fonte única da ordem de leitura.
- **Motor** (`publicar/build.mjs`): lê o manifesto, converte cada `.md` (markdown-it + anchor para âncoras de seção), extrai o cabeçalho de data de captura, envolve num **template** com barra lateral (sumário), navegação anterior/próximo e rodapé; estiliza os blocos pedagógicos (objetivos, verificação, mão na massa, apêndice) por convenção de marcação; reescreve links internos `.md → .html`.
- **Tema** (`publicar/tema/estilo.css`): tipografia legível, tema claro/escuro, código com realce, sumário fixo, responsivo. Os "boxes" do Diátaxis com estilos distintos (callouts).
- **Islands React** (P2): pontos de montagem (`<div data-viz="benchmark">`) que o build deixa preparados; os componentes React são construídos à parte e hidratam essas ilhas. MVP (P1) não depende deles.

## Fatiamento MVP-first (user stories → fases)

- **P1 — site navegável (US1)**: manifesto + motor + tema + geração de `docs/` a partir do Markdown atual, com sumário, navegação capítulo-a-capítulo, código realçado, callouts pedagógicos e data de captura visível. *Entregável testável agora.*
- **P2 — visualizações React (US1 cont.)**: componentes para o comparativo do benchmark, o registro de expiração e o radar de notas, montados como islands.
- **P3 — PDF via LaTeX (US2)**: geração do PDF do mesmo Markdown (via pandoc+LaTeX quando a infra tiver texlive; passo isolado atrás do comando de build).
- **P4 — CI + apêndice de infra (US3)**: GitHub Actions publica `docs/` a cada push no main; apêndice do livro (`livro/apendices/infra.md`) descreve o pipeline; portão de qualidade (link interno quebrado / capítulo que não compila falha o build).

## Decisões técnicas
- **Node** (não Python) para o motor: alinha com React (P2) e com o ecossistema de ferramentas de site. O harness-zero segue Python (são projetos distintos, decisão local).
- **Saída em `docs/`** no repositório: GitHub Pages serve de `main/docs` — sem servidor, sem branch extra. (Enquanto na branch 001, geramos e verificamos local; publica ao mergear.)
- **Sem conteúdo duplicado**: `docs/` é *gerado* (entra no `.gitignore`? Não — o GitHub Pages simples serve arquivos versionados; então `docs/` é commitado, mas nunca editado à mão. Alternativa CI-only decidida na P4). Para o MVP, commitar `docs/` gerado é aceitável e simples.

## Verificação (portões)
- `npm run build` roda sem erro e gera 1 `index.html` + N páginas de capítulo.
- Navegação: index → capítulo → próximo/anterior funcionam; links internos resolvidos.
- Data de captura visível nos capítulos v3.
- (P4) link interno quebrado falha o build.

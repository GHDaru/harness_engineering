# Spec 045: Download do livro — PDF e Markdown, completo e por capítulo

## Requisitos

- FR-001 (livro completo): a **entrada** (sumário) oferece download do livro em **PDF** (`pdf/engenharia-de-harness.pdf`) e **Markdown** (`md/engenharia-de-harness.md`, concatenação na ordem do sumário com cabeçalho de versão/DOI).
- FR-002 (por capítulo): cada página de capítulo oferece, no cabeçalho C01 (cap-meta), download do **.md fonte** (`md/<slug>.md`) e do **PDF do capítulo** (`pdf/<slug>.pdf`).
- FR-003 (motor): `build.mjs` copia os fontes `.md` publicados para `docs/md/` e gera o consolidado; `pdf.mjs` gera o PDF completo **e** um PDF por capítulo numerado em `docs/pdf/`.
- FR-004 (correção 043→PDF): o extrator do PDF perde o título dos capítulos (o `h1` saiu do `<article>` na spec 043) — o PDF volta a ter título por capítulo (e o do capítulo avulso ganha capa leve com versão/DOI).
- FR-005 (CI): o workflow instala Chromium e gera os PDFs **após** o build, antes do deploy do Pages; `playwright` vira devDependency do motor.
- FR-006 (verificação): o portão por capítulo confere links de download e a existência dos `.md` em `docs/md/`; PDFs são conferidos quando `docs/pdf/` existe (gerados depois do portão no CI).

## Decisões

- `.md` baixa com atributo `download`; PDF abre no viewer do navegador (sem `download`).
- Aparato entra no consolidado (livro completo), mas só capítulos numerados ganham PDF avulso.
- Sem PDFs commitados no repositório: tudo gerado no CI (docs/ segue fora do versionamento).

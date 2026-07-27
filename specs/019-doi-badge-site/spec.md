# Feature Specification: DOI no site e no README (badge + "Como citar")

**Feature Branch**: `019-doi-badge-site`

**Created**: 2026-07-27

**Status**: Draft

**Input**: O DOI foi emitido pelo Zenodo — **`10.5281/zenodo.21632412`** (`https://doi.org/10.5281/zenodo.21632412`). Fixar: badge do DOI no README, selo/link do DOI na **tela-capa** e uma seção **"Como citar"** no site (página do autor / back matter). Completa a feature 018.

## Requirements *(mandatory)*

- **FR-001**: O README DEVE exibir o **badge do DOI** (imagem do Zenodo linkando para `https://doi.org/10.5281/zenodo.21632412`), substituindo o marcador deixado na 018.
- **FR-002**: A **tela-capa (splash)** DEVE exibir o DOI como **link discreto** (ex.: junto ao selo de versão), apontando para `https://doi.org/10.5281/zenodo.21632412`.
- **FR-003**: A página **"Sobre o autor"** (back matter) DEVE ganhar uma seção **"Como citar"** com a referência formatada e o DOI.
- **FR-004**: O portão de link-check do build DEVE continuar verde; sem identificador interno de modelo.

## Success Criteria *(mandatory)*

- **SC-001**: README mostra o badge do DOI clicável.
- **SC-002**: A capa mostra o DOI (link) perto do selo de versão, sem estourar no mobile.
- **SC-003**: "Sobre o autor" tem "Como citar" com a referência + DOI.
- **SC-004**: Build verde; zero identificador interno de modelo.

## Assumptions

- DOI fornecido pelo autor: `10.5281/zenodo.21632412`. Se for o DOI de versão e não o concept, ambos resolvem; o concept aponta sempre à última versão (ajustável depois).
- Feature toca `publicar/` + `livro/` → ciclo spec-kit (Princípio VII); merge dispara deploy.

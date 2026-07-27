# Feature Specification: DOI e citação (Zenodo/DataCite)

**Feature Branch**: `018-doi-citacao-zenodo`

**Created**: 2026-07-27

**Status**: Draft

**Input**: O autor quer **registrar a obra com DOI**. Caminho: **Zenodo** (DataCite), via integração com o GitHub — cada _release_ vira um DOI, com um **concept DOI** (obra viva) e **DOIs de versão** (cada edição). Esta feature prepara o repositório: **licença**, metadados de citação (`CITATION.cff`, `.zenodo.json`), seção "Como citar" e espaço para o **badge do DOI**. A emissão do DOI é feita pelo autor no Zenodo (fluxo tutorado); o número volta depois e é fixado.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A obra fica citável e pronta para o DOI (Priority: P1)

Qualquer pessoa (ou o próprio Zenodo) encontra no repositório os **metadados de citação** corretos — autor com ORCID, título, versão, licença — e um botão "**Cite this repository**" no GitHub. Ao ligar o Zenodo e publicar um release, o **DOI é emitido** com os metadados certos.

**Independent Test**: `CITATION.cff` válido (GitHub mostra "Cite this repository"); `.zenodo.json` com autor+ORCID+licença; `LICENSE` presente; README com "Como citar".

**Acceptance Scenarios**:

1. **Given** o repositório, **When** abro a página no GitHub, **Then** vejo o botão "Cite this repository" (lido do `CITATION.cff`).
2. **Given** o Zenodo ligado ao repo, **When** publico um release, **Then** o depósito herda os metadados do `.zenodo.json` (autor Gilsiley + ORCID, título, licença, tipo = livro) e emite o DOI.
3. **Given** o DOI emitido, **When** atualizo o repo, **Then** o **badge do DOI** e a seção "Como citar" exibem o concept DOI.

### Edge Cases

- O DOI ainda não existe no primeiro setup: os arquivos ficam prontos com um marcador; o número é fixado depois (follow-up).
- Autoria de IA: **não** entra como creator (política ICMJE/COPE); fica **declarada na descrição** (consistente com o Guia §6 e a nota de co-autoria).
- Licença mista (texto + código): declarada de forma inequívoca (qual cobre o quê).

## Requirements *(mandatory)*

- **FR-001**: DEVE haver **licença(s)** no repositório: **CC BY 4.0** para o conteúdo (`LICENSE`) e **MIT** para o código (`LICENSE-CODE`), com nota no README dizendo o que cada uma cobre. (decisão do autor: recomendação CC BY 4.0 + MIT)
- **FR-002**: DEVE haver `CITATION.cff` válido: autor **Gilsiley Henrique Darú** (ORCID `0000-0002-8979-0461`), título, versão, data, URL/repo, licença, resumo, keywords.
- **FR-003**: DEVE haver `.zenodo.json` com metadados do depósito: creators (nome + ORCID), `upload_type=publication`, `publication_type=book`, `access_right=open`, `license=cc-by-4.0`, keywords, idioma `por`, `related_identifiers` apontando para o site.
- **FR-004**: A **co-autoria de IA** DEVE ser declarada na **descrição** dos metadados (não como creator), consistente com o Guia §6 e a nota de co-autoria.
- **FR-005**: O README DEVE ter seção **"Como citar"** e **"Licença"**, com espaço para o **badge do DOI** (fixado quando o DOI existir).
- **FR-006**: Sem segredo; sem identificador interno de modelo em qualquer artefato.

### Key Entities

- **CITATION.cff / .zenodo.json**: metadados de citação e de depósito.
- **LICENSE / LICENSE-CODE**: grants de conteúdo e de código.
- **Concept DOI / DOI de versão**: emitidos pelo Zenodo (fora do repo), fixados depois.

## Success Criteria *(mandatory)*

- **SC-001**: GitHub exibe "Cite this repository" a partir do `CITATION.cff`.
- **SC-002**: `.zenodo.json` tem autor+ORCID, licença e tipo corretos; a co-autoria de IA está na descrição.
- **SC-003**: `LICENSE` (CC BY 4.0) e `LICENSE-CODE` (MIT) presentes; README diz o que cada uma cobre.
- **SC-004**: README tem "Como citar" com espaço para o badge; zero segredo; zero identificador interno de modelo.

## Assumptions

- Zenodo (DataCite) é a agência; a emissão do DOI é ação do autor (tutorada), fora do repo.
- Licença: CC BY 4.0 (conteúdo) + MIT (código) — recomendação, ajustável antes de emitir o DOI.
- O badge/número do DOI é fixado num follow-up curto quando o DOI existir (inclui pôr o selo na capa/colofão do site).

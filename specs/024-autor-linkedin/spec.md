# Feature Specification: Foto + LinkedIn do autor (E06) e LinkedIn na capa (E07)

**Feature Branch**: `024-autor-linkedin` · **Created**: 2026-07-27

## Requisitos
- **FR-001 (E06)**: A página "Sobre o autor" DEVE exibir a **foto** do autor (`publicar/tema/autor.png` → `assets/autor.png`) e destacar o **LinkedIn**.
- **FR-002 (E07)**: A **tela-capa (splash)** DEVE incluir um link para o **LinkedIn** do autor nos créditos (repo é público).
- **FR-003**: Responsivo, theme-aware, `alt` na foto; build verde; sem identificador interno de modelo.

## Sucesso
- SC-001: `autor.html` mostra a foto + LinkedIn; SC-002: capa tem link do LinkedIn; SC-003: build verde.

LinkedIn: https://www.linkedin.com/in/gilsiley-dar%C3%BA/

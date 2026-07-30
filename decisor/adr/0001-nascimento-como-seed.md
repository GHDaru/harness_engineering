# ADR 0001 — Nascimento como seed autocontido, extração futura para repositório próprio

- **Status**: Aceito
- **Data**: 2026-07-30
- **Relacionado**: constituição v1.0.0; spec 001

## Contexto

O projeto Decisor (livro vivo + app MCDA) nasceu em uma sessão com acesso a dois
repositórios: `ghdaru/harness_engineering` (o modelo do livro vivo) e `ghdaru/maestro`
(a metodologia). Não existia repositório próprio, e criar um não estava no escopo
autorizado da sessão. O projeto, porém, precisa de raiz própria: CLAUDE.md/AGENTS.md,
constituição, specs e publicação no GitHub Pages independentes.

## Decisão

1. Nascer como **diretório autocontido `decisor/`** na branch
   `claude/multicriteria-decision-app-al35pb` do `harness_engineering` — o repositório
   cuja infraestrutura editorial o projeto herda.
2. Tudo dentro de `decisor/` é **relativo à sua própria raiz** (nenhuma referência a
   arquivos do harness_engineering), para que a extração seja um `git mv`/subtree limpo.
3. A extração para `ghdaru/decisor-multicriterio` (nome sugerido) deve acontecer **antes**
   de ativar o GitHub Pages do livro; os workflows em `decisor/.github/workflows/` já
   estão prontos e só passam a valer na raiz do novo repositório.

## Alternativas avaliadas

- **Criar repositório novo já** — rejeitado: ação externa fora do escopo autorizado da
  sessão (gate humano do Princípio VII / Maestro §8).
- **Misturar o conteúdo às pastas existentes do harness_engineering** — rejeitado:
  violaria a constituição daquele repositório (que governa o livro de harness) e
  tornaria a extração cirúrgica.
- **Nascer no repositório maestro** — rejeitado: lá vive a metodologia, não produtos;
  o CLAUDE.md do maestro restringe o repositório ao desenvolvimento da metodologia.

## Consequências

- O merge desta branch **não** deve ir ao `main` do harness_engineering sem decisão
  explícita do Steward; o caminho natural é extrair primeiro.
- Enquanto a extração não ocorre, os workflows de `decisor/.github/workflows/` são
  inertes (GitHub só executa workflows de `.github/` na raiz) — comportamento desejado.

## Fontes

- Constituição do harness_engineering (Princípio VII) e CLAUDE.md do maestro (regra de
  escopo de repositório) — ambos em seus repositórios de origem.

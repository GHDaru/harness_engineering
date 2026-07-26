# Quickstart — validação da feature

> Como provar, de ponta a ponta, que o estudo atende à spec. Não contém o conteúdo (isso é a implementação); é o roteiro de verificação.

## Pré-requisitos
- Node instalado (motor do livro em `publicar/`).
- Branch `010-estudo-metodologias-escrita`.

## Passos de validação

1. **Build + gate de link-check** (FR-008 / SC-005)
   ```sh
   cd publicar && node build.mjs
   ```
   Esperado: `✓ Livro gerado … (links internos OK)`, sem erro de link quebrado. O `guia-editorial.html` gerado contém a nova seção.

2. **Abrangência de survey** (FR-010 / SC-003)
   - Conferir que a Parte A lista **≥5** metodologias tradicionais e a Parte B **≥4** da era-IA, cada uma com fonte e uma frase de "o que estabelece".

3. **Fontes reais** (FR-005 / SC-002)
   - Amostrar as citações: cada uma tem DOI/ISBN/URL ou está marcada `⏳` (não-verificada). Zero referências inventadas. As novas fontes estão em `livro/bibliografia.md`.

4. **Método do livro nomeável** (US1 / SC-001)
   - Um leitor consegue, lendo a Parte D, nomear ≥4 práticas do livro e o porquê de cada uma.

5. **Divulgação de co-autoria** (FR-009 / SC-006)
   - A Parte D declara explicitamente a co-autoria humano+IA (Claude Code) sob curadoria/responsabilidade humanas.

6. **Postura equilibrada** (FR-004)
   - A Parte C trata riscos/limitações da IA (alucinação de fontes, integridade, reprodutibilidade), não só ganhos.

7. **Livro vivo** (Princípio IV)
   - A seção tem data de atualização; `HISTORICO.md` ganhou entrada de edição.

## Definition of Done
Todos os passos acima verdes + `tasks.md` com todas as tarefas concluídas + merge da branch `010` para `main` com deploy verde.

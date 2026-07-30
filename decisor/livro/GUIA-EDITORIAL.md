# Guia editorial — como escrever este livro

> Operacionaliza o Princípio III da constituição (`.specify/memory/constitution.md`).
> Linhagem: `livro/GUIA-EDITORIAL.md` do Engenharia de Harness (esqueleto v3).

## 1. O framework pedagógico

| Framework | O que dita aqui |
|---|---|
| **Backward Design** | Primeiro os objetivos (verbos de Bloom), depois as evidências (a seção Verificação + os testes da etapa), só então o conteúdo. |
| **4C/ID** | Etapas do `decisor-zero` = learning tasks (tarefa completa e realista); capítulos = supportive information; docstrings no código = just-in-time information; exercícios de completar = part-task practice. |
| **Diátaxis** | Tutorial (Mão na massa), explicação (O problema / Estado da arte), referência (fórmulas + Apêndice A), how-to (Quando usar) — nunca misturados na mesma seção. |
| **Carga Cognitiva** | Worked example antes de exercício; o caso âncora elimina o custo de entender um problema novo a cada método; uma ideia nova por vez; notação introduzida uma única vez (cap. 01) e reutilizada. |

## 2. O caso âncora (obrigatório)

Um único problema atravessa o livro: **a escolha de um apartamento** — 4 alternativas,
critérios de preço (R$), área (m²), tempo de deslocamento (min) e qualidade do bairro
(escala 1–5). Todo método novo é aplicado **primeiro** ao caso âncora, com o exemplo
resolvido passo a passo; os números vivem em `decisor-zero/etapas/*/tests/` como fixtures
(Princípio I: o worked example é teste). Só depois o capítulo pode trazer um segundo
domínio (fornecedores, tecnologia, políticas públicas) como exercício.

## 3. Esqueleto v3 de capítulo (obrigatório)

Cabeçalho literal:

```markdown
# NN — Título

> **Estado da arte capturado em AAAA-MM** · última revisão AAAA-MM-DD · [histórico](../HISTORICO.md)
```

Seções, na ordem:

1. `## Objetivos de aprendizagem` — 3–5, cada um abrindo com verbo de Bloom em negrito
   (**Explicar**, **Calcular**, **Implementar**, **Comparar**, **Avaliar**).
2. `## O problema` — a dor de decisão que motiva o capítulo, sempre encostada no caso âncora.
3. `## Fundamentos` — a fonte seminal do método *traduzida para decisões* ("Saaty propõe X,
   o que significa que você deve Y"); fórmulas em LaTeX; ponteiro para `bibliografia.md`.
4. `## O método passo a passo` — worked example completo no caso âncora, tabela por tabela,
   até o resultado final (que o teste da etapa reproduz).
5. `## Quando usar (e quando não)` — premissas, limitações e críticas com fonte
   (Princípio VI); fecha com `### Leitura executiva` terminando em "**O que levar** hoje: …".
6. `## Mão na massa — decisor-zero, etapa NN` — aponta a pasta, diz o que nasce no código
   e propõe o exercício de completar (part-task practice).
7. `## Verificação` — 2–3 perguntas mapeadas nos objetivos do item 1, com dica entre parênteses.
8. `---` + `## Apêndice A — [tema] nas ferramentas e na literatura aplicada` — como
   softwares/bibliotecas reais (pymcdm, scikit-criteria, planilhas…) e estudos de caso
   tratam o tema, com URLs; expandido a cada rodada, sem inchar o corpo.

Capítulos conceituais (00, panoramas) podem omitir 4 e 6, mantendo o resto.

## 4. Regras de escrita permanentes

- Notação única do livro (definida no cap. 01): $m$ alternativas $a_1..a_m$, $n$ critérios
  $c_1..c_n$, matriz de decisão $X = [x_{ij}]$, pesos $w_j$ com $\sum w_j = 1$.
- Sigla expandida na primeira ocorrência de cada capítulo; termos consagrados
  (trade-off, outranking, rank reversal) sem tradução forçada.
- Afirmação sensível ao tempo (versões de bibliotecas, links) vive sob a data de captura;
  matemática dos métodos é do tipo "não-expira".
- Toda edição atualiza `HISTORICO.md`: changelog + tabela de snapshot + linha
  `**IA**: agente <nome> (<fornecedor>); curadoria humana.`

## 5. Fluxo repetível para escrever um capítulo

1. Abrir a rodada (spec em `specs/NNN-*`), com o capítulo e a etapa no escopo.
2. Reunir a fonte seminal + 1–2 secundárias; validar e registrar em `bibliografia.md` (✓).
3. Implementar a etapa no `decisor-zero` com o worked example como teste — **antes** de
   fechar a prosa (se o exemplo não fecha no código, a prosa está errada).
4. Escrever no esqueleto v3; revisão developmental (estrutura) antes de copyedit.
5. Portões: `pytest` verde na etapa; `mkdocs build --strict` verde; datação no cabeçalho.
6. Registrar em `HISTORICO.md` e no `CHANGELOG.md`; merge após gate humano.

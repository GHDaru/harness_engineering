# Guia Editorial — regras operacionais do livro

> Versão operacional das orientações pedagógicas. O parecer completo (com fundamentação) está em [`estudos/2026-07-25-parecer-editorial-plano-pedagogico.md`](../estudos/2026-07-25-parecer-editorial-plano-pedagogico.md). Este guia é o que se consulta **enquanto escreve**.

## 1. O framework pedagógico em quatro linhas

| Framework | O que dita no livro |
|---|---|
| **Backward Design** | Todo capítulo se projeta de trás para frente: objetivos → evidências (verificação/prática) → só então o conteúdo |
| **4C/ID** | Etapas do harness-zero = tarefas inteiras; capítulos = informação de apoio; boxes no código = just-in-time; katas = treino de parte |
| **Diátaxis** | Quatro tipos de texto, nunca misturados na mesma seção: capítulo=explanation, harness-zero=tutorial, templates/benchmark=reference, "o que roubar"=how-to |
| **Carga Cognitiva** | Worked examples antes de exercício; exercícios são "complete", não "crie do zero"; andaime diminui etapa a etapa; uma ideia nova por vez |

## 2. Esqueleto v2 de capítulo (obrigatório; piloto: cap. 04)

1. **Objetivos** — 3–5, verbos de Bloom (explicar, comparar, implementar, avaliar)
2. **O problema** — por que a dimensão existe
3. **Fundamentos científicos** — 2–4 papers *traduzidos para decisões* ("o paper mostrou X → por isso o padrão é Y"); ponteiro para `bibliografia.md`
4. **Padrões de implementação** — o cardápio da indústria
5. **Evidência do benchmark** — como os harnesses avaliados implementam, com paths
6. **Mão na massa** — a etapa correspondente do harness-zero
7. **Síntese + "o que roubar"** — tabela comparativa e ideias exportáveis
8. **Verificação** — 2–3 perguntas que testam exatamente os objetivos do item 1

## 3. Regras de escrita permanentes

- **Evidência por caminho de arquivo** para qualquer afirmação sobre um harness; **status ✓** para qualquer citação científica (skill `academic-research` tem o fluxo).
- Notas 0–3 só comparam dentro da mesma categoria do benchmark.
- Cada componente descrito deve, quando possível, declarar sua **cláusula de expiração**.
- Prosa em português; termos técnicos consagrados (harness, loop, tool, prompt) **sem tradução**.
- Tabelas para fatos enumeráveis; explicação vive na prosa, não nas células.

## 4. Regras do harness-zero (as 4 condições do parecer)

1. **DDD leve** — linguagem ubíqua = glossário do livro; padrão tático só onde paga; DDD aparece como consequência nomeada no código.
2. **Arquitetura por refatoração** — cada porta nasce da dor do capítulo correspondente; nunca estrutura antecipada.
3. **Anti-apodrecimento** — modelo atrás de `LLMPort`; etapas autocontidas e executáveis; erros didáticos deliberados são **comentados como tal** no código.
4. **Chat congelado** — HTML+JS servido pelo backend; só evolui quando uma dimensão exigir superfície nova.

## 5. Ferramentas do repositório

- **spec-kit** (`.specify/` + comandos `/speckit-*`): para features novas do harness-zero ou seções grandes do livro, o fluxo é `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement` (com `/speckit-clarify` antes do plano quando o pedido for ambíguo). A constitution do projeto vive em `.specify/memory/`.
- **Skill `academic-research`** (`.claude/skills/`): fluxo de localizar → validar → registrar → integrar referências científicas.
- **`scripts/sync-forks.ps1`**: sincronização local dos forks com upstreams.

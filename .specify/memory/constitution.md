# Constituição — Livro de Engenharia de Harness

> A lei do projeto. Todo trabalho (edição de capítulo, avaliação de benchmark, código do harness-zero, pesquisa) segue estes princípios. Em conflito entre pedido pontual e constituição, a constituição prevalece — ou o conflito é explicitado antes de agir. Documentos operacionais: `livro/GUIA-EDITORIAL.md` (como escrever), `benchmark/README.md` (como avaliar).

## Princípios centrais

### I. Evidência acima de retórica (NÃO-NEGOCIÁVEL)
Toda afirmação sobre um harness exige **evidência**: o caminho do arquivo no código-fonte. Toda citação científica exige **status validado** (✓) no `livro/bibliografia.md`. Toda fonte da indústria é uma URL verificável. READMEs prometem; código e fontes primárias entregam. Sem evidência, não entra no corpo do livro.

### II. A fonte-base é o código
O livro nasce da leitura do código-fonte dos harnesses reais. Material científico e comercial **contextualizam e modernizam**, mas não substituem a inspeção do código. O tratamento por repositório (com paths) é a espinha empírica; vai para o **Apêndice A** de cada capítulo (complementação online). O corpo do capítulo recebe o **estado da arte** — o mais moderno, sintetizado.

### III. Método pedagógico combinado (o framework do livro)
Todo capítulo e toda etapa da construção seguem a combinação:
- **Backward Design** (Wiggins): escrever de trás para frente — objetivos (verbos de Bloom) → evidências/verificação → conteúdo.
- **4C/ID** (van Merriënboer): a trilha prática (`harness-zero`) é a espinha — etapas = *learning tasks* (tarefas inteiras); capítulos = *supportive information*; boxes no código = *just-in-time*; katas = *part-task practice*.
- **Diátaxis**: quatro tipos de texto, **nunca misturados** na mesma seção — capítulos = *explanation*, construção = *tutorial*, templates/benchmark = *reference*, "o que roubar" = *how-to*.
- **Carga Cognitiva** (Sweller): *worked examples* antes de exercício; *completion problems* ("complete", não "crie do zero"); *fading* do andaime etapa a etapa; uma ideia nova por vez.
O esqueleto v3 de capítulo (8 seções + Apêndice A) é a materialização deste princípio e é obrigatório.

### IV. Livro vivo (datação e expiração)
Coerência com a tese central (cláusula de expiração): o que se descreve é temporário. Todo capítulo v3 declara **data de captura** no cabeçalho; distinguem-se três datas (evento / captura / rodada do benchmark); toda edição atualiza `livro/HISTORICO.md`, incluindo o **registro de expiração** (o placar das previsões). Reavaliar = nova rodada, nunca sobrescrever silenciosamente. Toda edição registra também a **versão do modelo de IA** usada (e a sessão), porque saídas de LLM são não-determinísticas e a rastreabilidade é parte do rigor (Guia §6.C).

### V. Segurança e credenciais
Nenhum segredo (chave de API, token) entra em arquivo, commit ou texto publicado — nunca. Credenciais vivem só em ambiente / `.env` gitignored. Chave exposta é chave comprometida: alertar e orientar revogação. O código didático demonstra a prática correta (a regra do cap. 07 aplicada ao próprio projeto).

### VI. Neutralidade e acessibilidade
A análise é vendor-agnóstica: notas 0–3 comparam apenas dentro da mesma categoria do benchmark; nenhum harness é favorecido por marca. O livro é acessível — a trilha prática roda a custo zero (endpoint gratuito documentado, com créditos ao provedor). Prosa em português; termos técnicos consagrados (harness, loop, tool, prompt) sem tradução.

### VII. Spec-driven e branch-per-melhoria (NÃO-NEGOCIÁVEL)
**Toda melhoria — inclusive as pedagógicas e editoriais — passa pelo spec-kit: `spec` → `plan` → `tasks` → `implement`, cada uma em sua própria branch.** Não há "só editar direto no main": um capítulo novo, um refinamento de método, uma etapa do harness-zero, uma feature de infraestrutura — todos nascem de um spec (`specs/NNN-nome/spec.md`), ganham um plano e uma lista de tarefas, e só então são implementados, na branch `NNN-nome`. O merge para `main` acontece quando a melhoria está coerente e verificada. Isso torna a evolução do livro rastreável e profissional — o próprio processo do livro é um exemplo de harness bem-instrumentado.
- **Exceção única**: emendas a *esta constituição* (governança) podem ser feitas diretamente, pois são o meta-nível que habilita a própria regra — mas são registradas aqui e no `HISTORICO.md`.
- Correções triviais (typo, link quebrado, ajuste de uma linha) podem ir direto ao main com commit descritivo; a regra vale para *melhorias*, não para consertos pontuais.

## Restrições da construção (harness-zero)
1. **DDD leve** — linguagem ubíqua = glossário do livro; padrão tático só onde paga; DDD como consequência nomeada no código, não teoria.
2. **Arquitetura hexagonal por refatoração** — cada porta nasce da dor do capítulo correspondente; nunca estrutura antecipada.
3. **Anti-apodrecimento** — modelo atrás de `LLMPort`; etapas autocontidas e executáveis; erros didáticos deliberados são comentados como tais.
4. **Chat congelado** — HTML+JS servido pelo backend; só evolui quando uma dimensão exigir superfície nova. Stack: Python + FastAPI.

## Fluxo de trabalho e portões de qualidade
- Toda melhoria usa o spec-kit (princípio VII): `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement` (com `/speckit-clarify` quando ambíguo), em branch `NNN-nome`. Os planos devem respeitar esta constituição.
- Pesquisa científica segue a skill `academic-research` (localizar → validar → registrar → integrar).
- **Revisão em duas camadas** (Guia §6.A, tradição Sommers/Flower-Hayes): antes do copyedit de superfície, um passo de **revisão *developmental*** — re-ver estrutura e sentido do texto (o argumento fecha? a ordem serve ao leitor? há redundância/lacuna?). "Escrever é reescrever": nenhum trecho novo é publicado sem esse passo.
- Antes de publicar (commit/push): evidência presente (I), fonte-base respeitada (II), esqueleto/método aplicado (III), **revisão developmental feita** e datação/histórico atualizados — **com a versão do modelo registrada** — quando o estado da arte mudou (IV), sem segredos (V).
- Commits descrevem o "porquê"; o repositório é o registro. Push só quando o trabalho está coerente.

## Governança
Esta constituição prevalece sobre preferências pontuais. Emendas são registradas aqui e no `livro/HISTORICO.md`. O `CLAUDE.md` da raiz aponta para este documento como fonte de autoridade.

**Versão**: 1.2.0 | **Ratificada**: 2026-07-25 | **Última emenda**: 2026-07-26 (add. revisão developmental como portão de qualidade (A2); registro da versão do modelo na datação (A3) — achados do Guia §6, parecer `estudos/2026-07-26-achados-metodologia-escrita.md`)

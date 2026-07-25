---
name: academic-research
description: Pesquisa acadêmica para o livro de Engenharia de Harness — localizar, validar e citar papers científicos (arXiv, surveys, benchmarks) seguindo as regras editoriais do projeto. Use quando o usuário pedir para "buscar papers", "validar referências", "atualizar a bibliografia", "fundamentar um capítulo cientificamente", "pesquisa acadêmica", "literature review", ou quando um capítulo novo/retrofitado precisar da seção "Fundamentos científicos".
---

# Pesquisa acadêmica do livro de Engenharia de Harness

## Contexto do projeto

- A bibliografia oficial vive em `livro/bibliografia.md`, organizada por capítulo, com status por entrada.
- Todo capítulo no esqueleto v2 tem a seção **"Fundamentos científicos"**: 2–4 papers que sustentam decisões do capítulo, cada um com uma frase dizendo **o que ele estabelece** (nunca só o título).
- Regra de ouro do livro (vale para código e para papers): **afirmação exige evidência**. Nenhuma referência entra no corpo de um capítulo sem status ✓.

## Fluxo de trabalho

### 1. Localizar
- Priorize **surveys recentes** (2024+) como âncora do capítulo e 1–2 papers seminais como fundação histórica.
- Use WebSearch com consultas do tipo: `survey <dimensão> LLM agents arXiv <ano>` e variações do vocabulário da dimensão (ex.: para compactação: "context management", "memory hierarchy", "summarization long-horizon").
- Registre também as **lacunas**: dimensões sem literatura dedicada (hoje: extensibilidade, interfaces, embutidos, protocolos) são achado editorial, não fracasso de busca.

### 2. Validar (obrigatório antes de citar)
Estados possíveis de uma referência:
- **✓ validada** — ID↔título confirmado por fonte independente (resultado de busca que retorna o ID *junto* do título esperado; página do arXiv; Semantic Scholar).
- **⏳ pendente** — citada de memória ou de fonte única. Pode ficar em `bibliografia.md` com o marcador, mas **não pode ser citada no corpo de capítulo**.

Restrição conhecida deste ambiente: **arxiv.org e api.semanticscholar.org retornam 403 pelo proxy** (curl e WebFetch). Fallbacks, em ordem:
1. WebSearch com o ID entre aspas + palavras do título (`"2310.08560" MemGPT arxiv`) — se o resultado traz o ID com o título esperado, está validada;
2. Vários IDs por busca funcionam (`"ID1" palavra1 "ID2" palavra2 ...`), até ~4 por consulta;
3. Se nada confirmar, manter ⏳ e listar na resposta final para o usuário validar localmente (leva segundos fora do proxy).

### 3. Registrar
- Atualizar `livro/bibliografia.md`: seção do capítulo, formato `- [status] **Título** (autores se relevante) — arXiv [ID](https://arxiv.org/abs/ID). Frase sobre o que estabelece.`
- Marcar ⭐ na âncora do capítulo (no máximo 1–2 por capítulo).
- Se o paper alimenta mais de um capítulo, citar uma vez com nota cruzada ("também alimenta o cap. X").

### 4. Integrar ao capítulo
- A seção "Fundamentos científicos" **traduz** o paper para a decisão de engenharia: "Lost in the Middle mostrou X → por isso a escada preserva o tail". Nunca resumo solto do abstract.
- Terminar a seção com o ponteiro: `(Bibliografia completa e status de validação: livro/bibliografia.md.)`

## Anti-padrões (não fazer)
- Citar paper só por prestígio, sem conexão com uma decisão do capítulo.
- Confiar em ID de arXiv "de memória" sem validar — IDs errados são o erro mais comum e o mais corrosivo para a credibilidade do livro.
- Encher um capítulo com >4 referências: o livro é de engenharia; a ciência sustenta, não domina.
- Apagar uma referência que falhou na validação: rebaixe para ⏳ com nota do que falhou.

## Papers-âncora já validados (não rebuscar)
Ver `livro/bibliografia.md`. Destaques transversais: *From QA to Task Completion: Survey on Agent System and Harness Design* (2606.20683), *Recursive Agent Harnesses* (2606.13643), ReAct (2210.03629), MemGPT (2310.08560), SWE-bench (2310.06770), Lost in the Middle (2307.03172), Greshake prompt injection (2302.12173), Voyager (2305.16291).

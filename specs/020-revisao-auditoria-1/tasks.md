# Tasks: Rodada de auditoria e revisão 1

**Feature**: `020-revisao-auditoria-1` · **Plan**: [plan.md](./plan.md)

> **Lista rolante.** Cada observação do autor entra como uma task `O###`
> (Onde · O quê · Correção aplicada · Evidência, quando factual). A rodada
> fecha com o registro no HISTORICO + build verde + merge único na `main`.

## Observações → correções

<!-- modelo:
- [ ] **O001** `livro/capitulos/NN-arquivo.md` · seção "…" — <observação do autor> →
      correção: <o que foi trocado>. Evidência: <path/URL, se factual>.
-->

### Correções de conteúdo (auditoria)

- [ ] **O001** **Fundamentação total (estilo artigo científico).** Toda menção a um paper/fonte no texto deve **linkar para a Bibliografia**, e na Bibliografia o link para a **fonte** (DOI/URL). Vale também para **referências comerciais** (é livro, pode). *(parte vira tooling — ver E01.)*
- [ ] **O002** **"scaffolding" em português.** Traduzir/introduzir o termo — *andaime (scaffolding)* / arcabouço / estrutura de suporte — na 1ª aparição (já aparece no subtítulo) e no Glossário.
- [ ] **O003** **Siglas por extenso inline na 1ª ocorrência** de cada capítulo (a passada pesada; o auto-`<abbr>` da spec 023 já cobre o hover; isto é o texto literal "Nome Completo (SIGLA)").
- [ ] **O004** **Introdução — falar da lista completa de harnesses estudados** (não "rodada"): apresentar todos que passaram pelo estudo, com ponteiro para o apêndice do trabalho. *(o apêndice em si vira E04.)*

### Features estruturais derivadas (viram specs próprios; anotadas aqui)

- [ ] **E01** **Cross-link de citações (motor).** No build, menções a papers/fontes viram links para a Bibliografia; entradas da Bibliografia linkam a fonte. (deriva de O001)
- [ ] **E02** **Ilustração do cap. 00.** Imagem "modelo no centro, harness em volta", estilo **flat / isométrico / esquemático de blocos** (menos futurista). Gerar prompt + inserir asset.
- [ ] **E03** **Metadados de fork/sync dos harnesses.** No benchmark/lista, registrar **quando cada harness foi forkado/sincronizado** (não só a lista).
- [ ] **E04** **Apêndice "O estudo".** Lista completa dos harnesses avaliados, cada um com **resultado da análise + diagnóstico** e o **template de avaliação** adotado — mostrando todo o trabalho executado. (deriva de O004)
- [ ] **E05** **Companion → enviar sugestões.** O leitor manda sugestão pelo chat; o backend registra e **envia por email ao autor (ghdaru@gmail.com)** (serviço de email, chave no Railway) e/ou guarda no Postgres.
- [ ] **E06** **Página do autor: foto + LinkedIn.** Adicionar foto do autor (ex.: `publicar/tema/autor.jpg`) e o link do **LinkedIn** em `autor.md`.
- [ ] **E07** **Capa: link do LinkedIn** nos créditos da splash (repositório é público).

## Fechamento da rodada
- [ ] **F1** `livro/HISTORICO.md`: edição de revisão (nº na hora do fechamento) com resumo das correções + modelo de IA (A3).
- [ ] **F2** `node build.mjs` verde (link-check); screenshots das páginas tocadas aprovados pelo autor; sem identificador interno de modelo.
- [ ] **F3** Merge único `--no-ff` na `main` + push (publica o lote). (Opcional: autor cria Release → DOI de versão.)

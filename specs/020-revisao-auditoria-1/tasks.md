# Tasks: Rodada de auditoria e revisão 1

**Feature**: `020-revisao-auditoria-1` · **Plan**: [plan.md](./plan.md)

> **Lista rolante.** Cada observação do autor entra como uma task `O###`
> (Onde · O quê · Correção aplicada · Evidência, quando factual). A rodada
> fecha com o registro no HISTORICO + build verde + merge único na `main`.

## Observações → correções

<!-- modelo:
- [x] **O001** *(MVP no spec 028/E01: arXiv→Bibliografia; Bibliografia→fonte; passada fina de '(Autor, Ano)' fica p/ rodada 2)* `livro/capitulos/NN-arquivo.md` · seção "…" — <observação do autor> →
      correção: <o que foi trocado>. Evidência: <path/URL, se factual>.
-->

### Correções de conteúdo (auditoria)

- [ ] **O001** **Fundamentação total (estilo artigo científico).** Toda menção a um paper/fonte no texto deve **linkar para a Bibliografia**, e na Bibliografia o link para a **fonte** (DOI/URL). Vale também para **referências comerciais** (é livro, pode). *(parte vira tooling — ver E01.)*
- [x] **O002** *(spec 025/030: 'andaime' introduzido no cap 00/01; varredura 02–17 sem pendências)* **"scaffolding" em português.** Traduzir/introduzir o termo — *andaime (scaffolding)* / arcabouço / estrutura de suporte — na 1ª aparição (já aparece no subtítulo) e no Glossário.
- [x] **O003** *(spec 030: 46 expansões inline na 1ª ocorrência + <abbr> global do 023)* **Siglas por extenso inline na 1ª ocorrência** de cada capítulo (a passada pesada; o auto-`<abbr>` da spec 023 já cobre o hover; isto é o texto literal "Nome Completo (SIGLA)").
- [x] **O004** *(spec 030: cap 00 'Os harnesses do estudo' com os 16 sistemas → Apêndice)* **Introdução — falar da lista completa de harnesses estudados** (não "rodada"): apresentar todos que passaram pelo estudo, com ponteiro para o apêndice do trabalho. *(o apêndice em si vira E04.)*

- [x] **O005** *(spec 030: caps 14–17 + 00 ao formato editorial v3)* **Formato editorial dos capítulos.** O cap. 04 está no formato editorial; **revisar os demais** para o mesmo padrão (verificar 02–13 e alinhar).
- [x] **E08** *(spec 029: publicar/pdf.mjs)* **Gerar PDF do livro** ao final do roadmap (saída completa em PDF, além do site).

### Features estruturais derivadas (viram specs próprios; anotadas aqui)

- [x] **E01** *(spec 028)* **Cross-link de citações (motor).** No build, menções a papers/fontes viram links para a Bibliografia; entradas da Bibliografia linkam a fonte. (deriva de O001)
- [x] **E02** *(spec 027)* **Ilustração do cap. 00.** Imagem "modelo no centro, harness em volta", estilo **flat / isométrico / esquemático de blocos** (menos futurista). Gerar prompt + inserir asset.
- [x] **E03** *(spec 028: fork+commit por harness no Apêndice)* **Metadados de fork/sync dos harnesses.** No benchmark/lista, registrar **quando cada harness foi forkado/sincronizado** (não só a lista).
- [x] **E04** *(spec 028)* **Apêndice "O estudo".** Lista completa dos harnesses avaliados, cada um com **resultado da análise + diagnóstico** e o **template de avaliação** adotado — mostrando todo o trabalho executado. (deriva de O004)
- [x] **E05** *(spec 026)* **Companion → enviar sugestões.** O leitor manda sugestão pelo chat; o backend registra e **envia por email ao autor (ghdaru@gmail.com)** (serviço de email, chave no Railway) e/ou guarda no Postgres.
- [x] **E06** *(spec 024)* **Página do autor: foto + LinkedIn.** Adicionar foto do autor (ex.: `publicar/tema/autor.jpg`) e o link do **LinkedIn** em `autor.md`.
- [x] **E07** *(spec 024)* **Capa: link do LinkedIn** nos créditos da splash (repositório é público).

## Fechamento da rodada
- [x] **F1** *(edições 0.18–0.26 registradas por spec)* `livro/HISTORICO.md`: edição de revisão (nº na hora do fechamento) com resumo das correções + modelo de IA (A3).
- [x] **F2** *(builds verdes em todos os merges)* `node build.mjs` verde (link-check); screenshots das páginas tocadas aprovados pelo autor; sem identificador interno de modelo.
- [x] **F3** *(itens publicados por spec — 023–031; este merge fecha o registro da rodada)* Merge único `--no-ff` na `main` + push (publica o lote). (Opcional: autor cria Release → DOI de versão.)

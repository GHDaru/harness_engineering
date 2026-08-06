# Checklist de verificação — antes de todo merge na `main`

> **Quando usar:** em **toda** atualização deste repositório, no passo *implement* do ciclo
> spec-kit (ver [`CLAUDE.md`](../../CLAUDE.md)) e antes do `git merge --no-ff`.
> Vale também para as exceções que vão direto à `main` (correções triviais, governança) —
> nesses casos, só os blocos que se aplicam.

Cada item existe porque **já falhou uma vez**. A nota entre parênteses é o incidente que
o originou: é o que separa este checklist de uma lista de boas intenções.

---

## 0. Portão de entrada (antes de escrever qualquer linha)

- [ ] Estou numa branch `NNN-nome`, **não** na `main` (`git branch --show-current`).
- [ ] Existe `specs/NNN-nome/spec.md` (o QUÊ/PORQUÊ) — ou o caso é uma exceção explícita
      do Princípio VII (constituição, governança, typo, link quebrado).
- [ ] O `plan.md` passou pelo **Constitution Check**: 7 princípios, sem segredo,
      sem identificador interno de modelo.

## 1. Sempre — o build tem de ficar verde

```bash
cd publicar && npm run build     # 4 passos: build PT, build EN, verifica PT, verifica EN
```

- [ ] Os **quatro** passos passaram. `npm run build` já inclui o *link-check* interno:
      se ele imprimir `✗ N link(s) interno(s) quebrado(s)`, **é falha**, não aviso.
- [ ] `npm run pdf` roda (se o build de PDF for afetado — capítulos, tema, sumário).
- [ ] Testes da referência: `cd harness-um && python -m pytest tests/ -q`.
      *(o CI roda; rodar antes evita descobrir no merge)*

## 2. Se mexi em `livro/` — traduzir o delta (regra permanente, spec 067)

- [ ] Cada arquivo PT alterado teve o **par EN** atualizado (`livro/en/…`).
- [ ] O selo `<!-- i18n fonte:<pt> edicao:X hash:<md5-8> -->` da 1ª linha do arquivo EN
      foi regravado com o hash **real** do PT atual:

```bash
md5sum livro/capitulos/NN-nome.md | cut -c1-8
```

- [ ] Nenhum hash foi "estimado" ou copiado de outro arquivo. Um selo errado não quebra
      o build — ele mente na página, exibindo "em dia" para conteúdo defasado.
- [ ] Se o capítulo mudou de estado da arte: `livro/HISTORICO.md` recebe o registro de
      expiração, e o cabeçalho do capítulo recebe a nova data de captura.

## 3. Se mexi em conteúdo que o companion lê

Fontes do corpus: `livro/**`, `benchmark/{README,comparativo}.md`,
`benchmark/avaliacoes/*.md`, `radar/{RADAR,AGENTE}.md`, `radar/diario/*.md`.

```bash
cd chat-companion/backend && python3 build_corpus.py
```

- [ ] Corpus regenerado e commitado **na mesma branch**.
- [ ] Consulta de fumaça pelo termo novo (o nome do harness, a sigla, a data) retorna
      blocos com o campo `fonte` correto — não basta o bloco existir, ele precisa ser
      **encontrável** pela busca. *(o chat não achava o Grok mesmo com o Grok no radar)*

## 4. Se mexi em `benchmark/`

- [ ] `benchmark/comparativo.md` e `benchmark/notas.json` foram atualizados **juntos** —
      o JSON é a fonte das visualizações; divergência aparece só no gráfico.
- [ ] Para toda entrada em `notas.json`: `sum(notas) == total` e `len(notas) == 12`.

```bash
python3 - <<'PY'
import json
d = json.load(open("benchmark/notas.json"))
n = len(d["dimensoes"])
for cat in d["categorias"].values():
    for h in cat["harnesses"]:
        assert len(h["notas"]) == n, (h["nome"], "dimensões")
        assert sum(h["notas"]) == h["total"], (h["nome"], sum(h["notas"]), h["total"])
print("notas.json ok")
PY
```

- [ ] Se editei a **tabela** do comparativo por script: a linha preservou o `|` final e
      o alvo foi conferido por número de linha, não por regex de conteúdo.
      *(a tabela foi corrompida duas vezes: um `| 1 | Loop |` casava em três tabelas)*
- [ ] Toda avaliação nova tem página no site (ver bloco 6) e entra no `comparativo.md`.

## 5. Se mexi em UI (`publicar/tema/`, `build.mjs`, `jornal.mjs`, `viz/`)

O build verde **não** prova que a página funciona. Verificar no navegador:

- [ ] Screenshot da página afetada, **nos dois idiomas** (PT e `/en/`).
- [ ] Filtros e abas: clicar em cada um e confirmar que **nenhum esvazia a página**.
- [ ] Markdown não vazou como texto (`**`, `[texto](url)` visíveis no HTML renderizado).
- [ ] Fluxos com passos (tour, onboarding): percorrer até o fim — passo que depende de um
      painel aberto tem de **abrir o painel**, senão o balão fica órfão na tela.
- [ ] JS do tema: **nunca** declarar variável chamada `tx` (sombreia uma global e quebra o
      companion em silêncio — edição 0.64).

```bash
# padrão local: Chromium já instalado, node_modules do motor
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
NODE_PATH=/workspace/harness_engineering/publicar/node_modules \
node verificacao.mjs     # executablePath: "/opt/pw-browsers/chromium"
```

## 6. Se criei links — o repositório é privado

**Nenhum link novo pode apontar para o repositório no GitHub.** Todo acesso é pelo site.

- [ ] Rodei a busca e a lista de **alvos distintos** não cresceu (contar ocorrências não
      serve: o link do rodapé sozinho aparece em ~100 páginas):

```bash
cd publicar && npm run build && cd ..
grep -rho 'https://github.com/GHDaru/harness_engineering[^"<) ]*' docs --include=*.html | sort -u
```

      Linha de base (após a spec 083): **9 alvos** — a raiz do repo, o `.git`, a tag
      `v0.62.0`, `tree/main/harness-{um,zero}` e 4 `blob/main/…` para arquivos de
      **código** ainda não publicados (`scripts/sync-forks.ps1`,
      `publicar/DESIGN-SISTEMA.md`, `harness-um/README.md`,
      `chat-companion/backend/EMAIL.md`). Esses 4 aguardam decisão do editor
      (publicar / espelho público de código / reescrever a menção); **qualquer alvo
      novo além desses é regressão.**

- [ ] Conteúdo novo que precisa ser linkável (avaliação, ADR, estudo, template) foi
      registrado em `descobrirExtras()` (`publicar/build.mjs`) e ganhou página própria.
- [ ] O `mapaExtras` é construído **nos dois passes** (PT e EN) — no pass EN o slug leva
      prefixo `../`. *(um `EN ? [] : …` deixou o inglês inteiro apontando para o GitHub)*
- [ ] Nenhum link foi escrito à mão fora do reescritor de links (ex.: templates em
      `jornal.mjs`) — links hardcoded escapam do portão e do link-check.

## 7. Se mexi no Radar

- [ ] O agente escreveu **só** em `radar/`; commit `radar: AAAA-MM-DD`.
- [ ] `radar/RADAR.md` continua ordenado por data (a capa escolhe pela data — tabela fora
      de ordem já colocou um item **descartado** na capa).
- [ ] Contrato honrado: agregador é pista, não fonte; data verificada à parte do fato;
      candidato a corpus passou pela triagem de repositório (razão estrela/fork ≳ 5:1).
- [ ] Nada não verificado entrou sem ⏳.

## 8. Segurança e identidade (bloqueante, sempre)

- [ ] `git diff --cached` não contém segredo, token, senha ou URL com credencial.
      Credenciais só em variável de ambiente do Railway / `.env` gitignored.
- [ ] Nenhum **identificador interno de modelo** em commit, PR, código, comentário ou
      artefato publicado. O crédito no HISTÓRICO usa o nome público do produto.
- [ ] Nenhuma fonte fabricada: afirmação sobre harness tem caminho de arquivo; citação
      científica tem status ✓; fonte de indústria tem URL verificável; o resto leva ⏳.
- [ ] Material da proposta editorial **não** foi para este repositório (é privado).

## 9. Registro e fechamento

- [ ] `livro/HISTORICO.md`: nova edição (ou entrada de correção) quando a mudança afeta
      o livro, com a nota A3 do modelo de IA usado.
- [ ] Decisão relevante virou ADR em `adr/` (contexto → decisão → alternativas →
      justificativa → consequências).
- [ ] `git merge --no-ff NNN-nome` na `main` e `git push -u origin main`.
- [ ] **CI verde conferido depois do push** — o merge é o que publica; o merge não é o
      fim. Job `build` verde e `deploy` concluído.

---

## Anti-checklist — erros de método que este documento também cobra

- Não declarar "verificado" o que só foi construído. Build verde ≠ página correta.
- Não diagnosticar por memória: reconsultar o dado antes de afirmar que ele sumiu.
  *(afirmei que o corpus perdera o campo `fonte`; eu é que consultava a chave errada)*
- Não editar arquivo estruturado (tabela, JSON) por regex ampla sem asserção prévia que
  falhe se o alvo não for exatamente o esperado.
- Não deixar decisão do editor virar suposição do agente: quando as opções mudam o
  resultado, perguntar antes de implementar.

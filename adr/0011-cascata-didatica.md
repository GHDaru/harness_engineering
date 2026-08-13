# ADR 0011 — A cascata didática: ordem pela trilha, andaime decrescente, portão nos dois idiomas

- **Status**: **aceita** (2026-08-12) — decisão delegada pelo editor (*"chame dois especialistas subagentes, concilie suas respostas, registre em um ADR e prossiga"*)
- **Features**: `099`–`102` (os quatro lotes)
- **Decorre de**: specs `097` (camada v4) e `098` (primeiro lote), registradas nas edições 0.81 e 0.82 do [Histórico](../livro/HISTORICO.md)

## Contexto

Quatro dos 18 capítulos estão na camada didática v4 (00, 01, 02, 17). Faltam 14, e a pergunta é em que ordem, em quantas fatias e sob que portões.

A pergunta foi submetida a **dois especialistas independentes**, com lentes deliberadamente diferentes: um de **design instrucional** (Backward Design, 4C/ID, Diátaxis, carga cognitiva) e um de **produção editorial** (developmental editing, docs-as-code, i18n, portões em CI). Cada um leu o repositório e respondeu sem ver a resposta do outro.

**Onde concordaram, sem combinar:**

1. **"Pior métrica primeiro" está errado.** Era a ordem que eu havia proposto. Os dois a rejeitaram pelo mesmo argumento: o pior capítulo do livro é o **14 Convergências** (26,7 travessões/1k) e ele é o **pior candidato possível a primeiro**, porque é síntese dos outros treze. Travessão mede sintoma, não dificuldade nem dependência.
2. **O portão do exemplo trabalhado é frágil.** `temExemplo` é um regex de crase tripla: qualquer bloco de código satisfaz a regra pedagógica mais cara do livro. Um YAML de três linhas passa.
3. **14 é o último, sem exceção.**

**Onde divergiram:** a ordem dos outros treze. O de instrução propôs a **ordem das etapas do harness-zero**; o de produção propôs **folhas do grafo de referências primeiro**, para reduzir retrabalho.

**Verificação das duas premissas** (Princípio I — não se aceita relatório de agente sem conferir a fonte):

- ✅ O `harness-zero/README.md` publica mesmo a tabela **Etapa → Capítulo**, e a linha 72 diz *"o diff entre etapas consecutivas é a lição do capítulo"*. A ordem das etapas é `02-tools→05`, `03-contexto→03`, `04-sessoes→08`, `05-compactacao→04`, `06-permissoes→07`, `07-mcp→06`, `08-plan→09`, `09-subagentes→10`, `10-evals→11`, `11-hooks→12`, `12-skills→16`.
- ❌ **Uma premissa do especialista de instrução não se sustenta.** Ele argumentou que escrever fora da ordem das etapas *"obriga o autor a inventar exemplos fictícios ou a escrever para trás um artefato que ainda não nasceu"*. A mesma linha 72 diz que **a trilha está completa (etapas 00–12) e cada etapa é autocontida**. Nada precisa ser escrito para trás: os treze artefatos já existem e podem ser lidos em qualquer ordem. O que a ordem das etapas preserva é o **vocabulário**, não a existência do exemplo — argumento mais fraco do que o alegado, e ainda assim válido.
- ✅ Dos 14 restantes, **todos** têm seção de Verificação, **13** têm Apêndice A, e **todos os 14 têm zero blocos de código**. O exemplo trabalhado é o item caro; o travessão é o barato.
- ✅ **Dois selos i18n estão atrasados agora** (`appendix-study.md`, `appendix-usage.md`) com o `npm run build` **verde**. "Atrasado" é hoje um estado publicável.
- ✅ Os capítulos **15, 16 e 14 não têm seção "Mão na massa"**, e o 16 tem etapa correspondente (`12-skills`). É dívida estrutural, não estilo.

## Decisão

### 1. A ordem: a trilha do harness-zero, com o 07 antecipado

```
Lote A (spec 099):  05 Ferramentas · 03 Contexto · 07 Permissões
Lote B (spec 100):  08 Memória · 04 Compactação · 06 MCP
Lote C (spec 101):  09 Planejamento · 10 Subagentes · 11 Verificação · 12 Extensibilidade
Lote D (spec 102):  16 Auto-evolutivo · 13 Interfaces · 15 Embutido · 14 Convergências
```

É a ordem das etapas do harness-zero **com uma troca**: o cap. 07 sobe da posição 5 para a 3.

A troca concilia os dois pareceres e é a única mudança entre eles. O especialista de produção queria 07 no primeiro lote (é folha do grafo, e os quatro capítulos já em v4 fizeram promessa explícita a ele: *"o cap. 07 é inteiro sobre ela"*). O de instrução o queria na posição 5, com a justificativa de que *"a ferida do `read_file` foi aberta na etapa 03 e a dívida precisa ser paga cedo"* — antecipá-lo para logo depois do 03 **paga a dívida ainda mais cedo**, reforçando o próprio argumento em vez de contrariá-lo.

Duas dependências de conteúdo são invioláveis e sobrevivem ao lote:

- **08 antes de 04**, porque a compactação age na *visão* e nunca no *registro persistido*, e o registro nasce no 08. Aqui o parecer de instrução prevalece sobre o agrupamento por grafo, que colocaria 04 antes.
- **05 e 07 antes de 06**, porque o adapter MCP alimenta a `ToolPort` do 05 e a política do 07 vale para tool de MCP.

### 2. Fatiamento: quatro specs de 3–4 capítulos

Nem uma spec por capítulo, nem uma para os 14. Cada capítulo toca quatro arquivos compartilhados (`HISTORICO.md`, `mede-prosa.mjs`, `.specify/feature.json`, `corpus.json`), então 14 specs produzem 14 conflitos nos mesmos arquivos — e `corpus.json` tem 1,2 MB **numa linha só**, irresolvível à mão. Uma spec única para os 14 mantém uma branch viva por dias contra uma `main` que o CI move a cada push.

O lote de 3–4 é o ponto em que o custo fixo se dilui sem a branch envelhecer: a spec 098 custou 925 inserções em 13 arquivos e coube num dia.

**Regra de merge**, contra o conflito de corpus que já aconteceu: na branch, `git fetch origin main && git merge FETCH_HEAD` (resolvendo o corpus por **regeneração**, nunca à mão) **antes** do `--no-ff` para a main. Merge, jamais rebase — o rebase achatou o merge da spec 094.

### 3. O andaime desvanece ao longo do livro

A regra 2 do v4 passa a ter uma curva declarada, e o capítulo a declara no cabeçalho:

| Faixa | Capítulos | `andaime:` | O que o exemplo é |
|---|---|---|---|
| Novato | 00–08 | `completo` | código resolvido e comentado, com o raciocínio visível |
| Intermediário | 09–13 | `lacuna` | resolvido, com **uma lacuna deliberada** que o leitor fecha |
| Síntese | 14–16 | `proprio` | nenhum código novo: o exemplo é o harness que o leitor já construiu |

É a discordância do especialista de instrução, e ela é aceita porque corrige no v4 o mesmo defeito que o v4 corrigiu no v3. O *worked-example effect* de Sweller vem acompanhado do *expertise reversal effect* de Kalyuga: o exemplo totalmente resolvido ajuda o novato e **atrapalha** quem já é competente. Um piso constante de "≥ 1 bloco de código" aplica metade da lição que o livro ensina.

### 4. Os portões, antes do primeiro lote

Cinco correções no medidor, todas baratas e todas **nascendo verdes** — o que é a condição para não virarem ruído (lição da spec 097):

1. **Medir o EN também.** Hoje `mede-prosa.mjs` só enumera caminhos PT, e três strings suas são PT-hardcoded: `corpoDe()` corta em `## Apêndice A` (o EN diz "Appendix A", então o apêndice inteiro entra na conta e infla o EN) e `gabaritoSeparado` procura `## Respostas da verificação` (o EN diz "Verification answers"). **Metade do livro publicado não tem portão nenhum.**
2. **Exemplo trabalhado com forma, não só cerca.** O bloco tem de estar na seção `### Na prática` / `### In practice`, declarar linguagem e ter piso de linhas. Sem isso o portão aceita o YAML que já estava ali, que é *reward hacking* no sentido exato do cap. 11.
3. **Evidência não some.** Extrair os tokens que parecem caminho de arquivo antes e depois e reprovar se algum desapareceu do arquivo. Mover do corpo para o Apêndice A passa; apagar não passa. É a mitigação mecânica do risco nº 1 da spec 097, que hoje depende de atenção humana 14 vezes.
4. **Paridade estrutural PT/EN**: mesma contagem de `##`, `###` e cercas de código no par. Hoje há zero divergência nos 29 pares, então nasce verde e pega o modo de falha dominante da tradução em série.
5. **Selo i18n atrasado reprova o build**, com os dois apêndices atrasados como baseline nomeada. Hoje "PT mergeado, EN esquecido" passa por todos os portões.

O `REESCRITOS` deixa de ser lista à mão e passa a ser **derivado do marcador de cabeçalho** (`camada didática v4`), com asserção de que a lista de capítulos tem 18 — hoje ela é montada com `.filter(existsSync)` e um arquivo renomeado sairia da medição **sem falhar**.

### 5. Critério de parada da série

- `npm run build` verde terminando em **`✓ prosa: 36 capítulo(s) v4 dentro dos limites`** (18 PT + 18 EN);
- tabela do medidor com 36 linhas no `HISTORICO.md`, todas com `0 longas`, exemplo e gabarito;
- **zero** selos i18n atrasados nos 18 capítulos;
- nenhum caminho de evidência desaparecido;
- baseline de links para o GitHub ainda em **9 alvos distintos**;
- crescimento do corpo medido contra o alvo de +40% da spec 097, por capítulo;
- e **dois capítulos sorteados** — sorteados, não escolhidos por quem escreveu — lidos inteiros. Todos os portões acima medem ausência de defeito; nenhum mede presença de ensino.

## Alternativas avaliadas

- **A — Pior métrica primeiro** (minha proposta original). Rejeitada por unanimidade dos dois pareceres: poria o capítulo-síntese em primeiro lugar, e a métrica nem enxerga os dois capítulos mais quebrados pedagogicamente (15 e 16, sem "Mão na massa").
- **B — Ordem de leitura (03…16).** Rejeitada: otimiza para um leitor que ninguém tem, o que lê o livro no meio da reescrita. O repositório já rejeitou esse critério na prática ao reescrever 00, 01 e 17 fora de ordem.
- **C — Folhas do grafo de referências primeiro** (parecer de produção, puro). Aceita **em parte**: define o Lote A e a posição do 07, mas quebraria a dependência 08→04, que é de conteúdo e não de citação.
- **D — Ordem das etapas, pura** (parecer de instrução). Aceita **em parte**: é a espinha, mas deixaria o 07 tarde demais e apoiava-se numa premissa falsa (a de que os artefatos ainda não existem).
- **E — Reconciliada (escolhida).** Espinha das etapas + antecipação do 07. Custa uma troca de posição e satisfaz as duas justificativas simultaneamente.

## Consequências

- **Positivas**: o exemplo trabalhado de cada capítulo passa a ser **código versionado que já existe e roda**, não invenção; o andaime desvanece como o método manda; e o portão passa a cobrir os dois idiomas, o que hoje não acontece.
- **Custos aceitos**: quatro specs em vez de uma; um campo novo no cabeçalho de cada capítulo (`andaime:`); e cinco verificadores a mais no build.
- **Reversibilidade**: alta, e por isso a decisão foi delegada. Nada aqui é irreversível: capítulo é texto versionado, e a ordem de escrita não aparece no livro publicado.
- **Fronteira**: o portão continua **sintático**. Nenhum dos cinco verificadores mede se o capítulo ensina — por isso o critério de parada exige leitura humana de dois capítulos sorteados. Trocar isso por medição automática de qualidade de ensino exigiria nova ADR, e provavelmente um juiz LLM, que o cap. 11 mostra ser não-determinístico e enviesado por posição.

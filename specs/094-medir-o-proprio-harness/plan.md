# Plano — spec 094

## Constitution Check

| Princípio | Como esta spec o honra |
|---|---|
| **I — evidência acima de retórica** | o placar publicado é execução real, com data e versão; a ferramenta foi verificada no repositório (MIT, 164★/12 forks, não arquivada), não no site |
| **II — a fonte-base é o código** | o mapa dimensões↔capítulos sai das 36 checagens, não do material de divulgação |
| **III — o livro é vivo** | a caixa de honestidade tem "antes e depois" e envelhece com data explícita |
| **IV — nada de segredo** | um dos hooks passa a **impor** isso, em vez de pedir |
| **V — direito do leitor** | nenhuma coleta nova; a ferramenta roda na máquina dele, sem rede |
| **VI — sem identificador interno de modelo** | segundo hook passa a **impor** isso |
| **VII — ciclo spec-kit** | esta spec |

Sem segredo em artefato. Sem identificador interno de modelo em commit, código ou texto publicado.

## Ordem

**1. Medir e registrar o "antes" antes de tocar em qualquer coisa.** O placar de partida é dado
perecível: qualquer arquivo novo o altera. Ele já está capturado na spec e vai para o apêndice
literalmente.

**2. Correção do repositório, item a item, cada um justificado sem o placar.** Nesta ordem, porque
os hooks são o item de maior valor e o de maior risco de atrapalhar o trabalho — entram por último,
depois de os sensores estarem de pé.

**3. Medir o "depois"** e só então escrever o texto do livro, que cita os dois números.

**4. Livro**: apêndice novo → cap. 11 → cap. 01 → bibliografia. O apêndice primeiro porque os
outros dois apontam para ele.

**5. Traduzir o delta** (regra permanente, spec 067): cada arquivo PT alterado tem par EN
atualizado e selo `<!-- i18n fonte:… hash:<md5-8> -->` regravado com o **hash real** do PT final.

**6. Fechamento**: build 4 passos, testes, corpus, checklist, HISTORICO, merge `--no-ff`, push, CI.

## Decisões de projeto

### O ponto de entrada de testes
Um `Makefile` na raiz com `make test` que roda as três suítes. Não é adorno de scanner: é a
resposta executável à pergunta que hoje só o `CLAUDE.md` responde. Complementado por um
`pyproject.toml` de raiz que declara `testpaths` para os dois projetos Python — é o que faz o
`pytest` funcionar a partir da raiz, e o que o scanner reconhece como runner configurado.

### Linter e formatador
**Ruff**, um só para os dois projetos Python, configurado na raiz. Escolha por subtração: já é a
ferramenta mais provável de estar disponível, faz lint e formatação num binário, e não exige
adicionar dependência de desenvolvimento a dois `requirements`/`pyproject` distintos.

**Regra de não quebrar (R4)**: a configuração declara o padrão e o CI roda `ruff check` em modo
não-bloqueante nesta spec. Conformar o código existente é trabalho de outra spec — e misturar
"declarar padrão" com "reformatar tudo" produziria um diff em que nenhuma das duas coisas é
revisável.

### Os hooks
`.claude/settings.json`, três hooks, cada um impondo uma regra que hoje é prosa:

| Hook | Evento | Regra que passa a impor | Onde ela vivia |
|---|---|---|---|
| `guarda-segredo` | `PreToolUse` (Write/Edit) | conteúdo com assinatura de credencial não é gravado | constituição, Princípio IV |
| `guarda-identidade` | `PreToolUse` (Write/Edit) | identificador interno de modelo não entra em arquivo | constituição, Princípio VI |
| `guarda-git` | `PreToolUse` (Bash) | `push --force`, `reset --hard`, `clean -fdx` pedem confirmação | prática, em lugar nenhum |
| `formata-python` | `PostToolUse` (Write/Edit) | arquivo `.py` editado passa pelo formatador | nenhum |

Os scripts vivem em `.claude/hooks/`, são versionados (o scanner cobra isso em `HKS-05`, e com
razão: hook apontando para script ausente falha aberto em toda máquina menos a sua) e não têm
dependência além de Python 3, que o repositório já exige.

**O que os hooks deliberadamente não fazem**: impor "escrita somente em `radar/`". Essa regra é do
**agente do Radar**, não do repositório — um hook de repositório que bloqueasse `livro/` quebraria
todo o trabalho editorial normal. Fica registrado no apêndice como limite real da técnica: hook é
guarda-corpo **de repositório**, não de papel.

### A caixa de honestidade
Vai no apêndice, não no capítulo, e traz três coisas: o placar antes, o placar depois, e a **lista
do que não foi feito e por quê**. A terceira é a que dá valor às outras duas — sem ela, "subimos de
L2 para L3" é propaganda.

## Riscos

| Risco | Mitigação |
|---|---|
| hooks atrapalharem o trabalho normal | três hooks estreitos, todos com escape documentado; testados nesta sessão antes do merge |
| `ruff` indisponível no CI | passo de lint tolerante a ausência; a spec declara o padrão, não força a adoção |
| o apêndice novo quebrar a paridade PT/EN | sumários são espelhados **por posição** (`parDe` em `build.mjs`) — a entrada entra na mesma posição nos dois |
| o placar "depois" não atingir L3 | é resultado, não meta: se não atingir, o apêndice publica o número real e o gap que restou |

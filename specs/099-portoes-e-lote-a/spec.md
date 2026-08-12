# Spec 099 — Os portões, e o Lote A da cascata (05, 03, 07)

> Branch: `099-portoes-e-lote-a` · aberta em 2026-08-12
> Decisão: [ADR 0011](../../adr/0011-cascata-didatica.md) · método: [spec 097](../097-reescrita-didatica/spec.md)

## 1. Por que os portões vêm antes do lote

O ADR 0011 conciliou dois pareceres independentes e ambos apontaram o mesmo buraco: **metade do livro publicado não tinha portão nenhum**. O `mede-prosa.mjs` só enumerava caminhos PT, e três strings suas eram PT-hardcoded — o corte em `## Apêndice A` não casava com `## Appendix A`, então o apêndice inteiro entrava na conta de prosa do EN.

Medir o fim da série sem isso seria afirmar "terminou bem" sobre metade do livro.

## 2. O que os portões passaram a fazer

| Portão | O que passou a pegar |
|---|---|
| Medição nos dois idiomas | 18 PT + 18 EN, com apêndice, verificação, gabarito e marcador por idioma |
| Lista descoberta e conferida | a lista usava `.filter(existsSync)`: arquivo renomeado saía da medição **sem falhar** |
| `v4` derivado do cabeçalho | era lista à mão; capítulo reescrito e não inscrito publicava sem portão |
| Exemplo trabalhado com **forma** | dentro da seção `Na prática`, com linguagem declarada e piso de 6 linhas |
| `andaime:` declarado | curva de Kalyuga (ADR 0011 §3): piso constante aplicava metade da lição de Sweller |
| Paridade estrutural PT/EN | `##`, `###`, cercas e andaime iguais no par |
| Baseline de evidência | caminho de arquivo pode **mover** para o Apêndice A; não pode sumir |
| `verifica-selos.mjs` | selo i18n atrasado reprova o build (dois apêndices como dívida declarada) |
| `sela.mjs` | grava o selo por script, a partir da fonte, com os arquivos nomeados |

## 3. Dois erros meus, no mesmo dia

**O `sela.mjs` mentiu enquanto existiu na primeira versão.** Ele rodava sem argumentos e reselava tudo, inclusive os **dois apêndices cuja tradução estava atrasada de verdade**. Selo regravado sobre texto não traduzido não conserta o atraso: **apaga**. Os dois foram revertidos aos selos antigos, e a ferramenta passou a exigir os arquivos nomeados um a um — o hash é cálculo, mas a afirmação de sincronia é de quem traduziu.

**O terceiro falso positivo do medidor**, e da mesma família dos dois da spec 098: um comentário `# ...` **dentro** de um bloco Python é indistinguível de um cabeçalho markdown para quem olha só o começo da linha, e a seção `Na prática` do cap. 07 terminava no meio do primeiro exemplo. A varredura passou a ter estado de cerca. As três causas são uma só: **estrutura lida como se fosse marcação**.

## 4. O Lote A

Ordem do ADR 0011: espinha das etapas do harness-zero, com o 07 antecipado.

**05 Ferramentas** — cena: o parâmetro renomeado de `padrao` para `glob`, com o schema à mão ficando para trás; o modelo obedece o schema com perfeição e recebe `TypeError` a cada turno. Exemplo trabalhado: a mesma `buscar_arquivos` **três vezes** — schema à mão, schema derivado por `inspect`, e retorno separado em `dado` × `para_o_modelo`, com a conta de 4.100 caminhos (~60k tokens) contra ~400.

**03 Contexto** — cena: a fatura que quadruplica porque alguém pôs `Data e hora` no topo do system prompt e o cache por prefixo nunca mais acertou. Exemplo trabalhado: montador ingênuo × camadas por volatilidade, **mais o teste de estabilidade de prefixo** que imprime o offset da divergência e os 80 caracteres seguintes. É a peça mais barata do capítulo e não existia.

**07 Permissões** — cena: o `read_file` que o próprio leitor escreveu no cap. 03 lendo `~/.ssh/id_rsa` porque um `AGENTS.md` de repositório clonado mandou. Exemplo trabalhado: `decide()` como função pura, com `.resolve()` antes da comparação, `is_relative_to` em vez de prefixo de string e default fechado; **depois** o mesmo comando "permitido" dentro de `bwrap --unshare-net`, para separar política de contenção em código, não em prosa.

## 5. Medição final

Total da série: **14 capítulos v4** (7 PT + 7 EN) dentro dos limites, com travessões entre 0,0 e 7,2 por mil, frase média entre 13,7 e 18,5, e nenhuma frase acima de 60 palavras.

## 6. Fila

Lote B (spec 100): **08 Memória**, **04 Compactação**, **06 MCP** — nessa ordem, porque a compactação age na *visão* e nunca no *registro*, e o registro nasce no 08.

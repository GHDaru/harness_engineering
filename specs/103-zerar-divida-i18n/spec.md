# Spec 103 — Zerar a dívida i18n dos dois apêndices (e o que a investigação achou)

> Branch: `103-zerar-divida-i18n` · 2026-08-13 · fecha a pendência da [spec 102 §5](../102-lote-d/spec.md)

## 1. O pedido, e por que ele estava mal formulado

O pedido foi *"traduza os dois apêndices atrasados e zere a dívida"*. A primeira metade não tinha o que fazer: **nada estava sem tradução**.

`appendix-study.md` e `appendix-usage.md` entraram na `DIVIDA_DECLARADA` do `verifica-selos.mjs` na spec 099 porque o portão novo os apontou como atrasados. Eu li o veredito do portão — selo aponta para um hash que já não existe — e escrevi "tradução atrasada" no ADR, na spec e no relato ao editor. Não conferi.

O que a conferência mostra:

| Arquivo | Selo | Fonte PT no selo | Delta PT desde o selo |
|---|---|---|---|
| `livro/en/appendix-study.md` | `1a781be9` (ed. 0.61) | commit `c1d33e09`, 2026-08-06 | **um link**: `[Radar diário](…/radar/RADAR.md)` → `(radar-mesa.html)` |
| `livro/en/appendix-usage.md` | `fa3fed2c` (ed. 0.61) | commit `ba56f942`, 2026-07-29 | **um link**: `[ADR 0007](…/adr/0007-…md)` → `(adr-0007-cadencia-livro-vivo.html)` |

Os dois deltas são a mesma coisa: a migração de link da **spec 083** (site autossuficiente, conteúdo publicado como página). Nenhuma frase de conteúdo mudou nos dois lados.

E os arquivos EN **já traziam a forma migrada** — `../radar-mesa.html` na linha 36 do estudo, `../adr-0007-cadencia-livro-vivo.html` na linha 24 do uso. Quem fez a spec 083 atualizou o EN junto e não regravou o selo. Paridade estrutural confere: mesmos 8 títulos no estudo, mesmas 29 linhas de tabela, mesmos 4 títulos no uso.

Era **dívida de selo**, não dívida de tradução. Diferença que importa: dívida de tradução custa um dia de escrita; dívida de selo custa um comando.

## 2. O falso positivo que eu mesmo criei

Vale registrar o que quase entrou nesta spec como conserto. Na primeira leitura, achei um "resto" no EN: a linha 10 do `appendix-study.md` linka `sync-forks.ps1` pela URL do GitHub, enquanto o PT usa o caminho relativo `../scripts/sync-forks.ps1`.

Ia mudar. Antes, conferi o HTML gerado — e o build reescreve o link relativo do PT **exatamente para aquela URL**, porque `scripts/` não é página publicada. O EN não estava divergindo do PT: estava escrito na forma que o PT assume depois do build.

É a mesma família de erro do medidor de prosa: **estrutura lida como se fosse conteúdo**. O quinto caso, agora em link em vez de frase. Nada a consertar; o beco sem saída de `scripts/` continua registrado no [HISTORICO](../../livro/HISTORICO.md) como decisão pendente do editor.

## 3. O que muda

**Selos regravados** pelo `sela.mjs`, com os nomes explícitos (a ferramenta recusa selagem em massa desde a spec 099, por bom motivo):

```
node publicar/sela.mjs livro/en/appendix-study.md livro/en/appendix-usage.md
```

**Exemção removida.** `DIVIDA_DECLARADA` volta a ser um conjunto vazio no `verifica-selos.mjs`. Enquanto o nome está na lista, o portão passa por cima do arquivo — a dívida só é dívida de verdade quando sair de lá.

**Triagem embutida no `--conferir`.** A causa raiz desta spec não é o selo velho, é que **eu não distingui as duas dívidas**. O `sela.mjs --conferir` passa a responder a pergunta que eu deveria ter feito: para cada selo fora de sincronia, ele localiza o commit cuja fonte PT casa com o hash selado e informa quantas linhas do PT mudaram desde então, e se o arquivo EN foi tocado depois daquele commit.

```
~ appendix-study.md: 1a781be9 → 3f4ba7a0 (edição 0.61 → 0.86)
    selo em c1d33e09 (2026-08-06) · PT: 2 linha(s) desde então · EN tocado depois: sim
```

`EN tocado depois: sim` com PT mudando pouco é assinatura de dívida de selo. `não` com PT mudando muito é dívida de tradução. O portão continua reprovando as duas; quem lê agora sabe qual é sem fazer arqueologia de hash.

**Um número errado no relatório do portão.** Ao conferir a saída, o `verifica-selos.mjs` contava o arquivo exemptado duas vezes: uma como página "em dia" e outra como dívida declarada — `29 páginas em dia (+2 de dívida)` sobre um universo de 29 arquivos. O contador subia antes da comparação de hash. Agora sobe só quando o selo casa.

## 4. Dois links de GitHub que a cascata deixou entrar

O bloco 6 do checklist tem linha de base fixa: **9 alvos distintos** de `github.com/GHDaru/harness_engineering` no site gerado, dos quais 4 são arquivos de código aguardando decisão do editor. Conferido aqui, o site tinha **11**:

```
…/blob/main/specs/097-reescrita-didatica/spec.md
…/blob/main/specs/098-cascata-didatica/spec.md
```

Vieram de três menções escritas durante a cascata — no `GUIA-EDITORIAL.md`, no par EN e no cabeçalho do ADR 0011. `specs/` não é página publicada, então o reescritor de links faz o que faz com todo caminho não publicado: manda para o GitHub. Com o repositório privado, é porta fechada para o leitor.

As três viraram menção sem link, com o ponteiro para onde a decisão **está** publicada: `spec 097, registrada na edição 0.81 do Histórico`. O número da spec continua rastreável; o link morto sai. O checklist volta a 9 alvos.

Nenhum portão pegou isso, e não é falta de portão: o bloco 6 é uma **conferência manual**, e eu não a rodei nas specs 097–102. É o segundo item da série que passa porque o processo tem um passo humano que eu tratei como opcional.

## 5. Critério de parada

| Critério | Como se verifica |
|---|---|
| Os dois selos casam com a fonte PT | `node publicar/sela.mjs --conferir` → 0 a regravar |
| `DIVIDA_DECLARADA` vazia | leitura do `verifica-selos.mjs` |
| Portão reporta zero tolerância | `✓ selos i18n: 29 páginas EN em dia … (+0 de dívida declarada)` |
| Build inteiro verde | `npm run build` em `publicar/` |
| Corpus do companion regenerado | `python3 build_corpus.py` |
| CI verde na main depois do merge | Actions |
| Alvos de GitHub de volta à linha de base | `grep -rho …` em `docs` → **9** alvos |

## 6. O que fica em aberto

- Os **7 links para código** (`scripts/`, `harness-um/`, `chat-companion/`, `publicar/`) seguem becos sem saída para o leitor do site, nos dois idiomas. Decisão do editor, registrada no HISTORICO desde a spec 095: publicar, espelhar num repo público ou reescrever as menções.
- Nada mais na fila de i18n: com a exemção removida, o próximo atraso reprova o build no commit em que nascer.

# Spec 102 — Lote D, e o fim da cascata: 12, 13, 16, 15, 14

> Branch: `102-lote-d` · 2026-08-12 · decisão: [ADR 0011](../../adr/0011-cascata-didatica.md)

## 1. A curva de andaime, corrigida antes do lote

Antes de escrever o Lote D, corrigi uma infidelidade minha ao ADR: os capítulos **09, 10 e 11 estavam declarados `completo`** e o ADR os põe na faixa `lacuna`. Cada um recebeu uma **lacuna deliberada** no exemplo trabalhado, e a declaração foi trocada.

Não era só um rótulo. Sem a lacuna, o livro aplicaria metade da lição de Sweller que ele mesmo ensina — *worked-example effect* sem *expertise reversal effect*.

A curva agora é a do ADR: `completo` em 00–08, `lacuna` em 09–13, `proprio` em 14–16.

## 2. Os cinco capítulos

**12 Extensibilidade** (`lacuna`) — cena: o fork que ficou três versões atrás por causa de duas regras que não cabiam em lugar nenhum. Exemplo: o hook cujo **retorno é o canal de controle** (`None` segue, objeto reescreve, `block:` recusa com motivo), mais a conta a pagar — o plugin roda com a autoridade do harness.

**13 Interfaces** (`lacuna`) — cena: o modo headless de dois dias que virou duas semanas, porque o critério de parada morava dentro do renderizador do terminal. Exemplo: o núcleo publicando **eventos tipados**, com o adapter NDJSON de duas linhas que entrega o modo que custou duas semanas.

**16 Auto-evolutivo** (`proprio`) — cena: a terceira semana corrigindo o mesmo `print`, com o humano fazendo o trabalho de memória de longo prazo de graça. Ganhou a seção **"Mão na massa" que não existia**, apesar de a etapa 12 do harness-zero existir — dívida estrutural apontada pelo especialista de instrução e paga aqui.

**15 Embutido** (`proprio`) — cena: quatro minutos para ter um agente em produção, e a pergunta que o capítulo faz: **o que acontece na mensagem 200?**

**14 Convergências** (`proprio`) — cena: duas equipes, dois harnesses escolhidos por razões opostas, o mesmo desenho no quadro branco. O exemplo trabalhado é o **harness que o leitor construiu**: confira as oito convergências contra as suas treze etapas.

## 3. O custo do método roteirizado, medido

O Lote C registrou que a transformação roteirizada degrada prosa de um jeito que o portão não pega. O Lote D confirmou, e a leitura por sorteio do ADR §5 encontrou mais um tipo:

**Ponto final dentro de parênteses**, onde havia ponto e vírgula — `(o OpenClaw usa X. O IronClaw declara Y)`. Corrigido em **12 arquivos** por varredura própria.

Foi encontrado **lendo o cap. 12**, que caiu no sorteio. Nenhum portão o pegaria: é sintaticamente impecável e semanticamente pior.

## 4. Critério de parada (ADR 0011 §5)

| Critério | Estado |
|---|---|
| `✓ prosa: 36 capítulos v4` (18 PT + 18 EN) | ✅ |
| Zero selos i18n atrasados nos 18 capítulos | ✅ (2 apêndices como dívida declarada) |
| Nenhum caminho de evidência desaparecido | ✅ (portão de baseline verde) |
| Crescimento do corpo contra o alvo de +40% | ✅ **+29%** (31.623 → 40.670 palavras) |
| Dois capítulos sorteados, lidos inteiros | ✅ **03** e **12**, sorteados pelo hash do commit base |

## 5. O que fica em aberto

- **Dois apêndices EN atrasados** (`appendix-study`, `appendix-usage`), dívida declarada desde a spec 099 e nomeada no `verifica-selos.mjs`.
- **O portão continua sintático.** Ele mede ausência de defeito de forma e não mede presença de ensino. As três degradações desta série foram todas encontradas por leitura, nunca por medição — e é por isso que a leitura por amostragem ficou no critério de parada, e não como recomendação.

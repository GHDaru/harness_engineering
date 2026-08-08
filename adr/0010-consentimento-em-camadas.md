# ADR 0010 — Consentimento em camadas: continuidade e contato são coisas diferentes

- **Status**: **aceita** (2026-08-08) — aprovada pelo editor; implementada na spec 093
- **Feature**: `093-progresso-e-contato`
- **Emenda a**: [ADR 0009](0009-continuidade-por-email.md), cuja "fronteira explícita" exigia
  justamente esta ADR para ser movida

## Contexto

O editor pediu três coisas que, juntas, mudam a natureza do e-mail no livro:

1. o convite para guardar progresso está **discreto demais** e deve aparecer de verdade;
2. ele quer **guardar os e-mails** para avisar sobre livros futuros — *"desde que eles aceitem"*;
3. o leitor deve **ver o próprio progresso**, de forma simples.

O item 2 colide de frente com o que já foi prometido. Hoje, em três lugares do código que o
leitor lê, está escrito: *"Um e-mail, um link. Sem senha, sem cadastro, **sem informativo**"* — e
o e-mail que ele recebe diz *"você não receberá mais nada"*. A ADR 0009 registrou isso como
fronteira e determinou que movê-la exigiria nova ADR. É o que este documento faz.

O ponto delicado não é o pedido — é **quem já disse sim ao acordo antigo**. Essas pessoas
aceitaram uma coisa e receberiam outra. Nenhuma redação nova apaga isso.

## Decisão

**Dois consentimentos distintos, nunca embutidos um no outro.**

| | **Continuidade** | **Contato** |
|---|---|---|
| Para quê | e-mail como chave de progresso | avisar sobre livros novos |
| Quando | ao assinar (spec 080) | perguntado **depois**, à parte |
| Mensagens | só o link mágico | novidades, quando houver |
| Padrão | — | **desmarcado** |
| Sem ele | não há continuidade | continuidade segue inteira |

Consequências que decorrem disso, e que são a decisão de verdade:

1. **Ninguém é migrado.** Quem assinou sob "sem informativo" **não** entra na lista de contato por
   efeito desta ADR. É perguntado, uma vez, sem bloqueio, e o silêncio vale não.
2. **Consentimento é registro append-only, não flag.** Um booleano perde a história; a LGPD pede
   prova de *quando* a pessoa consentiu e *a que texto*. Cada "dei" e cada "revoguei" vira linha.
   O estado atual é a última linha por (e-mail, finalidade).
3. **Revogar contato não revoga continuidade.** São finalidades separadas; misturá-las puniria
   quem só não quer receber novidade.
4. **Toda mensagem de contato leva link de descadastro**, e o descadastro é um clique — sem
   login, sem formulário, sem "conte por que está saindo".
5. **A lista é exportável só com `ADMIN_TOKEN`**, e traz **apenas** quem tem contato ativo.

## Alternativas avaliadas

- **A — Um consentimento só, redação ampliada** ("guardar progresso e receber novidades"). Mais
  simples de construir e o que a maioria dos sites faz. Rejeitada: transforma um consentimento
  técnico em consentimento de marketing por tabela, e **força** quem só quer continuidade a
  aceitar contato. Consentimento forçado não é consentimento, e o livro ensina o contrário disso
  no cap. 07.
- **B — Caixa marcada por padrão.** Rejeitada pelo mesmo motivo, com o agravante de explorar a
  desatenção. O editor escreveu *"desde que eles aceitem"* — aceitar é ato, não é omissão.
- **C — Migrar os assinantes atuais e avisar depois.** Rejeitada: é exatamente quebrar a promessa
  que a ADR 0009 registrou. O custo de perguntar é baixo (a base é pequena); o custo de trair uma
  promessa escrita é o único ativo que um livro sobre evidência tem.
- **D — Dois consentimentos (escolhida).** Mais trabalho, e o número de e-mails na lista de
  contato será **menor** que o de assinantes. É a intenção: uma lista pequena de quem quis vale
  mais que uma lista grande de quem não percebeu.

## Consequências

- **Positivas**: o pedido do editor é atendido sem quebrar promessa; a base de contato nasce
  limpa e defensável; a arquitetura suporta finalidades futuras sem nova migração de schema.
- **Custos aceitos**: uma pergunta a mais no fluxo; lista menor; uma tabela nova.
- **Reversibilidade**: alta. Desligar contato é parar de perguntar e de exportar — a continuidade
  não depende dele.
- **Nova fronteira, que substitui a da ADR 0009**: o e-mail pode ser usado para **avisar sobre
  publicações do autor**, e nada além disso, apenas para quem consentiu nessa finalidade
  específica. Venda de lista, repasse a terceiro e mensagem de patrocinador continuam fora — e
  mudar *isto* exige, de novo, nova ADR.

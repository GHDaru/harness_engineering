# Feature Specification: o leitor vê seu progresso e pode aceitar ser avisado

**Feature Branch**: `093-progresso-e-contato`

**Created**: 2026-08-07

**Status**: **Aprovada pelo editor** — (1) substituir o Retomar, (2) gatilho no 1º capítulo, (3) base zerada · decisões
arquitetônicas na [ADR 0010](../../adr/0010-consentimento-em-camadas.md)

## O pedido

1. O convite para guardar progresso ficou **discreto demais** — deve aparecer e explicar.
2. O editor quer **guardar os e-mails** para avisar sobre livros futuros, *"desde que eles
   aceitem"*.
3. O leitor deve **ver o próprio progresso**, de forma simples.

## O diagnóstico de UX

O convite de hoje é uma linha de 12px no rodapé do painel do chat. Para vê-la, o leitor precisa
**abrir o chat** — coisa que a telemetria diz que quase ninguém faz: de 47 visitas, a maioria
parou na capa e no sumário.

Mas o problema real não é tamanho. É **momento**. O convite aparece antes de o progresso existir:
pede para guardar algo que ainda vale zero. Guardar duas páginas lidas não é oferta; guardar seis
capítulos é.

E há um vazio: **o leitor não vê o próprio progresso em lugar nenhum.** O cartão "Retomar" diz
onde ele parou, não quanto andou. Sem ver o que tem, ninguém quer guardar.

**A tese da proposta: mostrar o progresso É o convite.** O pedido 3 resolve o pedido 1.

## Proposta — três superfícies

### A. Cartão "Sua leitura" no sumário — *substitui o "Retomar"*

O cartão passa a mostrar o que o leitor conquistou, e só então oferece guardar:

```
┌──────────────────────────────────────────────────────────┐
│  SUA LEITURA                                              │
│  ████████░░░░░░░░░░░░░░  6 de 24 capítulos                │
│                                                            │
│  Você parou em: 05 — Design de Ferramentas   [Continuar →] │
│                                                            │
│  ⓘ Este progresso vive só neste navegador.                │
│    ✉ Guardar com um e-mail  ·  o que é isso?              │
└──────────────────────────────────────────────────────────┘
```

Conectado, a última linha vira: `✉ Sincronizado — seu@email · sair`.

Sem nenhum capítulo lido, o cartão **não aparece** (é o comportamento de hoje): não há progresso
para mostrar nem para guardar.

### B. Fim de capítulo — o momento de valor

Ao terminar um capítulo, **abaixo** dos botões anterior/próximo, um bloco discreto no fluxo do
texto — não flutuante, não modal:

```
  ✓ Capítulo 05 concluído · 6 de 24
    Seu progresso está só neste navegador. Guardar leva 10 segundos: [ e-mail ] [ enviar ]
```

Aparece a partir do **1º capítulo concluído** e some depois de conectado. Some também se
dispensado — e "dispensado" fica registrado, não volta a insistir. **Nunca cobre o texto.**

> **Por que no 1º e não no 3º, como eu propus primeiro.** O editor perguntou "por que não antes?"
> e a resposta estava na telemetria que este mesmo Radar já tinha lido: capa **17**, sumário **9**,
> introdução **7**, capítulo 01 — **3**. Um convite no 3º capítulo seria visto por ninguém. E quem
> lê um capítulo e some é **exatamente** quem perde o progresso: esperar o hábito se formar é
> oferecer o cinto depois da viagem. A regra genérica de produto ("não peça antes de entregar
> valor") perdeu para o dado do próprio livro.
>
> O tom se adapta em vez do gatilho: no primeiro capítulo é *"não perca o fio"*; do terceiro em
> diante é *"você já andou 6 de 24"*.

### C. Painel do companion — mantém, com o mesmo texto

Coerência de vocabulário com A e B. Sem mudança de comportamento.

## O segundo consentimento (ADR 0010)

Perguntado **depois** de o leitor entrar pelo link mágico, na página de sucesso e no painel —
nunca no ato de assinar, para não contaminar um consentimento com o outro:

```
  Quer que eu avise quando sair um livro novo?
  [ ] Sim, pode me avisar          ← desmarcado
  Você cancela em qualquer e-mail, num clique.
```

**Ninguém já assinante é migrado.** Quem assinou sob "sem informativo" é perguntado uma vez, sem
bloqueio; silêncio vale não.

**Decisão do editor: a base é zerada antes de valer o acordo novo.** Como não há leitores além
dele, a migração deixa de existir como problema — e o precedente fica registrado para quando a
base não for mais vazia. O reset usa o `/apagar` que a spec 080 já entregou; nenhum endpoint
destrutivo novo é criado para isso.

## Requisitos

### R1 — Progresso visível
- `GET /progresso/detalhe?session_id=` devolve os **slugs de capítulo distintos** visitados,
  derivados de `nav_events` (já existe, já segue o leitor na fusão) filtrados pela lista de
  capítulos do sumário. **Sem tabela nova.**
- Anônimo funciona: o cálculo cai para o `localStorage`, sem backend.

### R2 — Consentimento em camadas
- Tabela `consentimentos(email, finalidade, versao, aceito, created_at)` — **append-only**.
- `POST /consentimento` e `GET /consentimento?session_id=`.
- Revogar contato **não** toca continuidade.

### R3 — Exportação para o editor
- `GET /leitores?token=<ADMIN_TOKEN>` → só quem tem contato **ativo**, com a data e a versão do
  texto aceito. Nunca público.
- ⚠️ **`ADMIN_TOKEN` não existe hoje no ambiente** (confirmado na lista de variáveis do Railway).
  A rota nasce **desligada**, como `/suggestions` e a telemetria de administração — comportamento
  seguro por default. O editor define a variável quando for usar a lista.

### R4 — Descadastro de um clique
- Página `sair.html?e=<hash>` — link presente em toda mensagem de contato futura. Sem login.

## Não faz parte

- Envio de novidade em si (não há livro novo hoje) — a spec entrega a **base consentida**.
- Conta com senha, área restrita, perfil.
- Ranking, gamificação, medalhas.

## Aceite

- [ ] Cartão "Sua leitura" com barra e contagem, PT e EN
- [ ] Bloco de fim de capítulo a partir do 1º, dispensável e com dispensa lembrada
- [ ] Nenhuma superfície bloqueia leitura
- [ ] Consentimento de contato desmarcado por padrão e separado do de continuidade
- [ ] Revogação de contato preserva continuidade
- [ ] Assinantes atuais **não** migrados
- [ ] `GET /leitores` só com token e só contato ativo
- [ ] Testes verdes; build 4 passos; verificação em navegador nos dois idiomas

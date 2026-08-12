# Spec 100 — Lote B da cascata: 08 Memória e 04 Compactação

> Branch: `100-lote-b` · 2026-08-12 · decisão: [ADR 0011](../../adr/0011-cascata-didatica.md)

## 1. O lote encolheu de três para dois, e o motivo está registrado

O ADR 0011 previu o Lote B como **08, 04, 06**. Ele foi entregue com **08 e 04**, e o **06 MCP desce para o Lote C**.

O motivo é de orçamento de contexto da execução, não editorial: a série é longa e cada capítulo custa reescrita PT, tradução EN integral, selo e medição. Fechar o lote com dois capítulos **completos e verdes** vale mais que três pela metade — e a estrutura em lotes do ADR existe exatamente para que a fronteira possa se mover sem deixar o repositório num estado intermediário.

A dependência que o ADR declarou inviolável foi respeitada: **08 antes de 04**, porque a compactação age na *visão* e nunca no *registro*, e o registro nasce no 08.

## 2. Os dois capítulos

**08 Memória e Estado** — cena: quarenta minutos de trabalho, o terminal fecha, `--resume` traz a conversa inteira de volta e o `git status` mostra três arquivos modificados no meio da edição. **A conversa foi restaurada; o workspace não.** Duas coisas precisavam sobreviver ao mesmo acidente e só uma sobreviveu, que é a separação do capítulo.

Exemplo trabalhado: a `StorePort` de três métodos, com o contraste entre o adapter em memória e o SQLite (`commit()` por mensagem: durabilidade acima de vazão), e **depois** a segunda trilha, o checkpoint de workspace via `git stash create` + `update-ref` sob `refs/harness/`. Duas trilhas, dois stores, um índice em comum.

**04 Compactação** — cena: turno 40, a janela lota, o harness resume, e no turno 41 o agente **desfaz o próprio conserto**, porque o resumo dizia *"editei auth.py"* e não dizia como o arquivo ficou.

Exemplo trabalhado: a escada em código, com `truncar → podar → sumarizar` e a razão da ordem sendo **destrutividade**, não custo; o `arquivar()` que transforma truncamento em paginação; e o `estado_dos_arquivos` como campo **obrigatório** do resumo, que é literalmente o que faltou no turno 40.

## 3. O que o portão pegou, de novo

**Quarto falso positivo da família**, agora no portão de evidência: ele acusou o cap. 08 de perder dois "caminhos de arquivo" que eram `/memories` e `/memory` — **comandos de barra**, não caminhos. A heurística passou a exigir extensão ou barra final. E o texto ganhou de volta a especificidade que eu havia diluído ao reescrever, porque a acusação, embora mal fundamentada, apontava para uma perda real de precisão.

**E ele pegou duas perdas verdadeiras** no cap. 04: `harness-zero/` e `skills/compact/` haviam sumido na reescrita. Restaurados. É a primeira vez que esse portão paga o próprio custo.

## 4. Medição

**18 capítulos v4** (9 PT + 9 EN) dentro dos limites, com travessões entre 0,0 e 7,2 por mil, frase média entre 13,7 e 18,5, e nenhuma frase acima de 60 palavras.

## 5. Fila revista

Lote C (spec 101): **06 MCP**, **09 Planejamento**, **10 Subagentes**, **11 Verificação**.
Lote D (spec 102): **12 Extensibilidade**, **16 Auto-evolutivo**, **13 Interfaces**, **15 Embutido**, **14 Convergências** — com o 14 por último, sem exceção.

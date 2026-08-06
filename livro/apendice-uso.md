# Apêndice — Uso do livro (vivo)

> **Estado da arte capturado em 2026-07** · última revisão 2026-07-29 · [histórico e registro de expiração](HISTORICO.md)

Um livro que ensina **verificação** (cap. 11) e **observabilidade das interfaces** (cap. 13) deveria conseguir responder sobre si mesmo: *como este livro é usado?* Esta página responde — ao vivo.

## O que é medido (e o que não é)

Desde a edição 0.49, o site registra **navegação agregada**: qual página foi visitada, quantas vezes, por sessões **anônimas** — e somente depois que o leitor **aceita o aviso de telemetria** (o banner na primeira visita). Nada além disso:

- **Não** coletamos IP, user-agent, nome, email ou qualquer dado pessoal;
- a sessão é um identificador aleatório gerado pelo navegador, apagável pelo próprio leitor (o comando `/limpar` do companion remove tudo da sessão — direito ao esquecimento);
- o painel abaixo consome uma projeção **estritamente agregada** (`total` e contagens por página) — não existe endpoint público com dados individuais.

## O painel vivo

<div data-viz="uso-livro"></div>

*(Os números acima existem apenas na versão online — no PDF esta ilha é omitida por definição.)*

## Para que serve

Este painel é o mesmo insumo que orienta a **cadência do livro vivo** ([ADR 0007](adr-0007-cadencia-livro-vivo.html)): capítulos com mais atenção dos leitores têm prioridade na janela trimestral de revisão, e páginas ignoradas levantam a pergunta editorial certa — falta divulgação, ou falta reescrita?

É também uma demonstração em miniatura do que o livro prega: **instrumentar é a metade barata da verificação** — a metade cara é decidir o que fazer com o número. O registro de decisões fica, como sempre, no [Histórico](HISTORICO.md).

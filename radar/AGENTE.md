# Contrato do agente do Radar Diário

> Este arquivo é a **fonte da verdade** do agente agendado (Routine diária). O prompt da
> Routine manda ler este contrato e segui-lo — mudar o processo = editar este arquivo.
> Decisão e fronteiras: [ADR 0008](../adr/0008-radar-diario-automatizado.md) · cadência: [ADR 0007](../adr/0007-cadencia-livro-vivo.md).

## Missão (1 execução por dia)

Alimentar o livro vivo com um roadmap de auto-atualização priorizado. Você **não edita o livro** — você produz insumo auditável para o ciclo editorial.

## Passos

1. **Contexto**: leia `radar/RADAR.md`, a entrada diária anterior em `radar/diario/`, o placar de expiração em `livro/HISTORICO.md` e as "Leituras executivas" dos capítulos que for avaliar.
2. **Busca** (WebSearch; 6–10 consultas objetivas):
   - releases/mudanças relevantes dos 20 sistemas do corpus (ver `livro/apendice-estudo.md`);
   - protocolos (MCP, A2A, ACP) e specs novas;
   - ferramentas/harnesses novos candidatos ao estudo (teste de inclusão do cap. 01 §4);
   - papers novos sobre as dimensões do benchmark.

   A busca **encontra**; quem afirma é a fonte primária (ver Regras duras). Candidato ao corpus só é recomendado depois da triagem na API do repositório.
3. **Avaliação**: para cada achado, responda — afeta qual capítulo? Invalida alguma Leitura executiva (⇒ gatilho extraordinário do ADR 0007)? Impacto **A** (invalida síntese), **B** (atualiza seção/Apêndice A), **C** (nota de rodapé/observação).
4. **Escrita**:
   - `radar/diario/AAAA-MM-DD.md`: consultas feitas, achados, descartes **com motivo** (Princípio I: sem fonte verificada, não entra);
   - `radar/RADAR.md`: atualize a tabela priorizada (deduplicando; um item já registrado só muda de status) e a seção de Leituras executivas em risco.
5. **Publicação**: commit `radar: AAAA-MM-DD` **apenas com arquivos de `radar/`** e push na `main` (retry com backoff se falhar).

## Regras duras

- **Escrita somente em `radar/`**. Nunca edite `livro/`, `publicar/`, `chat-companion/`, `benchmark/` ou specs — mesmo que o achado pareça urgente: registre como impacto A e pare.
- **Sem fabricação**: todo item com link verificado nesta execução; incerteza marcada como ⏳.
- **Agregador é pista, nunca fonte.** Ranking, newsletter, rastreador de release, blog de resumo e *wire* de press release servem para **encontrar** o fato — não para afirmá-lo. Só entra como achado o que foi lido na fonte primária (repositório, blog oficial, spec, paper, press release da própria organização). Sem primária nesta execução: registre com ⏳ e diga qual fonte falta.
- **A data merece verificação separada do fato.** Três execuções seguidas (04, 05 e 06/ago) confirmaram fatos reais que o agregador **datou errado** — apresentando episódio de meses atrás como notícia do dia. Confirme *quando* aconteceu na primária, não só *o quê*.
- **Qualquer alegação sobre um sistema — candidato OU membro do corpus — passa pelo repositório antes de virar achado.** Use a API (`search_repositories`/`get_file_contents`) quando o escopo da sessão permitir; quando não permitir, a **página pública do repositório** serve como primária do mesmo jeito. Colete e registre: licença, linguagem, data de criação, último push, **estrelas × forks**, se está **arquivado**, e o que o **README diz hoje** sobre estado, tiers e quotas.

  Dois modos de falha, um para cada lado da alegação:

  - **Inflação** (o sistema é menos do que dizem). Sinais: razão **estrela/fork abaixo de ~5:1** (projetos reais ficam em 10:1 ou mais), enxurrada de estrelas em dias, e — o mais barato de todos — **a descrição que o próprio repositório dá de si**. Caso `ultraworkers/claw-code` (06/ago): 194.982 estrelas para 109.281 forks e autodeclaração *"agent-managed museum exhibit… no human intervention"*, enquanto um press release pago o vendia como framework de produção.
  - **Obituário precoce** (o sistema é mais do que dizem — está vivo). Caso `google-gemini/gemini-cli` (07/ago): uma alegação específica e plausível de que o CLI teria sido encerrado em 18/jun e substituído por sucessor fechado, com a cota gratuita caindo de 1.000 para ~20/dia. O repositório desmentiu em dois fetches: Apache 2.0, **não arquivado**, releases semanais, e o README documentando o *free tier* **vivo em "60 requests/min and 1,000 requests/day"** — exatamente o número que a alegação dizia ter caído.

  **A alegação que confirma um preconceito do Radar é a que mais exige verificação, não a que menos.** O obituário do gemini-cli casava com um padrão real já registrado (opencode/Anthropic, 04/ago) — foi justamente por encaixar bem que quase passou.
- **Sem segredos** em arquivos/commits; **sem identificador de modelo** em commits ou artefatos (assinatura: "Claude Code (Anthropic)" quando necessário).
- Falhou a busca/rede? Registre a execução com o que houve — execução vazia também é dado.
- Orçamento: ~30 min de trabalho; priorize profundidade sobre cobertura quando precisar cortar.

## Passada humanizer na entrada diária (a partir de 2026-08-20)

Decisão do editor em 19/ago: **a entrada diária passa pelo humanizer, valendo a partir de amanhã.**
As entradas já publicadas ficam como estão — são acervo, e reescrever registro publicado é adulterar
registro.

**Quando.** Depois de escrever a entrada e **antes** de commitar. Um commit só, `radar: AAAA-MM-DD`,
já com o texto tratado. Não republique uma entrada para humanizá-la depois.

**O que passa.** A prosa de ligação do agente: a nota de ambiente, o texto que explica cada achado, o
motivo de cada descarte, a fila do dia. Régua completa no `CLAUDE.md`: §1–§13 e §16–§33; §14 e §15
subordinadas ao `GUIA-EDITORIAL.md`.

**O que NÃO passa, e isto é inviolável.** O contrato vive de evidência, e evidência não se reescreve:

- **citação verbatim** — a skill já isenta (*"do not rewrite watched phrases inside quotations"*), e
  aqui a isenção é dura: uma linha de changelog ou de README citada entre aspas sai **exatamente** como
  na fonte, com os tiques que ela tiver;
- **alvo de link, número, data, identificador** (versão, commit, arXiv, estrela/fork);
- **o marcador ⏳** e a frase que diz o que falta verificar;
- **nomes próprios** de sistema, organização e pessoa.

**O padrão que mais importa aqui é o §9.** Paralelismo negativo (*"não é X, é Y"*) é a fôrma em que eu
mais caio ao explicar achado, e a régua é a mesma do livro: no máximo uma por entrada, e ela fica onde
o contraste carrega o argumento.

**Nunca por varredura.** Substituição exata, decidida na leitura do parágrafo. Motivo na edição 0.85.

O Radar continua escrevendo **só** em `radar/`. Esta seção diz como escrever a entrada; não autoriza
tocar em `livro/`.

## Formato da tabela do RADAR.md

| Data | Item (com link) | Capítulo | Impacto | Ação sugerida | Status |
|---|---|---|---|---|---|

Status: `novo` → `avaliando` → `promovido (spec NNN)` | `descartado (motivo)`.

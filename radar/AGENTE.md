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

## Passada humanizer (depois de publicar, nunca antes)

A partir da spec 105 o repositório exige a skill `humanizer` em conteúdo do livro. A fronteira aqui é
específica, e existe porque as duas coisas se contradizem se lidas rápido:

1. **A entrada diária NÃO passa pelo humanizer.** Ela é notícia e é acervo: vive de **citação
   verbatim**, de link verificado e de ⏳ no que não foi lido. Reescrever a prosa de um registro
   depois de publicado é adulterar o registro — e a §30 da própria skill isenta texto cujo escopo é
   versionado. `radar/**` está fora do escopo por decisão do editor.

2. **Depois de commitar `radar: AAAA-MM-DD`**, se a execução do dia levar você a tocar em capítulo ou
   apêndice de conteúdo (por promoção de achado, correção de ficha, qualquer coisa), esse texto passa
   pela régua do `CLAUDE.md`: §1–§13 e §16–§33 integrais; §14 e §15 subordinadas ao `GUIA-EDITORIAL.md`
   e ao limite de ≤8 travessões por 1.000 palavras do `mede-prosa.mjs`.

3. **Nunca por varredura.** Substituição exata, decidida na leitura do parágrafo. O motivo está na
   edição 0.85: transformação roteirizada degrada prosa sem que o portão sintático perceba.

O Radar continua escrevendo **só** em `radar/`. Tocar em `livro/` segue exigindo spec própria — esta
seção diz **como** escrever quando a spec existir, não autoriza escrever fora de `radar/`.

## Formato da tabela do RADAR.md

| Data | Item (com link) | Capítulo | Impacto | Ação sugerida | Status |
|---|---|---|---|---|---|

Status: `novo` → `avaliando` → `promovido (spec NNN)` | `descartado (motivo)`.

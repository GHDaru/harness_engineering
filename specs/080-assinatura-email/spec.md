# Feature Specification: subscrição por e-mail como chave de progresso (link mágico)

**Feature Branch**: `080-assinatura-email`

**Created**: 2026-08-06

**Status**: Aprovada pelo editor — *"a) link mágico, b) aprovado, convite discreto e sem bloquear, c) progresso sincronizado + histórico de chat. sem aviso."*

## Problema

Hoje o leitor é **anônimo por navegador**: `cmp_sid` (sessão do companion) e `hz_ultimo`
(último capítulo lido) vivem só no `localStorage`. Consequência prática: quem lê no notebook e
retoma no celular **perde tudo** — progresso, objetivo declarado e a conversa inteira com o
tutor. Não há nenhuma chave que ligue os dois navegadores.

Limpar o navegador tem o mesmo efeito. O livro é vivo e longo (24 capítulos + apêndices); a
leitura acontece em sessões separadas por dias. Perder o fio é o modo de falha mais provável.

## Solução

Um **e-mail** vira a chave de continuidade — nada de senha, nada de cadastro. O leitor informa o
e-mail, recebe um **link mágico** de uso único, e ao clicar o navegador **adota a sessão
canônica** daquele leitor. Como histórico de chat, objetivo e consentimento já são indexados por
`session_id` no backend, eles passam a seguir o leitor **de graça**; só o progresso de leitura
precisa deixar o `localStorage` e ganhar persistência.

**Não é login.** Não há senha, não há sessão autenticada, não há área restrita. É uma chave de
continuidade — o mesmo modelo do "link de retomada" de um formulário longo.

### Regras inegociáveis do pedido do editor

1. **Não bloqueia.** A navegação anônima continua completa: todo o livro, o companion, o tour, os
   downloads. Sem e-mail nada é negado; só a continuidade entre dispositivos fica de fora.
2. **Convite discreto.** Uma linha, dispensável, no fim do painel do companion e no cartão
   "Retomar" da capa. Nunca um modal, nunca um *interstitial*, nunca no meio da leitura.
3. **Sem aviso.** Nenhum informativo, nenhuma newsletter, nenhuma mensagem de produto. O e-mail
   serve para **um** propósito: entregar o link mágico. Isso é declarado no próprio convite e é
   uma restrição de implementação, não uma promessa de marketing.

## Requisitos

### R1 — Subscrição (`POST /assinar`)

- Aceita `{email, session_id?, lang?}`. Normaliza o e-mail (trim + minúsculas), valida formato e
  tamanho (≤ 254).
- Cria o leitor se não existir, com um `session_id` **canônico gerado no servidor** com entropia
  criptográfica (`secrets.token_urlsafe(24)`) — nunca derivado do e-mail.
- Emite um token de uso único, **guardado só como hash SHA-256**, com validade de 30 minutos.
- Envia o link `<SITE>/entrar.html?t=<token>` (ou `/en/entrar.html` conforme `lang`) por SMTP.
- **Resposta idêntica** para e-mail novo e e-mail já cadastrado (sem enumeração de contas).
- Rate-limit por e-mail e por IP.
- Sem SMTP configurado: responde `{ok:true, enviado:false}` e o widget diz a verdade ao leitor —
  o link **nunca** aparece na resposta HTTP.

### R2 — Entrada (`POST /entrar`)

- Aceita `{token, session_id?}`. Procura pelo **hash** do token; recusa token expirado,
  inexistente ou já usado. No Postgres, a marca de uso e a validação vão na **mesma sentença**
  (`UPDATE … WHERE usado_em IS NULL AND expira_em >= now() RETURNING email`), para que dois
  cliques simultâneos no mesmo link não passem os dois.
- Devolve `{ok, email, session_id}` — o `session_id` canônico do leitor.
- Se veio um `session_id` anônimo diferente, **funde** a sessão anônima na canônica (mensagens,
  objetivo, consentimento, navegação e progresso) e apaga a anônima. Fundir, não descartar: o
  leitor que conversou antes de assinar não perde a conversa.

### R3 — Progresso sincronizado (`GET`/`POST /progresso`)

- `POST {session_id, lang, slug, titulo}` — upsert do último capítulo lido, **um por idioma**.
- `GET ?session_id=` — devolve os itens para o cartão "Retomar".
- O `localStorage` continua sendo a fonte imediata (funciona offline e sem backend); o servidor é
  o espelho que atravessa dispositivos. Na entrada, o remoto vence se for mais recente.

### R4 — Identidade e saída

- `GET /leitor?session_id=` → `{email}` ou `{email:null}`.
- `DELETE /leitor` → apaga leitor, sessão, mensagens, progresso e links pendentes (LGPD,
  Princípio V). O botão fica ao lado do "conectado como…".
- "Sair" no navegador apenas volta a uma sessão anônima nova; não apaga nada no servidor.

### R5 — Superfície (PT e EN)

- Página `entrar.html` gerada nos **dois** idiomas: consome o `?t=`, chama `/entrar`, adota o
  `session_id`, sincroniza o progresso e manda o leitor de volta ao ponto em que parou.
- Convite discreto no painel do companion e no cartão "Retomar" da capa.
- Estado conectado visível no painel: `✉ conectado como leitor@exemplo.com · sair · apagar`.
- Comandos do chat: `/assinar <email>`, `/sair`, `/apagar`.

## Não faz parte desta spec

- Newsletter, informativo, e-mail transacional de qualquer outra natureza.
- Área restrita, conteúdo pago, qualquer gate sobre o livro.
- Sincronizar preferências de navegador (tema, dock, modo, chave BYOK) — são do dispositivo.
- Verificação de identidade além da posse do e-mail.

## Riscos e como são tratados

| Risco | Tratamento |
|---|---|
| Token vazado no histórico do navegador / referer | Uso único + TTL 30 min; `entrar.html` limpa o `?t=` da URL com `history.replaceState` logo após o POST |
| Token legível no banco | Guardado só como hash SHA-256 |
| Enumeração de leitores | Resposta idêntica para e-mail conhecido e desconhecido |
| Abuso do envio (spam via formulário) | Rate-limit por e-mail e por IP |
| `session_id` como credencial de fato | Já era verdade antes desta spec; agora ele é gerado com entropia criptográfica no servidor, e não mais por `crypto.randomUUID()` do navegador |
| SMTP indisponível | A subscrição falha **visivelmente**, sem meio-caminho e sem expor o link |

## Aceite

- [x] `POST /assinar` → link enviado; token de uso único expira em 30 min *(envio real depende do SMTP no Railway; o caminho é coberto por teste com o envio substituído)*
- [x] Segundo uso do mesmo token é recusado
- [x] `POST /entrar` funde a sessão anônima: as mensagens de antes da assinatura continuam lá
- [x] Progresso gravado no navegador A aparece no navegador B após o link mágico
- [x] Navegação anônima intacta: nenhuma página, download ou função exige e-mail
- [x] Convite não bloqueia e é dispensável
- [x] `DELETE /leitor` remove tudo *(verificado contra o `MemoryStore`; o `PostgresStore` apaga por `ON DELETE CASCADE` das `sessions`)*
- [x] Testes do backend verdes; build 4 passos verde; verificação em navegador nos dois idiomas
- [x] Nenhum segredo em arquivo, commit ou log; nenhum link novo para o repositório
- [x] Checklist `.specify/memory/checklist-verificacao.md` percorrido

## Dependência externa (ação do editor)

O envio depende de `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS` no Railway — o mesmo
procedimento de `chat-companion/backend/EMAIL.md`. **Enquanto não estiverem configuradas**, o
código sobe e todo o resto funciona; o convite exibe a mensagem honesta de que o envio está
desativado. Nenhuma credencial entra no repositório.

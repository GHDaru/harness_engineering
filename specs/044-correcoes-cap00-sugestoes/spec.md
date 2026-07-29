# Spec 044: Correções — cap. 00 (contagem de arquétipos) + sugestão sob demanda + email via Gmail

## Contexto

Três correções apontadas pelo editor (2026-07-29):
1. O cap. 00 diz "**três** arquétipos" mas apresenta **quatro** grupos (código, agentes pessoais self-hosted, embutidos, frameworks).
2. O botão 💡 "enviar sugestão ao autor" fica **sempre visível** no cabeçalho do companion; deveria aparecer **só quando o leitor solicitar**.
3. O autor quer usar a **conta Gmail** dele para **receber e enviar** os emails de sugestão.

## Requisitos

- FR-001 (cap. 00): a contagem bate com a lista — "quatro arquétipos". O cap. 01 §5 ("três arquétipos" com 3 itens) é outra taxonomia, consistente internamente: **não muda**.
- FR-002 (companion): o formulário de sugestão **não é visível por default** e **não há botão permanente** no cabeçalho. Ele abre quando o leitor solicita no próprio chat:
  - comando explícito `/sugerir` (ou `/sugestao`); **ou**
  - intenção clara na mensagem (contém "sugest…" junto de "autor"/"enviar"/"mandar").
  A solicitação é interceptada no widget (não vai ao LLM); o formulário abre com uma mensagem de sistema explicando. A mensagem de boas-vindas menciona o comando (descobribilidade).
- FR-003 (email): o backend já envia por SMTP (best-effort, sugestão sempre persistida). Documentar a configuração **Gmail** (senha de app + variáveis no Railway); `From` = `SMTP_USER` (a conta Gmail), `To` = `SUGGESTION_EMAIL_TO` (default já é a conta do autor). **Nenhuma credencial no repositório, no chat ou em commit** — só em variáveis de ambiente do Railway.
- FR-004: build + link-check + portão por capítulo verdes; corpus do companion regenerado (cap. 00 mudou).

## Fora de escopo

- Trocar o provedor de email ou adicionar fila/retry; validar o SMTP em CI (depende de segredo).

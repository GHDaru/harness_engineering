# Feature Specification: a área do editor

**Feature Branch**: `096-area-do-editor`

**Created**: 2026-08-11

**Status**: **Aprovada pelo editor** — *"Pode construir a área do editor"*

## O pedido, e a pergunta que o motivou

O editor ia definir o `ADMIN_TOKEN` e parou numa pergunta melhor que a resposta que existia:

> *"como ele sabe que sou eu, como consigo acessar? Não tem interface? não daria para colocar na
> variável o meu email como admin, assim isto destrava?"*

As três perguntas expõem o mesmo defeito. O `ADMIN_TOKEN` **não autentica ninguém**: é senha
compartilhada que viaja na **barra de endereço**, e URL vaza por histórico, `Referer`, sincronização
de navegador e captura de tela. E não há interface — mesmo com o token, o editor montaria URLs à
mão para ler JSON cru.

A intuição do editor acerta o ponto de arquitetura: **o livro já tem como provar quem ele é**. A
spec 080 entregou o link mágico, que prova posse da caixa de e-mail. Inventar um segundo mecanismo
de autenticação, pior que o primeiro, é o que estava em vigor.

## Decisão

**É editor quem provou o e-mail E sabe a senha.** Dois fatores, cada um cobrindo a fraqueza do
outro:

| Fator | O que prova | Onde já existia |
|---|---|---|
| e-mail em `ADMIN_EMAILS` | posse da caixa (link mágico, uso único, 30 min) | spec 080 |
| `ADMIN_SENHA` | intenção, no momento da ação | novo |

**Por que a senha e não só o e-mail.** O `session_id` é credencial ao portador: quem copiar o
`cmp_sid` de um navegador esquecido *é* o leitor. Para ler progresso isso é aceitável; para
exportar a lista de contato o raio de alcance é outro (cap. 07). A senha re-prova **intenção no
momento**, e vale por 30 minutos — o mesmo prazo do link mágico, por simetria e porque um prazo a
mais para lembrar é um prazo a mais para errar.

> Eu havia proposto uma coleira diferente — exigir entrada recente pelo link mágico, com coluna
> nova em `readers`. A senha cobre o mesmo risco **sem mudar o schema** e sem depender de o editor
> lembrar de reentrar. Proposta trocada pela do editor, que era melhor.

## Requisitos

### R1 — Configuração, e as três portas
```
ADMIN_EMAILS=ghdaru@gmail.com      # quem pode ser editor (lista, separada por vírgula)
ADMIN_SENHA=<senha longa>          # o segundo fator do painel
ADMIN_TOKEN=<token>                # a porta de script, que já existia
```
Todas **vazias por padrão**. Sem `ADMIN_EMAILS` **ou** sem `ADMIN_SENHA`, o painel do editor não
existe — exigir as duas é o default seguro. O `ADMIN_TOKEN` continua valendo sozinho, para `curl` e
automação.

### R2 — Destrancar
- `POST /admin/entrar {session_id, senha}` — só destranca se o e-mail da sessão estiver em
  `ADMIN_EMAILS` **e** a senha conferir. Comparação em **tempo constante**.
- Sessão destrancada vive **em memória**, com prazo de 30 min. Reiniciou o serviço, destranca de
  novo — persistir concessão de privilégio é dívida que ninguém revisa.
- Rate limit próprio, mais apertado que o do chat.
- **Resposta idêntica** para e-mail fora da lista e senha errada. Dizer qual dos dois falhou é
  entregar metade da porta.

### R3 — As rotas passam a aceitar as duas portas
`/leitores`, `/suggestions` e `/telemetry` aceitam **ou** `token=` (script) **ou** um `session_id`
destrancado. O comportamento sem nenhum dos dois não muda: **403**.

### R4 — A área no painel
Comando `/editor` no companion, como `/assinar` e `/apagar` já são. Pede a senha, e ao destrancar
mostra:
- **sugestões dos leitores** — e há razão para suspeitar de acúmulo: a spec 087 registrou que elas
  *"nunca chegaram ao autor"* pelo bloqueio de SMTP, e que *"a sugestão sempre esteve salva no
  banco"*;
- **lista de contato** (spec 093) com contagem e exportação;
- **telemetria** de administração.

A área **não se insinua** para quem não é editor: sem destrancar, `/editor` responde igual a
qualquer comando desconhecido.

### R5 — `/health` diz o estado, nunca o valor
```json
"admin": { "token": true, "emails": 1, "senha": true }
```
Booleanos e contagem. É o remédio das specs 085/086 aplicado à última variável que não o tinha:
hoje não dá para distinguir "desligada" de "protegida" — as duas respondem `403 token inválido` — e
o editor não tem como conferir se a variável chegou ao serviço certo. Foi exatamente esse buraco
que custou duas rodadas de palpite no SMTP.

## Não faz parte

- Login com senha para leitores. Isto é **só** para a lista de `ADMIN_EMAILS`; a leitura anônima
  segue completa e sem cadastro, e a ADR 0009 não é tocada.
- Recuperação de senha. Esqueceu, troca a variável no Railway.
- Ação destrutiva pelo painel do editor. Ler e exportar, não apagar.

## Aceite

- [ ] Sem as variáveis, tudo se comporta como hoje (403), e nenhum teste existente muda
- [ ] `/admin/entrar` destranca só com e-mail da lista **e** senha certa, em tempo constante
- [ ] E-mail fora da lista e senha errada devolvem a **mesma** resposta
- [ ] Sessão destrancada expira em 30 min; rate limit próprio
- [ ] `/leitores`, `/suggestions` e `/telemetry` aceitam token **ou** sessão destrancada
- [ ] `/editor` no painel, invisível para quem não é editor, PT e EN
- [ ] `/health` com `admin` em estado, nunca valor
- [ ] Testes cobrindo: sem variável, senha errada, e-mail errado, expiração, e as duas portas

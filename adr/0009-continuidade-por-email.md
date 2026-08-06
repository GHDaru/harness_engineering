# ADR 0009 — Continuidade de leitura por e-mail (link mágico), sem login

- **Status**: aceita (2026-08-06)
- **Feature**: `080-assinatura-email`

## Contexto

O leitor era anônimo **por navegador**: `cmp_sid` (sessão do companion) e `hz_ultimo` (último
capítulo lido) viviam só no `localStorage`. Quem lia no notebook e retomava no celular perdia
progresso, objetivo declarado e a conversa inteira com o tutor. Num livro de 24 capítulos lido em
sessões separadas por dias, perder o fio é o modo de falha mais provável — e limpar o navegador
tem o mesmo efeito.

As forças em tensão: (1) o Princípio VI exige **acesso a custo zero e sem atrito**; (2) o
Princípio V proíbe guardar mais dado pessoal do que o necessário; (3) o editor foi explícito —
*"convite discreto e sem bloquear"*, *"sem aviso"* (nenhum informativo, nenhuma newsletter).

## Alternativas avaliadas

- **A — Login com senha (conta tradicional)**: resolve a continuidade, mas cria hash de senha,
  recuperação de senha, e sobretudo um **muro** na entrada de um livro aberto. Contra o
  Princípio VI e contra o pedido explícito do editor.
- **B — Só `localStorage` + exportar/importar um arquivo de progresso**: zero dado pessoal, mas
  transfere ao leitor um trabalho manual que ninguém faz. Não resolve o caso real.
- **C — OAuth (Google/GitHub)**: sem senha nossa, porém acopla o livro a um provedor, coleta mais
  dado do que precisamos e exige que o leitor tenha (e queira usar) aquela conta.
- **D — E-mail + link mágico de uso único (escolhida)**: um campo, um clique, nenhuma senha. O
  e-mail guardado é o **único** dado pessoal, e serve a um propósito só: entregar o link.

## Decisão

**D.** O e-mail é uma **chave de continuidade, não um login**: não há senha, não há sessão
autenticada, não há área restrita, e nada no livro é negado a quem não informa e-mail. O e-mail
aponta para um `session_id` canônico; abrir o link mágico faz o navegador **adotar** esse id — e,
como histórico, objetivo e consentimento já eram indexados por `session_id`, eles passam a
atravessar dispositivos sem código novo. Só o progresso de leitura ganhou tabela.

Corolário de segurança assumido junto: a sessão canônica passa a ser gerada **no servidor** com
entropia criptográfica. O `session_id` sempre foi, de fato, uma credencial — quem o tem lê o
histórico. Deixá-lo a cargo do `crypto.randomUUID()` do navegador era aceitável enquanto ele não
estava ligado a um e-mail; deixou de ser.

## Consequências

- **Positivas**: continuidade real entre aparelhos; um único dado pessoal, com finalidade única e
  declarada; `DELETE /leitor` apaga tudo (Princípio V); a navegação anônima permanece **completa**.
- **Custos aceitos**: passamos a guardar e-mails, o que antes não fazíamos — daí o mínimo de dado,
  o token só como hash SHA-256, a resposta idêntica para e-mail conhecido e desconhecido (sem
  enumeração) e o rate-limit por e-mail e por IP. Aceita-se também a dependência de SMTP: sem ele
  a assinatura **falha visivelmente**, em vez de fingir que enviou.
- **Reversibilidade**: alta. Remover a feature é apagar três tabelas e o convite; a leitura
  anônima é o caminho padrão e continua funcionando sozinha, inclusive com o backend fora do ar.
- **Fronteira explícita**: o e-mail **nunca** será usado para informativo, novidade ou qualquer
  outra mensagem. Mudar isso exige nova ADR — não é decisão de implementação.

# Pesquisa: post × código do external-sandbox

Lido em 17/11/2026.

- Post: <https://blog.primeradiant.com/external-sandboxes-for-coding-agents/> (Simon Willison, Prime Radiant, 16 Nov 2026).
- Repositório do protocolo: `prime-radiant-inc/external-sandbox`, commit `0681c98a08b2bbdbd9f59fa5bef21c38caccbccf` (16/nov/2026). Arquivos: `PROTOCOL.md`, `README.md`, `COVERAGE.md`, `claude-code/README.md`, `claude-code/claude-shell-prefix.sh`, `codex/README.md`.
- Extensão do Pi: `prime-radiant-inc/external-sandbox-pi`, `README.md` no default branch no momento da leitura.

Triagem do repositório do protocolo (API): Apache-2.0, Python, criado 2026-10-09, push 2026-11-16, não arquivado, 18 estrelas, 1 fork. Não entra no corpus.

## O que post e código dizem juntos

- O agente continua na máquina de quem o usa. O comando vai a um Linux isolado, com pastas montadas e, se o proxy estiver ligado, sites permitidos.
- Há três protótipos com o mesmo protocolo, em repositórios que publicam à parte: v86 (Node.js, Alpine em WebAssembly), Apple Containers (Python), Quicksand/QEMU (Python).
- São protótipos. O post diz que não foram auditados para carga sensível. `COVERAGE.md` diz que um verde não é prova de isolamento nem certificação.
- No Claude Code, Read e Edit ficam no host. Frase do `claude-code/README.md`: "native file tools such as Read/Edit still access host files." O script `claude-shell-prefix.sh` só reencaminha o comando para o cliente, com o comentário de não avaliá-lo ali.
- No Pi, as sete ferramentas (`bash`, `read`, `write`, `edit`, `grep`, `find`, `ls`) e os atalhos `!` e `!!` vão ao sandbox. Sem resposta, erro, sem recuo ao host.
- No Codex, processo, arquivos e `apply_patch` vão pelo `/codex`. `danger-full-access` pede para não empilhar o sandbox da plataforma. `sandboxType: none` significa ausência desse segundo sandbox, com a execução ainda no convidado (`PROTOCOL.md`).
- A chave não entra no documento da política. O campo é `secretEnv`, nome de variável do host. Um site permitido pode transformar o segredo e devolvê-lo. O eco literal é redatado.
- Montagem com escrita é a pasta real. O convidado é Linux. Dependência compilada no macOS pode precisar de reinstalação.
- "Externo" qualifica o agente, não o computador. O post descarta rodar o agente dentro do sandbox (exemplo citado: Fly Sprites).

## Divergências — prevalece o código

1. **O abre do post é mais largo do que o Claude Code.** O lead diz que todo comando executa no Linux isolado. O corpo do post já corrige: só a ferramenta Bash atravessa. O `claude-code/README.md` alarga de novo, para o outro lado: o prefixo também cobre hook de shell, linha de status e a subida de MCP por stdio, porque é assim que o Claude Code aplica `CLAUDE_CODE_SHELL_PREFIX`. Read e Edit continuam de fora. O capítulo fica com o README.
2. **Rede desligada não é exigência do núcleo.** O post e o `codex/README.md` dizem que os três servidores nascem sem rede. `PROTOCOL.md`: com o proxy desligado, o protocolo não promete rede além da configuração offline de cada backend. O capítulo separa as duas frases.
3. **O atalho `!` do Codex não vai ao sandbox.** O post mostra `!uname -a` no Pi, e ali funciona. `codex/README.md`: na configuração só remota, o `!` da interface exige ambiente local, falha, e pode encerrar a interface. O post não diz isso.
4. **"No seu Mac" é a cena do post, não o contrato.** O cliente do prefixo exige macOS ou Linux. Apple Containers e Quicksand, no post, pedem Apple silicon. As portas 8686, 8687 e 8688 são exemplos atuais. `PROTOCOL.md` trata a porta como escolha de implementação.
5. **A suíte não exercita o agente.** `README.md` e `COVERAGE.md`: o runner não chama modelo e não exige Claude, Codex ou Pi. Um verde é interoperabilidade do fio nos perfis escolhidos.

Nenhuma dessas divergências derruba a Leitura executiva. Qualificam o que se pode copiar.

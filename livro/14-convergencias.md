# 14. Convergências e Tendências

> **Estado da arte capturado em 2026-07** · última revisão 2026-08-12 · [histórico e registro de expiração](HISTORICO.md)
>
> Camada didática v4, ver [Guia Editorial §2.1](GUIA-EDITORIAL.md).
> andaime: proprio
>
> **Capítulo de síntese**, consolida o que os capítulos 02–13 mediram, separa o que já é disciplina do que ainda é aposta, e aplica a cláusula de expiração ao inventário completo. Este capítulo é vivo: cada nova rodada do benchmark (`benchmark/`) o atualiza, confirmando convergências, resolvendo divergências ou aposentando componentes expirados.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:
1. **Enumerar** as oito convergências arquiteturais da primeira rodada e **explicar** por que convergência independente sinaliza disciplina consolidada;
2. **Distinguir** as dimensões consolidadas das dimensões em divergência real, e **justificar** por que a contenção é a divergência mais consequente;
3. **Aplicar** a cláusula de expiração a um componente de harness qualquer, identificando por que ele existe e sob que condição expira;
4. **Avaliar** um harness novo contra o checklist de convergências, cobrando justificativa para cada ausência;
5. **Antecipar** as tendências a acompanhar nas próximas rodadas e o que cada uma implicaria para o desenho de harnesses.

## O mesmo desenho no quadro branco de duas equipes

Duas equipes, dois harnesses, escolhidos por razões opostas. Uma queria integração com a nuvem que já usava; a outra queria código aberto e auditável.

Seis meses depois, alguém repara que os dois quadros brancos têm o mesmo desenho. Loop com parada estrutural. Arquivo de instruções na raiz do projeto. Compactação em camadas. Modo de planejamento como permissão. Hooks de ciclo de vida.

Nenhuma das duas equipes copiou a outra. Os dois projetos que elas usam também não copiaram um ao outro: linguagens diferentes, empresas diferentes, cronogramas que não se cruzam.

**Convergência independente é o argumento mais forte que este livro tem**, e é por isso que o capítulo existe. Quando implementações que não se falam chegam à mesma solução, a solução não é moda: é resposta a uma restrição real.

E o mais interessante não é a lista das oito coisas que todos inventaram igual. É a nona, que ninguém inventou igual, porque é ali que a disciplina ainda está aberta.

## Na prática: a tabela contra o harness que você construiu

Este capítulo não pede código novo, e a razão é o argumento dele. O exemplo trabalhado é o **harness que você construiu ao longo do livro**.

Pegue as oito convergências e confira uma a uma contra as suas treze etapas. Você implementou parada estrutural no cap. 02 sem consultar nenhum harness. Implementou arquivo de contexto no 03, escada de compactação no 04, plan mode como permissão no 09, hooks no 12. Não copiou ninguém: seguiu a dor de cada capítulo.

Se você reinventou as oito, a tese está provada no seu próprio repositório, e não por citação.

Agora a coluna que interessa mais: **as divergências que você teve de decidir sozinho**. Onde o livro te deu duas opções e nenhuma resposta, você escolheu, e é exatamente ali que a indústria também ainda escolhe. Essa lista é o seu mapa do que ainda está em aberto.

## O problema

Os capítulos anteriores analisaram o harness dimensão por dimensão, contexto, compactação, tools, permissões, loop. Falta a pergunta que dá sentido ao conjunto: **o que é acidente de implementação e o que é anatomia da disciplina?** Sem essa síntese, cada capítulo é um catálogo de escolhas; com ela, o leitor ganha um critério de projeto, saber o que copiar sem hesitar, onde ainda cabe apostar diferente, e o que vai desaparecer quando os modelos melhorarem.

O instrumento de medida é a convergência independente. Quando equipes que não se coordenam, em stacks e culturas diferentes, chegam à mesma arquitetura, isso é evidência forte de que o problema (e não a moda) determinou a solução. E o instrumento de projeção é a cláusula de expiração do capítulo 01: todo componente de harness é uma prótese para uma limitação atual do modelo, e portanto todo componente deve declarar quando espera se tornar desnecessário.

## O estado da arte

### O achado central da primeira rodada: oito convergências

Três harnesses, três stacks (Effect-TS, TypeScript, Python), três origens (startup independente, big tech, academia/porta didática), e uma convergência arquitetural. Sem coordenação, os três chegaram a:

1. **Arquivo de contexto hierárquico na raiz do projeto** — `AGENTS.md` / `GEMINI.md` / `CLAUDE.md`: o mesmo artefato com três nomes (cap. 03).
2. **Compactação em escada**, truncar tools → prune → sumarizar via LLM, com disparo automático por limiar (cap. 04).
3. **Schema de tools derivado de tipos**. Effect Schema, classes declarativas, Pydantic: ninguém escreve JSON Schema à mão (cap. 05).
4. **MCP como integração padrão**, três clientes completos sobre os SDKs oficiais (cap. 06).
5. **Plan mode como modo de permissão**, read-only imposto pelo sistema de permissões, não pedido ao modelo (cap. 09).
6. **Hooks de ciclo de vida**, before/after tool, compactação, sessão (cap. 12).
7. **Headless com saída estruturada** — `-p` + JSON/NDJSON para scripting e CI (cap. 13).
8. **Parada por ausência de tool-call + limite de turnos**, a mecânica universal do loop (cap. 02).

Quando implementações independentes convergem assim, a anatomia está consolidada: **isto é a disciplina**, não mais um conjunto de escolhas idiossincráticas. Um harness novo que não implemente os oito itens acima precisa justificar cada ausência.

### Onde ainda há divergência real

As dimensões sem consenso são o mapa das apostas em aberto:

- **Contenção** (cap. 07): política + sandbox de SO obrigatórios (gemini-cli), política + paths sensíveis fixos (OpenHarness), ou só política (opencode)? A divergência mais consequente, é a que define o risco operacional.
- **Multi-agente** (cap. 10): ferramenta pontual, serviço com registry, ou time persistente com mailbox? Três filosofias incompatíveis; o vencedor depende de quão bons os modelos ficarão em coordenação.
- **Quem decide continuar** (cap. 02): heurística estrutural ou uma inferência extra por turno (next-speaker check)?
- **Neutralidade de modelo** (cap. 12): ~26 provedores (opencode) contra vitrine de um ecossistema (gemini-cli). Aposta comercial, não técnica, mas define quem sobrevive à comoditização dos modelos.
- **Evals comportamentais** (cap. 11): na rodada 1, só um dos três tratava comportamento do agente como superfície de regressão, a rodada 2 confirmou a previsão e a lacuna fechou (ver cap. 11). Previsão fácil: em dois anos, isso será tão obrigatório quanto CI.

### A cláusula de expiração, aplicada

Retomando a tese do capítulo 01, todo componente de harness é uma prótese para uma limitação atual do modelo. O exercício que todo harness deveria fazer, aplicado ao que estudamos:

| Componente | Existe porque... | Expira quando... |
|---|---|---|
| Compactação | janelas são finitas e caras | contexto longo ficar barato e confiável |
| Plan mode | modelos agem precipitadamente | modelos planejarem espontaneamente sob risco |
| Next-speaker check | o modelo não sinaliza bem o fim do turno | protocolos de turno nativos do modelo |
| Policy engine / aprovações | modelos não são confiáveis com ações destrutivas | confiabilidade calibrada e verificável |
| Prompt por família de modelo | modelos respondem diferente a instruções | convergência de instruction-following |
| Subagente para exploração | dumps de arquivos poluem o contexto | contexto abundante + atenção robusta |
| Repo-map / índices de código | o modelo não "carrega" o repo inteiro | contexto de milhões de tokens utilizável |

O que **não** expira: sandbox (contenção é sobre o mundo, não sobre a capacidade do modelo), interfaces, verificação do trabalho (testes/LSP, verdade externa ao modelo), e os protocolos de interoperabilidade (MCP, A2A, formatos de skill). A engenharia de harness de longo prazo mora aí: **na fronteira entre o agente e o mundo, não na muleta para a limitação do modelo**.

### Tendências a acompanhar nas próximas rodadas

1. **Padronização do arquivo de contexto**, a pressão por `AGENTS.md` neutro cross-vendor.
2. **Skills/plugins portáveis**, o OpenHarness já carrega skills do formato Claude Code; um "MCP da extensibilidade" está se formando.
3. **Agente-como-serviço**. A2A server, agent cards, SDKs: harnesses expondo-se uns aos outros.
4. **Segurança como dimensão de primeira classe**, parsing de shell, trusted folders, evals de injection: hoje exceção, amanhã baseline (hipótese confirmada na rodada 2 com o Codex CLI).
5. **Reversibilidade**, checkpoint git com `/rewind`: quando desfazer é barato, a política pode ser mais frouxa; espere mais harnesses copiando.
6. **O harness mínimo**, na contramão da sofisticação, projetos como mini-swe-agent (~100 linhas) testam quanto do *scaffolding* (andaime) o modelo moderno já dispensa. É a cláusula de expiração virando experimento.

### Leitura executiva

- Oito dimensões já convergiram entre implementações independentes, são o checklist mínimo de um harness sério; ausências exigem justificativa.
- As divergências reais (contenção, multi-agente, next-speaker, neutralidade de modelo, evals comportamentais) são o mapa das apostas em aberto, contenção é a de maior consequência operacional.
- A cláusula de expiração separa próteses temporárias (compactação, plan mode, repo-map...) do que é permanente: sandbox, interfaces, verificação externa e protocolos de interoperabilidade.
- O valor de longo prazo da engenharia de harness está na fronteira agente–mundo; o resto muda de dono ou desaparece conforme os modelos melhoram.
- Este capítulo é o placar vivo do livro: cada rodada do benchmark confirma convergências, resolve divergências ou aposenta componentes expirados.

> **Consulte também**: a coleção viva [Awesome Harness Engineering. Foundations](https://github.com/GHDaru/awesome-harness-engineering#foundations) reúne mais recursos consultáveis desta dimensão, curados por problema.

## Verificação

1. Por que a convergência **independente** (três stacks, três origens) é evidência mais forte de consolidação do que a adoção de um padrão por vários projetos que se copiam? (Releia "O problema" e o achado central.)
2. Um harness novo não implementa plan mode nem arquivo de contexto na raiz. Segundo este capítulo, qual é a postura correta ao avaliá-lo, e o que você exigiria do autor?
3. Aplique a cláusula de expiração a um componente que **não** está na tabela (por exemplo, o next-speaker check já está; escolha hooks de ciclo de vida ou headless): ele existe por limitação do modelo ou por necessidade da fronteira agente–mundo? Ele expira?
4. Entre as cinco divergências listadas, qual define o risco operacional e qual é uma aposta comercial em vez de técnica? Justifique com o texto.

---

## Respostas da verificação

**1.** Porque adoção por cópia prova apenas que uma ideia se espalhou, e ideias ruins se espalham. Convergência **independente** prova outra coisa: que projetos sem contato, com linguagens, prazos e incentivos diferentes, encontraram a mesma solução para a mesma restrição. Isso elimina a explicação social e deixa a explicação estrutural, a solução existe porque o problema existe. É o mesmo raciocínio da replicação em ciência: um resultado repetido por um laboratório que não conhece o primeiro vale mais que dez citações do primeiro.

**2.** A postura correta é **perguntar o que ele resolve no lugar**, não apontar ausência. As convergências são respostas a restrições reais; quem não as implementa ou resolveu a restrição por outro caminho, ou ainda não a encontrou. O que se exige do autor é exatamente isso, por escrito: qual mecanismo cumpre o papel do plan mode, e o que acontece quando a janela de contexto acaba sem arquivo de instruções na raiz. Uma resposta boa é uma arquitetura diferente; uma resposta ruim é silêncio ou "o modelo cuida disso". A diferença entre as duas é o que separa uma escolha de uma lacuna.

**3.** Tome os **hooks de ciclo de vida**. Eles não existem por limitação do modelo: existem porque **terceiros precisam mudar o comportamento sem forkar**, que é uma necessidade organizacional e não cognitiva. Nenhuma melhoria de capacidade do modelo faz a equipe de segurança parar de querer bloquear um comando. Logo, hooks não expiram, são fronteira, como os protocolos do cap. 17.

O contraste esclarece a regra: a compactação **expira** quando a janela deixar de ser escassa, porque ela existe só para contornar essa escassez. O teste é sempre o mesmo: se você não consegue nomear a capacidade cujo surgimento tornaria o componente inútil, provavelmente ele não é prótese, é fronteira.

**4.** A divergência que define o **risco operacional** é a de contenção: harnesses com política de permissão mas sem sandbox de sistema operacional apostam na obediência do modelo, e a diferença entre os dois grupos aparece no dia do incidente, não no dia da avaliação. É a mesma leitura do cap. 07, e é a única divergência da lista cujo custo é medido em consequência, não em conveniência.

A divergência que é **aposta comercial** é a de abertura do modelo contra abertura do harness. Publicar o modelo e fechar o scaffolding, ou o inverso, não decorre de nenhuma restrição técnica: é uma decisão sobre onde a empresa acha que o valor vai ficar. E o fato de casas diferentes apostarem em direções opostas, com a mesma informação, é a evidência de que ninguém sabe, o que a torna uma aposta, e não uma arquitetura.

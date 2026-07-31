# Glossário

As siglas deste livro, **por extenso**, com uma explicação curta e o **contexto** em que aparecem. No corpo dos capítulos, passar o mouse sobre uma sigla mostra o seu significado (`abbr`); aqui está a referência completa. As expansões foram conferidas no próprio texto (Princípio I).

## Agentes, protocolos e orquestração

- **MCP — Model Context Protocol.** Protocolo aberto que padroniza como um harness pluga ferramentas, dados e prompts externos ao modelo. *Aparece em:* cap. 06 (MCP) e cap. 17 (Protocolos).
- **ACP — Agent Client Protocol.** Protocolo (origem Zed) para a conversa **agente ↔ editor/cliente**. Não confundir com o *Agent Communication Protocol* da IBM (também "ACP"), encerrado e fundido ao A2A. *Aparece em:* cap. 13 (Interfaces), cap. 17.
- **MRTR — Multi Round-Trip Requests.** Padrão da spec MCP 2026-07-28 que substitui as requisições iniciadas pelo servidor (sampling/elicitation): o servidor responde `input_required` e o cliente retenta com as respostas. *Aparece em:* cap. 06.
- **DCR — Dynamic Client Registration.** Registro dinâmico de clientes OAuth; depreciado na spec MCP 2026-07-28 em favor do CIMD. *Aparece em:* cap. 06.
- **CIMD — Client ID Metadata Documents.** Sucessor do DCR na autorização do MCP: a identidade do cliente vem de um documento de metadados. *Aparece em:* cap. 06.
- **A2A — Agent-to-Agent.** Protocolo de **delegação entre agentes** (origem Google, doado à Linux Foundation). *Aparece em:* cap. 10 (Subagentes), cap. 17.
- **LSP — Language Server Protocol.** Padrão que inspirou os protocolos de agente: separa a "inteligência" (server) da interface (client). *Aparece em:* cap. 11, cap. 12, cap. 14.
- **RPC — Remote Procedure Call.** Chamar um procedimento em outro processo/máquina como se fosse local; base de vários protocolos. *Aparece em:* caps. 05, 06, 10 e 12.
- **MAST — Multi-Agent System Failure Taxonomy.** Taxonomia de modos de falha de sistemas multiagente (do artigo *"Why Do Multi-Agent LLM Systems Fail?"*). *Aparece em:* cap. 10 (Subagentes), bibliografia.
- **RAG — Retrieval-Augmented Generation.** Geração aumentada por recuperação: buscar trechos relevantes e injetá-los no contexto. *Aparece em:* cap. 03 (Contexto), cap. 08.

## Modelos e IA

- **IA — Inteligência Artificial** (em inglês, **AI — Artificial Intelligence**). *Aparece em:* todo o livro.
- **LLM — Large Language Model** (modelo de linguagem grande). O modelo que o harness envolve. *Aparece em:* todo o livro.
- **GPT — Generative Pre-trained Transformer.** Família de modelos de linguagem. *Aparece em:* caps. 01, 05 e 09, bibliografia.
- **SWE-bench / SWE-agent — Software Engineering** (benchmark / agente de engenharia de software). *Aparece em:* cap. 11 (Evals).

## Ferramentas, interfaces e rede

- **API — Application Programming Interface.** Contrato pelo qual programas se falam. *Aparece em:* todo o livro.
- **SDK — Software Development Kit.** Kit para construir sobre uma plataforma (ex.: o Agent SDK). *Aparece em:* cap. 12 (Extensibilidade), cap. 13.
- **CLI — Command-Line Interface.** Interface de linha de comando. *Aparece em:* cap. 13.
- **TUI — Text (Terminal) User Interface.** Interface de texto interativa no terminal. *Aparece em:* cap. 13.
- **IDE — Integrated Development Environment.** Ambiente integrado de desenvolvimento (ex.: VS Code). *Aparece em:* cap. 13.
- **UI — User Interface** / **UX — User Experience.** Interface e experiência do usuário. *Aparece em:* cap. 13.
- **HCI — Human-Computer Interaction.** Interação humano-computador (campo científico). *Aparece em:* cap. 13.
- **HTTP — HyperText Transfer Protocol.** Protocolo da web. *Aparece em:* caps. 06, 10, 11 e 13.
- **SSE — Server-Sent Events.** Streaming de eventos do servidor para o cliente (usado no chat). *Aparece em:* cap. 13.
- **JSON — JavaScript Object Notation.** Formato de dados dos schemas de ferramentas. *Aparece em:* cap. 05, 06.
- **SO — Sistema Operacional.** *Aparece em:* cap. 07 (Permissões e Sandboxing).
- **CI — Continuous Integration** (integração contínua). *Aparece em:* cap. 11, aparato.
- **DDD — Domain-Driven Design.** Design orientado a domínio; guia o `harness-zero`. *Aparece em:* construção prática.

## Editorial, publicação e pesquisa

- **DOI — Digital Object Identifier.** Identificador persistente da obra (Zenodo). *Aparece em:* aparato, capa.
- **ORCID — Open Researcher and Contributor ID.** Identificador do pesquisador (do autor). *Aparece em:* aparato, "Sobre o autor".
- **ISBN — International Standard Book Number.** Identificador padrão de livros. *Aparece em:* Guia Editorial.
- **CC — Creative Commons.** Família de licenças abertas (o conteúdo é CC BY 4.0). *Aparece em:* licença, aparato.
- **MIT.** Licença permissiva de software (nome vem do *Massachusetts Institute of Technology*); cobre o código. *Aparece em:* licença.
- **ICMJE — International Committee of Medical Journal Editors** e **COPE — Committee on Publication Ethics.** Diretrizes de autoria/ética seguidas na divulgação de co-autoria de IA. *Aparece em:* Guia Editorial §6.
- **ICLR — International Conference on Learning Representations.** Conferência científica citada na bibliografia. *Aparece em:* bibliografia.

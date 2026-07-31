<!-- i18n fonte:livro/glossario.md edicao:0.61 hash:749ef66d -->
# Glossary

The acronyms of this book, **spelled out**, with a short explanation and the **context** in which they appear. In the body of the chapters, hovering over an acronym shows its meaning (`abbr`); here is the complete reference. The expansions were checked against the text itself (Principle I).

## Agents, protocols and orchestration

- **MCP — Model Context Protocol.** Open protocol that standardizes how a harness plugs external tools, data and prompts into the model. *Appears in:* ch. 06 (MCP) and ch. 17 (Protocols).
- **ACP — Agent Client Protocol.** Protocol (originated at Zed) for the **agent ↔ editor/client** conversation. Not to be confused with IBM's *Agent Communication Protocol* (also "ACP"), discontinued and merged into A2A. *Appears in:* ch. 13 (Interfaces), ch. 17.
- **MRTR — Multi Round-Trip Requests.** Pattern from the MCP 2026-07-28 spec that replaces server-initiated requests (sampling/elicitation): the server responds `input_required` and the client retries with the answers. *Appears in:* ch. 06.
- **DCR — Dynamic Client Registration.** Dynamic registration of OAuth clients; deprecated in the MCP 2026-07-28 spec in favor of CIMD. *Appears in:* ch. 06.
- **CIMD — Client ID Metadata Documents.** DCR's successor in MCP authorization: the client's identity comes from a metadata document. *Appears in:* ch. 06.
- **A2A — Agent-to-Agent.** Protocol for **delegation between agents** (originated at Google, donated to the Linux Foundation). *Appears in:* ch. 10 (Subagents), ch. 17.
- **LSP — Language Server Protocol.** The standard that inspired agent protocols: it separates the "intelligence" (server) from the interface (client). *Appears in:* ch. 11, ch. 12, ch. 14.
- **RPC — Remote Procedure Call.** Calling a procedure in another process/machine as if it were local; the basis of several protocols. *Appears in:* chs. 05, 06, 10 and 12.
- **MAST — Multi-Agent System Failure Taxonomy.** Taxonomy of failure modes of multi-agent systems (from the paper *"Why Do Multi-Agent LLM Systems Fail?"*). *Appears in:* ch. 10 (Subagents), bibliography.
- **RAG — Retrieval-Augmented Generation.** Generation augmented by retrieval: fetch relevant excerpts and inject them into the context. *Appears in:* ch. 03 (Context), ch. 08.

## Models and AI

- **AI — Artificial Intelligence** (in the Portuguese original, **IA — Inteligência Artificial**). *Appears in:* the whole book.
- **LLM — Large Language Model.** The model the harness wraps. *Appears in:* the whole book.
- **GPT — Generative Pre-trained Transformer.** A family of language models. *Appears in:* chs. 01, 05 and 09, bibliography.
- **SWE-bench / SWE-agent — Software Engineering** (benchmark / software-engineering agent). *Appears in:* ch. 11 (Evals).

## Tools, interfaces and networking

- **API — Application Programming Interface.** The contract through which programs talk to each other. *Appears in:* the whole book.
- **SDK — Software Development Kit.** A kit for building on top of a platform (e.g. the Agent SDK). *Appears in:* ch. 12 (Extensibility), ch. 13.
- **CLI — Command-Line Interface.** *Appears in:* ch. 13.
- **TUI — Text (Terminal) User Interface.** Interactive text interface in the terminal. *Appears in:* ch. 13.
- **IDE — Integrated Development Environment.** (e.g. VS Code). *Appears in:* ch. 13.
- **UI — User Interface** / **UX — User Experience.** The user's interface and experience. *Appears in:* ch. 13.
- **HCI — Human-Computer Interaction.** (a scientific field). *Appears in:* ch. 13.
- **HTTP — HyperText Transfer Protocol.** The protocol of the web. *Appears in:* chs. 06, 10, 11 and 13.
- **SSE — Server-Sent Events.** Streaming of events from server to client (used in the chat). *Appears in:* ch. 13.
- **JSON — JavaScript Object Notation.** The data format of tool schemas. *Appears in:* ch. 05, 06.
- **OS — Operating System** (in the Portuguese original, **SO — Sistema Operacional**). *Appears in:* ch. 07 (Permissions and Sandboxing).
- **CI — Continuous Integration.** *Appears in:* ch. 11, apparatus.
- **DDD — Domain-Driven Design.** Guides the `harness-zero`. *Appears in:* the hands-on build.

## Editorial, publishing and research

- **DOI — Digital Object Identifier.** The work's persistent identifier (Zenodo). *Appears in:* apparatus, cover.
- **ORCID — Open Researcher and Contributor ID.** The researcher's identifier (the author's). *Appears in:* apparatus, "About the author".
- **ISBN — International Standard Book Number.** The standard identifier for books. *Appears in:* Editorial Guide.
- **CC — Creative Commons.** A family of open licenses (the content is CC BY 4.0). *Appears in:* license, apparatus.
- **MIT.** Permissive software license (the name comes from the *Massachusetts Institute of Technology*); covers the code. *Appears in:* license.
- **ICMJE — International Committee of Medical Journal Editors** and **COPE — Committee on Publication Ethics.** Authorship/ethics guidelines followed in disclosing AI co-authorship. *Appears in:* Editorial Guide §6.
- **ICLR — International Conference on Learning Representations.** Scientific conference cited in the bibliography. *Appears in:* bibliography.

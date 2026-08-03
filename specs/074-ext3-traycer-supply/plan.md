# Plano — spec 074

1. Avaliador (agente) sobre `/workspace/traycer` @ 65fc3d7 → traycer.md + JSON de notas +
   veredito de inclusão + levantamento supply-chain do Traycer.
2. Em paralelo (eu): evidências de supply chain colhidas nos clones locais do corpus:
   - QM → Pi (fork com patch de segurança próprio, `package.json:58`), Claude Agent SDK (:50),
     Codex (:60), opencode (:61-62,72);
   - Kimi Code → pi-tui vendorizado (`packages/pi-tui`, agradecimento `README.md:122`);
   - software-agent-sdk → Codex/gemini-cli como subprocessos ACP
     (`openhands/agent_server/conversation_service.py:723`, `event_service.py:873`);
   - Grok Build → retoma sessões de Claude/Codex/Cursor (`views/session_picker.rs`), lê
     AGENTS.md/CLAUDE.md/.cursor;
   - n8n → LangChain (`@n8n/nodes-langchain/package.json`), com reinternalização do loop (V3);
   - Pi ← `pi-xai-oauth` (provedor xAI via pacote de terceiros, radar 2026-08-01).
3. Apêndice `livro/apendice-supply-chain.md`: conceito, tabela consumidor→fornecedor→mecanismo→
   evidência, diagrama textual, leitura (3 implicações) e ângulo de segurança. Espelho EN +
   sumario.json/sumario.en.json (mesma posição).
4. Integração da avaliação conforme veredito (corpus 21 ou recusa documentada); radar; deltas
   EN + selos; corpus companion; build 4 passos; HISTORICO 0.68; merge --no-ff; CI.

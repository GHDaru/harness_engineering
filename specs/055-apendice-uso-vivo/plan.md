# Plan — 055

1. Backend: projeção pública de `nav_stats` (drop `ultimos`); teste: semeia consent+nav e valida contagem agregada e ausência de campos sensíveis.
2. `tema/uso.js`: lê `window.COMPANION.backend`; fetch `/telemetry/publico`; render em DOM puro (kpis + lista de barras, max 12, largura % do maior); títulos: mapa slug→título embutido? Não — deriva do sumário? A página não tem o mapa; solução: prettify (slug → "02 Loop Do Agente" com hífens→espaços e capitulação) + casos especiais (index/sumario). Simples e sem acoplamento.
3. Motor: `cpSync` do uso.js + `<script ... defer>` ao lado do viz.js; CSS `.uso-*` theme-aware no estilo.css.
4. Conteúdo: apêndice curto (Diátaxis: referência/explicação), com selo de data e a ilha; entrada no sumario.json (Aparato, entre "Apêndice — O estudo" e "Bibliografia").
5. Verificações: suíte backend; e2e playwright com uvicorn echo semeando 3 páginas; build+portão+corpus; HISTORICO 0.50; merge --no-ff; push.

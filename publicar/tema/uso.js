/* Ilha viva "Uso do livro" (spec 055) — JS puro, sem dependências.
   Preenche <div data-viz="uso-livro"> com o agregado público da telemetria
   (GET /telemetry/publico — só contagens por página; nada pessoal).
   Sem backend ou com erro: mensagem honesta. No PDF a ilha é ocultada. */
(function () {
  "use strict";
  var alvo = document.querySelector('[data-viz="uso-livro"]');
  if (!alvo) return;
  var BACKEND = ((window.COMPANION || {}).backend || "").replace(/\/+$/, "");

  function el(tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; }
  function titulo(slug) {
    var especiais = { "index": "Capa", "sumario": "Entrada (sumário)", "comparativo": "Benchmark — Comparativo",
      "historico": "Histórico", "glossario": "Glossário", "bibliografia": "Bibliografia",
      "guia-editorial": "Guia Editorial", "apendice-estudo": "Apêndice — O estudo",
      "apendice-uso": "Apêndice — Uso do livro", "autor": "Sobre o autor" };
    if (especiais[slug]) return especiais[slug];
    var m = slug.match(/^(\d+)-(.+)$/);
    var nome = (m ? m[2] : slug).replace(/-/g, " ");
    nome = nome.charAt(0).toUpperCase() + nome.slice(1);
    return m ? (m[1] + " — " + nome) : nome;
  }
  function falha() {
    alvo.innerHTML = "";
    alvo.appendChild(el("p", "uso-off", "📊 Os dados vivos de uso estão indisponíveis agora — tente recarregar em instantes. (Os números existem só na versão online do livro.)"));
  }
  if (!BACKEND) { falha(); return; }

  fetch(BACKEND + "/telemetry/publico").then(function (r) {
    if (!r.ok) throw new Error("HTTP " + r.status);
    return r.json();
  }).then(function (d) {
    alvo.innerHTML = "";
    var kpis = el("div", "uso-kpis");
    [["Visitas registradas", d.total], ["Páginas distintas", d.paginas_distintas]].forEach(function (k) {
      var c = el("div", "uso-kpi");
      c.appendChild(el("b", null, String(k[1])));
      c.appendChild(el("span", null, k[0]));
      kpis.appendChild(c);
    });
    alvo.appendChild(kpis);
    var pares = Object.keys(d.por_pagina || {}).map(function (s) { return [s, d.por_pagina[s]]; })
      .sort(function (a, b) { return b[1] - a[1]; }).slice(0, 12);
    if (!pares.length) {
      alvo.appendChild(el("p", "uso-off", "Ainda não há visitas registradas — os números aparecem conforme os leitores aceitam a telemetria."));
      return;
    }
    var max = pares[0][1];
    var lista = el("div", "uso-lista");
    pares.forEach(function (pr) {
      var linha = el("div", "uso-linha");
      linha.appendChild(el("span", "uso-nome", titulo(pr[0])));
      var trilho = el("div", "uso-trilho");
      var barra = el("i"); barra.style.width = Math.max(3, Math.round(100 * pr[1] / max)) + "%";
      trilho.appendChild(barra); linha.appendChild(trilho);
      linha.appendChild(el("b", "uso-n", String(pr[1])));
      lista.appendChild(linha);
    });
    alvo.appendChild(lista);
    alvo.appendChild(el("p", "uso-nota", "Contagens agregadas e anônimas, registradas apenas com consentimento. Atualiza a cada visita à página."));
  }).catch(falha);
})();

/* Knowledge Graph interativo (spec 057) — JS puro, canvas, zero dependências.
   Preenche <div data-viz="grafo-livro"> com assets/grafo.json (derivado do
   conteúdo a cada build). Interações: arrasto, zoom (roda), hover, clique
   (destaca vizinhos + painel com link), filtros por tipo na legenda. */
(function () {
  "use strict";
  var alvo = document.querySelector('[data-viz="grafo-livro"]');
  if (!alvo) return;

  var CORES = { capitulo: "#e0a24a", harness: "#78aeff", conceito: "#6fd08a", etapa: "#c79be0" };
  var NOMES = { capitulo: "Capítulos", harness: "Harnesses do corpus", conceito: "Conceitos", etapa: "harness-zero" };
  var RAIO = { capitulo: 11, harness: 8, conceito: 8, etapa: 6 };

  function el(tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; }

  fetch("assets/grafo.json").then(function (r) {
    if (!r.ok) throw new Error("HTTP " + r.status);
    return r.json();
  }).then(iniciar).catch(function () {
    alvo.innerHTML = "";
    alvo.appendChild(el("p", "kg-off", "📊 O grafo não carregou — recarregue a página. (A visualização existe só na versão online.)"));
  });

  function iniciar(g) {
    alvo.innerHTML = "";
    var wrap = el("div", "kg");
    var canvas = document.createElement("canvas");
    var painel = el("div", "kg-painel"); painel.hidden = true;
    var legenda = el("div", "kg-legenda");
    wrap.appendChild(canvas); wrap.appendChild(painel); alvo.appendChild(wrap); alvo.appendChild(legenda);

    var ctx = canvas.getContext("2d");
    var W = 0, H = 0, DPR = Math.max(1, window.devicePixelRatio || 1);
    function medir() {
      W = wrap.clientWidth; H = Math.max(460, Math.min(640, window.innerHeight * 0.62));
      canvas.width = W * DPR; canvas.height = H * DPR;
      canvas.style.width = W + "px"; canvas.style.height = H + "px";
    }
    medir(); window.addEventListener("resize", function () { medir(); desenhar(); });

    // estado
    var nos = g.nos.map(function (n) {
      return Object.assign({}, n, {
        x: W / 2 + (Math.random() - 0.5) * W * 0.7,
        y: H / 2 + (Math.random() - 0.5) * H * 0.7,
        vx: 0, vy: 0, grau: 0
      });
    });
    var porId = {}; nos.forEach(function (n) { porId[n.id] = n; });
    var arestas = g.arestas.filter(function (a) { return porId[a.de] && porId[a.para]; });
    arestas.forEach(function (a) { porId[a.de].grau += a.peso; porId[a.para].grau += a.peso; });
    var visiveis = { capitulo: true, harness: true, conceito: true, etapa: true };
    var zoom = 1, panX = 0, panY = 0;
    var selecionado = null, hover = null, arrastando = null, panning = false;
    var lastX = 0, lastY = 0;

    // legenda com filtros
    Object.keys(NOMES).forEach(function (t) {
      var b = el("button", "kg-filtro on");
      var dot = el("span", "kg-dot"); dot.style.background = CORES[t];
      b.appendChild(dot); b.appendChild(document.createTextNode(NOMES[t]));
      b.addEventListener("click", function () {
        visiveis[t] = !visiveis[t]; b.className = "kg-filtro" + (visiveis[t] ? " on" : "");
        if (selecionado && !visiveis[selecionado.tipo]) fecharPainel();
        desenhar();
      });
      legenda.appendChild(b);
    });
    legenda.appendChild(el("span", "kg-dica", "arraste os nós · roda = zoom · clique = conexões"));

    function noVisivel(n) { return visiveis[n.tipo]; }
    function arestaVisivel(a) { return noVisivel(porId[a.de]) && noVisivel(porId[a.para]); }
    function vizinhos(id) {
      var s = new Set([id]);
      arestas.forEach(function (a) { if (a.de === id) s.add(a.para); if (a.para === id) s.add(a.de); });
      return s;
    }

    // física: repulsão + molas + gravidade ao centro (O(n²) ok para ~52 nós)
    var temperatura = 1;
    function passo() {
      var i, j, n, m, dx, dy, d2, d, f;
      for (i = 0; i < nos.length; i++) {
        n = nos[i]; if (!noVisivel(n)) continue;
        for (j = i + 1; j < nos.length; j++) {
          m = nos[j]; if (!noVisivel(m)) continue;
          dx = n.x - m.x; dy = n.y - m.y; d2 = dx * dx + dy * dy + 40; d = Math.sqrt(d2);
          f = 2600 / d2;
          n.vx += (dx / d) * f; n.vy += (dy / d) * f;
          m.vx -= (dx / d) * f; m.vy -= (dy / d) * f;
        }
      }
      arestas.forEach(function (a) {
        if (!arestaVisivel(a)) return;
        var s = porId[a.de], t = porId[a.para];
        var ddx = t.x - s.x, ddy = t.y - s.y;
        var dist = Math.sqrt(ddx * ddx + ddy * ddy) + 0.01;
        var ff = (dist - 90) * 0.004 * Math.min(3, a.peso);
        s.vx += (ddx / dist) * ff; s.vy += (ddy / dist) * ff;
        t.vx -= (ddx / dist) * ff; t.vy -= (ddy / dist) * ff;
      });
      nos.forEach(function (nn) {
        if (!noVisivel(nn) || nn === arrastando) return;
        nn.vx += (W / 2 - nn.x) * 0.0015; nn.vy += (H / 2 - nn.y) * 0.0015;
        nn.x += nn.vx * temperatura; nn.y += nn.vy * temperatura;
        nn.vx *= 0.85; nn.vy *= 0.85;
      });
      if (temperatura > 0.05) temperatura *= 0.995;
    }

    function desenhar() {
      ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
      ctx.clearRect(0, 0, W, H);
      ctx.save();
      ctx.translate(panX, panY); ctx.scale(zoom, zoom);
      var escuro = document.documentElement.getAttribute("data-tema") === "escuro" ||
        (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches && !document.documentElement.getAttribute("data-tema"));
      var corLinha = escuro ? "rgba(255,255,255," : "rgba(0,0,0,";
      var foco = selecionado ? vizinhos(selecionado.id) : null;

      arestas.forEach(function (a) {
        if (!arestaVisivel(a)) return;
        var s = porId[a.de], t = porId[a.para];
        var dim = foco && !(foco.has(a.de) && foco.has(a.para));
        ctx.strokeStyle = corLinha + (dim ? "0.04" : (0.10 + Math.min(0.25, a.peso * 0.03))) + ")";
        ctx.lineWidth = dim ? 0.5 : Math.min(3, 0.5 + a.peso * 0.15);
        ctx.beginPath(); ctx.moveTo(s.x, s.y); ctx.lineTo(t.x, t.y); ctx.stroke();
      });
      nos.forEach(function (n) {
        if (!noVisivel(n)) return;
        var dim = foco && !foco.has(n.id);
        var r = RAIO[n.tipo] + Math.min(6, n.grau * 0.04);
        ctx.globalAlpha = dim ? 0.18 : 1;
        ctx.fillStyle = CORES[n.tipo];
        ctx.beginPath(); ctx.arc(n.x, n.y, r, 0, Math.PI * 2); ctx.fill();
        if (n === selecionado || n === hover) {
          ctx.strokeStyle = escuro ? "#fff" : "#111"; ctx.lineWidth = 2;
          ctx.beginPath(); ctx.arc(n.x, n.y, r + 2, 0, Math.PI * 2); ctx.stroke();
        }
        if (n.tipo === "capitulo" || n === hover || n === selecionado || zoom > 1.5) {
          ctx.globalAlpha = dim ? 0.25 : 1;
          ctx.fillStyle = escuro ? "#e6e6e4" : "#1c1c1c";
          ctx.font = (n.tipo === "capitulo" ? "600 " : "") + "11px sans-serif";
          ctx.textAlign = "center";
          var rot = n.tipo === "capitulo" ? n.rotulo.split("—")[0].trim() : n.rotulo;
          ctx.fillText(rot, n.x, n.y - r - 5);
        }
        ctx.globalAlpha = 1;
      });
      ctx.restore();
    }

    function loop() { passo(); desenhar(); requestAnimationFrame(loop); }
    requestAnimationFrame(loop);

    // gancho mínimo para testes automatizados (e2e da spec 057)
    window.__kg = { nNos: nos.length, nArestas: arestas.length, porId: porId,
      abrir: function (id) { if (porId[id]) abrirPainel(porId[id]); }, visiveis: visiveis };

    // coordenadas do mouse no espaço do grafo
    function coord(ev) {
      var r = canvas.getBoundingClientRect();
      return { x: (ev.clientX - r.left - panX) / zoom, y: (ev.clientY - r.top - panY) / zoom };
    }
    function noEm(p) {
      for (var i = nos.length - 1; i >= 0; i--) {
        var n = nos[i]; if (!noVisivel(n)) continue;
        var r = RAIO[n.tipo] + Math.min(6, n.grau * 0.04) + 3;
        var dx = n.x - p.x, dy = n.y - p.y;
        if (dx * dx + dy * dy <= r * r) return n;
      }
      return null;
    }

    function vizinhosN(id) { return vizinhos(id).size - 1; }
    function abrirPainel(n) {
      selecionado = n; painel.hidden = false; painel.innerHTML = "";
      var dot = el("span", "kg-dot"); dot.style.background = CORES[n.tipo];
      var tt = el("div", "kg-p-t"); tt.appendChild(dot); tt.appendChild(document.createTextNode(" " + n.rotulo));
      painel.appendChild(tt);
      painel.appendChild(el("div", "kg-p-sub", NOMES[n.tipo] + " · " + vizinhosN(n.id) + " conexões"));
      var ln = el("a", "kg-p-link", "abrir página →"); ln.href = n.url; painel.appendChild(ln);
      var x = el("button", "kg-p-x", "×"); x.setAttribute("aria-label", "Fechar");
      x.addEventListener("click", fecharPainel); painel.appendChild(x);
    }
    function fecharPainel() { selecionado = null; painel.hidden = true; }

    var downX = 0, downY = 0;
    canvas.addEventListener("mousedown", function (ev) {
      var p = coord(ev), n = noEm(p);
      if (n) { arrastando = n; } else { panning = true; }
      lastX = downX = ev.clientX; lastY = downY = ev.clientY;
    });
    window.addEventListener("mousemove", function (ev) {
      if (arrastando) {
        var p = coord(ev); arrastando.x = p.x; arrastando.y = p.y; arrastando.vx = arrastando.vy = 0;
        temperatura = Math.max(temperatura, 0.3);
      } else if (panning) {
        panX += ev.clientX - lastX; panY += ev.clientY - lastY;
        lastX = ev.clientX; lastY = ev.clientY;
      } else if (ev.target === canvas) {
        var h = noEm(coord(ev));
        if (h !== hover) { hover = h; canvas.style.cursor = h ? "pointer" : "grab"; }
      }
    });
    window.addEventListener("mouseup", function (ev) {
      var clique = Math.abs(ev.clientX - downX) < 4 && Math.abs(ev.clientY - downY) < 4;
      if (arrastando && clique) {
        if (selecionado === arrastando) fecharPainel(); else abrirPainel(arrastando);
      } else if (panning && clique && ev.target === canvas) {
        fecharPainel();
      }
      arrastando = null; panning = false;
    });
    canvas.addEventListener("wheel", function (ev) {
      ev.preventDefault();
      var fator = ev.deltaY < 0 ? 1.12 : 0.89;
      var r = canvas.getBoundingClientRect();
      var mx = ev.clientX - r.left, my = ev.clientY - r.top;
      panX = mx - (mx - panX) * fator; panY = my - (my - panY) * fator;
      zoom = Math.max(0.35, Math.min(4, zoom * fator));
      desenhar();
    }, { passive: false });
  }
})();

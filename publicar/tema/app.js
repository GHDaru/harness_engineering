// Interações mínimas do site: alternância de tema (persistida) e o "Retomar"
// da experiência de entrada (spec 021). Dependency-free.
(function () {
  var raiz = document.documentElement;
  var chave = "harness-tema";
  var salvo = localStorage.getItem(chave);
  if (salvo) raiz.setAttribute("data-tema", salvo);
  else if (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches)
    raiz.setAttribute("data-tema", "escuro");
  var btn = document.getElementById("alt-tema");
  if (btn)
    btn.addEventListener("click", function () {
      var atual = raiz.getAttribute("data-tema") === "escuro" ? "claro" : "escuro";
      raiz.setAttribute("data-tema", atual);
      localStorage.setItem(chave, atual);
    });

  // --- Progresso de leitura (spec 021) ---
  var corpo = document.body;
  var slug = corpo.getAttribute("data-slug");
  var titulo = corpo.getAttribute("data-titulo");
  var ehIndex = corpo.classList.contains("pagina-index");
  var LANG = corpo.getAttribute("data-lang") || "pt";
  var CHAVE_ULT = "hz_ultimo" + (LANG === "en" ? "_en" : "");

  // Ao abrir um capítulo (não o sumário), grava como "último lido".
  if (slug && !ehIndex && slug !== "sumario") {
    try { localStorage.setItem(CHAVE_ULT, JSON.stringify({ slug: slug, titulo: titulo })); } catch (e) {}
  }

  function mostrarRetomar(u) {
    var card = document.getElementById("ent-retomar");
    var cap = document.getElementById("ent-ret-cap");
    if (!u || !u.slug || !card || !cap) return;
    card.setAttribute("href", u.slug + ".html");
    cap.textContent = u.titulo || u.slug;
    card.hidden = false;
  }

  var local = null;
  try { local = JSON.parse(localStorage.getItem(CHAVE_ULT) || "null"); } catch (e) {}

  // No sumário, popula o card "Retomar" (ou o mantém oculto se não há histórico).
  if (ehIndex) mostrarRetomar(local);

  // --- Espelho do progresso no servidor (spec 080) ---
  // O localStorage continua sendo a fonte IMEDIATA: funciona offline, funciona
  // sem backend, e é o que pinta o card acima sem esperar rede. O servidor é o
  // espelho que atravessa aparelhos e entra em cena depois. `window.COMPANION`
  // é definido por um <script> inline DEPOIS deste arquivo — daí o DOMContentLoaded.
  document.addEventListener("DOMContentLoaded", function () {
    var CFG = window.COMPANION || {};
    var BACKEND = (CFG.backend || "").replace(/\/+$/, "");
    if (!BACKEND) return;
    var sid = "";
    try { sid = localStorage.getItem("cmp_sid") || ""; } catch (e) {}
    if (!sid) return;  // sessão ainda não criada pelo companion: nada a espelhar

    if (slug && !ehIndex && slug !== "sumario") {
      fetch(BACKEND + "/progresso", {
        method: "POST", headers: { "content-type": "application/json" },
        body: JSON.stringify({ session_id: sid, lang: LANG, slug: slug, titulo: titulo || slug })
      }).catch(function () {});
      return;
    }
    if (!ehIndex) return;

    fetch(BACKEND + "/progresso?session_id=" + encodeURIComponent(sid))
      .then(function (r) { return r.json(); })
      .then(function (d) {
        var itens = (d && d.itens) || [];
        for (var i = 0; i < itens.length; i++) {
          if (itens[i].lang !== LANG || !itens[i].slug) continue;
          if (local && local.slug === itens[i].slug) return;   // já é o que está na tela
          mostrarRetomar({ slug: itens[i].slug, titulo: itens[i].titulo });
          try { localStorage.setItem(CHAVE_ULT, JSON.stringify({ slug: itens[i].slug, titulo: itens[i].titulo })); } catch (e) {}
          return;
        }
      })
      .catch(function () {});
  });
})();

// i18n (spec 067): preferência de idioma + convite discreto na capa.
(function () {
  var corpo = document.body;
  var lang = corpo.getAttribute("data-lang") || "pt";
  var pill = document.querySelector(".lang-pill a[data-lang-alvo]");
  if (pill) pill.addEventListener("click", function () {
    try { localStorage.setItem("hz_lang", pill.getAttribute("data-lang-alvo")); } catch (e) {}
  });
  try { localStorage.setItem("hz_lang_visto_" + lang, "1"); } catch (e) {}
  // Convite: só na capa PT, navegador em inglês, sem preferência gravada. Nunca redirect.
  if (!corpo.classList.contains("splash-body") || lang !== "pt") return;
  var pref = null; try { pref = localStorage.getItem("hz_lang"); } catch (e) {}
  var navEn = (navigator.language || "").toLowerCase().indexOf("en") === 0;
  if (pref || !navEn) return;
  var ctas = document.querySelector(".splash-ctas");
  if (!ctas) return;
  var p = document.createElement("p");
  p.className = "lang-sugestao";
  p.innerHTML = '\ud83c\udf10 This book is also available in <a href="en/index.html">English</a>.';
  ctas.parentNode.insertBefore(p, ctas.nextSibling);
})();

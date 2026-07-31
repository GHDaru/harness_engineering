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

  // No sumário, popula o card "Retomar" (ou o mantém oculto se não há histórico).
  if (ehIndex) {
    try {
      var u = JSON.parse(localStorage.getItem(CHAVE_ULT) || "null");
      var card = document.getElementById("ent-retomar");
      var cap = document.getElementById("ent-ret-cap");
      if (u && u.slug && card && cap) {
        card.setAttribute("href", u.slug + ".html");
        cap.textContent = u.titulo || u.slug;
        card.hidden = false;
      }
    } catch (e) {}
  }
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

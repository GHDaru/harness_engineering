// Interações mínimas do site: alternância de tema (persistida) e nada mais.
// As ilhas de visualização React (data-viz) serão hidratadas por um bundle
// próprio na fase P2 — este arquivo permanece dependency-free.
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
})();

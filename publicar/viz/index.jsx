// Ponto de entrada das ilhas de visualização. Encontra cada <div data-viz="...">
// nas páginas geradas e monta o componente React correspondente. Progressive
// enhancement: sem JS, a página mostra as tabelas Markdown estáticas (fallback).
import React from "react";
import { createRoot } from "react-dom/client";
import BenchmarkTabela from "./BenchmarkTabela.jsx";
import Expiracao from "./Expiracao.jsx";

const COMPONENTES = {
  "benchmark-codigo": BenchmarkTabela,
  expiracao: Expiracao,
};

for (const el of document.querySelectorAll("[data-viz]")) {
  const Comp = COMPONENTES[el.getAttribute("data-viz")];
  if (Comp) {
    el.innerHTML = "";
    createRoot(el).render(<Comp />);
  }
}

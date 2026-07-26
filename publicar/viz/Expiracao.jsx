import React, { useState } from "react";
import notas from "./dados.js";

// Registro de expiração (o placar das previsões) com filtro por estado.
const ESTADOS = [
  { emoji: "🔵", rotulo: "aberta" },
  { emoji: "🟡", rotulo: "em movimento" },
  { emoji: "🟢", rotulo: "cumprida" },
  { emoji: "🔴", rotulo: "não-expira" },
];

export default function Expiracao() {
  const [filtro, setFiltro] = useState(null);
  const itens = notas.expiracao.filter((e) => !filtro || e.estado === filtro);
  const contar = (emoji) => notas.expiracao.filter((e) => e.estado === emoji).length;

  return (
    <div className="viz">
      <div className="viz-titulo">Registro de expiração <span className="viz-sub">(o placar das previsões — clique para filtrar)</span></div>
      <div className="viz-filtros">
        <button className={"viz-fbtn" + (filtro === null ? " ativo" : "")} onClick={() => setFiltro(null)}>Todos ({notas.expiracao.length})</button>
        {ESTADOS.map((s) => {
          const n = contar(s.emoji);
          if (!n) return null;
          return (
            <button key={s.emoji} className={"viz-fbtn" + (filtro === s.emoji ? " ativo" : "")} onClick={() => setFiltro(filtro === s.emoji ? null : s.emoji)}>
              {s.emoji} {s.rotulo} ({n})
            </button>
          );
        })}
      </div>
      <div className="viz-cards">
        {itens.map((e, i) => (
          <div key={i} className="viz-card">
            <div className="viz-card-top"><span className="viz-emoji">{e.estado}</span><b>{e.componente}</b></div>
            <div className="viz-card-linha"><span className="viz-rot">existe porque</span> {e.existe}</div>
            <div className="viz-card-linha"><span className="viz-rot">expira quando</span> {e.expira}</div>
            <div className="viz-card-ev">{e.evidencia}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

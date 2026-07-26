import React, { useState } from "react";
import notas, { corNota } from "./dados.js";

// Comparativo interativo dos harnesses de código: tabela ordenável + heatmap.
// Célula colorida por nota (0-3). Clicar no cabeçalho ordena por aquela dimensão.
export default function BenchmarkTabela() {
  const cat = notas.categorias.codigo;
  const dims = notas.dimensoes;
  const [ordem, setOrdem] = useState({ chave: "total", desc: true });

  const linhas = [...cat.harnesses].sort((a, b) => {
    const va = ordem.chave === "total" ? a.total : a.notas[ordem.chave];
    const vb = ordem.chave === "total" ? b.total : b.notas[ordem.chave];
    return ordem.desc ? vb - va : va - vb;
  });

  const ordenar = (chave) =>
    setOrdem((o) => ({ chave, desc: o.chave === chave ? !o.desc : true }));
  const seta = (chave) => (ordem.chave === chave ? (ordem.desc ? " ▾" : " ▴") : "");

  return (
    <div className="viz">
      <div className="viz-titulo">Comparativo — harnesses de código <span className="viz-sub">(notas 0–3 · clique numa coluna para ordenar)</span></div>
      <div className="viz-scroll">
        <table className="viz-heat">
          <thead>
            <tr>
              <th className="viz-esq" onClick={() => ordenar("total")} style={{ cursor: "pointer" }}>Harness{seta("total")}</th>
              {dims.map((d, i) => (
                <th key={i} onClick={() => ordenar(i)} title={d} style={{ cursor: "pointer" }}>{i + 1}{seta(i)}</th>
              ))}
              <th onClick={() => ordenar("total")} style={{ cursor: "pointer" }}>Σ{seta("total")}</th>
            </tr>
          </thead>
          <tbody>
            {linhas.map((h) => (
              <tr key={h.nome}>
                <td className="viz-esq">{h.nome}</td>
                {h.notas.map((n, i) => (
                  <td key={i} className="viz-cel" style={{ background: corNota(n) }} title={`${dims[i]}: ${n}`}>{n}</td>
                ))}
                <td className="viz-total">{h.total}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="viz-legenda">
        {dims.map((d, i) => <span key={i}><b>{i + 1}</b> {d}</span>)}
      </div>
      <div className="viz-escala">
        Escala: {[0,1,2,3].map((n) => <span key={n} className="viz-chip" style={{ background: corNota(n) }}>{n}</span>)}
        <span className="viz-sub">0 ausente · 1 básico · 2 sólido · 3 referência</span>
      </div>
    </div>
  );
}

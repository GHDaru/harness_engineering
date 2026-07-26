// Importa as notas do benchmark em tempo de build (esbuild resolve o JSON),
// então o bundle é autocontido — sem fetch, funciona offline e sob subpath.
import notas from "../../benchmark/notas.json" with { type: "json" };
export default notas;

// Cor por nota 0-3 (escala sequencial legível em claro/escuro via CSS var).
export const corNota = (n) =>
  n === 3 ? "var(--n3)" : n === 2 ? "var(--n2)" : n === 1 ? "var(--n1)" : "var(--n0)";

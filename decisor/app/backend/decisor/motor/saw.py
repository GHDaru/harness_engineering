"""SAW (Simple Additive Weighting), o método aditivo clássico.

Formulação: Hwang & Yoon (1981), LNEMS 186, e Fishburn (1967), Operations
Research 15(3) — ver livro/bibliografia.md. Normalização min-max com inversão
para critérios de custo; escore = soma ponderada dos desempenhos normalizados.
Será o assunto do cap. 04 do livro; o produto o expõe desde já como método v0.

Motor puro: sem I/O, sem banco (constituição, "Restrições" §2).
"""

from decisor.motor.tipos import Problema


def normalizar_minmax(problema: Problema) -> list[list[float]]:
    """r_ij em [0, 1], onde 1 é sempre o melhor desempenho do critério.

    Benefício: r = (x - min) / (max - min) · Custo: r = (max - x) / (max - min).
    Critério em que todas as alternativas empatam não discrimina: r = 0.
    """
    colunas = list(zip(*problema.desempenhos))
    normalizada: list[list[float]] = [[] for _ in problema.alternativas]
    for j, coluna in enumerate(colunas):
        menor, maior = min(coluna), max(coluna)
        amplitude = maior - menor
        for i, x in enumerate(coluna):
            if amplitude == 0:
                r = 0.0
            elif problema.criterios[j].direcao == "beneficio":
                r = (x - menor) / amplitude
            else:
                r = (maior - x) / amplitude
            normalizada[i].append(r)
    return normalizada


def ranquear_saw(problema: Problema) -> list[dict]:
    """Ranking SAW: escore_i = Σ_j w_j · r_ij, em ordem decrescente."""
    if problema.pesos is None:
        raise ValueError("SAW exige pesos (some 1); ver cap. 03 do livro")
    normalizada = normalizar_minmax(problema)
    escores = {
        nome: sum(w * r for w, r in zip(problema.pesos, linha))
        for nome, linha in zip(problema.alternativas, normalizada)
    }
    ordenado = sorted(escores.items(), key=lambda par: par[1], reverse=True)
    return [
        {"posicao": pos, "alternativa": nome, "escore": round(escore, 6)}
        for pos, (nome, escore) in enumerate(ordenado, start=1)
    ]

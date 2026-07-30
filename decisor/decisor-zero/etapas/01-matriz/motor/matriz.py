"""A matriz de decisão — o objeto que todo método MCDA consome.

Formulação clássica de Hwang & Yoon (1981), "Multiple Attribute Decision Making"
(Springer, LNEMS 186), cap. 1: m alternativas, n critérios com direção
(benefício/custo), matriz X[m][n] de desempenhos e pesos w com soma 1.
Ver livro/capitulos/01-problema-multicriterio.md.

Motor puro: sem FastAPI, sem I/O — testável sozinho (regra 2 do decisor-zero).
"""

from dataclasses import dataclass, field

DIRECOES = ("beneficio", "custo")


class ErroDeModelagem(ValueError):
    """A matriz viola a definição do cap. 01 — o erro diz qual regra quebrou."""


@dataclass(frozen=True)
class Criterio:
    nome: str
    direcao: str  # "beneficio" (maior é melhor) ou "custo" (menor é melhor)
    unidade: str = ""

    def __post_init__(self) -> None:
        if self.direcao not in DIRECOES:
            raise ErroDeModelagem(
                f"critério {self.nome!r}: direção {self.direcao!r} inválida "
                f"(use {DIRECOES})"
            )


@dataclass(frozen=True)
class MatrizDecisao:
    """m alternativas × n critérios, com desempenhos e (opcionalmente) pesos."""

    alternativas: list[str]
    criterios: list[Criterio]
    desempenhos: list[list[float]]  # X[i][j]: alternativa i no critério j
    pesos: list[float] | None = field(default=None)

    def __post_init__(self) -> None:
        m, n = len(self.alternativas), len(self.criterios)
        if m == 0 or n == 0:
            raise ErroDeModelagem("é preciso ao menos 1 alternativa e 1 critério")
        if len(self.desempenhos) != m:
            raise ErroDeModelagem(
                f"{m} alternativas, mas {len(self.desempenhos)} linhas de desempenho"
            )
        for i, linha in enumerate(self.desempenhos):
            if len(linha) != n:
                raise ErroDeModelagem(
                    f"linha {i} ({self.alternativas[i]!r}) tem {len(linha)} "
                    f"desempenhos para {n} critérios"
                )
        if self.pesos is not None:
            if len(self.pesos) != n:
                raise ErroDeModelagem(f"{n} critérios, mas {len(self.pesos)} pesos")
            if abs(sum(self.pesos) - 1.0) > 1e-9:
                raise ErroDeModelagem(
                    f"pesos devem somar 1 (somam {sum(self.pesos):.6f})"
                )
            # NOTA didática (cap. 01, exercício): a definição exige w_j >= 0,
            # mas este validador ainda não checa negatividade — complete-o.

    def soma_crua(self) -> dict[str, float]:
        """A agregação ingênua do cap. 01: somar desempenhos sem normalizar.

        Existe só para provar o absurdo — critérios em escalas incomensuráveis
        fazem a soma virar "o preço com ruído" (ver o teste homônimo).
        """
        return {
            nome: float(sum(linha))
            for nome, linha in zip(self.alternativas, self.desempenhos)
        }

    def ranking_por(self, escores: dict[str, float]) -> list[str]:
        """Nomes das alternativas em ordem decrescente de escore."""
        return sorted(escores, key=escores.__getitem__, reverse=True)

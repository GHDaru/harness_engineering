"""O problema multicritério — mesma anatomia da MatrizDecisao do decisor-zero.

m alternativas × n critérios (com direção) + desempenhos + pesos opcionais
(Hwang & Yoon, 1981). Validação idêntica à da etapa 01; aqui em Pydantic porque
o produto recebe o problema pela API e o persiste.
"""

from pydantic import BaseModel, field_validator, model_validator

DIRECOES = ("beneficio", "custo")


class CriterioSpec(BaseModel):
    nome: str
    direcao: str
    unidade: str = ""

    @field_validator("direcao")
    @classmethod
    def direcao_conhecida(cls, valor: str) -> str:
        if valor not in DIRECOES:
            raise ValueError(f"direção {valor!r} inválida (use {DIRECOES})")
        return valor


class Problema(BaseModel):
    alternativas: list[str]
    criterios: list[CriterioSpec]
    desempenhos: list[list[float]]
    pesos: list[float] | None = None

    @model_validator(mode="after")
    def dimensoes_consistentes(self) -> "Problema":
        m, n = len(self.alternativas), len(self.criterios)
        if m == 0 or n == 0:
            raise ValueError("é preciso ao menos 1 alternativa e 1 critério")
        if len(self.desempenhos) != m:
            raise ValueError(f"{m} alternativas, {len(self.desempenhos)} linhas")
        for i, linha in enumerate(self.desempenhos):
            if len(linha) != n:
                raise ValueError(f"linha {i} tem {len(linha)} valores para {n} critérios")
        if self.pesos is not None:
            if len(self.pesos) != n:
                raise ValueError(f"{n} critérios, {len(self.pesos)} pesos")
            if any(w < 0 for w in self.pesos):
                raise ValueError("pesos não podem ser negativos")
            if abs(sum(self.pesos) - 1.0) > 1e-9:
                raise ValueError(f"pesos devem somar 1 (somam {sum(self.pesos):.6f})")
        return self

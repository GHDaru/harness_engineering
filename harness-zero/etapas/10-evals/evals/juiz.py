"""Juiz — LLM-as-judge atrás do LLMPort (cap. 11).

Quando o critério não é binário ("a resposta explicou bem?"), usa-se um
modelo como juiz: recebe pergunta, resposta e critérios, devolve nota e
justificativa. Aqui o juiz fala pelo MESMO LLMPort do harness — com echo
ele demonstra o mecanismo; com uma chave real, julga de verdade.
"""

import json


def julgar(llm, pergunta: str, resposta: str, criterios: list[str]) -> dict:
    prompt = (
        "Você é um juiz de qualidade. Avalie a RESPOSTA para a PERGUNTA "
        "segundo os CRITÉRIOS. Devolva SÓ um JSON {\"nota\": 0-10, \"justificativa\": \"...\"}.\n\n"
        f"PERGUNTA: {pergunta}\nRESPOSTA: {resposta}\nCRITÉRIOS: {'; '.join(criterios)}"
    )
    r = llm.complete([{"role": "user", "content": prompt}], [])
    try:
        return json.loads(r.get("content") or "")
    except (ValueError, TypeError):
        return {"nota": None, "justificativa": "(juiz indisponível — adapter echo? use uma chave real)"}

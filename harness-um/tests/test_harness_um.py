"""Testes do harness-um — todos offline, via ProvedorEco (cap. 11 aplicado a si mesmo)."""

import json

from harness_um import CaixaDeFerramentas, Decisao, Harness, Politica, ProvedorEco, ferramenta
from harness_um.compactacao import Compactador, estimar_tokens
from harness_um.extensao import GerenciadorDeGanchos, carregar_habilidades
from harness_um.loop import LoopDoAgente
from harness_um.mcp import ClienteMCP
from harness_um.memoria import Memoria, Sessao
from harness_um.plano import Plano
from harness_um.provedores import ChamadaDeFerramenta
from harness_um.verificacao import Verificador, python_compila


def harness_eco(tmp_path, **kw):
    return Harness.padrao(tmp_path, provedor=ProvedorEco(), **kw)


# --- loop + ferramentas (caps. 02 e 05) ---

def test_loop_executa_ferramenta_de_ponta_a_ponta(tmp_path):
    (tmp_path / "nota.txt").write_text("o livro vive", encoding="utf-8")
    h = harness_eco(tmp_path)
    resposta = h.conversar('leia @usar ler_arquivo {"caminho": "nota.txt"}')
    assert "o livro vive" in resposta  # o resultado da tool voltou ao modelo e à resposta

def test_loop_responde_texto_sem_ferramenta(tmp_path):
    h = harness_eco(tmp_path)
    assert h.conversar("olá harness").startswith("eco: olá harness")

def test_esquema_derivado_da_assinatura():
    @ferramenta
    def somar(a: int, b: int = 2) -> str:
        """Soma dois inteiros."""
        return str(a + b)
    assert somar.esquema["properties"]["a"]["type"] == "integer"
    assert somar.esquema["required"] == ["a"]
    assert somar.descricao == "Soma dois inteiros."

def test_ferramenta_presa_a_raiz(tmp_path):
    h = harness_eco(tmp_path)
    resultado = h.caixa.executar("ler_arquivo", {"caminho": "../../etc/passwd"})
    assert "fora da raiz" in resultado


# --- permissões (cap. 07) ---

def test_politica_nega_e_o_loop_sobrevive(tmp_path):
    h = harness_eco(tmp_path)
    h.loop.politica.regras["executar_shell"] = Decisao.NEGAR
    resposta = h.conversar('@usar executar_shell {"comando": "rm -rf /"}')
    assert "negada pela política" in resposta

def test_perguntar_sem_aprovador_nega(tmp_path):
    h = harness_eco(tmp_path)  # aprovador default: nega
    resposta = h.conversar('@usar escrever_arquivo {"caminho": "x.txt", "conteudo": "oi"}')
    assert "negada pelo humano" in resposta
    assert not (tmp_path / "x.txt").exists()

def test_aprovador_humano_permite(tmp_path):
    h = harness_eco(tmp_path, aprovador=lambda c: True)
    h.conversar('@usar escrever_arquivo {"caminho": "x.txt", "conteudo": "oi"}')
    assert (tmp_path / "x.txt").read_text(encoding="utf-8") == "oi"


# --- compactação (cap. 04) ---

def test_compactador_resume_e_preserva_a_cauda():
    historico = []
    for i in range(30):
        historico.append({"role": "user", "content": [{"tipo": "texto", "texto": f"pedido {i} " + "x" * 400}]})
        historico.append({"role": "assistant", "content": [{"tipo": "texto", "texto": f"resposta {i} " + "y" * 400}]})
    c = Compactador(limite_tokens=1000, cauda=6)
    assert c.precisa(historico)
    novo = c.compactar(historico)
    assert len(novo) < len(historico)
    assert "resumo de" in str(novo[0]["content"])
    assert novo[0]["role"] == "user" and novo[1]["role"] == "assistant"  # alternância preservada
    assert "resposta 29" in str(novo[-1]["content"])  # cauda intacta
    assert estimar_tokens(novo) < estimar_tokens(historico)


# --- memória e sessões (cap. 08) ---

def test_memoria_anota_e_persiste(tmp_path):
    m = Memoria(tmp_path / "MEMORIA.md")
    m.anotar("preferimos português no domínio")
    assert "português no domínio" in m.ler()

def test_sessao_registra_e_carrega(tmp_path):
    s = Sessao(tmp_path)
    s.registrar({"role": "user", "content": "oi"})
    s.registrar({"role": "assistant", "content": "olá"})
    assert [m["role"] for m in s.carregar()] == ["user", "assistant"]


# --- plano (cap. 09) ---

def test_plano_e_artefato_persistente(tmp_path):
    p = Plano(caminho=tmp_path / "plano.json")
    p.adicionar("escrever o apêndice")
    p.marcar(1, "concluido")
    assert "[x] 1." in p.render()
    assert Plano.carregar(tmp_path / "plano.json").itens[0]["estado"] == "concluido"


# --- subagentes (cap. 10) ---

def test_subagente_isola_contexto_e_devolve_so_o_resultado(tmp_path):
    h = harness_eco(tmp_path)
    antes = len(h.historico)
    resposta = h.conversar('@usar tarefa {"descricao": "investigue o motivo do universo"}')
    assert "investigue o motivo do universo" in resposta  # eco do filho voltou como resultado
    # pai ganhou só: user, assistant(chamada), user(resultado), assistant(final)
    assert len(h.historico) == antes + 4

def test_subagente_nao_muta(tmp_path):
    h = harness_eco(tmp_path)
    resposta = h.conversar('@usar tarefa {"descricao": "@usar escrever_arquivo {\\"caminho\\": \\"mal.txt\\", \\"conteudo\\": \\"x\\"}"}')
    assert not (tmp_path / "mal.txt").exists()
    assert "desconhecida" in resposta or "negada" in resposta  # caixa restrita do filho


# --- verificação (cap. 11) ---

def test_verificador_reporta_python_quebrado(tmp_path):
    h = harness_eco(tmp_path, aprovador=lambda c: True)
    resposta = h.conversar('@usar escrever_arquivo {"caminho": "quebrado.py", "conteudo": "def x(:"}')
    assert "verificação" in resposta and "não compila" in resposta

def test_verificador_silencia_com_python_valido():
    chamada = ChamadaDeFerramenta(id="1", nome="escrever_arquivo",
                                  argumentos={"caminho": "ok.py", "conteudo": "x = 1\n"})
    assert Verificador().verificar(chamada, "escrito") == []


# --- ganchos e habilidades (cap. 12) ---

def test_gancho_veta_ferramenta(tmp_path):
    h = harness_eco(tmp_path, aprovador=lambda c: True)
    h.loop.ganchos.registrar("antes_ferramenta",
                             lambda evento, dados: "sexta-feira: sem deploy" if dados["nome"] == "executar_shell" else None)
    resposta = h.conversar('@usar executar_shell {"comando": "echo oi"}')
    assert "vetada por gancho" in resposta and "sexta-feira" in resposta

def test_habilidades_carregam_e_divulgam_progressivamente(tmp_path):
    skill = tmp_path / "habilidades" / "revisar" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text("# Revisa textos do livro\nPasso 1: ler.\nPasso 2: cortar.", encoding="utf-8")
    h = harness_eco(tmp_path)
    assert "revisar: Revisa textos do livro" in h.montador.montar()  # só a descrição no contexto
    corpo = h.caixa.executar("invocar_habilidade", {"nome": "revisar"})
    assert "Passo 2: cortar." in corpo  # o corpo inteiro, só quando invocada


# --- MCP (cap. 06) ---

def test_cliente_mcp_stateless_vira_ferramenta_comum():
    def transporte_falso(url, corpo, headers):
        assert headers["Mcp-Method"] == corpo["method"]  # espelho da spec 2026-07-28
        assert "initialize" not in corpo["method"]       # núcleo stateless: sem handshake
        if corpo["method"] == "tools/list":
            return {"result": {"tools": [{"name": "clima", "description": "Clima de uma cidade",
                                          "inputSchema": {"type": "object", "properties": {"cidade": {"type": "string"}}}}]}}
        return {"result": {"content": [{"type": "text", "text": f"ensolarado em {corpo['params']['arguments']['cidade']}"}]}}

    cliente = ClienteMCP("http://exemplo/mcp", transporte=transporte_falso)
    ferramentas = cliente.como_ferramentas()
    assert ferramentas[0].nome == "mcp_clima" and ferramentas[0].muta
    assert ferramentas[0].executar(cidade="Curitiba") == "ensolarado em Curitiba"


# --- contexto (cap. 03) ---

def test_contexto_montado_em_camadas_vivas(tmp_path):
    h = harness_eco(tmp_path)
    h.memoria.anotar("fato durável")
    h.plano.adicionar("primeiro passo")
    contexto = h.montador.montar()
    assert "Memória durável" in contexto and "fato durável" in contexto
    assert "Plano atual" in contexto and "primeiro passo" in contexto

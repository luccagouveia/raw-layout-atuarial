# app/src/raw/schema.py

class SituacaoNaoSuportada(Exception):
    pass


# ==========================================================
# SERVIDOR – Layout V1
# Ordem EXATA conforme dicionário PRODAM
# ==========================================================

SERVIDOR_HEADERS_V1 = [

    # Referência
    "NU_ANO",
    "NU_MES",

    # Ente
    "CO_IBGE",
    "NO_ENTE",
    "SG_UF",

    # Massa / Fundo
    "CO_COMP_MASSA",
    "CO_TIPO_FUNDO",

    # Órgão
    "NU_CNPJ_ORGAO",
    "NO_ORGAO",

    # Poder
    "CO_PODER",
    "CO_TIPO_PODER",

    # População
    "CO_TIPO_POPULACAO",

    # Cargo
    "CO_TIPO_CARGO",
    "CO_CRITERIO_ELEGIBILIDADE",

    # Identificação
    "ID_SERVIDOR_MATRICULA",
    "ID_SERVIDOR_CPF",
    "ID_SERVIDOR_PIS_PASEP",

    # Dados pessoais
    "CO_SEXO_SERVIDOR",
    "CO_EST_CIVIL_SERVIDOR",
    "DT_NASC_SERVIDOR",

    # Situação funcional
    "CO_SITUACAO_FUNCIONAL",
    "CO_TIPO_VINCULO",

    # Datas de ingresso
    "DT_ING_SERV_PUB",
    "DT_ING_ENTE",
    "DT_ING_CARREIRA",
    "NO_CARREIRA",
    "DT_ING_CARGO",
    "NO_CARGO",

    # Remuneração
    "VL_BASE_CALCULO",
    "VL_REMUNERACAO",
    "VL_CONTRIBUICAO",

    # Tempos
    "NU_TEMPO_RGPS",
    "NU_TEMPO_RPPS_MUN",
    "NU_TEMPO_RPPS_EST",
    "NU_TEMPO_RPPS_FED",

    # Dependentes
    "NU_DEPENDENTES",

    # Abono
    "IN_ABONO_PERMANENCIA",
    "DT_INICIO_ABONO",

    # Previdência
    "IN_PREV_COMP",
    "VL_TETO_ESPECIFICO",

    # Atuarial
    "DT_PROV_APOSENT"
]


def get_headers(situacao: str, layout_versao: int = 1) -> list:
    """
    Retorna a lista de campos (headers) conforme a situação e versão do layout.
    """

    situacao = situacao.upper()

    if situacao == "SERVIDOR" and layout_versao == 1:
        return SERVIDOR_HEADERS_V1

    raise SituacaoNaoSuportada(
        f"Schema não definido para situação={situacao}, layout_versao={layout_versao}"
    )

# =====================================================
# COLUNAS TERRITORIAIS PADRÃO
# =====================================================
COLUNAS_TERRITORIAIS = [
    "estado",
    "municipio"
]

# =====================================================
# NOMES AMIGÁVEIS DAS COLUNAS
# =====================================================
INDICADORES_MAP_CHAGAS = {

    # UDs
    "uds_pesquisadas": "UDs Pesquisadas",
    "uds_positivas": "UDs Positivas",
    "uds_com_ninfas": "UDs com Presença de Ninfas",
    "uds_apenas_adultos": "UDs com Presença Apenas de Adultos",

    # Localidades
    "localidades_pesquisadas": "Localidades Pesquisadas",
    "localidades_positivas": "Localidades Positivas",

    # Triatomíneos
    "triatomineos_examinados": "Triatomíneos Examinados",
    "triatomineos_infectados": "Triatomíneos Infectados",

    # Indicadores
    "infestacao": "Infestação",
    "dispersao": "Dispersão",
    "colonizacao": "Colonização",
    "taxa_visitacao": "Taxa de Visitação",
    "infeccao_natural": "Infecção Natural"
}

# =====================================================
# CONFIGURAÇÃO DOS INDICADORES
# =====================================================
INDICADORES_FORMULA_CHAGAS = {

    "infestacao": {

        "calculo": "(uds_positivas / uds_pesquisadas) * 100",

        "colunas_kpi": [
            "uds_pesquisadas",
            "uds_positivas"
        ],

        "colunas_tabela": [
            *COLUNAS_TERRITORIAIS,
            "uds_pesquisadas",
            "uds_positivas",
            "infestacao"
        ],

        "group_by": COLUNAS_TERRITORIAIS,

        "agregacoes": {
            "uds_pesquisadas": "sum",
            "uds_positivas": "sum"
        }
    },

    "dispersao": {

        "calculo": "(localidades_positivas / localidades_pesquisadas) * 100",

        "colunas_kpi": [
            "localidades_pesquisadas",
            "localidades_positivas"
        ],

        "colunas_tabela": [
            *COLUNAS_TERRITORIAIS,
            "localidades_pesquisadas",
            "localidades_positivas",
            "dispersao"
        ],

        "group_by": COLUNAS_TERRITORIAIS,

        "agregacoes": {
            "localidades_pesquisadas": "sum",
            "localidades_positivas": "sum"
        }
    },

    "colonizacao": {

        "calculo": "(uds_com_ninfas / uds_positivas) * 100",

        "colunas_kpi": [
            "uds_positivas",
            "uds_com_ninfas"
        ],

        "colunas_tabela": [
            *COLUNAS_TERRITORIAIS,
            "uds_positivas",
            "uds_com_ninfas",
            "colonizacao"
        ],

        "group_by": COLUNAS_TERRITORIAIS,

        "agregacoes": {
            "uds_positivas": "sum",
            "uds_com_ninfas": "sum"
        }
    },

    "taxa_visitacao": {

        "calculo": "(uds_apenas_adultos / uds_positivas) * 100",

        "colunas_kpi": [
            "uds_positivas",
            "uds_apenas_adultos"
        ],

        "colunas_tabela": [
            *COLUNAS_TERRITORIAIS,
            "uds_positivas",
            "uds_apenas_adultos",
            "taxa_visitacao"
        ],

        "group_by": COLUNAS_TERRITORIAIS,

        "agregacoes": {
            "uds_positivas": "sum",
            "uds_apenas_adultos": "sum"
        }
    },

    "infeccao_natural": {

        "calculo": "(triatomineos_infectados / triatomineos_examinados) * 100",

        "colunas_kpi": [
            "triatomineos_examinados",
            "triatomineos_infectados"
        ],

        "colunas_tabela": [
            *COLUNAS_TERRITORIAIS,
            "triatomineos_examinados",
            "triatomineos_infectados",
            "infeccao_natural"
        ],

        "group_by": COLUNAS_TERRITORIAIS,

        "agregacoes": {
            "triatomineos_examinados": "sum",
            "triatomineos_infectados": "sum"
        }
    }
}
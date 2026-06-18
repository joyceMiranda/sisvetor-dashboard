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
INDICADORES_MAP_DENGUE = {

    # Imóveis
    "imoveis_programados": "Imóveis Programados",
    "imoveis_visitados": "Imóveis Visitados",
    "qt_imoveis_fechados_recusas" : "Imóveis Fechados/Recusas",
    "imoveis_fechados_recusas": "Imóveis Fechados/Recusas",

    # Criadouros
    "criadouros_encontrados": "Criadouros Encontrados",

    # Classificação dos Criadouros
    "tipo_criadouro": "Tipo de Criadouro",
    "descricao_criadouro": "Descrição",
    "quantidade_criadouros": "Quantidade",

    # Indicadores
    "cobertura_territorial": "Cobertura Territorial",
    "densidade_criadouros": "Densidade de Criadouros Encontrados",
    "imoveis_fechados_recusas": "Proporção de Imóveis Fechados/Recusas",
    }

INDICADORES_FORMULA_DENGUE = {

    "cobertura_territorial": {

        "calculo": "(imoveis_visitados / imoveis_programados) * 100",

        "colunas_kpi": [
            "imoveis_programados",
            "imoveis_visitados"
        ],

        "colunas_tabela": [
            *COLUNAS_TERRITORIAIS,
            "imoveis_programados",
            "imoveis_visitados",
            "cobertura_territorial"
        ],

        "group_by": [
            "estado",
            "municipio"
        ],

        "agregacoes": {
            "imoveis_programados": "sum",
            "imoveis_visitados": "sum"
        }
    },

    "densidade_criadouros": {

        "calculo": "(criadouros_encontrados / imoveis_visitados) * 100",

        "colunas_kpi": [
            "criadouros_encontrados",
            "imoveis_visitados"
        ],

        "colunas_tabela": [
            *COLUNAS_TERRITORIAIS,
            "criadouros_encontrados",
            "imoveis_visitados",
            "densidade_criadouros"
        ],

        "group_by": [
            "estado",
            "municipio"
        ],

        "agregacoes": {
            "criadouros_encontrados": "sum",
            "imoveis_visitados": "sum"
        }
    },

    "imoveis_fechados_recusas": {

        "calculo": "(qt_imoveis_fechados_recusas / imoveis_visitados) * 100",

        "colunas_kpi": [
            "imoveis_visitados",
            "qt_imoveis_fechados_recusas"
        ],

        "colunas_tabela": [
            *COLUNAS_TERRITORIAIS,
            "imoveis_visitados",
            "qt_imoveis_fechados_recusas",
            "imoveis_fechados_recusas"
        ],

        "group_by": [
            "estado",
            "municipio"
        ],

        "agregacoes": {
            "imoveis_visitados": "sum",
            "qt_imoveis_fechados_recusas": "sum"
        }
    },

}
import streamlit as st
import pandas as pd
import numpy as np


# =====================================================
# FUNÇÃO PRINCIPAL DE CARGA DO DATASET
# =====================================================
# @st.cache_data:
# faz cache no Streamlit para evitar recriar
# o dataset a cada interação do usuário
# =====================================================
@st.cache_data
def load_data():

    # =====================================================
    # SEED FIXA
    # =====================================================
    # garante que os números aleatórios gerados
    # sejam sempre os mesmos
    # útil para manter o mock consistente
    # =====================================================
    np.random.seed(42)

    # =====================================================
    # ESTADOS UTILIZADOS NO MOCK
    # =====================================================
    # apenas estes estados terão dados
    # e aparecerão destacados no mapa
    # =====================================================
    estados = [
        "AM",
        "BA",
        "DF",
        "GO",
        "MG",
        "PA",
        "RO"
    ]

    # =====================================================
    # MAPEAMENTO DAS REGIÕES
    # =====================================================
    # relaciona cada UF à sua região brasileira
    # =====================================================
    regioes_map = {

        "AM": "Norte",

        "BA": "Nordeste",

        "DF": "Centro-Oeste",

        "GO": "Centro-Oeste",

        "MG": "Sudeste",

        "PA": "Norte",

        "RO": "Norte"
    }

    # =====================================================
    # MUNICÍPIOS
    # =====================================================
    # nomes compatíveis com o GeoJSON IBGE
    # utilizado no mapa do Folium
    # =====================================================
    municipios = {

        # =============================================
        # AMAZONAS
        # =============================================
        "AM": [
            "Manaus",
            "Parintins",
            "Itacoatiara"
        ],

        # =============================================
        # BAHIA
        # =============================================
        "BA": [
            "Salvador",
            "Feira de Santana",
            "Vitória da Conquista"
        ],

        # =============================================
        # DISTRITO FEDERAL
        # =============================================
        "DF": [
            "Brasília"
        ],

        # =============================================
        # GOIÁS
        # =============================================
        "GO": [
            "Goiânia",
            "Anápolis",
            "Aparecida de Goiânia"
        ],

        # =============================================
        # MINAS GERAIS
        # =============================================
        "MG": [
            "Belo Horizonte",
            "Uberlândia",
            "Contagem"
        ],

        # =============================================
        # PARÁ
        # =============================================
        "PA": [
            "Belém",
            "Santarém",
            "Marabá"
        ],

        # =============================================
        # RONDÔNIA
        # =============================================
        "RO": [
            "Porto Velho",
            "Ji-Paraná",
            "Ariquemes"
        ]
    }

    # =====================================================
    # ORGANIZAÇÃO SISVETOR
    # =====================================================
    unidade = "Ministério da Saúde"

    # =====================================================
    # SUBUNIDADES / TERRITÓRIOS
    # =====================================================
    # alguns estados possuem mais de um território
    # =====================================================
    subunidades_map = {

        "SES - AM": [
            "Território 1",
            "Território 2"
        ],

        "SES - DF": [
            "Território 3",
            "Território 4"
        ],

        "SES - MG": [
            "Território 5",
            "Território 6"
        ]
    }

    # =====================================================
    # PERÍODOS
    # =====================================================
    # anos e meses utilizados no mock
    # =====================================================
    anos = [2026, 2025, 2024, 2023]

    meses = list(range(1, 13))

    # =====================================================
    # LISTA FINAL DE REGISTROS
    # =====================================================
    data = []

    # =====================================================
    # GERAÇÃO DOS DADOS MOCK
    # =====================================================
    for ano in anos:

        for mes in meses:

            for uf in estados:

                # =========================================
                # REGIÃO DO ESTADO
                # =========================================
                regiao = regioes_map[uf]

                # =========================================
                # MUNICÍPIOS DO ESTADO
                # =========================================
                mun_list = municipios.get(uf)

                # =========================================
                # SUBUNIDADE
                # =========================================
                ses = f"SES - {uf}"

                # =========================================
                # TERRITÓRIOS
                # =========================================
                territorios = subunidades_map.get(
                    ses,
                    ["Território 1"]
                )

                # =========================================
                # LOOP DOS TERRITÓRIOS
                # =========================================
                for territorio in territorios:

                    # =====================================
                    # LOOP DOS MUNICÍPIOS
                    # =====================================
                    for mun in mun_list:

                        # =================================
                        # BASE ALEATÓRIA
                        # =================================
                        # utilizada para gerar indicadores
                        # correlacionados
                        # =================================
                        base = np.random.rand()

                        # =================================
                        # INDICADORES EPIDEMIOLÓGICOS
                        # =================================

                        infestacao = np.clip(
                            base + np.random.normal(0, 0.1),
                            0,
                            1
                        )

                        dispersao = np.clip(
                            base + np.random.normal(0, 0.1),
                            0,
                            1
                        )

                        colonizacao = np.clip(
                            base + np.random.normal(0, 0.1),
                            0,
                            1
                        )

                        infeccao_natural = np.clip(
                            base + np.random.normal(0, 0.1),
                            0,
                            1
                        )

                        taxa_visitacao = np.clip(
                            base + np.random.normal(0, 0.1),
                            0,
                            1
                        )

                        # =================================
                        # UDS PESQUISADAS
                        # =================================
                        uds_pesquisadas = np.random.randint(
                            50,
                            500
                        )

                        # =================================
                        # UDS POSITIVAS
                        # =================================
                        # proporcional ao índice
                        # de infestação
                        # =================================
                        uds_positivas = int(
                            uds_pesquisadas
                            * infestacao
                            * np.random.uniform(0.1, 0.5)
                        )

                        # =================================
                        # ADICIONA REGISTRO AO DATASET
                        # =================================
                        data.append({

                            # -----------------------------
                            # DIMENSÃO TEMPORAL
                            # -----------------------------
                            "data": f"{ano}-{mes:02d}-01",

                            "ano": ano,

                            "mes": mes,

                            # -----------------------------
                            # DIMENSÃO GEOGRÁFICA
                            # -----------------------------
                            "estado": uf,

                            "municipio": mun,

                            "regiao": regiao,

                            # -----------------------------
                            # ESTRUTURA ORGANIZACIONAL
                            # -----------------------------
                            "unidade": unidade,

                            "subunidade": ses,

                            "territorio": territorio,

                            # -----------------------------
                            # INDICADORES
                            # -----------------------------
                            "infestacao": infestacao,

                            "dispersao": dispersao,

                            "colonizacao": colonizacao,

                            "infeccao_natural": infeccao_natural,

                            "taxa_visitacao": taxa_visitacao,

                            # -----------------------------
                            # INDICADORES OPERACIONAIS
                            # -----------------------------
                            "uds_pesquisadas": uds_pesquisadas,

                            "uds_positivas": uds_positivas
                        })

    # =====================================================
    # CONVERSÃO PARA DATAFRAME
    # =====================================================
    df = pd.DataFrame(data)

    # =====================================================
    # RETORNO FINAL
    # =====================================================
    return df
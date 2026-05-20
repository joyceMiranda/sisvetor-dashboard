import streamlit as st
import pandas as pd
import numpy as np


@st.cache_data
def load_data():

    np.random.seed(42)

    # =====================================================
    # ESTADOS
    # =====================================================
    estados = [
        "AC", "AM", "RR", "PA", "AP", "RO", "TO",
        "MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA",
        "MT", "MS", "GO", "DF",
        "MG", "ES", "RJ", "SP",
        "PR", "SC", "RS"
    ]

    regioes_map = {
        "AC": "Norte", "AM": "Norte", "RR": "Norte", "PA": "Norte", "AP": "Norte", "RO": "Norte", "TO": "Norte",
        "MA": "Nordeste", "PI": "Nordeste", "CE": "Nordeste", "RN": "Nordeste",
        "PB": "Nordeste", "PE": "Nordeste", "AL": "Nordeste", "SE": "Nordeste", "BA": "Nordeste",
        "MT": "Centro-Oeste", "MS": "Centro-Oeste", "GO": "Centro-Oeste", "DF": "Centro-Oeste",
        "MG": "Sudeste", "ES": "Sudeste", "RJ": "Sudeste", "SP": "Sudeste",
        "PR": "Sul", "SC": "Sul", "RS": "Sul"
    }

    municipios = {
        "SP": ["São Paulo", "Campinas", "Santos"],
        "RJ": ["Rio de Janeiro", "Niterói", "Petrópolis"],
        "MG": ["Belo Horizonte", "Uberlândia", "Juiz de Fora"],
        "BA": ["Salvador", "Feira de Santana", "Ilhéus"],
        "RS": ["Porto Alegre", "Caxias do Sul", "Pelotas"],
        "PR": ["Curitiba", "Londrina", "Maringá"],
    }

    # =====================================================
    # ORGANIZAÇÃO SISVETOR
    # =====================================================
    unidade = "Ministério da Saúde"

    subunidades_map = {
        "SES - AM": ["Território 1", "Território 2"],
        "SES - DF": ["Território 3", "Território 4"],
        "SES - MG": ["Território 5", "Território 6"],
    }

    # =====================================================
    # PERÍODO
    # =====================================================
    anos = [2026, 2025, 2024, 2023]
    meses = list(range(1, 13))

    data = []

    for ano in anos:
        for mes in meses:
            for uf in estados:

                regiao = regioes_map[uf]

                mun_list = municipios.get(
                    uf,
                    [f"Município {uf} A", f"Município {uf} B"]
                )

                # Define SES baseada no estado
                ses = f"SES - {uf}"

                # Se não existir SES mapeada → usa genérica
                territorios = subunidades_map.get(
                    ses,
                    ["Território 1"]
                )

                for territorio in territorios:
                    for mun in mun_list:

                        base = np.random.rand()

                        infestacao = np.clip(base + np.random.normal(0, 0.1), 0, 1)
                        dispersao = np.clip(base + np.random.normal(0, 0.1), 0, 1)
                        colonizacao = np.clip(base + np.random.normal(0, 0.1), 0, 1)
                        infeccao_natural = np.clip(base + np.random.normal(0, 0.1), 0, 1)
                        taxa_visitacao = np.clip(base + np.random.normal(0, 0.1), 0, 1)

                        uds_pesquisadas = np.random.randint(50, 500)
                        uds_positivas = int(
                            uds_pesquisadas
                            * infestacao
                            * np.random.uniform(0.1, 0.5)
                        )

                        data.append({
                            "data": f"{ano}-{mes:02d}-01",
                            "ano": ano,
                            "mes": mes,
                            "estado": uf,
                            "municipio": mun,
                            "regiao": regiao,

                            # 👇 NOVAS COLUNAS ORGANIZACIONAIS
                            "unidade": unidade,
                            "subunidade": ses,
                            "territorio": territorio,

                            # Indicadores
                            "infestacao": infestacao,
                            "dispersao": dispersao,
                            "colonizacao": colonizacao,
                            "infeccao_natural": infeccao_natural,
                            "taxa_visitacao": taxa_visitacao,
                            "uds_pesquisadas": uds_pesquisadas,
                            "uds_positivas": uds_positivas
                        })

    df = pd.DataFrame(data)

    return df
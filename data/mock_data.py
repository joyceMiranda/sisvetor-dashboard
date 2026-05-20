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

    # =====================================================
    # REGIÕES
    # =====================================================
    regioes_map = {
        "AC": "Norte", "AM": "Norte", "RR": "Norte", "PA": "Norte", "AP": "Norte", "RO": "Norte", "TO": "Norte",
        "MA": "Nordeste", "PI": "Nordeste", "CE": "Nordeste", "RN": "Nordeste",
        "PB": "Nordeste", "PE": "Nordeste", "AL": "Nordeste", "SE": "Nordeste", "BA": "Nordeste",
        "MT": "Centro-Oeste", "MS": "Centro-Oeste", "GO": "Centro-Oeste", "DF": "Centro-Oeste",
        "MG": "Sudeste", "ES": "Sudeste", "RJ": "Sudeste", "SP": "Sudeste",
        "PR": "Sul", "SC": "Sul", "RS": "Sul"
    }

    # =====================================================
    # MUNICÍPIOS (MOCK COMPLETO)
    # =====================================================
    municipios = {
        "AC": ["Rio Branco", "Cruzeiro do Sul", "Sena Madureira"],
        "AM": ["Manaus", "Parintins", "Itacoatiara"],
        "RR": ["Boa Vista", "Rorainópolis", "Caracaraí"],
        "PA": ["Belém", "Santarém", "Ananindeua"],
        "AP": ["Macapá", "Santana", "Laranjal do Jari"],
        "RO": ["Porto Velho", "Ji-Paraná", "Ariquemes"],
        "TO": ["Palmas", "Araguaína", "Gurupi"],

        "MA": ["São Luís", "Imperatriz", "Caxias"],
        "PI": ["Teresina", "Parnaíba", "Picos"],
        "CE": ["Fortaleza", "Sobral", "Juazeiro do Norte"],
        "RN": ["Natal", "Mossoró", "Parnamirim"],
        "PB": ["João Pessoa", "Campina Grande", "Santa Rita"],
        "PE": ["Recife", "Olinda", "Caruaru"],
        "AL": ["Maceió", "Arapiraca", "Palmeira dos Índios"],
        "SE": ["Aracaju", "Itabaiana", "Lagarto"],
        "BA": ["Salvador", "Feira de Santana", "Vitória da Conquista"],

        "MT": ["Cuiabá", "Várzea Grande", "Rondonópolis"],
        "MS": ["Campo Grande", "Dourados", "Três Lagoas"],
        "GO": ["Goiânia", "Anápolis", "Aparecida de Goiânia"],
        "DF": ["Brasília", "Plano Piloto", "Ceilândia"],

        "MG": ["Belo Horizonte", "Uberlândia", "Contagem"],
        "ES": ["Vitória", "Vila Velha", "Serra"],
        "RJ": ["Rio de Janeiro", "Niterói", "Duque de Caxias"],
        "SP": ["São Paulo", "Campinas", "Santos"],

        "PR": ["Curitiba", "Londrina", "Maringá"],
        "SC": ["Florianópolis", "Joinville", "Blumenau"],
        "RS": ["Porto Alegre", "Caxias do Sul", "Pelotas"]
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

    # =====================================================
    # GERAÇÃO DO DATASET
    # =====================================================
    for ano in anos:
        for mes in meses:
            for uf in estados:

                regiao = regioes_map[uf]

                mun_list = municipios.get(uf)

                ses = f"SES - {uf}"

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

                            # organização
                            "unidade": unidade,
                            "subunidade": ses,
                            "territorio": territorio,

                            # indicadores
                            "infestacao": infestacao,
                            "dispersao": dispersao,
                            "colonizacao": colonizacao,
                            "infeccao_natural": infeccao_natural,
                            "taxa_visitacao": taxa_visitacao,
                            "uds_pesquisadas": uds_pesquisadas,
                            "uds_positivas": uds_positivas
                        })

    return pd.DataFrame(data)
import pandas as pd
import numpy as np


def load_data():

    np.random.seed(42)

    estados = ["AM", "BA", "DF", "GO", "MG", "PA", "RO"]

    regioes_map = {
        "AM": "Norte",
        "BA": "Nordeste",
        "DF": "Centro-Oeste",
        "GO": "Centro-Oeste",
        "MG": "Sudeste",
        "PA": "Norte",
        "RO": "Norte"
    }

    municipios = {
        "AM": ["Manaus", "Parintins", "Itacoatiara"],
        "BA": ["Salvador", "Feira de Santana", "Vitória da Conquista"],
        "DF": ["Brasília"],
        "GO": ["Goiânia", "Anápolis", "Aparecida de Goiânia"],
        "MG": ["Belo Horizonte", "Uberlândia", "Contagem"],
        "PA": ["Belém", "Santarém", "Marabá"],
        "RO": ["Porto Velho", "Ji-Paraná", "Ariquemes"]
    }

    subunidades_map = {
        "SES - AM": ["Território 1", "Território 2"],
        "SES - DF": ["Território 3", "Território 4"],
        "SES - MG": ["Território 5", "Território 6"]
    }

    anos = [2026, 2025, 2024, 2023]
    meses = list(range(1, 13))

    indicadores_lista = [
        "infestacao",
        "dispersao",
        "colonizacao",
        "infeccao_natural",
        "taxa_visitacao"
    ]

    data = []

    for ano in anos:
        for mes in meses:
            for uf in estados:

                regiao = regioes_map[uf]
                mun_list = municipios[uf]
                ses = f"SES - {uf}"

                territorios = subunidades_map.get(ses, ["Território 1"])

                for territorio in territorios:
                    for mun in mun_list:

                        base = np.random.rand()

                        registro = {
                            "data": f"{ano}-{mes:02d}-01",
                            "ano": ano,
                            "mes": mes,
                            "estado": uf,
                            "municipio": mun,
                            "regiao": regiao,
                            "unidade": "Ministério da Saúde",
                            "subunidade": ses,
                            "territorio": territorio,
                            "uds_pesquisadas": np.random.randint(50, 500),
                        }

                        # indicadores dinâmicos
                        for ind in indicadores_lista:
                            valor = np.clip(
                                (base + np.random.normal(0, 0.1)) * 100,
                                0,
                                100
                            )
                            registro[ind] = round(valor, 2)

                        # UDs positivas proporcional ao infestacao
                        infestacao = registro["infestacao"]

                        percentual_positividade = np.random.uniform(
                            infestacao * 0.2,
                            infestacao * 0.6
                        )

                        percentual_positividade = min(percentual_positividade, 100)

                        registro["uds_positivas"] = int(
                            registro["uds_pesquisadas"] * percentual_positividade / 100
                        )

                        data.append(registro)

    return pd.DataFrame(data)
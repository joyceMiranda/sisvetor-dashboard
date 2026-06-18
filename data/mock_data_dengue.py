import pandas as pd
import numpy as np


def load_data_dengue():
    """
    Gera um conjunto de dados simulados para o dashboard SISVETOR.

    O dataset contém:
    - Estrutura geográfica (Região > Estado > Município)
    - Estrutura organizacional (Unidade > Subunidade > Território)
    - Variáveis primárias utilizadas nas ações de controle da dengue
    - Indicadores calculados automaticamente

    Retorna:
        pandas.DataFrame
    """

    np.random.seed(42)

    # ==========================================================
    # ESTADOS CONTEMPLADOS NO MOCK
    # ==========================================================
    estados = ["AM", "BA", "DF", "GO", "MG", "PA", "RO"]

    # ==========================================================
    # MAPEAMENTO ESTADO -> REGIÃO
    # ==========================================================
    regioes_map = {
        "AM": "Norte",
        "BA": "Nordeste",
        "DF": "Centro-Oeste",
        "GO": "Centro-Oeste",
        "MG": "Sudeste",
        "PA": "Norte",
        "RO": "Norte"
    }

    # ==========================================================
    # MUNICÍPIOS POR ESTADO
    # ==========================================================
    municipios = {
        "AM": ["Manaus", "Parintins", "Itacoatiara"],
        "BA": ["Salvador", "Feira de Santana", "Vitória da Conquista"],
        "DF": ["Brasília"],
        "GO": ["Goiânia", "Anápolis", "Aparecida de Goiânia"],
        "MG": ["Belo Horizonte", "Uberlândia", "Contagem"],
        "PA": ["Belém", "Santarém", "Marabá"],
        "RO": ["Porto Velho", "Ji-Paraná", "Ariquemes"]
    }

    # ==========================================================
    # CÓDIGOS IBGE DOS MUNICÍPIOS
    # ==========================================================
    municipios_ibge = {
        "Manaus": "1302603",
        "Parintins": "1303403",
        "Itacoatiara": "1301902",
        "Salvador": "2927408",
        "Feira de Santana": "2910800",
        "Vitória da Conquista": "2933307",
        "Brasília": "5300108",
        "Goiânia": "5208707",
        "Anápolis": "5201108",
        "Aparecida de Goiânia": "5201405",
        "Belo Horizonte": "3106200",
        "Uberlândia": "3170206",
        "Contagem": "3118601",
        "Belém": "1501402",
        "Santarém": "1506807",
        "Marabá": "1504208",
        "Porto Velho": "1100205",
        "Ji-Paraná": "1100122",
        "Ariquemes": "1100023"
    }

    # ==========================================================
    # SUBUNIDADES/TERRITÓRIOS
    # ==========================================================
    subunidades_map = {
        "SES - AM": ["Território 1", "Território 2"],
        "SES - DF": ["Território 3", "Território 4"],
        "SES - MG": ["Território 5", "Território 6"]
    }

    # ==========================================================
    # TIPOS DE CRIADOUROS
    # ==========================================================
    tipos_criadouros = [
        {
            "tipo_criadouro": "D1",
            "descricao_criadouro": "Pneus e outros materiais rodantes"
        },
        {
            "tipo_criadouro": "D2",
            "descricao_criadouro": "Lixo e recipientes plásticos"
        },
        {
            "tipo_criadouro": "A2",
            "descricao_criadouro": "Depósito de água ao nível do solo"
        },
        {
            "tipo_criadouro": "A1",
            "descricao_criadouro": "Caixas d'água elevadas"
        },
        {
            "tipo_criadouro": "D3",
            "descricao_criadouro": "Reservatórios móveis"
        },
        {
            "tipo_criadouro": "E1",
            "descricao_criadouro": "Outros tipos de criadouros"
        }
    ]

    # ==========================================================
    # PERÍODO SIMULADO
    # ==========================================================
    anos = [2026, 2025, 2024, 2023]
    meses = list(range(1, 13))

    data = []

    # ==========================================================
    # GERAÇÃO DOS DADOS
    # ==========================================================
    for ano in anos:
        for mes in meses:
            for uf in estados:

                regiao = regioes_map[uf]
                mun_list = municipios[uf]

                ses = f"SES - {uf}"

                territorios = subunidades_map.get(
                    ses,
                    ["Território 1"]
                )

                for territorio in territorios:

                    for mun in mun_list:

                        registro = {
                            "data": f"{ano}-{mes:02d}-01",
                            "ano": ano,
                            "mes": mes,
                            "estado": uf,
                            "municipio": mun,
                            "cod_ibge": municipios_ibge[mun],
                            "regiao": regiao,
                            "unidade": "Ministério da Saúde",
                            "subunidade": ses,
                            "territorio": territorio
                        }

                        # ==================================================
                        # VARIÁVEIS PRIMÁRIAS
                        # ==================================================

                        # Imóveis programados
                        registro["imoveis_programados"] = (
                            np.random.randint(100, 1501)
                        )

                        # Imóveis visitados
                        registro["imoveis_visitados"] = (
                            np.random.randint(
                                int(
                                    registro["imoveis_programados"] * 0.60
                                ),
                                registro["imoveis_programados"] + 1
                            )
                        )

                        # Qtde Imóveis fechados/recusas
                        registro["qt_imoveis_fechados_recusas"] = (
                            np.random.randint(
                                0,
                                int(
                                    registro["imoveis_visitados"] * 0.10
                                ) + 1
                            )
                        )

                        # Imóveis inspecionados
                        registro["imoveis_inspecionados"] = (
                            registro["imoveis_visitados"]
                            - registro["qt_imoveis_fechados_recusas"]
                        )

                        # Criadouros encontrados
                        registro["criadouros_encontrados"] = (
                            np.random.randint(0, 51)
                        )

                        # Classificação dos criadouros
                        for criadouro in tipos_criadouros:

                            registro_tipo = registro.copy()

                            registro_tipo["tipo_criadouro"] = criadouro["tipo_criadouro"]

                            registro_tipo["descricao_criadouro"] = (
                                criadouro["descricao_criadouro"]
                            )

                            registro_tipo["quantidade_criadouros"] = (
                                np.random.randint(
                                    1,
                                    max(
                                        2,
                                        int(registro["criadouros_encontrados"] * 0.30)
                                    )
                                )
                            )

                            registro_tipo["classificacao_criadouros"] = round(
                                np.random.uniform(1, 100),
                                2
                            )

                            # ==================================================
                            # INDICADORES
                            # ==================================================

                            # Cobertura Territorial
                            registro_tipo["cobertura_territorial"] = round(
                                (
                                    registro_tipo["imoveis_visitados"]
                                    /
                                    registro_tipo["imoveis_programados"]
                                ) * 100,
                                2
                            )

                            # Proporção de Imóveis Fechados/Recusas
                            registro_tipo["imoveis_fechados_recusas"] = (
                                round(
                                    (
                                        registro_tipo["qt_imoveis_fechados_recusas"]
                                        /
                                        registro_tipo["imoveis_visitados"]
                                    ) * 100,
                                    2
                                )
                                if registro_tipo["imoveis_visitados"] > 0
                                else 0
                            )

                            # Densidade de Criadouros Encontrados
                            registro_tipo["densidade_criadouros"] = (
                                round(
                                    (
                                        registro_tipo["criadouros_encontrados"]
                                        /
                                        registro_tipo["imoveis_inspecionados"]
                                    ),
                                    4
                                )
                                if registro_tipo["imoveis_inspecionados"] > 0
                                else 0
                            )

                            # Classificação dos Criadouros
                            registro_tipo["classificacao_criadouros"] = (
                                registro_tipo["classificacao_criadouros"]
                            )

                            data.append(registro_tipo)

    # ==========================================================
    # CONVERSÃO PARA DATAFRAME
    # ==========================================================
    df = pd.DataFrame(data)

    return df
import pandas as pd
import numpy as np


def load_data_chagas():
    """
    Gera um conjunto de dados simulados para o dashboard SISVETOR.

    O dataset contém:
    - Estrutura geográfica (Região > Estado > Município)
    - Estrutura organizacional (Unidade > Subunidade > Território)
    - Variáveis primárias utilizadas nos cálculos entomológicos
    - Indicadores calculados automaticamente

    Retorna:
        pandas.DataFrame
    """

    # Define uma semente fixa para que os dados
    # gerados sejam sempre os mesmos em cada execução.
    np.random.seed(14)

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
    # Alguns estados possuem mais de um território.
    # ==========================================================
    subunidades_map = {
        "SES - AM": ["Território 1", "Território 2"],
        "SES - DF": ["Território 3", "Território 4"],
        "SES - MG": ["Território 5", "Território 6"]
    }

    # ==========================================================
    # PERÍODO SIMULADO
    # ==========================================================
    anos = [2026, 2025, 2024, 2023]

    # Meses de janeiro a dezembro
    meses = list(range(1, 13))

    # Lista que armazenará todos os registros
    data = []

    # ==========================================================
    # GERAÇÃO DOS DADOS
    # ==========================================================
    for ano in anos:
        for mes in meses:
            for uf in estados:

                # Obtém a região do estado
                regiao = regioes_map[uf]

                # Obtém municípios do estado
                mun_list = municipios[uf]

                # Nome da subunidade
                ses = f"SES - {uf}"

                # Recupera territórios.
                # Caso o estado não possua configuração,
                # utiliza Território 1 como padrão.
                territorios = subunidades_map.get(
                    ses,
                    ["Território 1"]
                )

                # Percorre todos os territórios
                for territorio in territorios:

                    # Percorre todos os municípios
                    for mun in mun_list:

                        # ==================================================
                        # DADOS CADASTRAIS
                        # ==================================================
                        registro = {
                            "data": f"{ano}-{mes:02d}-01",
                            "ano": ano,
                            "mes": mes,
                            "estado": uf,
                            "municipio": mun,
                            "municipio_ibge": municipios_ibge[mun],
                            "regiao": regiao,
                            "unidade": "Ministério da Saúde",
                            "subunidade": ses,
                            "territorio": territorio
                        }

                        # ==================================================
                        # VARIÁVEIS PRIMÁRIAS
                        # ==================================================

                        # --------------------------------------------------
                        # Número de UDs pesquisadas
                        # --------------------------------------------------
                        registro["uds_pesquisadas"] = np.random.randint(
                            20,
                            401
                        )

                        # --------------------------------------------------
                        # Número de UDs positivas
                        # Entre 5% e 30% das pesquisadas
                        # --------------------------------------------------
                        min_positivas = max(
                            1,
                            int(registro["uds_pesquisadas"] * 0.05)
                        )

                        max_positivas = max(
                            min_positivas + 1,
                            int(registro["uds_pesquisadas"] * 0.30)
                        )

                        registro["uds_positivas"] = np.random.randint(
                            min_positivas,
                            max_positivas
                        )

                        # --------------------------------------------------
                        # Número de localidades pesquisadas
                        #
                        # Sempre menor que UDs pesquisadas.
                        # Entre 10% e 30% das UDs.
                        # --------------------------------------------------
                        max_localidades = max(
                            2,
                            int(registro["uds_pesquisadas"] * 0.30)
                        )

                        registro["localidades_pesquisadas"] = np.random.randint(
                            1,
                            max_localidades + 1
                        )

                        # --------------------------------------------------
                        # Número de localidades positivas
                        # --------------------------------------------------
                        registro["localidades_positivas"] = np.random.randint(
                            0,
                            registro["localidades_pesquisadas"] + 1
                        )

                        # --------------------------------------------------
                        # Número de UDs com presença de ninfas
                        # --------------------------------------------------
                        registro["uds_com_ninfas"] = np.random.randint(
                            0,
                            registro["uds_positivas"] + 1
                        )

                        # --------------------------------------------------
                        # Número de UDs com apenas adultos
                        #
                        # Complemento das UDs positivas.
                        # --------------------------------------------------
                        registro["uds_apenas_adultos"] = (
                            registro["uds_positivas"]
                            - registro["uds_com_ninfas"]
                        )

                        # --------------------------------------------------
                        # Número de triatomíneos examinados
                        #
                        # Valores pequenos e compatíveis
                        # com levantamentos entomológicos.
                        # --------------------------------------------------
                        registro["triatomineos_examinados"] = np.random.randint(
                            1,
                            51
                        )

                        # --------------------------------------------------
                        # Número de triatomíneos infectados
                        #
                        # Máximo de 30% dos examinados.
                        # --------------------------------------------------
                        registro["triatomineos_infectados"] = np.random.randint(
                            0,
                            int(
                                registro["triatomineos_examinados"] * 0.30
                            ) + 1
                        )


                        # ==================================================
                        # INDICADORES ENTOMOLÓGICOS
                        # ==================================================

                        # --------------------------------------------------
                        # Índice de Infestação
                        #
                        # (UDs positivas / UDs pesquisadas) × 100
                        # --------------------------------------------------
                        registro["infestacao"] = round(
                            (
                                registro["uds_positivas"]
                                /
                                registro["uds_pesquisadas"]
                            ) * 100,
                            2
                        )

                        # --------------------------------------------------
                        # Índice de Dispersão
                        #
                        # (Localidades positivas /
                        #  Localidades pesquisadas) × 100
                        # --------------------------------------------------
                        registro["dispersao"] = round(
                            (
                                registro["localidades_positivas"]
                                /
                                registro["localidades_pesquisadas"]
                            ) * 100,
                            2
                        )

                        # --------------------------------------------------
                        # Índice de Colonização
                        #
                        # (UDs com presença de ninfas /
                        #  UDs positivas) × 100
                        # --------------------------------------------------
                        registro["colonizacao"] = (
                            round(
                                (
                                    registro["uds_com_ninfas"]
                                    /
                                    registro["uds_positivas"]
                                ) * 100,
                                2
                            )
                            if registro["uds_positivas"] > 0
                            else 0
                        )

                        # --------------------------------------------------
                        # Índice de Visitação
                        #
                        # (UDs com apenas adultos /
                        #  UDs positivas) × 100
                        # --------------------------------------------------
                        registro["taxa_visitacao"] = (
                            round(
                                (
                                    registro["uds_apenas_adultos"]
                                    /
                                    registro["uds_positivas"]
                                ) * 100,
                                2
                            )
                            if registro["uds_positivas"] > 0
                            else 0
                        )

                        # --------------------------------------------------
                        # Índice de Infecção Natural
                        #
                        # (Triatomíneos infectados /
                        #  Triatomíneos examinados) × 100
                        # --------------------------------------------------
                        registro["infeccao_natural"] = (
                            round(
                                (
                                    registro["triatomineos_infectados"]
                                    /
                                    registro["triatomineos_examinados"]
                                ) * 100,
                                2
                            )
                            if registro["triatomineos_examinados"] > 0
                            else 0
                        )
                        # Adiciona o registro à lista final
                        data.append(registro)

    # ==========================================================
    # CONVERSÃO PARA DATAFRAME
    # ==========================================================
    df = pd.DataFrame(data)

    return df
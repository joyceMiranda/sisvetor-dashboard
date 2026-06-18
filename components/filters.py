import streamlit as st
import pandas as pd
from utils.maps_utils import UF_NOME_MAP


def render_filters(df):

    st.sidebar.title("🔎 Filtros")

    df = df.copy()

    # Converte a coluna "data" para o tipo datetime, permitindo operações e análises temporais.
    df["data"] = pd.to_datetime(df["data"])



    # =====================================================
    # MAPA DE MESES
    # =====================================================
    meses_map = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março",
        4: "Abril", 5: "Maio", 6: "Junho",
        7: "Julho", 8: "Agosto", 9: "Setembro",
        10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }

    """
    # =====================================================
    # MODO DE VISUALIZAÇÃO
    # =====================================================
    with st.sidebar.expander("Escopo da Análise", expanded=True):
        modo = st.radio(
            label="",
            options=["🌎 Visão Territorial"],
            index=0,
            label_visibility="collapsed"
        )
    """


    # =====================================================
    # 🦟 VETOR
    # =====================================================
    with st.sidebar.expander("🔬 Controle Vetorial", expanded=True):

        vetor = st.selectbox(
            "Vetor",
            ["Dengue", "Doença de Chagas"],
            index=1
        )

    # =====================================================
    # 🌎 ABRANGÊNCIA TERRITORIAL
    # =====================================================
    visao = "Nacional"

    with st.sidebar.expander("🌎  Abrangência Territorial ", expanded=True):

        opcoes_visao = ["Nacional", "Regional"]

        visao = st.selectbox(
            "Visão",
            opcoes_visao,
            index=opcoes_visao.index(
            st.session_state["visao"]
            )
        )
    
        st.session_state["visao"] = visao

        if visao == "Regional":

            # =========================
            # REGIÃO
            # =========================
            opcoes_regiao = [
                "Todos",
                "Norte",
                "Nordeste",
                "Centro-Oeste",
                "Sudeste",
                "Sul"
            ]
           
            regiao = st.selectbox(
                    "Região",
                    opcoes_regiao,
                    index=opcoes_regiao.index(st.session_state["regiao"])
                )
            
            st.session_state["regiao"] = regiao


            if regiao != "Todos":
                df = df[df["regiao"] == regiao]

                # =========================
                # ESTADO (SÓ APARECE SE REGIÃO SELECIONADA)
                # =========================
                opcoes_estado = ["Todos"] + sorted(df["estado"].unique())

                estado = st.selectbox(
                    "Estado",
                    opcoes_estado,
                    index=(
                        opcoes_estado.index(st.session_state["estado"])
                        if st.session_state["estado"] in opcoes_estado
                        else 0
                    )
                )

                st.session_state["estado"] = estado

                if estado != "Todos":
                    df = df[df["estado"] == estado]
                    st.session_state["nm_estado"] = UF_NOME_MAP[estado]

                    # =========================
                    # MUNICÍPIO
                    # =========================
                    opcoes_municipio = ["Todos"] + sorted(df["municipio"].unique())

                    municipio = st.selectbox(
                        "Município",
                        opcoes_municipio,
                        index=(
                            opcoes_municipio.index(st.session_state["municipio"])
                            if st.session_state["municipio"] in opcoes_municipio
                            else 0
                        )
                    )

                    st.session_state["municipio"] = municipio

                    if municipio != "Todos":
                        
                        df = df[df["municipio"] == municipio]

                        municipio_ibge = (
                            df[df["municipio"] == municipio]
                            ["municipio_ibge"]
                            .astype(str) #converte para texto
                            .iloc[0] #pega o primeiro valor
                        )
                    
                        st.session_state["municipio_ibge"] = municipio_ibge
                    else:
                        st.session_state["municipio_ibge"] = None

                    
                else:
                    st.session_state["municipio"] = "Todos"
                    st.session_state["municipio_ibge"] = None

            else:
                st.info("Selecione uma região para detalhar estados e municípios.")

        else:
            st.info("Dados agregados do Brasil")

    """
                
    # =====================================================
    # 🏢 ORGANIZAÇÃO SISVETOR
    # =====================================================
    if modo == "🏢 Áreas de Gestão":

        with st.sidebar.expander(
            "🏢 Áreas de Gestão",
            expanded=True
        ):

            if {"unidade", "subunidade", "territorio"}.issubset(df.columns):

                # UNIDADE
                unidades = sorted(df["unidade"].dropna().unique())

                unidade = st.selectbox(
                    "Unidade Organizacional",
                    unidades
                )

                df_unidade = df[df["unidade"] == unidade]

                # SUBUNIDADE
                subunidades_opcoes = sorted(
                    df_unidade["subunidade"].dropna().unique()
                )

                subunidades = st.multiselect(
                    "Subunidades",
                    subunidades_opcoes,
                    default=subunidades_opcoes
                )

                df = df_unidade[
                    df_unidade["subunidade"].isin(subunidades)
                ]

                # TERRITÓRIO (só aparece após unidade)
                territorios_opcoes = sorted(
                    df["territorio"].dropna().unique()
                )

                territorio = st.selectbox(
                    "Território",
                    ["Todos"] + territorios_opcoes
                )

                if territorio != "Todos":
                    df = df[df["territorio"] == territorio]

            else:
                st.warning("Dados organizacionais não disponíveis.")

    """
    # =====================================================
    # PERÍODO
    # =====================================================
    with st.sidebar.expander("📅 Período", expanded=True):

        anos = sorted(df["data"].dt.year.unique(), reverse=True)
        ano = st.selectbox("Ano", anos)

        
        mes_inicio = st.selectbox(
            "Mês inicial",
            list(meses_map.values()),
            index=0
        )

    
        mes_fim = st.selectbox(
            "Mês final",
            list(meses_map.values()),
            index=11
        )

        mes_inicio_num = [k for k, v in meses_map.items() if v == mes_inicio][0]
        mes_fim_num = [k for k, v in meses_map.items() if v == mes_fim][0]

        if mes_inicio_num > mes_fim_num:
            mes_inicio_num, mes_fim_num = mes_fim_num, mes_inicio_num

        df = df[df["data"].dt.year == ano]
        df = df[
            (df["data"].dt.month >= mes_inicio_num)
            & (df["data"].dt.month <= mes_fim_num)
        ]
    

    return df, visao, vetor



import streamlit as st
import pandas as pd


def render_filters(df):

    st.sidebar.title("🔎 Filtros")

    df = df.copy()
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

    
    # =====================================================
    # MODO DE VISUALIZAÇÃO
    # =====================================================
    with st.sidebar.expander("Escopo da Análise", expanded=True):
        modo = st.radio(
            label="",
            options=["🌎 Visão Territorial", "🏢 Áreas de Gestão"],
            index=0,
            label_visibility="collapsed"
        )

   # =====================================================
    # 🌎 VISÃO TERRITORIAL
    # =====================================================
    visao = "Nacional"

    if modo == "🌎 Visão Territorial":

        with st.sidebar.expander("🌎 Visão Territorial", expanded=True):

            visao = st.selectbox(
                "Abrangência",
                ["Nacional", "Regional"]
            )

            if visao == "Regional":

                # =========================
                # REGIÃO
                # =========================
                regiao = st.selectbox(
                    "Região",
                    ["Todos", "Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
                )

                if regiao != "Todos":
                    df = df[df["regiao"] == regiao]

                    # =========================
                    # ESTADO (SÓ APARECE SE REGIÃO SELECIONADA)
                    # =========================
                    estado = st.selectbox(
                        "Estado",
                        ["Todos"] + sorted(df["estado"].unique())
                    )

                    if estado != "Todos":
                        df = df[df["estado"] == estado]

                        # =========================
                        # MUNICÍPIO
                        # =========================
                        municipio = st.selectbox(
                            "Município",
                            ["Todos"] + sorted(df["municipio"].unique())
                        )

                        if municipio != "Todos":
                            df = df[df["municipio"] == municipio]

                else:
                    st.info("Selecione uma região para detalhar estados e municípios.")

            else:
                st.info("Dados agregados do Brasil")
                
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


    # =====================================================
    # PERÍODO
    # =====================================================
    with st.sidebar.expander("📅 Período", expanded=True):

        anos = sorted(df["data"].dt.year.unique(), reverse=True)
        ano = st.selectbox("Ano", anos)

        col1, col2 = st.columns(2)

        with col1:
            mes_inicio = st.selectbox(
                "Mês inicial",
                list(meses_map.values()),
                index=0
            )

        with col2:
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
    

    return df, visao
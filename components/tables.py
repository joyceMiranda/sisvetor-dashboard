import streamlit as st
import pandas as pd


def render_tables(df, INDICADORES_MAP, indicadores):

    df_table = df.copy()

    # =====================================================
    # DEFINE NÍVEL DE AGREGAÇÃO
    # =====================================================
    titulo = "📋 Dados Estratificados"

    estado_foco = st.session_state.get("estado", "Todos")
    municipio_foco = st.session_state.get("municipio", "Todos")

    # =====================================================
    # CONTEXTO TERRITORIAL
    # =====================================================
    agrupamento = ["estado"]

    if estado_foco != "Todos":

        agrupamento = ["municipio"]

        estado_selecionado = (
            f"{st.session_state['nm_estado']} ({estado_foco})"
        )

        if municipio_foco != "Todos":
            municipio_selecionado = municipio_foco
        else:
            municipio_selecionado = None

    else:
        estado_selecionado = None
        municipio_selecionado = None

    # =====================================================
    # CABEÇALHO
    # =====================================================
    st.subheader(titulo)

    if municipio_selecionado:

        st.info(
            f"Município selecionado: "
            f"{municipio_selecionado} ({estado_foco})"
        )

    elif estado_selecionado:

        st.info(
            f"Estado selecionado: "
            f"{estado_selecionado}"
        )

    # =====================================================
    # FILTRA INDICADORES VÁLIDOS
    # =====================================================
    indicadores_validos = [
        i for i in indicadores if i in df_table.columns
    ]

    if not indicadores_validos:
        st.warning("Nenhum indicador válido encontrado.")
        return

    # =====================================================
    # LOOP INDICADORES
    # =====================================================
    for indicador in indicadores_validos:

        agregacoes = {
            "uds_pesquisadas": "sum",
            "uds_positivas": "sum",
            indicador: "mean"
        }

        tabela = (
            df_table
            .groupby(agrupamento, as_index=False)
            .agg(agregacoes)
        )

        nome_indicador = INDICADORES_MAP[indicador]

        tabela.rename(columns={
            "estado": "Estado",
            "municipio": "Município",
            "uds_pesquisadas": "UDs Pesquisadas",
            "uds_positivas": "UDs Positivas",
            indicador: nome_indicador
        }, inplace=True)

        # =====================================================
        # KPIs DINÂMICOS
        # =====================================================
        total_uds_pesquisadas = tabela["UDs Pesquisadas"].sum()
        total_uds_positivas = tabela["UDs Positivas"].sum()
        taxa_indicador = tabela[nome_indicador].mean()

        # formatação
        tabela[nome_indicador] = tabela[nome_indicador].round(2).map(lambda x: f"{x:.2f}%")

        csv = tabela.to_csv(index=False).encode("utf-8-sig")

        # =====================================================
        # EXPANDER
        # =====================================================
        with st.expander(f"📊 {nome_indicador}", expanded=True):

            kpi1, kpi2, kpi3 = st.columns(3)

            with kpi1:
                st.metric("UDs Pesquisadas",
                          f"{total_uds_pesquisadas:,.0f}".replace(",", "."))

            with kpi2:
                st.metric("UDs Positivas",
                          f"{total_uds_positivas:,.0f}".replace(",", "."))

            with kpi3:
                st.metric(nome_indicador,
                          f"{taxa_indicador:.2f}%")


            html_table = tabela.to_html(
                index=False,
                classes="sisvetor-table",
                border=0
            )

            st.markdown(html_table, unsafe_allow_html=True)

            st.download_button(
                "⬇️ Exportar CSV",
                csv,
                file_name=f"{indicador}.csv",
                mime="text/csv",
                width="stretch",
                key=f"download_{indicador}"
            )

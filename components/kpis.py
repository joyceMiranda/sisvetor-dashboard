import streamlit as st

def render_kpis(df):

    #st.title("📊 Indicadores de Desempenho (KPIs) ")

    # =====================================================
    # KPIs
    # =====================================================
    col1, col2 = st.columns(2)

    col1.metric(
        "UDs Pesquisadas",
        int(df["uds_pesquisadas"].sum())
    )

    col2.metric(
        "UDs Positivas",
        int(df["uds_positivas"].sum())
    )
import streamlit as st

def render_kpis(df):

    #st.title("📊 Indicadores de Desempenho (KPIs) ")

    # =====================================================
    # CSS KPIs (FUNDO DESTACADO)
    # =====================================================
    st.markdown("""
        <style>
        div[data-testid="stMetric"] {
            background-color: #f0f6ff;
            padding: 15px;
            border-radius: 12px;
            border: 1px solid #d0e2ff;
            text-align: center;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
        }

        div[data-testid="stMetricValue"] {
            color: #0d6efd;
            font-size: 32px;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

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
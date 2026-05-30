import streamlit as st
import plotly.express as px
import pandas as pd


def render_charts(df, INDICADORES_MAP, indicadores):

    df = df.copy()

    # =========================================================
    # PREPARAÇÃO TEMPORAL
    # =========================================================
    df["data"] = pd.to_datetime(df["data"])
    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.to_period("M").astype(str)

    # =========================================================
    # EVOLUÇÃO MENSAL
    # =========================================================
    st.subheader("📈 Evolução Mensal")

    df_month = df.groupby("mes", as_index=False)[indicadores].mean()

    # cria chart apenas dos indicadores ativos
    rename_map = {k: INDICADORES_MAP[k] for k in indicadores}

    # renomeia dataframe somente para o gráfico
    df_plot = df_month.rename(columns=rename_map)

    fig1 = px.line(
        df_plot,
        x="mes",
        y=list(rename_map.values()),
        markers=True,
        labels={
            "mes": "",  
            "value": "",             
            "label": INDICADORES_MAP.keys()        
        }
    )

    # Remove o prefixo "variable=" exibido pelo Plotly no tooltip (hover)
    fig1.for_each_trace(
        lambda t: t.update(
            hovertemplate=t.hovertemplate.replace("variable=", "")
        )
    )

    

    fig1.update_layout(
        height=350,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.25,
            xanchor="center",
            x=0.5,
            title_text=""
        ),
        margin=dict(
            b=80
        )
    )

    fig1.update_yaxes(ticksuffix="%")

    st.plotly_chart(fig1, use_container_width=True)
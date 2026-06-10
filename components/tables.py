import streamlit as st
import pandas as pd
from utils.maps_utils import COLUNAS_TABLES_KPI
 
# =====================================================
# CONFIGURAÇÃO DOS INDICADORES
# =====================================================
INDICADORES_CONFIG = {
    "infestacao": {
        "formula": "IND = (UDs positivas / UDs pesquisadas) × 100",
        "colunas": [
            "uds_pesquisadas",
            "uds_positivas"
        ],
        "agregacoes": {
            "uds_pesquisadas": "sum",
            "uds_positivas": "sum",
            "infestacao": "mean"
        }
    },

    "dispersao": {
        "formula": "IND = (Localidades positivas / Localidades pesquisadas) × 100",
        "colunas": [
            "localidades_pesquisadas",
            "localidades_positivas"
        ],
        "agregacoes": {
            "localidades_pesquisadas": "sum",
            "localidades_positivas": "sum",
            "dispersao": "mean"
        }
    },

    "colonizacao": {
        "formula": "IND = (UDs com presença de ninfas / UDs positivas) × 100",
        "colunas": [
            "uds_positivas",
            "uds_com_ninfas"
        ],
        "agregacoes": {
            "uds_positivas": "sum",
            "uds_com_ninfas": "sum",
            "colonizacao": "mean"
        }
    },

    "taxa_visitacao": {
        "formula": "IND = (UDs apenas adultos / UDs positivas) × 100",
        "colunas": [
            "uds_positivas",
            "uds_apenas_adultos"
        ],
        "agregacoes": {
            "uds_positivas": "sum",
            "uds_apenas_adultos": "sum",
            "taxa_visitacao": "mean"
        }
    },

    "infeccao_natural": {
        "formula": "IND = (Triatomíneos infectados / Triatomíneos examinados) × 100",
        "colunas": [
            "triatomineos_examinados",
            "triatomineos_infectados"
        ],
        "agregacoes": {
            "triatomineos_examinados": "sum",
            "triatomineos_infectados": "sum",
            "infeccao_natural": "mean"
        }
    }
}


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

    estado_selecionado = None
    municipio_selecionado = None

    if estado_foco != "Todos":

        estado_selecionado = (
            f"{st.session_state['nm_estado']} ({estado_foco})"
        )

        # mantém Estado e Município
        agrupamento = ["estado", "municipio"]

        if municipio_foco != "Todos":
            municipio_selecionado = municipio_foco  

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
        i for i in indicadores
        if i in df_table.columns
    ]

    if not indicadores_validos:
        st.warning("Nenhum indicador válido encontrado.")
        return

    # =====================================================
    # LOOP INDICADORES
    # =====================================================
    for indicador in indicadores_validos:

        config = INDICADORES_CONFIG[indicador]

        # =====================================================
        # AGREGAÇÃO
        # =====================================================
        tabela = (
            df_table
            .groupby(agrupamento, as_index=False)
            .agg(config["agregacoes"])
        )

        nome_indicador = INDICADORES_MAP[indicador]

        

        # =====================================================
        # RENOMEIA COLUNAS
        # =====================================================
        rename_cols = {
            "estado": COLUNAS_TABLES_KPI["estado"],
            "municipio": COLUNAS_TABLES_KPI["municipio"],
            indicador: nome_indicador
        }

        for col in config["colunas"]:
            rename_cols[col] = COLUNAS_TABLES_KPI.get(
                col,
                col.replace("_", " ").title()
            )

        tabela.rename(
            columns=rename_cols,
            inplace=True
        )

        # =====================================================
        # KPIs DINÂMICOS
        # =====================================================
        col1 = config["colunas"][0]
        col2 = config["colunas"][1]

        label1 = COLUNAS_TABLES_KPI[col1]
        label2 = COLUNAS_TABLES_KPI[col2]

        total_campo1 = tabela[label1].sum()
        total_campo2 = tabela[label2].sum()

        taxa_indicador = tabela[nome_indicador].mean()

        # =====================================================
        # FORMATAÇÃO
        # =====================================================
        tabela[nome_indicador] = (
            tabela[nome_indicador]
            .round(2)
            .map(lambda x: f"{x:.2f}%")
        )

        csv = tabela.to_csv(
            index=False
        ).encode("utf-8-sig")

        # =====================================================
        # EXPANDER
        # =====================================================
        with st.expander(
            f"📊 {nome_indicador}",
            expanded=True
        ):
            


            kpi1, kpi2, kpi3 = st.columns(3)

            with kpi1:
                st.metric(
                    label1,
                    f"{total_campo1:,.0f}".replace(",", ".")
                )

            with kpi2:
                st.metric(
                    label2,
                    f"{total_campo2:,.0f}".replace(",", ".")
                )

            with kpi3:
                st.metric(
                    nome_indicador,
                    f"{taxa_indicador:.2f}%"
                )
            
            if st.button(
                "ℹ️ Fórmula",
                key=f"info_{indicador}",
                width="stretch",
                help="Visualizar Fórmula"):
                    mostrar_formula(indicador, nome_indicador)

            html_table = tabela.to_html(
                index=False,
                classes="sisvetor-table",
                border=0
            )

            st.markdown(
                html_table,
                unsafe_allow_html=True
            )

            st.download_button(
                "⬇️ Exportar CSV",
                csv,
                file_name=f"{indicador}.csv",
                mime="text/csv",
                width="stretch",
                help="Fazer Download",
                key=f"download_{indicador}"
            )

@st.dialog("Fórmula do Indicador", width="large")
def mostrar_formula(indicador, nome_indicador):

    config = INDICADORES_CONFIG[indicador]

    st.markdown(f"**{nome_indicador}**")

    st.code(config["formula"])

    '''
    st.markdown("### Variáveis utilizadas")

    for coluna in config["colunas"]:
        st.write(f"• {COLUNAS_TABLES_KPI[coluna]}")
    '''
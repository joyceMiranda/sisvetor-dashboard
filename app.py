import streamlit as st
from data.mock_data import load_data

from components.filters import render_filters
from components.kpis import render_kpis
from components.maps import render_map
from components.charts import render_charts

st.set_page_config(layout="wide")


# =========================================================
# DADOS
# =========================================================
df = load_data()

# =========================================================
# TÍTULO DA PÁGINA
# =========================================================
st.title("SISVETOR - Dashboard")
st.caption("Acompanhamento de Indicadores - Doença de Chagas")

INDICADORES_MAP = {
    "Infestação": "infestacao",
    "Dispersão": "dispersao",
    "Colonização": "colonizacao"
}

indicadores_label = st.multiselect(
    "📊 Indicadores",
    list(INDICADORES_MAP.keys()),
    default=list(INDICADORES_MAP.keys())    
)

indicadores = [INDICADORES_MAP[i] for i in indicadores_label]

# =========================================================
# ESTADO GLOBAL (MAPA → FILTROS)
# =========================================================
if "estado" not in st.session_state:
    st.session_state["estado"] = "Todos"

# =========================================================
# FILTROS
# =========================================================
df_filtered, visao = render_filters(df)

# =========================================================
# APLICA FILTRO DO MAPA (SE HOUVER)
# =========================================================
if st.session_state["estado"] != "Todos":
    df_filtered = df_filtered[df_filtered["estado"] == st.session_state["estado"]]

# =========================================================
# SEGURANÇA
# =========================================================
if df_filtered is None or df_filtered.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

# =========================================================
# INDICE TOTAL
# =========================================================
if not indicadores:
    indicadores = ["infestacao"]

df_filtered["indice_total"] = df_filtered[indicadores].mean(axis=1)

# salva estado global
st.session_state["df_filtered"] = df_filtered

# =========================================================
# KPIs
# =========================================================
render_kpis(df_filtered)

# =========================================================
# LAYOUT
# =========================================================
col_map, col_charts = st.columns([5, 5])

with col_map:
    render_map(df_filtered)

with col_charts:
    render_charts(df_filtered, indicadores)
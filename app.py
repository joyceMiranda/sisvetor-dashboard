import streamlit as st
from data.mock_data import load_data

from components.filters import render_filters
from components.kpis import render_kpis
from components.maps import render_map
from components.charts import render_charts
from utils.maps_utils import NOME_UF_MAP

st.set_page_config(layout="wide")

# =========================================================
# IMPORTAÇÃO CSS
# =========================================================
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("assets/styles.css")


# =========================================================
# DADOS
# =========================================================
df = load_data()

# =========================================================
# TÍTULO DA PÁGINA
# =========================================================
st.title("SISVETOR Chagas — Dashboard de Vigilância Entomológica")
st.caption("")

st.subheader("📊 Indicadores")

INDICADORES_MAP = {
    "infestacao": "Infestação",
    "dispersao": "Dispersão",
    "colonizacao": "Colonização",
    "infeccao_natural": "Infecção Natural",
    "taxa_visitacao": "Taxa de Visitação"
}

indicadores = st.multiselect(
    "",
    options=INDICADORES_MAP,
    default=list(INDICADORES_MAP)[:1],
    format_func=INDICADORES_MAP.get,
    label_visibility="collapsed"
)


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
    map_data = render_map(df_filtered, INDICADORES_MAP, indicadores)

    if map_data and map_data.get("last_active_drawing"):
        props = map_data["last_active_drawing"].get("properties", {})

        nome = props.get("name")

        estado = NOME_UF_MAP.get(nome)

        if estado:
            st.session_state["estado"] = estado
            st.rerun()

with col_charts:
    render_charts(df_filtered, INDICADORES_MAP, indicadores)


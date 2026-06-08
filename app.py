import streamlit as st
from data.mock_data import load_data

from components.filters import render_filters
from components.maps import render_map
from components.charts import render_charts
from utils.maps_utils import NOME_UF_MAP

from components.tables import render_tables

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
#st.caption("")

st.markdown(
    """
    <div class="update-caption">
        ℹ️ Os dados apresentados neste painel são atualizados diariamente às 03:00 (horário de Brasília)
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("📊 Indicadores")

INDICADORES_MAP = {
    "infestacao": "Infestação",
    "dispersao": "Dispersão",
    "colonizacao": "Colonização",
    "infeccao_natural": "Infecção Natural",
    "taxa_visitacao": "Taxa de Visitação"
}

indicadores = st.multiselect(
    label="📊 Indicadores",
    options=INDICADORES_MAP,
    default=list(INDICADORES_MAP),
    format_func=INDICADORES_MAP.get,
    label_visibility="collapsed"
)




# =========================================================
# ESTADO GLOBAL (MAPA → FILTROS)
# =========================================================
if "estado" not in st.session_state:
    st.session_state["estado"] = "Todos"
    st.session_state["nm_estado"] = ""

if "municipio" not in st.session_state:
    st.session_state["municipio"] = "Todos"

if "municipio_ibge" not in st.session_state:
    st.session_state["municipio_ibge"] = None


# =========================================================
# FILTROS
# =========================================================
df_filtered, visao = render_filters(df)

# =========================================================
# APLICA FILTRO DO MAPA (SE HOUVER)
# =========================================================
if st.session_state["estado"] != "Todos":
    df_filtered = df_filtered[
        df_filtered["estado"] == st.session_state["estado"]
    ]

if st.session_state["municipio_ibge"]:

    df_filtered = df_filtered[
        df_filtered["cod_ibge"] ==
        st.session_state["municipio_ibge"]
    ]

# =========================================================
# SEGURANÇA
# =========================================================
if df_filtered is None or df_filtered.empty:
    st.warning("Nenhum dado encontrado para o(s) filtro(s) selecionado(s).")
    if  st.session_state["estado"] != "Todos":
        if st.button("⬅️ Voltar para o Brasil"):
            st.session_state["estado"] = "Todos"
            st.session_state["municipio"] = "Todos"
            st.session_state["municipio_ibge"] = None
            st.rerun()
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
#render_kpis(df_filtered)

# =========================================================
# LAYOUT
# =========================================================
#col_map, col_charts = st.columns([5, 5])

#with col_map:

# =========================================================
# CAPTURA DE CLIQUES - MAPA FOLIUM
# =========================================================

# Renderiza o mapa e recebe os dados da última feição
# (estado ou município) clicada pelo usuário.
map_data = render_map(df_filtered, INDICADORES_MAP, indicadores)

# Verifica se houve clique em algum elemento do mapa.
# O objeto "last_active_drawing" contém os atributos da área selecionada.
if map_data and map_data.get("last_active_drawing"):

    # Recupera as propriedades do polígono clicado
    # (name, id, tooltip, etc.).
    props = map_data["last_active_drawing"].get("properties", {})

    # Nome da área clicada.
    # Exemplo:
    # Estado: "Minas Gerais"
    # Município: "Belo Horizonte"
    nome = props.get("name")

    # Código IBGE da feição clicada.
    # Para municípios corresponde ao código IBGE do município.
    codigo_ibge = props.get("id")

    # =====================================================
    # CLIQUE EM ESTADO (NAVEGAÇÃO BRASIL → ESTADO)
    # =====================================================
    # Se nenhum estado estiver selecionado, o mapa está
    # exibindo o Brasil. Nesse caso o clique representa
    # a seleção de um estado.
    if st.session_state["estado"] == "Todos":

        # Converte o nome do estado para sua UF.
        # Exemplo:
        # "Minas Gerais" -> "MG"
        estado = NOME_UF_MAP.get(nome)

        if estado:

            # Salva a UF selecionada.
            st.session_state["estado"] = estado

            # Salva o nome completo do estado.
            st.session_state["nm_estado"] = nome

            # Recarrega a aplicação para renderizar
            # o mapa no nível estadual.
            st.rerun()

    # =====================================================
    # CLIQUE EM MUNICÍPIO (NAVEGAÇÃO ESTADO → MUNICÍPIO)
    # =====================================================
    # Se já existe um estado selecionado e ainda não existe
    # município selecionado, o clique representa a seleção
    # de um município dentro do estado.
    elif st.session_state["municipio"] == "Todos":

        # Salva o nome do município selecionado.
        st.session_state["municipio"] = nome

        # Salva o código IBGE do município para localizar
        # seu polígono posteriormente.
        st.session_state["municipio_ibge"] = codigo_ibge

        # Recarrega a aplicação para renderizar
        # o mapa focado no município.
        st.rerun()

#with col_charts:
render_charts(df_filtered, INDICADORES_MAP, indicadores)


st.divider()

render_tables(
    df_filtered,
    INDICADORES_MAP,
    indicadores
)


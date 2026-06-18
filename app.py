import streamlit as st
from data.mock_data_chagas import load_data_chagas
from data.mock_data_dengue import load_data_dengue

from components.filters import render_filters
from components.maps import render_map
from components.charts import render_charts

from utils.maps_utils import *
from utils.maps_utils_chagas import *
from utils.maps_utils_dengue import *

from components.tables import render_tables

st.set_page_config(layout="wide")

# =========================================================
# IMPORTAÇÃO CSS
# =========================================================
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("assets/styles.css")

# =====================================================
# INICIALIZAÇÃO 
# =====================================================
if "estado" not in st.session_state:
    st.session_state["estado"] = "Todos"

if "municipio" not in st.session_state:
    st.session_state["municipio"] = "Todos"

if "municipio_ibge" not in st.session_state:
    st.session_state["municipio_ibge"] = None

if "visao" not in st.session_state:
    st.session_state["visao"] = "Nacional"

if "regiao" not in st.session_state:
    st.session_state["regiao"] = "Todos"


# =========================================================
# VETOR PADRÃO
# =========================================================
if "vetor" not in st.session_state:
    st.session_state["vetor"] = vetor = "Doença de Chagas"

# =========================================================
# DADOS
# =========================================================
if st.session_state["vetor"] == "Dengue":
    df = load_data_dengue()
else:
    df = load_data_chagas()

#st.write(df)


# =========================================================
# FILTROS
# =========================================================
df_filtered, visao, vetor = render_filters(df)


# =========================================================
# TROCA DE VETOR
# =========================================================
if vetor != st.session_state["vetor"]:

    st.session_state["vetor"] = vetor

    # limpa navegação do mapa
    st.session_state["estado"] = "Todos"
    st.session_state["municipio"] = "Todos"
    st.session_state["municipio_ibge"] = None

    st.rerun()

# =========================================================
# TÍTULO DA PÁGINA
# =========================================================

st.title("SisVetor — Dashboard de Vigilância Entomológica")

st.markdown(
    f'<div class="caption-destaque">{vetor}</div>',
    unsafe_allow_html=True
)

st.subheader("📊 Indicadores")


if vetor == "Dengue":
    INDICADORES_FORMULA = INDICADORES_FORMULA_DENGUE
    INDICADORES_MAP = INDICADORES_MAP_DENGUE
else:
    INDICADORES_FORMULA = INDICADORES_FORMULA_CHAGAS
    INDICADORES_MAP = INDICADORES_MAP_CHAGAS

indicadores = st.multiselect(
    "📊 Indicadores",
    options=list(INDICADORES_FORMULA.keys()),
    default=list(INDICADORES_FORMULA.keys()),
     format_func=lambda x: INDICADORES_MAP[x],
    label_visibility="collapsed"
)


st.markdown(
    """
    <div class="update-caption">
        ℹ️ Os dados apresentados neste painel são atualizados diariamente às 03:00 (horário de Brasília)
    </div>
    """,
    unsafe_allow_html=True
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
# APLICA FILTRO DO MAPA (SE HOUVER)
# =========================================================
if st.session_state["estado"] != "Todos":
    df_filtered = df_filtered[
        df_filtered["estado"] == st.session_state["estado"]
    ]

if st.session_state["municipio_ibge"]:

    df_filtered = df_filtered[
        df_filtered["municipio_ibge"] ==
        st.session_state["municipio_ibge"]
    ]

# =========================================================
# SEGURANÇA
# =========================================================
if df_filtered is None or df_filtered.empty:
    st.warning("Nenhum dado encontrado para o(s) filtro(s) selecionado(s).")
    if  st.session_state["estado"] != "Todos":
        if st.button("⬅️ Voltar para o Brasil"):
            st.session_state["visao"] = "Nacional"
            st.session_state["regiao"] = "Todos"
            st.session_state["estado"] = "Todos"
            st.session_state["municipio"] = "Todos"
            st.session_state["municipio_ibge"] = None
            st.rerun()
    st.stop()

# salva estado global
st.session_state["df_filtered"] = df_filtered


# =========================================================
# MAPA - CAPTURA DE CLIQUES 
# =========================================================

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
    if st.session_state["estado"] == "Todos":

        # Converte o nome do estado para sua UF.
        # Exemplo:
        # "Minas Gerais" -> "MG"
        estado = NOME_UF_MAP.get(nome)

        if estado:

            st.session_state["visao"] = "Regional"

            # obtém a região do estado clicado
            regiao = (
                df[df["estado"] == estado]
                ["regiao"]
                .iloc[0]
            )

            st.session_state["regiao"] = regiao

            # Salva a UF selecionada.
            st.session_state["estado"] = estado

            # Salva o nome completo do estado.
            st.session_state["nm_estado"] = nome

            st.session_state["municipio"] = "Todos"
            
            st.session_state["municipio_ibge"] = None

            # Recarrega a aplicação para renderizar
            # o mapa no nível estadual.
            st.rerun()

    # =====================================================
    # CLIQUE EM MUNICÍPIO (NAVEGAÇÃO ESTADO → MUNICÍPIO)
    # =====================================================
    elif (st.session_state["municipio"] != nome):

        st.session_state["municipio"] = nome

        st.session_state["municipio_ibge"] = codigo_ibge

        # Recarrega a aplicação para renderizar
        # o mapa focado no município.
        st.rerun()

#with col_charts:
render_charts(df_filtered, INDICADORES_MAP, indicadores)


st.divider()

render_tables(
    df_filtered,
    vetor,
    INDICADORES_MAP,
    INDICADORES_FORMULA,
    indicadores
)


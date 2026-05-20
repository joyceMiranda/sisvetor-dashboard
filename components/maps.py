import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from utils.maps_utils import ESTADO_COORDS, UF_NOME_MAP


# =========================================================
# FUNÇÃO PRINCIPAL
# =========================================================
def render_map(df, INDICADORES_MAP, indicadores):

    st.subheader("🗺️ Monitoramento Nacional")

    # =========================================================
    # BOTÃO VOLTAR (SÓ APARECE QUANDO ESTIVER EM UM ESTADO)
    # =========================================================
    if st.session_state.get("estado", "Todos") != "Todos":
        col_back = st.columns([1])[0]

        with col_back:
            if st.button("⬅️ Voltar para o Brasil"):
                st.session_state["estado"] = "Todos"
                st.rerun()

    # =========================================================
    # GEOJSON DOS ESTADOS
    # é um jeito de guardar informações de localização e mapas usando texto JSON.
    # =========================================================
    geojson_url = (
        "https://raw.githubusercontent.com/"
        "codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
    )

    states_geo = requests.get(geojson_url).json()

    # =========================================================
    # AGREGAÇÃO DINÂMICA
    # =========================================================

    agg_dict = {indicador: "mean" for indicador in indicadores}

    # indicadores operacionais fixos
    agg_dict.update({
        "uds_pesquisadas": "sum",
        "uds_positivas": "sum"
    })

    df_map = df.groupby("estado", as_index=False).agg(agg_dict)

    estado_foco = st.session_state.get("estado", "Todos")

    # =========================================================
    # MAPA BASE (BRASIL CENTRALIZADO)
    # =========================================================
    if estado_foco == "Todos":
        m = folium.Map(
            location=[-14.5, -52],
            zoom_start=4.2,
            tiles="cartodbpositron",
            zoom_control=True
        )
    else:
        lat, lon = ESTADO_COORDS[estado_foco]

        m = folium.Map(
            location=[lat, lon],
            zoom_start=5.8,
            tiles="cartodbpositron",
            zoom_control=True
        )

    # trava navegação fora do país (efeito dashboard)
    m.options["maxBounds"] = [
        [-34.5, -75],   # sudoeste
        [6, -33]        # nordeste
    ]

    # =========================================================
    # MODO BRASIL (TODOS OS ESTADOS)
    # =========================================================
    if estado_foco == "Todos":

        folium.GeoJson(
                states_geo,
                name="Estados",
                style_function=lambda x: {
                    "fillColor": "transparent",
                    "color": "#555",
                    "weight": 1
                },
                highlight_function=lambda x: {
                    "weight": 3,
                    "color": "#003366"
                }
            ).add_to(m)

    # =========================================================
    # MODO ESTADO (SO UM ESTADO)
    # =========================================================
    else:

        estado_nome = UF_NOME_MAP[estado_foco]

        estado_geo = {
            "type": "FeatureCollection",
            "features": [
                f for f in states_geo["features"]
                if f["properties"]["name"] == estado_nome
            ]
        }

        folium.GeoJson(
            estado_geo,
            style_function=lambda x: {
                "fillColor": "#cfe8ff",
                "color": "#003366",
                "weight": 3
            }
        ).add_to(m)

    if estado_foco != "Todos":
        df_map = df_map[df_map["estado"] == estado_foco]

    # =========================================================
    # MARCADORES (BALÃOZINHO TIPO GOOGLE MAPS)
    # =========================================================
    for _, row in df_map.iterrows():

        estado = row["estado"]

        if estado not in ESTADO_COORDS:
            continue

        lat, lon = ESTADO_COORDS[estado]

        # ===============================
        # TOOLTIP DINÂMICO
        # ===============================
        tooltip = f"<b>Estado:</b> {estado}<br>"

        # =========================================================
        # INDICADORES FIXOS
        # =========================================================
        tooltip += f"<b>UDs Pesquisadas:</b> {row['uds_pesquisadas']}<br>"
        tooltip += f"<b>UDs Positivas:</b> {row['uds_positivas']}<br>"

        for indicador in indicadores:

            # =========================================================
            # INDICADORES DINÂMICOS
            # =========================================================
            label = INDICADORES_MAP[indicador]
            valor = row[indicador]

            tooltip += f"<b>{label}:</b> {valor:.2f}<br>"

           

        folium.Marker(
        location=[lat, lon],
        tooltip=tooltip,
        icon=folium.CustomIcon(
            icon_image="https://maps.google.com/mapfiles/ms/icons/red-dot.png",
            icon_size=(18, 18)    
        )
    ).add_to(m)

    # =========================================================
    # RENDER STREAMLIT
    # =========================================================
    map_data = st_folium(
        m,
        width=None,
        height=450,
        returned_objects=["last_active_drawing"]
    )

    # retorna clique para o app
    return map_data
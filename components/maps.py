import streamlit as st
import folium
from streamlit_folium import st_folium
import requests


# =========================================================
# COORDENADAS CENTRAIS DOS ESTADOS
# =========================================================
ESTADO_COORDS = {
    "AC": [-8.77, -70.55], "AL": [-9.62, -36.82], "AP": [1.41, -51.77],
    "AM": [-3.47, -65.10], "BA": [-12.96, -38.51], "CE": [-5.20, -39.53],
    "DF": [-15.83, -47.86], "ES": [-19.19, -40.34], "GO": [-15.98, -49.86],
    "MA": [-4.96, -45.27], "MT": [-12.64, -55.42], "MS": [-20.51, -54.54],
    "MG": [-18.10, -44.38], "PA": [-3.79, -52.48], "PB": [-7.06, -35.55],
    "PR": [-24.89, -51.55], "PE": [-8.28, -35.07], "PI": [-7.71, -42.65],
    "RJ": [-22.84, -43.15], "RN": [-5.22, -36.52], "RS": [-30.01, -51.22],
    "RO": [-10.83, -63.34], "RR": [1.99, -61.33], "SC": [-27.33, -49.44],
    "SP": [-23.55, -46.63], "SE": [-10.90, -37.07], "TO": [-10.25, -48.25]
}


# =========================================================
# FUNÇÃO PRINCIPAL
# =========================================================
def render_map(df, INDICADORES_MAP, indicadores):

    st.subheader("🗺️ Monitoramento Nacional")

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

    # =========================================================
    # MAPA BASE (BRASIL CENTRALIZADO)
    # =========================================================
    m = folium.Map(
        location=[-14.5, -52],   # centro geográfico do Brasil
        zoom_start=4.2,          # 👈 aumenta zoom inicial
        tiles="cartodbpositron",
        zoom_control=True
    )

    # trava navegação fora do país (efeito dashboard)
    m.options["maxBounds"] = [
        [-34.5, -75],   # sudoeste
        [6, -33]        # nordeste
    ]

    # =========================================================
    # CONTORNO DOS ESTADOS
    # =========================================================
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
            "color": "#d62728"
        }
    ).add_to(m)

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

        for indicador in indicadores:
            label = INDICADORES_MAP[indicador]
            valor = row[indicador]

            tooltip += f"<b>{label}:</b> {valor:.2f}<br>"

        folium.Marker(
        location=[lat, lon],
        tooltip=tooltip,
        icon=folium.CustomIcon(
            icon_image="https://maps.google.com/mapfiles/ms/icons/red-dot.png",
            icon_size=(18, 18)   # 👈 tamanho menor
        )
    ).add_to(m)

    # =========================================================
    # RENDER STREAMLIT
    # =========================================================
    st_folium(
        m,
        width=None,   # ocupa toda coluna (controlado no app.py)
        height=450
    )
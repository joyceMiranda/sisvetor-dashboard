import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from utils.maps_utils import ESTADO_COORDS, UF_NOME_MAP, NOME_UF_MAP, UF_IBGE_PREFIX
from shapely.geometry import shape


# =========================================================
# FUNÇÃO PRINCIPAL
# =========================================================
def render_map(df, INDICADORES_MAP, indicadores):

    st.subheader("🗺️ Monitoramento Geográfico")


   
    # =========================================================
    # GEOJSON DOS ESTADOS
    # é um jeito de guardar informações de localização e mapas usando texto JSON.
    # =========================================================
    geojson_url = (
        "https://raw.githubusercontent.com/"
        "codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
    )

    states_geo = requests.get(geojson_url).json()

    estado_foco = st.session_state.get("estado", "Todos")

    municipio_foco = st.session_state.get("municipio", "Todos")

    estado_selecionado = ""

    # =========================================================
    # BOTÃO VOLTAR
    # =========================================================

    if municipio_foco != "Todos" and estado_foco != "Todos":

        st.info(
            f"Município selecionado: {municipio_foco} ({estado_foco})"
        )

        if st.button("⬅️ Voltar para o Estado"):
            st.session_state["municipio"] = "Todos"
            st.session_state["municipio_ibge"] = None
            st.rerun()

    elif estado_foco != "Todos":

        estado_selecionado = (
            st.session_state["nm_estado"]
            + " ("
            + st.session_state["estado"]
            + ")"
        )

        
        st.info(
            f"Estado selecionado: {estado_selecionado}"
        )

        if st.button("⬅️ Voltar para o Brasil"):
            st.session_state["estado"] = "Todos"
            st.rerun()


    # =========================================================
    # MAPA BASE (BRASIL CENTRALIZADO)
    # =========================================================
    #BRASIL
    if estado_foco == "Todos":
        m = folium.Map(
            location=[-14.5, -52],
            zoom_start=4.2,
            tiles="cartodbpositron",
            zoom_control=True
        )
    #ESTADO
    elif municipio_foco == "Todos":
        lat, lon = ESTADO_COORDS[estado_foco]

        m = folium.Map(
            location=[lat, lon],
            zoom_start=6.0,
            tiles="cartodbpositron",
            zoom_control=True
        )
    #MUNICIPIO
    else:

        municipios_url = (
            "https://raw.githubusercontent.com/"
            "tbrugz/geodata-br/master/geojson/geojs-100-mun.json"
        )

        response = requests.get(municipios_url)

        municipios_geo = response.json()

        municipio_geo = {
            "type": "FeatureCollection",
            "features": [
                f
                for f in municipios_geo["features"]
                if f["properties"]["id"]
                == st.session_state["municipio_ibge"]
            ]
        }

        if not municipio_geo["features"]:
            st.error(
                f"Município IBGE {st.session_state['municipio_ibge']} não encontrado."
            )
            return None

        feature = municipio_geo["features"][0]

        #TOOLTIP MUNICÍPIO

        df_municipio = df[
            (df["estado"] == estado_foco)
            & (df["municipio"] == municipio_foco)
        ]

        tooltip = f"<b>Município:</b> {municipio_foco} ({estado_foco})<br>"

        if not df_municipio.empty:

            for indicador in indicadores:
                label = INDICADORES_MAP[indicador]
                valor = df_municipio[indicador].mean()
                tooltip += f"<b>{label}:</b> {valor:.2f}%<br>"

        else:
            tooltip += "<b><i>*Sem dados para análise</i></b>"

        feature["properties"]["tooltip"] = tooltip

        geom = shape(feature["geometry"])
        centroid = geom.centroid

        m = folium.Map(
            location=[centroid.y, centroid.x],
            zoom_start=11,
            tiles="cartodbpositron"
        )
    
        minx, miny, maxx, maxy = geom.bounds

        folium.GeoJson(
            municipio_geo,

            style_function=lambda x: {
                "fillColor": "#ff6b6b",
                "color": "#003366",
                "weight": 4,
                "fillOpacity": 0.45
            },

            tooltip=folium.GeoJsonTooltip(
                fields=["tooltip"],
                aliases=[""],
                sticky=True,
                labels=False,
                localize=True,
                style="""
                    background-color: white;
                    border: 1px solid #666;
                    border-radius: 4px;
                    padding: 8px;
                    font-size: 18px;
                """
            )

        ).add_to(m)

        m.fit_bounds([
            [miny, minx],
            [maxy, maxx]
        ])

    # trava navegação fora do país (efeito dashboard)
    m.options["maxBounds"] = [
        [-34.5, -75],   # sudoeste
        [6, -33]        # nordeste
    ]

    # =========================================================
    # MODO BRASIL (TODOS OS ESTADOS)
    # =========================================================
    if estado_foco == "Todos":

        for feature in states_geo["features"]:

            estado_nome = feature["properties"]["name"]

            uf = NOME_UF_MAP.get(estado_nome)

            if uf:

                df_estado = df[df["estado"] == uf]

                tooltip = f"<b>Estado:</b> {estado_nome} ({uf})<br>"

                if not df_estado.empty:

                    for indicador in indicadores:
                        label = INDICADORES_MAP[indicador]
                        valor = df_estado[indicador].mean() if not df_estado.empty else 0
                        tooltip += f"<b>{label}:</b> {valor:.2f}%<br>"

                else:
                    tooltip += "<b><i>*Sem dados para análise</i></b>"
                    
                feature["properties"]["tooltip"] = tooltip

        folium.GeoJson(
        states_geo,
        name="Estados",

        style_function=lambda feature: {
            "fillColor": (
                "#ff6b6b"
                #lógica para só destacar estados com indicadores com valor
                if not df[
                    df["estado"] == NOME_UF_MAP.get(feature["properties"]["name"])
                ].empty
                else "#cfe8ff"
            ),

            "color": "#555",
            "weight": 1,
            "fillOpacity": 0.45
        },

        highlight_function=lambda x: {
            "weight": 3,
            "color": "#003366"
        },

        tooltip=folium.GeoJsonTooltip(
            fields=["tooltip"],
            aliases=[""],
            sticky=True,
            labels=False,
            localize=True,
            style="""
                background-color: white;
                border: 1px solid #666;
                border-radius: 4px;
                padding: 8px;
                font-size: 18px;
            """
        )
    ).add_to(m)
    # =========================================================
    # MODO ESTADO (SO UM ESTADO)
    # =========================================================
    elif municipio_foco == "Todos":

        estado_nome = UF_NOME_MAP[estado_foco]

        estado_geo = {
            "type": "FeatureCollection",
            "features": [
                f for f in states_geo["features"]
                if f["properties"]["name"] == estado_nome
            ]
        }

        # contorno do estado
        folium.GeoJson(
            estado_geo,
            style_function=lambda x: {
                "fillColor": "#cfe8ff",
                "color": "#003366",
                "weight": 3,
                "fillOpacity": 0.2
            }
        ).add_to(m)

        # =========================================================
        # MUNICÍPIOS DO ESTADO
        # =========================================================
        municipios_url = (
            "https://raw.githubusercontent.com/"
            "tbrugz/geodata-br/master/geojson/geojs-100-mun.json"
        )

        response = requests.get(municipios_url)

        if response.status_code == 200:

            municipios_geo = response.json()

            #st.write(municipios_geo["features"][0]["properties"])

            # filtra apenas municípios do estado selecionado
            municipios_estado = {
                "type": "FeatureCollection",
                "features": [
                    f for f in municipios_geo["features"]
                    if f["properties"]["id"][:2]
                    == UF_IBGE_PREFIX[estado_foco]
                ]
            }

            for feature in municipios_estado["features"]:

                municipio_nome = feature["properties"]["name"]

                df_municipio = df[
                    (df["estado"] == estado_foco)
                    & (df["municipio"] == municipio_nome)
                ]

                tooltip = ""

                tooltip += f"<b>Município:</b> {municipio_nome} ({estado_foco}) <br>"

                if not df_municipio.empty:

                    # =========================================================
                    # INDICADORES DINÂMICOS
                    # =========================================================
                    for indicador in indicadores:

                        label = INDICADORES_MAP[indicador]

                        if not df_municipio.empty:
                            valor = df_municipio[indicador].mean()
                        else:
                            valor = 0

                        tooltip += f"<b>{label}:</b> {valor:.2f}%<br>"

                else:
                    tooltip += "<b><i>*Sem dados para análise</i></b>"

                feature["properties"]["tooltip"] = tooltip
           
            folium.GeoJson(
                municipios_estado,

                style_function=lambda feature: {

                    "fillColor": (
                        "#ff6b6b"
                        if not df[
                            (df["estado"] == estado_foco)
                            & (
                                df["municipio"]
                                == feature["properties"]["name"]
                            )
                        ].empty
                        else "#ffffff"
                    ),

                    "color": "#666",

                    "weight": 1,

                    "fillOpacity": (
                        0.45
                        if not df[
                            (df["estado"] == estado_foco)
                            & (
                                df["municipio"]
                                == feature["properties"]["name"]
                            )
                        ].empty
                        else 0.05
                    )
                },

                highlight_function=lambda feature: {
                    "fillColor": "#4a90e2",
                    "color": "#003366",
                    "weight": 3,
                    "fillOpacity": 0.4
                },

                tooltip=folium.GeoJsonTooltip(
                    fields=["tooltip"],
                    aliases=[""],
                    sticky=True,
                    labels=True,
                    localize=True,
                    style="""
                        background-color: white;
                        border: 1px solid #666;
                        border-radius: 4px;
                        padding: 8px;
                        font-size: 18px;
                    """
                )

            ).add_to(m)
        

    # =========================================================
    # RENDER STREAMLIT
    # =========================================================
    
    map_data = st_folium(
        m,
        width=None,
        height=550,
        returned_objects=["last_active_drawing"]
    )

    # retorna clique para o app
    return map_data
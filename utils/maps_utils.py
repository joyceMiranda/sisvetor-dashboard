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

UF_NOME_MAP = {
    "AC": "Acre",
    "AL": "Alagoas",
    "AP": "Amapá",
    "AM": "Amazonas",
    "BA": "Bahia",
    "CE": "Ceará",
    "DF": "Distrito Federal",
    "ES": "Espírito Santo",
    "GO": "Goiás",
    "MA": "Maranhão",
    "MT": "Mato Grosso",
    "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais",
    "PA": "Pará",
    "PB": "Paraíba",
    "PR": "Paraná",
    "PE": "Pernambuco",
    "PI": "Piauí",
    "RJ": "Rio de Janeiro",
    "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul",
    "RO": "Rondônia",
    "RR": "Roraima",
    "SC": "Santa Catarina",
    "SP": "São Paulo",
    "SE": "Sergipe",
    "TO": "Tocantins"
}

# versão inversa: trocar índice por valor
NOME_UF_MAP = {v: k for k, v in UF_NOME_MAP.items()}



import requests
import streamlit as st

# =========================
# ESTADOS IBGE
# =========================
@st.cache_data
def get_estados():
    """
    Retorna lista de estados IBGE:
    [(sigla, nome), ...]
    """
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"

    r = requests.get(url, timeout=10)

    if r.status_code == 200:
        data = r.json()
        return sorted([(e["sigla"], e["nome"]) for e in data])

    return []


# =========================
# MUNICÍPIOS IBGE
# =========================
@st.cache_data
def get_municipios(uf):
    """
    Retorna municípios de um estado (UF)
    """
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"

    r = requests.get(url, timeout=10)

    if r.status_code == 200:
        return sorted([m["nome"] for m in r.json()])

    return []


# =========================
# REGIÕES (DERIVADAS - IBGE OFICIAL)
# =========================
REGIOES = {
    "Norte": ["AM", "PA", "AC", "RO", "RR", "AP", "TO"],
    "Nordeste": ["MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA"],
    "Centro-Oeste": ["MT", "MS", "GO", "DF"],
    "Sudeste": ["SP", "RJ", "MG", "ES"],
    "Sul": ["PR", "SC", "RS"]
}


def get_regiao(uf):
    """
    Retorna região do estado
    """
    for regiao, ufs in REGIOES.items():
        if uf in ufs:
            return regiao
    return "Desconhecida"
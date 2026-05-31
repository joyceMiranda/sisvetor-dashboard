# 🏛️ SISVETOR Chagas — Dashboard de Vigilância Entomológica

Sistema de monitoramento dos indicadores entomológicos da Doença de Chagas, com visualização territorial, análise temporal e suporte à decisão em saúde pública.

---

## ⚙️ Stack Tecnológica

### 🖥️ Interface

* Streamlit

### 📊 Visualização de dados

* Folium (mapas interativos)
* GeoJSON (limites territoriais)
* Plotly Express (gráficos)

### 🗂️ Processamento de dados

* Pandas
* NumPy

---

## 🌎 Módulos do Sistema

### 📍 Visão Territorial

Hierarquia geográfica:

```
Nacional → Regional → Estado → Município
```

---

### 📊 Indicadores Monitorados

* Infestação
* Dispersão
* Colonização 
* Infecção Natural
* Taxa de Visitação

---

## 🧱 Arquitetura do Projeto

```
app.py
│
├── components/
│   ├── filters.py      # Filtros
│   ├── maps.py         # Mapa interativo  
│   ├── charts.py       # Gráficos  
├── data/
│   └── mock_data.py    # Dados simulados
├── assets/
│   └── style.css       # Customização visual
├── utils/
│   └── maps_utils.py   # dados geográficos
```
---
## 🚀 Execução

```bash
streamlit run app.py
```

---

## 📌 Status do Projeto

🚧 Em desenvolvimento ativo
📊 Foco em expansão de indicadores e adequação de interface


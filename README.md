# 🏛️ SISVETOR Chagas — Dashboard de Vigilância Entomológica

Sistema de monitoramento dos indicadores entomológicos da Doença de Chagas, com visualização territorial, análise temporal e suporte à decisão em saúde pública.

---

## 🧱 Arquitetura do Projeto

```
app.py
│
├── components/
│   ├── filters.py      # Filtros territoriais e organizacionais
│   ├── maps.py         # Mapa interativo (Folium)
│   ├── charts.py       # Gráficos (Plotly)
│   └── kpis.py         # Indicadores resumidos
│
├── data/
│   └── mock_data.py    # Dados simulados
│
├── assets/
│   └── style.css       # Customização visual (UI/UX)
├── utils/
│   └── maps_utils.py   # dados geográficos
```

---

## ⚙️ Stack Tecnológica

### 🖥️ Interface

* Streamlit

### 📊 Visualização de dados

* Plotly Express
* Folium (mapas interativos)
* GeoJSON (limites territoriais)

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

### 🏢 Organização SISVETOR

Estrutura institucional:

```
Unidade → Subunidade → Território
```

---

### 📊 Indicadores Monitorados

* Infestação
* Dispersão
* Colonização 
* Infecção Natural

---

## 🚀 Execução

```bash
streamlit run app.py
```

---

## 📌 Status do Projeto

🚧 Em desenvolvimento ativo
📊 Foco em expansão de indicadores e organização SISVETOR

---

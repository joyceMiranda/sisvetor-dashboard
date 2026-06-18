import streamlit as st
import pandas as pd


def render_tables(df, vetor, INDICADORES_MAP, INDICADORES_FORMULA, indicadores):

    df_table = df.copy()

    # =====================================================
    # DEFINE NÍVEL DE AGREGAÇÃO
    # =====================================================
    titulo = "📋 Dados Estratificados"

    estado_foco = st.session_state.get("estado", "Todos")
    municipio_foco = st.session_state.get("municipio", "Todos")

    # =====================================================
    # CONTEXTO TERRITORIAL
    # =====================================================
    estado_selecionado = None
    municipio_selecionado = None

    if estado_foco != "Todos":

        estado_selecionado = (
            f"{st.session_state['nm_estado']} ({estado_foco})"
        )

        if municipio_foco != "Todos":
            municipio_selecionado = municipio_foco  

    # =====================================================
    # CABEÇALHO
    # =====================================================
    st.subheader(titulo)

    if municipio_selecionado:

        st.info(
            f"Município selecionado: "
            f"{municipio_selecionado} ({estado_foco})"
        )

    elif estado_selecionado:

        st.info(
            f"Estado selecionado: "
            f"{estado_selecionado}"
        )

    # =====================================================
    # PLACEHOLDER DO BOTÃO DE EXPORTAÇÃO
    # =====================================================
    container_exportacao = st.empty()

    # =====================================================
    # TABELAS PARA EXPORTAÇÃO
    # =====================================================
    tabelas_exportacao = []

    # =====================================================
    # PLACEHOLDER DO BOTÃO DE EXPORTAÇÃO
    # =====================================================
    container_exportacao = st.empty()

    # =====================================================
    # FILTRA INDICADORES VÁLIDOS
    # =====================================================
    indicadores_validos = [
        i for i in indicadores
        if i in df_table.columns
    ]

    if not indicadores_validos:
        st.warning("Nenhum indicador válido encontrado.")
        return

    # =====================================================
    # LOOP INDICADORES
    # =====================================================
    for indicador in indicadores_validos:

        formula = INDICADORES_FORMULA[indicador]

        tabela = (
            df_table
            .groupby(formula.get("group_by", []), as_index=False)
            .agg(formula["agregacoes"])
        )

        # =====================================================
        # RECALCULA INDICADOR APLICANDO O CALCULO DEFINIFO NO MAPS_UTILS
        # =====================================================
        if "calculo" in formula:

            tabela[indicador] = (
                tabela.eval(formula["calculo"])
                .replace([float("inf"), -float("inf")], 0)
                .fillna(0)
                .round(2)
            )
     


        nome_indicador = INDICADORES_MAP[indicador]

        # =====================================================
        # KPIs DINÂMICOS
        # =====================================================
        show_kpi = len(formula["colunas_kpi"]) > 0

        if show_kpi:

            kpis = []

            totais = {}

            for coluna in formula["colunas_kpi"]:

                valor = tabela[coluna].sum()

                totais[coluna] = valor

                kpis.append({
                    "coluna": coluna,
                    "label": INDICADORES_MAP[coluna],
                    "valor": valor
                })

            if "calculo" in formula:

                taxa_indicador = (
                    pd.DataFrame([totais])
                    .eval(formula["calculo"])
                    .iloc[0]
                )

            else:

                taxa_indicador = 0

                
        # =====================================================
        # FORMATAÇÃO 
        # =====================================================
        tabela[indicador] = (
            tabela[indicador]
            .round(2)
            .map(lambda x: f"{x:.2f}%") 
        )


        # =====================================================
        # RENOMEIA COLUNAS
        # =====================================================
        rename_cols = {
            "estado": "Estado",
            "municipio": "Município",
            indicador: nome_indicador
        }

        for col in formula["colunas_tabela"]:
            rename_cols[col] = INDICADORES_MAP.get(
                col,
                col.replace("_", " ").title()
            )

        tabela_exibicao = tabela.copy()

        # =====================================================
        # FORMATA COLUNAS NUMÉRICAS PARA EXIBIÇÃO
        # =====================================================        
        for col in tabela_exibicao.select_dtypes(include="number").columns:
            if col != indicador:  # não formata o indicador percentual
                tabela_exibicao[col] = tabela_exibicao[col].apply(
                    lambda x: f"{x:,.0f}".replace(",", ".")
                )

        tabela_exibicao.rename(
            columns=rename_cols,
            inplace=True
        )

        colunas_exibicao = []

        for col in formula["colunas_tabela"]:

            nome_coluna = rename_cols.get(col, col)

            if nome_coluna in tabela_exibicao.columns:
                colunas_exibicao.append(nome_coluna)

        tabela_exibicao = tabela_exibicao[colunas_exibicao]

        tabela_exportacao = tabela_exibicao.copy()

        tabela_exportacao.insert(
            0,
            "Indicador",
            nome_indicador
        )

        tabelas_exportacao.append(tabela_exportacao)

        # =====================================================
        # EXPANDER
        # =====================================================
        with st.expander(
            f"📊 {nome_indicador}",
            expanded=True
        ):
            
            if show_kpi:

                cols = st.columns(
                    len(formula["colunas_kpi"]) + 1
                )

                for i, coluna in enumerate(
                    formula["colunas_kpi"]
                ):

                    valor = tabela[coluna].sum()

                    with cols[i]:

                        st.metric(
                            INDICADORES_MAP[coluna],
                            f"{valor:,.0f}".replace(",", ".")
                        )

                with cols[-1]:

                    st.metric(
                        nome_indicador,
                        f"{taxa_indicador:.2f}%"
                    )
            
            if st.button(
                "ℹ️ Fórmula",
                key=f"info_{indicador}",
                width="stretch",
                help="Visualizar Fórmula"):
                    mostrar_formula(indicador, nome_indicador, INDICADORES_FORMULA)

            html_table = tabela_exibicao.to_html(
                index=False,
                classes="sisvetor-table",
                border=0
            )

            st.markdown(
                html_table,
                unsafe_allow_html=True
            )

    # =====================================================
    # EXPORTAÇÃO CSV
    # =====================================================
    if tabelas_exportacao:

        df_exportacao = pd.concat(
            tabelas_exportacao,
            ignore_index=True,
            sort=False
        )

        csv = df_exportacao.to_csv(
            index=False,
            sep=";"
        ).encode("utf-8-sig")

        container_exportacao.download_button(
            "⬇️ Exportar Todos",
            csv,
            file_name=f"{vetor}_Estado_{estado_foco}_Municipio_{municipio_foco}.csv",
            mime="text/csv",
            width="stretch",
            help="Fazer Download"
        )


@st.dialog("Fórmula do Indicador", width="large")
def mostrar_formula(indicador, nome_indicador, INDICADORES_FORMULA):

    formula = INDICADORES_FORMULA[indicador]

    st.markdown(f"**{nome_indicador}**")

    st.code(formula["calculo"])

    '''
    st.markdown("### Variáveis utilizadas")

    for coluna in config["colunas"]:
        st.write(f"• {COLUNAS_TABLES_KPI[coluna]}")
    '''
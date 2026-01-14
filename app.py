import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da Página
st.set_page_config(
    page_title="One Bank - Dashboard de Análise de Churn",
    page_icon="🏦",
    layout="wide"
)

# Carregamento dos dados
@st.cache_data
def load_data():
    df = pd.read_csv('Customer-Churn-Records.csv')
    return df

df = load_data()


# --- ESTILOS E CORES (Baseado no Notebook) ---
COLOR_CHURN = "#106EBE"  # Azul
COLOR_NO_CHURN = "#0FFCBE"  # Menta
TEMPLATE = "plotly_white"


# --- FUNÇÕES ---
@st.cache_data
def load_data(file):
    if file is not None:
        df = pd.read_csv(file)
    else:
        return None

    # Mapeamento da variável alvo (EXITED) para melhor visualização 
    if 'Exited' in df.columns:
        df['Status'] = df['Exited'].map({0: 'Não Churn', 1: 'Churn'})
    return df


# --- INTERFACE PRINCIPAL ---
st.title("🏦 One Bank - Análise de Churn de Clientes")
st.markdown("""
#### Este dashboard interativo reproduz as análises a luz dos dados do dataset, permitindo explorar como diferentes variáveis impactam a decisão do cliente de sair do banco (**Churn**).
""")


if df is not None:
    # Definição de Variáveis
    target = 'Status'

    # Variáveis Categóricas e Numéricas
    cat_cols = ['Geography', 'Gender', 'HasCrCard', 'IsActiveMember', 'Card Type', 'Complain']
    num_cols = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'EstimatedSalary', 'Satisfaction Score',
                'Point Earned']

    # --- MENU DE NAVEGAÇÃO ---
    analysis_type = st.radio(
        "Selecione o Tipo de Análise:",
        ["Variáveis Categóricas x Churn", "Variáveis Numéricas x Churn"],
        horizontal=True
    )

    st.markdown("---")

    # --- ANÁLISE CATEGÓRICA ---
    if analysis_type == "Variáveis Categóricas x Churn":
        col1, col2 = st.columns([1, 3])

        with col1:
            st.subheader("Configuração")
            selected_cat = st.selectbox("Escolha uma variável categórica:", cat_cols)

            # Cálculo de Taxa de Churn
            churn_rate = df.groupby(selected_cat)['Exited'].mean().sort_values(ascending=False) * 100

            st.write(f"**Taxa de Churn por {selected_cat}:**")
            st.dataframe(churn_rate.apply(lambda x: f"{x:.2f}%"), use_container_width=True)

        with col2:
            st.subheader(f"Distribuição de Churn por {selected_cat}")

            # Gráfico de Barras Empilhadas ou Agrupadas
            fig_cat = px.histogram(
                df,
                x=selected_cat,
                color=target,
                barmode='group',
                color_discrete_map={'Churn': COLOR_CHURN, 'Não Churn': COLOR_NO_CHURN},
                template=TEMPLATE,
                text_auto=True,
                title=f"Contagem de Clientes: {selected_cat} vs Churn"
            )
            fig_cat.update_layout(yaxis_title="Número de Clientes", xaxis_title=selected_cat)
            st.plotly_chart(fig_cat, use_container_width=True)

            # Gráfico de Proporção
            st.markdown(f"**Proporção Relativa (%)**")
            df_prop = pd.crosstab(df[selected_cat], df[target], normalize='index').reset_index()
            fig_prop = px.bar(
                df_prop,
                x=selected_cat,
                y=['Não Churn', 'Churn'],
                color_discrete_map={'Churn': COLOR_CHURN, 'Não Churn': COLOR_NO_CHURN},
                template=TEMPLATE,
                title=f"Percentual de Churn por {selected_cat}"
            )
            fig_prop.update_layout(yaxis_title="Proporção", xaxis_title=selected_cat, legend_title="Status")
            st.plotly_chart(fig_prop, use_container_width=True)

            # --- ANÁLISE NUMÉRICA ---
    elif analysis_type == "Variáveis Numéricas x Churn":
            col1, col2 = st.columns([1, 3])

            with col1:
                st.subheader("Configuração")
                selected_num = st.selectbox("Escolha uma variável numérica:", num_cols)

                # Escolha do tipo de gráfico
                viz_type = st.radio(
                    "Tipo de Visualização:",
                    [
                        "Comparação de Médias (Barras)",
                        "Distribuição (Histograma/Densidade)",
                        "Dispersão (Scatter Plot)",
                        "Detalhado (Boxplot)"
                    ]
                )

                # Estatísticas rápidas
                avg_churn = df[df['Exited'] == 1][selected_num].mean()
                avg_no_churn = df[df['Exited'] == 0][selected_num].mean()
                diff_pct = ((avg_churn - avg_no_churn) / avg_no_churn) * 100

                st.markdown("---")
                st.metric(label=f"Média (Churn)", value=f"{avg_churn:.2f}")
                st.metric(label=f"Média (Não Churn)", value=f"{avg_no_churn:.2f}", delta=f"{diff_pct:.1f}% vs Churn")

            with col2:
                st.subheader(f"Análise de {selected_num} vs Churn")

                # OPÇÃO 1: GRÁFICO DE BARRAS (MÉDIAS)
                if viz_type == "Comparação de Médias (Barras)":
                    st.markdown(
                        f"**O que este gráfico mostra:** Compara o valor médio de *{selected_num}* entre quem saiu e quem ficou.")
                    df_mean = df.groupby(target)[selected_num].mean().reset_index()
                    fig_bar = px.bar(
                        df_mean, x=target, y=selected_num, color=target, text_auto='.2s',
                        color_discrete_map={'Churn': COLOR_CHURN, 'Não Churn': COLOR_NO_CHURN},
                        template=TEMPLATE, title=f"Média de {selected_num} por Status"
                    )
                    fig_bar.update_layout(showlegend=False)
                    st.plotly_chart(fig_bar, use_container_width=True)

                # OPÇÃO 2: HISTOGRAMA / DENSIDADE
                elif viz_type == "Distribuição (Histograma/Densidade)":
                    st.markdown(f"**O que este gráfico mostra:** Onde se concentram a maioria dos clientes.")
                    fig_hist = px.histogram(
                        df, x=selected_num, color=target, barmode="overlay",
                        histnorm='probability density', opacity=0.6,
                        color_discrete_map={'Churn': COLOR_CHURN, 'Não Churn': COLOR_NO_CHURN},
                        template=TEMPLATE, title=f"Distribuição de {selected_num} (Curva de Densidade)"
                    )
                    fig_hist.update_layout(yaxis_title="Densidade / Frequência", xaxis_title=selected_num)
                    st.plotly_chart(fig_hist, use_container_width=True)

                # OPÇÃO 3: SCATTER PLOT 
                elif viz_type == "Dispersão (Scatter Plot)":
                    st.markdown("**Análise de Dispersão:**")
                    scatter_mode = st.radio(
                        "Escolha o modo:",
                        ["Visualizar Distribuição (Strip Plot)", "Cruzar com outra Variável (Scatter Bivariado)"],
                        horizontal=True
                    )

                    if scatter_mode == "Visualizar Distribuição (Strip Plot)":
                        st.markdown(f"*Mostra cada cliente como um ponto. Ajuda a ver a densidade real dos dados.*")
                        fig_strip = px.strip(
                            df, x=target, y=selected_num, color=target, stripmode='overlay',
                            color_discrete_map={'Churn': COLOR_CHURN, 'Não Churn': COLOR_NO_CHURN},
                            template=TEMPLATE, title=f"Distribuição de Pontos: {selected_num}"
                        )
                        st.plotly_chart(fig_strip, use_container_width=True)

                    else:  # Scatter Bivariado
                        st.markdown(f"*Cruze '{selected_num}' com outra variável para encontrar padrões.*")
                        # Remove a variável atual da lista para não comparar com ela mesma
                        other_cols = [c for c in num_cols if c != selected_num]
                        var_y = st.selectbox("Selecione a 2ª Variável (Eixo Y):", other_cols)

                        fig_scat = px.scatter(
                            df, x=selected_num, y=var_y, color=target,
                            color_discrete_map={'Churn': COLOR_CHURN, 'Não Churn': COLOR_NO_CHURN},
                            template=TEMPLATE, opacity=0.6,
                            title=f"Relação: {selected_num} vs {var_y}"
                        )
                        st.plotly_chart(fig_scat, use_container_width=True)

                # OPÇÃO 4: BOXPLOT
                else:
                    st.markdown(f"**O que este gráfico mostra:** Detalhes estatísticos (medianas e quartis).")
                    fig_box = px.box(
                        df, x=target, y=selected_num, color=target,
                        color_discrete_map={'Churn': COLOR_CHURN, 'Não Churn': COLOR_NO_CHURN},
                        template=TEMPLATE, title=f"Boxplot de {selected_num}"
                    )
                    st.plotly_chart(fig_box, use_container_width=True)
# --- RODAPÉ ---
st.markdown("---")
st.markdown("Desenvolvido com Streamlit")

import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da Página
st.set_page_config(
    page_title="One Bank - Dashboard de Análise de Churn",
    page_icon="🏦",
    layout="wide"
)

# --- ESTILOS E CORES ---
COLOR_CHURN = "#DD8452"  # Laranja
COLOR_NO_CHURN = "#4C72B0"  # Azul
TEMPLATE = "plotly_white"

# --- FUNÇÃO DE CARREGAMENTO AUTOMÁTICO ---
@st.cache_data
def load_data():
    # URL pública do dataset (GitHub Raw)
    url = "https://raw.githubusercontent.com/Nagano11/bank_churn/main/Customer-Churn-Records.csv"
    try:
        df = pd.read_csv(url)
        if 'Exited' in df.columns:
            df['Status'] = df['Exited'].map({0: 'Não Churn', 1: 'Churn'})
        return df
    except Exception as e:
        st.error(f"Não foi possível carregar os dados automaticamente. Erro: {e}")
        return None

# --- INTERFACE PRINCIPAL ---
st.title("🏦 One Bank - Análise Bivariada de Churn")
st.markdown("""
Este dashboard carrega automaticamente os dados de Churn bancário para análise exploratória.
""")

# Carrega os dados
df = load_data()

if df is not None:
    # Definição de Variáveis
    target = 'Status'
    cat_cols = ['Geography', 'Gender', 'HasCrCard', 'IsActiveMember', 'Card Type', 'Complain']
    num_cols = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'EstimatedSalary', 'Satisfaction Score', 'Point Earned']

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
            
            # Gráfico de Barras Empilhadas
            fig_cat = px.histogram(
                df, x=selected_cat, color=target, barmode='group',
                color_discrete_map={'Churn': COLOR_CHURN, 'Não Churn': COLOR_NO_CHURN},
                template=TEMPLATE, text_auto=True,
                title=f"Contagem de Clientes: {selected_cat} vs Churn"
            )
            fig_cat.update_layout(yaxis_title="Número de Clientes", xaxis_title=selected_cat)
            st.plotly_chart(fig_cat, use_container_width=True)
            
            # Gráfico de Proporção
            st.markdown(f"**Proporção Relativa (%)**")
            df_prop = pd.crosstab(df[selected_cat], df[target], normalize='index').reset_index()
            fig_prop = px.bar(
                df_prop, x=selected_cat, y=['Não Churn', 'Churn'], 
                color_discrete_map={'Churn': COLOR_CHURN, 'Não Churn': COLOR_NO_CHURN},
                template=TEMPLATE, title=f"Percentual de Churn por {selected_cat}"
            )
            fig_prop.update_layout(yaxis_title="Proporção", xaxis_title=selected_cat, legend_title="Status")
            st.plotly_chart(fig_prop, use_container_width=True)

    # --- ANÁLISE NUMÉRICA ---
    elif analysis_type == "Variáveis Numéricas x Churn":
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.subheader("Configuração")
            selected_num = st.selectbox("Escolha uma variável numérica:", num_cols)
            
            viz_type = st.radio(
                "Tipo de Visualização:",
                ["Comparação de Médias (Barras)", "Distribuição (Histograma/Densidade)", "Dispersão (Scatter Plot)", "Detalhado (Boxplot)"]
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
            
            if viz_type == "Comparação de Médias (Barras)":
                df_mean = df.groupby(target)[selected_num].mean().reset_index()
                fig_bar = px.bar(
                    df_mean, x=target, y=selected_num, color=target, text_auto='.2s',
                    color_discrete_map={'Churn': COLOR_CHURN, 'Não Churn': COLOR_NO_CHURN},
                    template=TEMPLATE, title=f"Média de {selected_num} por Status"
                )
                fig_bar.update_layout(showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)

            elif viz_type == "Distribuição (Histograma/Densidade)":
                fig_hist = px.histogram(
                    df, x=selected_num, color=target, barmode="overlay", 
                    histnorm='probability density', opacity=0.6,
                    color_discrete_map={'Churn': COLOR_CHURN, 'Não Churn': COLOR_NO_CHURN},
                    template=TEMPLATE, title=f"Distribuição de {selected_num}"
                )
                st.plotly_chart(fig_hist, use_container_width=True)

            elif viz_type == "Dispersão (Scatter Plot)":
                scatter_mode = st.radio("Modo:", ["Strip Plot", "Scatter Bivariado"], horizontal=True)
                if scatter_mode == "Strip Plot":
                    fig_strip = px.strip(
                        df, x=target, y=selected_num, color=target, stripmode='overlay',
                        color_discrete_map={'Churn': COLOR_CHURN, 'Não Churn': COLOR_NO_CHURN},
                        template=TEMPLATE, title=f"Distribuição de Pontos: {selected_num}"
                    )
                    st.plotly_chart(fig_strip, use_container_width=True)
                else:
                    other_cols = [c for c in num_cols if c != selected_num]
                    var_y = st.selectbox("Selecione a 2ª Variável (Eixo Y):", other_cols)
                    fig_scat = px.scatter(
                        df, x=selected_num, y=var_y, color=target,
                        color_discrete_map={'Churn': COLOR_CHURN, 'Não Churn': COLOR_NO_CHURN},
                        template=TEMPLATE, opacity=0.6, title=f"{selected_num} vs {var_y}"
                    )
                    st.plotly_chart(fig_scat, use_container_width=True)

            else:
                fig_box = px.box(
                    df, x=target, y=selected_num, color=target,
                    color_discrete_map={'Churn': COLOR_CHURN, 'Não Churn': COLOR_NO_CHURN},
                    template=TEMPLATE, title=f"Boxplot de {selected_num}"
                )
                st.plotly_chart(fig_box, use_container_width=True)

# --- RODAPÉ ---
st.markdown("---")
st.markdown("Desenvolvido com Streamlit • Dados carregados via GitHub [One Bank]")

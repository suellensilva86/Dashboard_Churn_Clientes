import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title="Dashboard de Churn de Clientes", layout="wide")

# Carregamento dos dados
@st.cache_data
def load_data():
    df = pd.read_csv('data/Customer-Churn-Records.csv')
    return df

df = load_data()

# Título do Dashboard
st.title("📊 Dashboard de Análise de Churn (Retenção de Clientes)")
st.markdown("Esta aplicação analisa o comportamento dos clientes e identifica padrões de cancelamento (churn).")

# SIDEBAR (Filtros)
st.sidebar.header("Filtros")
geography = st.sidebar.multiselect(
    "Selecione o País:",
    options=df["Geography"].unique(),
    default=df["Geography"].unique()
)

gender = st.sidebar.multiselect(
    "Selecione o Gênero:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

card_type = st.sidebar.multiselect(
    "Tipo de Cartão:",
    options=df["Card Type"].unique(),
    default=df["Card Type"].unique()
)

# Aplicando filtros
df_selection = df.query(
    "Geography == @geography & Gender == @gender & `Card Type` == @card_type"
)

#  MÉTRICAS PRINCIPAIS
total_clientes = df_selection.shape[0]
churn_percent = (df_selection["Exited"].mean() * 100)
media_satisfaction = df_selection["Satisfaction Score"].mean()
media_balance = df_selection["Balance"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Clientes", f"{total_clientes}")
col2.metric("Taxa de Churn", f"{churn_percent:.1f}%")
col3.metric("Satisfação Média", f"{media_satisfaction:.2f} / 5")
col4.metric("Saldo Médio", f"${media_balance:,.2f}")

st.markdown("""---""")

# GRÁFICOS
col_left, col_right = st.columns(2)

# Churn por Geografia
with col_left:
    st.subheader("Churn por País")
    churn_geo = df_selection.groupby("Geography")["Exited"].mean().reset_index()
    fig_geo = px.bar(churn_geo, x="Geography", y="Exited",
                     title="Taxa de Churn por Localização",
                     labels={"Exited": "Taxa de Churn", "Geography": "País"},
                     color="Geography", text_auto='.2%')
    st.plotly_chart(fig_geo, use_container_width=True)

# Distribuição de Idade por Churn
with col_right:
    st.subheader("Distribuição de Idade")
    fig_age = px.histogram(df_selection, x="Age", color="Exited",
                           title="Idade vs. Churn (0=Ficou, 1=Saiu)",
                           nbins=30, barmode="group",
                           color_discrete_map={0: "#636EFA", 1: "#EF553B"})
    st.plotly_chart(fig_age, use_container_width=True)

col_left2, col_right2 = st.columns(2)

# Churn por Tipo de Cartão
with col_left2:
    st.subheader("Churn por Tipo de Cartão")
    fig_card = px.pie(df_selection, names="Card Type", values="Exited",
                      title="Proporção de Churn por Categoria de Cartão",
                      hole=0.4)
    st.plotly_chart(fig_card, use_container_width=True)

# Score de Crédito vs Salário Estimado
with col_right2:
    st.subheader("Crédito vs Salário")
    fig_scatter = px.scatter(df_selection.sample(min(len(df_selection), 1000)),
                             x="CreditScore", y="EstimatedSalary",
                             color="Exited", size="Age",
                             title="Amostra: Crédito vs Salário (Tamanho = Idade)",
                             opacity=0.6)
    st.plotly_chart(fig_scatter, use_container_width=True)

# TABELA DE DADOS
if st.checkbox("Mostrar Dados Brutos"):
    st.dataframe(df_selection)
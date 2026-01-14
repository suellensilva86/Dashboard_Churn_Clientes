# 🏦 One Bank - Dashboard de Análise de Churn

Este projeto consiste em um dashboard interativo desenvolvido em **Python** e **Streamlit** para realizar a Análise Exploratória de Dados (EDA) de clientes bancários. O foco principal é investigar o comportamento de **Churn** (evasão de clientes), permitindo visualizar como diferentes variáveis (demográficas e financeiras) influenciam a decisão do cliente de deixar o banco.

O dashboard foi construído com base na Seção de Análise Bivariada do notebook original `One_Bank.ipynb`.

## 📋 Escopo do Projeto

O objetivo desta aplicação é democratizar o acesso aos dados da análise de churn, permitindo que usuários (técnicos ou leigos) possam:
1.  **Carregar dados automaticamente** sem necessidade de manipulação de arquivos.
2.  **Explorar variáveis categóricas** (ex: Gênero, País) para identificar taxas de cancelamento.
3.  **Analisar variáveis numéricas** (ex: Salário, Idade, Score de Crédito) através de visualizações simples e avançadas.
4.  **Tomar decisões** baseadas em dados visuais claros e interativos.

## 🚀 Funcionalidades

### 1. Carregamento Automático de Dados
- Conexão direta com o repositório de dados (GitHub) para buscar o dataset `Customer-Churn-Records.csv`.
- Tratamento inicial e mapeamento da variável alvo (`Exited` -> `Status`).

### 2. Análise de Variáveis Categóricas
- Seleção dinâmica de variáveis (Geografia, Gênero, Cartão de Crédito, etc.).
- **Tabela de Taxa de Churn:** Mostra a porcentagem exata de perda em cada categoria.
- **Gráficos:**
  - Histograma de Contagem (Quantos clientes saíram vs. ficaram).
  - Barras 100% Empilhadas (Proporção visual do Churn).

### 3. Análise de Variáveis Numéricas
- Seleção dinâmica de variáveis (Score, Idade, Salário, Saldo, etc.).
- **Métricas Rápidas:** Comparativo da média entre quem saiu (Churn) e quem ficou.
- **Visualizações Flexíveis (para todos os públicos):**
  - 📊 **Comparação de Médias:** Gráfico de barras simples para entendimento rápido.
  - 📉 **Distribuição (Densidade):** Histograma sobreposto para ver concentração de clientes.
  - 📍 **Dispersão (Scatter Plot):** Modos *Strip Plot* e *Scatter Bivariado* para encontrar correlações complexas.
  - 📦 **Boxplot:** Análise estatística detalhada (quartis e outliers).

## 🛠️ Tecnologias Utilizadas

* **[Python 3.x](https://www.python.org/)**: Linguagem base.
* **[Streamlit](https://streamlit.io/)**: Framework para criação de web apps de dados.
* **[Pandas](https://pandas.pydata.org/)**: Manipulação e análise de dados tabulares.
* **[Plotly Express](https://plotly.com/python/plotly-express/)**: Criação de gráficos interativos e dinâmicos.

## 📦 Como Executar o Projeto

Siga os passos abaixo para rodar o dashboard na sua máquina local.

### Pré-requisitos
Certifique-se de ter o Python instalado.

### 1. Clonar ou Baixar o Projeto
Salve o arquivo `app.py` em uma pasta.

### 2. Instalar as Dependências
Abra o terminal na pasta do projeto e execute:

```bash
pip install streamlit pandas plotly


# Bibliotecas 
#============================================
import pandas as pd
import numpy as np
import inflection
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import folium 
import locale

from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from PIL import Image
from datetime import time
from datetime import datetime
 

st.set_page_config(page_title="Main", page_icon="🏠", layout="wide", initial_sidebar_state='auto')

# Funções
#============================================

# 1. Preenchimento do nome dos países
#============================================

COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}

#===============================================
def country_name(country_id):
    return COUNTRIES[country_id]



# 2. Criação do Tipo de Categoria de Comida
#===============================================

def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"


# 3. Criação do nome das Cores 
#================================================

COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]

#================================================

def adjust_columns_order(dataframe):
    df = dataframe.copy()

    new_cols_order = [
        "restaurant_id",
        "restaurant_name",
        "country",
        "city",
        "address",
        "locality",
        "locality_verbose",
        "longitude",
        "latitude",
        "cuisines",
        "price_type",
        "average_cost_for_two",
        "currency",
        "has_table_booking",
        "has_online_delivery",
        "is_delivering_now",
        "aggregate_rating",
        "rating_color",
        "color_name",
        "rating_text",
        "votes",
    ]

    return df.loc[:, new_cols_order]


#  4. Renomeando as colunas do Dataframe
#============================================

def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df


#  5. Limpeza dos dados
#==============================================

def clean_code(df1):
    """ Esta função tem a responsabilidade de limpar o dataframe

        Tipos de limpeza:
        1. Removendo os valores NaN
        2. Renomeando as colunas
        3. Criação de colunas
        4. Categorizando tipo de restaurantes por 1 tipo de culinária
        5. Removendo Linhas Duplicadas
        6. Ajustando as colunas em ordem 
        7. Eliminando a possibilidade de ter espaços nas colunas Texto/ object(trim)    

        Input: Dataframe
        Output: Dataframe 
    """

    # 1. Removendo os valores NaN
    df1 = df1.dropna()

    # 2. Renomeando as colunas
    df1 = rename_columns(df1)

    # 3. Criação de colunas
    df1['price_type'] = df1.loc[:, 'price_range'].apply(lambda x: create_price_tye(x))
    df1["country"] = df1.loc[:, "country_code"].apply(lambda x: country_name(x))
    df1["color_name"] = df1.loc[:, "rating_color"].apply(lambda x: color_name(x))

    # 4. Categorizando tipo de restaurantes por 1 tipo de culinária
    df1['cuisines'] = df1['cuisines'].astype(str)
    df1['cuisines'] = df1.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

    # 5. Removendo Linhas Duplicadas
    df1 = df1.drop_duplicates()

    # 6. Ajustando as colunas em ordem 
    df1 = adjust_columns_order(df1)

    # 7. Eliminando a possibilidade de ter espaços nas colunas Texto/ object(trim)
    # df1.dtypes

    df1.loc[:, 'restaurant_name'] = df1.loc[:, 'restaurant_name'].str.strip()
    df1.loc[:, 'city'] = df1.loc[:, 'city'].str.strip()
    df1.loc[:, 'address'] = df1.loc[:, 'address'].str.strip()
    df1.loc[:, 'locality'] = df1.loc[:, 'locality'].str.strip()
    df1.loc[:, 'locality_verbose'] = df1.loc[:, 'locality_verbose'].str.strip()
    df1.loc[:, 'cuisines'] = df1.loc[:, 'cuisines'].str.strip()
    df1.loc[:, 'currency'] = df1.loc[:, 'currency'].str.strip()
    df1.loc[:, 'rating_color'] = df1.loc[:, 'rating_color'].str.strip()
    df1.loc[:, 'rating_text'] = df1.loc[:, 'rating_text'].str.strip()
    df1.loc[:, 'country'] = df1.loc[:, 'country'].str.strip()
    df1.loc[:, 'color_name'] = df1.loc[:, 'color_name'].str.strip()

    return df1

#  6.  Coluna 1 : Grafico  # Top 10 melhores tipos de culinárias
#=================================================================

def melhores_tipos_culinarias(df1):
        top_10_culinarias = df2.groupby('cuisines').mean('aggregate_rating').reset_index()
        top_10_restaurants = top_10_culinarias.nlargest(10, 'aggregate_rating').reset_index()

        colunas_indesejadas = ['index', 'restaurant_id', 'longitude', 'latitude', 'average_cost_for_two', 'has_table_booking', 'has_online_delivery', 'is_delivering_now', 'votes']
        dados = top_10_restaurants.drop(colunas_indesejadas, axis=1)

        custom_colors = [(0.0, 'red'), (0.5, 'green'), (1.0, 'blue')]

        fig = px.bar(
            dados,
            x='cuisines',
            y='aggregate_rating',
            hover_data=['cuisines'],
            color='aggregate_rating',
            labels={'aggregate_rating': 'Média de Avaliação'},
            height=400,
            color_continuous_scale=custom_colors
        )

        fig.update_layout(
            plot_bgcolor='black',
            title="Top 10 melhores tipos de culinárias",
            xaxis_title="Tipos de culinárias",
            yaxis_title="Média de Avaliações",
        )

        st.plotly_chart(fig)

        return fig 

#  7.  Coluna 1 : Grafico  # Média de Avaliação
#=================================================================

def avaliacao_media(df1):
        top_10_culinarias = df2.groupby('cuisines').mean('aggregate_rating').reset_index()
        top_10_restaurants = top_10_culinarias.nsmallest(10, 'aggregate_rating').reset_index()

        colunas_indesejadas = ['index', 'restaurant_id', 'longitude', 'latitude', 'average_cost_for_two','has_table_booking','has_online_delivery', 'is_delivering_now','votes']
        dados = top_10_restaurants.drop(colunas_indesejadas, axis=1)
        custom_colors = [(0.0, 'red'), (0.5, 'green'), (1.0, 'blue')]

        # Crie o gráfico de barras com a paleta de cores Plotly
        fig = px.bar(
            dados,
            x='cuisines',
            y='aggregate_rating',
            hover_data=['cuisines'],
            color='aggregate_rating',
            labels={'aggregate_rating': 'Média de Avaliação'},
            height=400,
            # Paleta pre dinida
            #color_continuous_scale=px.colors.qualitative.Plotly
            # Paleta customizada
            color_continuous_scale=custom_colors 
        )

        # Personalize o layout para adicionar um fundo preto
        fig.update_layout(
            plot_bgcolor='black',  # Define o fundo do gráfico como preto
            #paper_bgcolor='black'  # Define o fundo da área do gráfico como preto
            title= " Top 10 piores tipos de culinárias",
            xaxis_title="Tipos de culinárias",
            yaxis_title=" Média de Avalições",
        )

        st.plotly_chart(fig)

        return fig


#----------------------------------------------------- Inicio da Estrutura Lógica do Código ---------------------------------------------

# DataFrame importado
#============================================
dataFrame = pd.read_csv( 'Datasets/zomato.csv' )

# Limpando os dados
#============================================
df1 = clean_code(dataFrame)
df2 = df1.copy()

#====================================================================================================
# SIDEBAR 
#====================================================================================================

image = Image.open( "logo.png")
st.sidebar.image( image, width=180)   
st.sidebar.markdown( '# O seu mais novo Restaurante Favorito' )     
st.sidebar.markdown( """___""")

st.sidebar.markdown('## Filtros:')


#----- Criando filro de Países -----

country_options = st.sidebar.multiselect(
    'Escolha os Paises que Deseja visualizar as Informações ',
    ["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia", "Philippines", "United States of America", "Singapure", "United Arab Emirates", "India", "Indonesia", "New Zeland", "Sri Lanka", "Turkey"],
    default = ["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia", "Philippines", "United States of America", "Singapure", "United Arab Emirates", "India", "Indonesia", "New Zeland", "Sri Lanka", "Turkey"],)

#====================================================================================================
# Habilidatação dos filtros
#====================================================================================================

# Filtro País

linhas = df1['country'].isin(country_options)
df2 = df1.loc[linhas, :]

st.sidebar.markdown( """___""")
st.sidebar.markdown( '##### Desenvolvido por Comunidade DS')
st.sidebar.markdown( '###### Cientista de Dados: Renato Sanches Ruiz')

#============================================
#  Layout no Streamlit
#============================================

st.write('# 🍽️ Visão Tipos de Cozinhas')
st.markdown("#### Melhores Restaurantes dos principais tipos Culinários")

# 1º Container:

st.container()

count_city =df2.groupby( ['restaurant_id', 'restaurant_name','country','city','cuisines', 'currency','average_cost_for_two','votes'] )['aggregate_rating'].mean().sort_values(ascending=False).reset_index()
count_10_city =count_city.head(10)
st.dataframe(count_10_city)

st.markdown("""___""")

#==============================================================================================================================================

# 2º Container:

with st.container():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Top 10 melhores tipos de culinárias
        melhores_tipos_culinarias(df1)
    
    with col2:
        st.dataframe(df1)

    # Adiciona uma margem entre as duas colunas
    st.markdown("<div style='margin: 20px;'></div>", unsafe_allow_html=True)
  
st.markdown("""___""")

#===================================================================================================================================

# 3º Container:

with st.container():
    col1, col2 = st.columns([3, 1])

    
    with col1:
        # Média de Avaliação
        avaliacao_media(df1)
    
    with col2:
        st.dataframe(df1)

    # Adiciona uma margem entre as duas colunas
    st.markdown("<div style='margin: 20px;'></div>", unsafe_allow_html=True)

st.markdown("""___""")












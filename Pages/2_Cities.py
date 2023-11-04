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

#  6. Top 10 cidades com mais restaurantes na Base
#===================================================

def city_restaurants( df1):
    count_city =df2.groupby( ['city', 'country'] )['restaurant_id'].count().sort_values(ascending=False).reset_index()
    count_10_city =count_city.head(10)
    data =count_10_city.copy()

    x = count_city['city']  # Cidades
    y = count_10_city['restaurant_id']  # Contagem de restaurantes

    fig = go.Figure(data=[go.Bar(
        x=x,
        y=y,
        text=y,
        textposition='auto',
        marker_color=['blue', 'green', 'red', 'blue', 'green', 'red', 'blue', 'green', 'red', 'blue']
    )])

    fig.update_layout(
        title="(Top 10) Cidades com mais Restaurantes na Base de dados",
        xaxis_title="Cidades",
        yaxis_title="Quantidade de Restaurantes",
        width=800,
        height=500,
        plot_bgcolor='black',
    )

    st.plotly_chart(fig)

    return fig

#  7. Coluna: Gráfico 1 ( Top 7 Cidades com melhores avaliações acima de 4 )
#=============================================================================

def avaliacao_acima_de_quatro(df1):
    restaurantes_acima_de_4 = df2[df2['aggregate_rating'] > 4]
    media_por_cidade = restaurantes_acima_de_4.groupby('city')['aggregate_rating'].mean()
    top_cidades = media_por_cidade.sort_values(ascending=False).head(7).round(2)

    x1 = top_cidades.index  # Cidades
    y1 = top_cidades.values  # Médias de avaliação

    fig1 = go.Figure(data=[go.Bar(
        x=x1,
        y=y1,
        text=y1,
        textposition='auto',
        marker_color=['blue', 'green', 'red', 'blue', 'green', 'red', 'blue']  # Cores para as barras
    )])

    fig1.update_layout(
        title="(Top 7) Cidades com melhores avaliações acima de 4",
        xaxis_title="Cidades",
        yaxis_title="Média de Avaliações",
        plot_bgcolor='black',
        width=550  # Largura do gráfico
    )

    st.plotly_chart(fig1)

    return fig1

#  8. Coluna: Gráfico 2 ( Top 8 Cidades com média de avaliações abaixo de 2.5 )
#================================================================================

def avaliacao_menor_que_dois(df1):
    menor_que_2 = df2[df2['aggregate_rating'] < 2.5]
    media_por_cidade2 = menor_que_2.groupby('city')['aggregate_rating'].mean()
    resultado = media_por_cidade2.sort_values(ascending=False).head(8).round(2)

    x2 = resultado.index  # Cidades
    y2 = resultado.values  # Médias de avaliação

    fig2 = go.Figure(data=[go.Bar(
        x=x2,
        y=y2,
        text=y2,
        textposition='auto',
        marker_color=['blue', 'green', 'red', 'blue', 'green', 'red', 'blue', 'green']  # Cores para as barras
    )])

    fig2.update_layout(
        title="(Top 8) Cidades com média de avaliações abaixo de 2.5",
        xaxis_title="Cidades",
        yaxis_title="Média de Avaliações",
        plot_bgcolor='black',
        width=600  # Largura do gráfico
    )

    st.plotly_chart(fig2)

    return fig2

#  9.  Quantidade de restaurantes com avaliações abaixo de 2.5'
#================================================================================

def contagem_restaurante_menorque_dois(df1):
    restaurantes_abaixo_de_2_5 = df2[df2['aggregate_rating'] < 2.5]
    contagem_por_cidade = restaurantes_abaixo_de_2_5['city'].value_counts().reset_index()

    contagem_por_cidade.columns = ['Cidades', 'Quantidade de Restaurantes']
    quantidade_total = contagem_por_cidade['Quantidade de Restaurantes'].sum()
    print(f"Quantidade total de restaurantes com avaliação abaixo de 2.5:",quantidade_total )

    cores = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
    fig = px.bar(contagem_por_cidade, x='Cidades', y='Quantidade de Restaurantes', color='Cidades',title='Quantidade de restaurantes com avaliações abaixo de 2.5', color_discrete_sequence=cores, width=900, height=550)
    fig.update_layout(plot_bgcolor='#000000')
   
    st.plotly_chart(fig)
    
    return fig

#  10.  # (Top 10) Cidades com mais Restaurantes, com tipo de culinária distinta
#================================================================================

def culinarias_distintas(df1):
    df =df2.groupby('city')['cuisines'].nunique().nlargest(10).reset_index()
    df.columns = ['Cidades', 'Quantidade de tipos de culinária únicas']

    cores = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
    fig = px.bar(df, x='Cidades', y='Quantidade de tipos de culinária únicas', color='Cidades',title='(Top 10) Cidades com mais Restaurantes, com tipo de culinária distinta', color_discrete_sequence=cores, width=900, height=500)

    fig.update_layout(plot_bgcolor='#000000')

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
st.sidebar.markdown( '# Filtros' )


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

st.write('# 🏙️ Visão Cidades')

with st.container():
    # Top 10 cidades com mais restaurantes na Base

    city_restaurants(df1)

st.markdown("""___""")

#========================================================================================================================

# Ajuste a largura das colunas
col1, col2 = st.columns(2)


with col1:

    # Gráfico 1 ( Top 7 Cidades com melhores avaliações acima de 4 )
    avaliacao_acima_de_quatro(df1)


with col2:

    # Gráfico 2 ( Top 8 Cidades com média de avaliações abaixo de 2.5 )
    avaliacao_menor_que_dois(df1)

st.markdown("""___""")

#_________________________________________________________________________________________________________________

with st.container():

    # Quantidade de restaurantes com avaliações abaixo de 2.5'
    contagem_restaurante_menorque_dois(df1)

st.markdown("""___""") 

#___________________________________________________________________________________________________________________

with st.container():   

    # (Top 10) Cidades com mais Restaurantes, com tipo de culinária distinta
    culinarias_distintas(df1)

st.markdown("""___""") 


















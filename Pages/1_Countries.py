# Bibliotecas necessárias
#============================================
import pandas as pd
import numpy as np
import inflection
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import folium 
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import locale
from PIL import Image
import time
from datetime import datetime
from haversine import haversine


st.set_page_config(page_title="Countries", page_icon="🌍", layout="wide", initial_sidebar_state='auto')

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

# 6. Quantidade de Restaurantes registrados por País
#===========================================================================================

def count_restaurants(df1):
    count = df2.groupby('country')['restaurant_id'].count()
    count_city =count.sort_values(ascending=False)

    fig = px.bar(count_city, title='Quantidade de Restaurantes registrados por País',text_auto = '.2s' )
    fig.update_xaxes(title="Paises", title_font_color= 'orange', ticks = 'outside', tickfont_color= 'red')
    fig.update_yaxes(title="Quantidade de Restaurantes registrados", title_font_color= 'orange', ticks = 'outside', tickfont_color= 'red')
    cores = ['orange', 'red','orange', 'red','orange', 'red','orange', 'red','orange', 'red','orange', 'red','orange', 'red','orange']
    fig.update_traces(marker_color=cores)
    fig.update_layout( plot_bgcolor='black')
    fig.update_layout(width=1000, height=500)  # Aumentar o tamanho do gráfico
    fig.update_layout(title_text="Quantidade de Restaurantes registrados por País", title_font_size=20, title_font_color="orange")  # Tornar o título mais visível

    st.plotly_chart(fig)

    return fig


# 7. Quantidade de cidades registradas por País
#===========================================================================================

def count_city(df1):
    count_city = df2.groupby('country')['city'].nunique()
    count_city_2 =count_city.sort_values(ascending=False)
    
    # Plotando o grafico:
    fig = px.bar(count_city_2, title='Quantidade de cidades registradas por País', text_auto = '.2s' )
    fig.update_xaxes(title="Paises", title_font_color= 'orange', ticks = 'outside', tickfont_color= 'red')
    fig.update_yaxes(title="Quantidade de cidades", title_font_color= 'orange', ticks = 'outside', tickfont_color= 'red')
    cores = ['orange', 'red','orange', 'red','orange', 'red','orange', 'red','orange', 'red','orange', 'red','orange', 'red','orange']
    fig.update_traces(marker_color=cores)
    fig.update_layout( plot_bgcolor='black')
    fig.update_layout(width=1000, height=500)  # Aumentar o tamanho do gráfico
    fig.update_layout(title_text="Quantidade de Cidades registradas por País", title_font_size=20, title_font_color="orange")  # Tornar o título mais visível

    st.plotly_chart(fig)

    return fig

# 8. Média de avaliações feitas por País
#===========================================================================================

def country_mean_votes(df1):
    count_city = df2.groupby('country')['votes'].mean().sort_values(ascending=False)
    count_city_2 =count_city.sort_values(ascending=False)

    fig = px.bar(count_city_2, title='Média de avaliações feitas por País', text_auto = '.2s' )
    fig.update_xaxes(title="Paises", title_font_color= 'orange', ticks = 'outside', tickfont_color= 'red')
    fig.update_yaxes(title="Quantidade de avaliações", title_font_color= 'orange', ticks = 'outside', tickfont_color= 'red')
    cores = ['orange', 'red','orange', 'red','orange', 'red','orange', 'red','orange', 'red','orange', 'red','orange', 'red','orange']
    fig.update_traces(marker_color=cores)
    fig.update_layout( plot_bgcolor='black')
    fig.update_layout(title_text="Média de avaliações feitas por País", title_font_size=20, title_font_color="orange")  # Tornar o título mais visível

    st.plotly_chart(fig)

    return fig

# 9. Avaliação média por País
#===========================================================================================

def country_mean_rating(df1):
    df =df2.groupby('country')['aggregate_rating'].mean().round(2).sort_values(ascending=False)

    fig = px.bar(df, title='Avaliações média por País', text_auto = '.2s' )
    fig.update_xaxes(title="Paises", title_font_color= 'orange', ticks = 'outside', tickfont_color= 'red')
    fig.update_yaxes(title="Média das avaliações", title_font_color= 'orange', ticks = 'outside', tickfont_color= 'red')
    cores = ['orange', 'red','orange', 'red','orange', 'red','orange', 'red','orange', 'red','orange', 'red','orange', 'red','orange']
    fig.update_traces(marker_color=cores)
    fig.update_layout( plot_bgcolor='black')
    fig.update_layout(title_text="Avaliação média por País", title_font_size=20, title_font_color="orange")  # Tornar o título mais visível

    st.plotly_chart(fig)

    return fig

# 10. Média de prato para duas Pessoas
#===========================================================================================

def country_mean_fortwo(df1):
# Criando o DataFrame df_aux com os dados
    df_aux = (df1.loc[:, ['country', 'average_cost_for_two']].groupby(['country']).mean()
            .sort_values('average_cost_for_two', ascending=False).reset_index())


    # Criando o gráfico
    fig = px.bar(df_aux,
                x='country',
                y='average_cost_for_two',
                text='average_cost_for_two',
                text_auto='.2f',
                title='Média de Preço de um Prato para Duas Pessoas por País',
                labels={
                    'country': 'Países',
                    'average_cost_for_two': 'Preço do Prato para Duas Pessoas'})

    # Personalizando o layout do gráfico
    fig.update_layout(title_text="Média de Preços de um prato para Duas Pessoas por País", title_font_size=20, title_font_color="orange")  # Tornar o título mais visível
    fig.update_layout(width=1000, height=500)  # Aumentar o tamanho do gráfico

    # Definindo as cores das colunas
    fig.update_traces(marker=dict(color=['red', 'orange']))

    # Definindo o fundo preto
    fig.update_layout(plot_bgcolor='black')

    # Adicionando cores aos textos do eixo x e y
    fig.update_xaxes(tickfont=dict(color='red'))  # Cor vermelha para o eixo x
    fig.update_yaxes(tickfont=dict(color='red'))  # Cor laranja para o eixo y

    # Adicionando cores laranja às labels
    fig.update_layout(xaxis_title=dict(font=dict(color='orange')))
    fig.update_layout(yaxis_title=dict(font=dict(color='orange')))

    # Exibindo o gráfico
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

#st.sidebar.markdown ("<h3 style='text-align: center; color: red;'> O seu mais novo Restaurante Favorito</h3>", unsafe_allow_html=True)
st.sidebar.markdown ('''___''')
st.sidebar.markdown( '# Filtros' )


#====================================================================================================
# FILTROS SIDEBAR
#====================================================================================================

#st.sidebar.markdown ('# Filtros')


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

st.markdown('# 🌎 Visão Países')


with st.container():

    # Quantidade de Restaurantes registrados por país
    count_restaurants(df1)

st.markdown( """___""")


#==================================================================================================================================

with st.container():

    # Quantidade de cidades registradas por País
    count_city(df1)

st.markdown( """___""")


#==================================================================================================================================

# Dois gráficos plotados lado a lado

col1, col2 = st.columns(2)

with col1:
    # Gráfico 1 (Média de avaliações feitas por País)
    country_mean_votes(df1)


with col2:
    # Gráfico 2 (Avaliação média por País)
    country_mean_rating(df1)

st.markdown( """___""")

#==================================================================================================================================

st.container()

country_mean_fortwo(df1)

st.markdown( """___""")













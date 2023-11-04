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

# 6. Plotando mapa
#===========================================================================================

def group_map (df1):
    # Armazenando os dados na variável df_aux.
    df_aux = (df1.loc[:, ['city', 'aggregate_rating', 'currency', 'cuisines', 'color_name', 'restaurant_id','latitude', 'longitude', 'average_cost_for_two', 'restaurant_name']]
                    .groupby(['city', 'cuisines','color_name', 'currency', 'restaurant_id', 'restaurant_name'])
                    .median().reset_index())

    # Criando o mapa.
    map1 = folium.Map()
    marker_cluster = folium.plugins.MarkerCluster().add_to(map1)

    # Inserindo os pinos com informações e cores distintas                   
    for i in range ( len (df_aux) ):
            popup_html = f'<div style="width: 250px;">' \
                        f"<b>{df_aux.loc[i, 'restaurant_name']}</b><br><br>" \
                        \
                        f"Preço para dois: {df_aux.loc[i, 'average_cost_for_two']:.2f} ( {df_aux.loc[i, 'currency']})<br> " \
                        f"Type: {df_aux.loc[i, 'cuisines']}<br>" \
                        f"Nota: {df_aux.loc[i, 'aggregate_rating']}/5.0" \
                        f'</div>'
            folium.Marker ([df_aux.loc[i, 'latitude'], df_aux.loc[i, 'longitude']],
                        popup=popup_html, width=500, height=500, tooltip='clique aqui', parse_html=True,  
                        zoom_start=30, tiles= 'Stamen Toner', 
                        icon=folium.Icon(color=df_aux.loc[i, 'color_name'] , icon='home')).add_to(marker_cluster)
    # Exibindo o mapa    
    folium_static( map1, width=1024 , height=450)   

    return map1


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

# Barra lateral: Logo e nome da empresa
image = Image.open( "logo.png")
st.sidebar.image( image, width=180)   
st.sidebar.markdown( '# O seu mais novo Restaurante Favorito' )     
st.sidebar.markdown( """___""")

#----- Criando filro de Países -----
st.sidebar.markdown( '# Filtros' )

countries = st.sidebar.multiselect(
        "Escolha os Paises que Deseja visualizar as Informações",
        df1.loc[:, "country"].unique().tolist(),
        default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia", "Philippines", "United States of America", "Singapure", "United Arab Emirates", "India", "Indonesia", "New Zeland", "Sri Lanka", "Turkey"],
)

#-----Habilitando o filtro de Países -----
linhas_selecionadas = df1['country'].isin( countries )
df1 = df1.loc[linhas_selecionadas, :]


# Final da barra lateral
st.sidebar.markdown( """___""")
st.sidebar.markdown( '##### Desenvolvido por Comunidade DS')
st.sidebar.markdown( '###### Cientista de Dados: Renato Sanches Ruiz')



#============================================
#  Layout no Streamlit
#============================================


st.markdown("# Fome Zero!")

st.markdown("#### O Melhor lugar para encontrar seu mais novo restaurante favorito!")

st.markdown("#### Temos as seguintes marcas dentro da nossa plataforma:")


st.container()

col1, col2, col3, col4, col5 = st.columns (5, gap='small')

with st.container():
    with col1:
        #Quantidade de restaurantes cadastrados
        df_aux = df1.loc[:, 'restaurant_id'].nunique()
        col1.metric ( label='Restaurantes Cadastrados', value=df_aux, help='Quantidade Restaurantes conforme filtro')

    with col2:
        #Quantidade de países 
        df_aux = df1.loc[:, 'country'].nunique()
        col2.metric ( label='Países Selecionados', value=df_aux, help='Quantidade de Países conforme filtro')
    
    with col3:
        #Quantidade de cidades
        df_aux = df1.loc[:,'city'].nunique()
        col3.metric ( label='Cidades Cadastradas', value=df_aux, help='Quantidade de Cidades conforme filtro')

    with col4:
        #Quantidade de Avaliações feitas na plataforma
        df_aux = df1.loc[:,'votes'].sum()
        locale.setlocale(locale.LC_ALL, '')
        df_aux = locale.format_string('%d', df_aux, grouping=True)
        col4.metric ( label='Avaliações na Plataforma', value=df_aux, help='Qtde Avaliações conforme filtro')

    with col5:
        #Quantidade de tipos de culinárias feitas na plataforma
        df_aux = df1.loc[:,'cuisines'].nunique()
        col5.metric ( label='Tipos de Culinárias Oferecidas', value=df_aux, help='Qtde Avaliações conforme filtro')


st.container()

st.write ('### 🌎 Mapa com a Localização dos restaurantes')
group_map(df1)

st.markdown("""___""")





    






































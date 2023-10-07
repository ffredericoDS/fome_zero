#libraries



import plotly.express as px
import pandas as pd
import inflection
import streamlit as st



df = pd.read_csv('../dataset/zomato.csv')
    
############LIMPEZA###################




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
def country_name(country_id):
    return COUNTRIES[country_id]

df['Country'] = df['Country Code'].apply(country_name)

def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
    
df['Price_Type'] = df['Price range'].apply(create_price_type)

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

df['Color_Name'] = df['Rating color'].apply(color_name)

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

df = rename_columns(df)

df["cuisines"] = df["cuisines"].apply(lambda x: x.split(",")[0] if isinstance(x, str) else x)

import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

def mapa(df):
    # Selecionar as colunas desejadas
    colunas = ['restaurant_id', 'restaurant_name', 'city', 'average_cost_for_two', 'currency', 'longitude', 'latitude', 'cuisines', 'aggregate_rating', 'rating_text']
    df = df[colunas]
    
    # Criar um mapa Folium
    map = folium.Map()

    # Adicionar um cluster de marcadores para restaurantes
    marker_cluster = MarkerCluster(name="restaurantes").add_to(map)

    def cor(rating_text):
        # Mapear cores com base no texto de classificação (exemplo simples)
        if rating_text == 'Bom':
            return 'green'
        elif rating_text == 'Médio':
            return 'orange'
        else:
            return 'red'

    for index, location_info in df.iterrows():
        # Adicionar marcadores com informações relevantes
        folium.Marker([location_info['latitude'], location_info['longitude']],
                      popup=f"Nome: {location_info['restaurant_name']}<br>Custo Médio: {location_info['average_cost_for_two']} {location_info['currency']}<br>Rating: {location_info['aggregate_rating']}",
                      icon=folium.Icon(color=cor(location_info['rating_text']), icon='home')).add_to(marker_cluster)

    # Exibir o mapa no Streamlit
    folium_static(map, width=740, height=360)

# Exemplo de uso:
# mapa(df)
    
    
    
    
st.set_page_config(page_title='main page', page_icon='🎲',layout='wide')    
#---------------------------------------------------------------#
##barra lateral
with st.sidebar:
    st.title('Fome Zero')

    st.header('Filtros')
options = st.sidebar.multiselect(
    'Escolha os países que deseja vizualizar os restaurantes:',
    ['Canada', 'United States of America','New Zeland','Brazil', 'Australia', 'England', 'South Africa',
     'India','Turkey','Philippines','Qatar','Sri Lanka','Indonesia','Singapure','United Arab Emirates'],
    default = ['Canada', 'United States of America','New Zeland','Brazil', 'Australia', 'England', 'South Africa',
               'India','Turkey','Philippines','Qatar','Sri Lanka','Indonesia','Singapure','United Arab Emirates'] )


st.sidebar.header('dados tratados:')
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df)

st.sidebar.download_button(
    label="Download data",
    data=csv,
    file_name='zomato.csv',
    mime='text/csv',
)

linhas_selecionadas = df['country'].isin(options)
df = df.loc[linhas_selecionadas,:]












#--------------------------------------------------------------#

## centro 

st.title('Fome Zero')
st.header('O melhor lugar para encontrar seu mais novo restaurante favorito!')
st.subheader('Temos as seguintes marcas dentro da plataforma:')

with st.container():
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        df_grouped = df['restaurant_id'].nunique()
        col1.metric('qtd restaurantes :',df_grouped)
        
        
       
    with col2:
        df_grouped = df['country'].nunique()
        col2.metric('paises cadastrado',df_grouped)
        
        
        
    
    with col3:
        df_grouped = df["city"].nunique()
        st.metric('qtd cidades',df_grouped)  
        
        
    with col4:
        df_grouped = df['votes'].sum()
        st.metric('avaliações feitas:',df_grouped )
        
        
        
        
    with col5:
        df_grouped= df['cuisines'].nunique()
        st.metric('tipos de culinaria:',df_grouped)
        
with st.container():
        mapa(df)
        
 


            

import pandas as pd
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# Leitura do arquivo CSV
df = pd.read_csv('dataset/zomato.csv')

# Função para mapear o nome do país pelo código
def country_name(country_id):
    COUNTRIES = {
        1: "India",
        14: "Australia",
        30: "Brazil",
        37: "Canada",
        94: "Indonesia",
        148: "New Zeland",
        162: "Philippines",
        166: "Qatar",
        184: "Singapore",
        189: "South Africa",
        191: "Sri Lanka",
        208: "Turkey",
        214: "United Arab Emirates",
        215: "England",
        216: "United States of America",
    }
    return COUNTRIES.get(country_id)

# Aplicando a função para criar uma nova coluna 'Country'
df['Country'] = df['Country Code'].apply(country_name)

# Função para renderizar o mapa com os restaurantes
def render_map(df):
    # Seleção das colunas desejadas
    colunas = ['restaurant_id', 'city', 'average_cost_for_two', 'currency', 'longitude', 'latitude', 'cuisines', 'aggregate_rating', 'rating_text']
    df = df[colunas]
    
    # Criar um mapa Folium
    map = folium.Map()

    # Adicionar um cluster de marcadores para restaurantes
    marker_cluster = MarkerCluster(name="restaurantes").add_to(map)

    def cor(rating_text):
        # Mapear cores com base no texto de classificação
        if rating_text == 'Bom':
            return 'green'
        elif rating_text == 'Médio':
            return 'orange'
        else:
            return 'red'

    for index, location_info in df.iterrows():
        # Adicionar marcadores com informações relevantes
        folium.Marker([location_info['latitude'], location_info['longitude']],
                      popup=f"Nome: {location_info['restaurant_name']}"
                            f"<br>Custo Médio: {location_info['average_cost_for_two']} {location_info['currency']}"
                            f"<br>Rating: {location_info['aggregate_rating']}",
                      icon=folium.Icon(color=cor(location_info['rating_text']), icon='home')).add_to(marker_cluster)

    # Exibir o mapa no Streamlit
    folium_static(map, width=740, height=360)

# Configuração da página Streamlit
st.set_page_config(page_title='main page', page_icon='🎲', layout='wide')    

# Barra lateral
with st.sidebar:
    st.title('Fome Zero')
    st.header('Filtros')

    options = st.sidebar.multiselect(
        'Escolha os países que deseja visualizar os restaurantes:',
        ['Canada', 'United States of America','New Zeland','Brazil', 'Australia', 'England', 'South Africa',
         'India','Turkey','Philippines','Qatar','Sri Lanka','Indonesia','Singapore','United Arab Emirates'],
        default = ['Canada', 'United States of America','New Zeland','Brazil', 'Australia', 'England', 'South Africa',
                   'India','Turkey','Philippines','Qatar','Sri Lanka','Indonesia','Singapore','United Arab Emirates']
    )

    st.sidebar.header('Dados tratados:')

    def convert_df(df):
        # Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(df)

    st.sidebar.download_button(
        label="Download data",
        data=csv,
        file_name='zomato.csv',
        mime='text/csv'
    )

    linhas_selecionadas = df['Country'].isin(options)
    df_filtered = df.loc[linhas_selecionadas,:].copy()  # Renomeie aqui

# Centro
with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        df_grouped = df_filtered['restaurant_id'].nunique()  # Alterado aqui
        col1.metric('Quantidade de restaurantes:', df_grouped)
        
    with col2:
        df_grouped = df_filtered['Country'].nunique()  # Alterado aqui
        col2.metric('Países cadastrados', df_grouped)
        
    with col3:
        df_grouped = df_filtered["city"].nunique()  # Alterado aqui
        col3.metric('Quantidade de cidades', df_grouped)  
        
    with col4:
        df_grouped = df_filtered['votes'].sum()  # Alterado aqui
        col4.metric('Avaliações feitas:', df_grouped)
        
    with col5:
        df_grouped = df_filtered['cuisines'].nunique()  # Alterado aqui
        col5.metric('Tipos de culinária:', df_grouped)

# Renderizar o mapa
with st.container():
    render_map(df_filtered)  # Alterado aqui também


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

#########################################
    
    
    
    
st.set_page_config(page_title='main page', page_icon='👨‍🍳',layout='wide')    
    
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


st.sidebar.write("""---""")

#st.sidebar.markdown('## Selecione a quantidade de dados que deseja visualizar:')
#qtd_restaurantes = st.sidebar.select_slider('Quantidade:', 
 #                options=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], value=(20))
# ,format_func=special_internal_function, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False, label_visibility="visible")

st.sidebar.write("""---""")
st.sidebar.write('Powered By: Frederico Pereira')



#restaurantes = qtd_restaurantes








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

st.title('👨‍🍳Visão Tipos de Cusinhas👨‍🍳')
st.header('Melhores Restaurantes dos principais tipos culinários:')

with st.container():
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        df_grouped = df.loc[df['cuisines']== 'Italian' ,['aggregate_rating','restaurant_name']].groupby('restaurant_name').mean().sort_values(by='aggregate_rating',ascending=False)
        df_grouped =df_grouped.head(1)
        media_rating = df_grouped['aggregate_rating'].mean()
        col1.metric("italian Celino's", media_rating)

        
        
        
    with col2:
        df_grouped = df.loc[df['cuisines']== 'American' ,['aggregate_rating','restaurant_name']].groupby('restaurant_name').mean().sort_values(by='aggregate_rating',ascending=False)
        df_grouped =df_grouped.head(1)
        media_rating = df_grouped['aggregate_rating'].mean()
        col2.metric("american Fat Cat", media_rating)
        
        
        
        
    with col3:
        df_grouped = df.loc[df['cuisines']== 'Japanese' ,['aggregate_rating','restaurant_name']].groupby('restaurant_name').mean().sort_values(by='aggregate_rating',ascending=False)
        df_grouped =df_grouped.head(1)
        media_rating = df_grouped['aggregate_rating'].mean()
        col3.metric("japanese Samurai", media_rating)
        
        
        
        
    with col4:
        df_grouped = df.loc[df['cuisines']== 'Arabian' ,['aggregate_rating','restaurant_name']].groupby('restaurant_name').mean().sort_values(by='aggregate_rating',ascending=False)
        df_grouped =df_grouped.head(1)
        media_rating = df_grouped['aggregate_rating'].mean()
        col4.metric("arabian Mandi@36", media_rating)
        
        
        
        
    with col5:
        df_grouped = df.loc[df['cuisines']== 'Brazilian' ,['aggregate_rating','restaurant_name']].groupby('restaurant_name').mean().sort_values(by='aggregate_rating',ascending=False)
        df_grouped =df_grouped.head(1)
        media_rating = df_grouped['aggregate_rating'].mean()
        col5.metric("brazil Aprazível", media_rating)
        
        
st.title("top 50 Restaurantes")
with st.container():
    df_grouped = df.loc[df['aggregate_rating'] == 4.9,].reset_index()
    df_grouped = df_grouped.head(51)
    st.dataframe(df_grouped)
    
    
    
with st.container():
    col1,col2 = st.columns(2)
    with col1:
        st.header('top 10 melhores tipos de culinaria')
        df_grouped = df.loc[:,['cuisines','aggregate_rating']].groupby('cuisines').mean().sort_values(by='aggregate_rating',ascending=False)
        df_grouped = df.loc[:,['cuisines','aggregate_rating']].groupby('cuisines').mean().sort_values(by='aggregate_rating',ascending=False).reset_index()
        df_grouped = df_grouped.head(11)
        fig = px.bar(df_grouped,x='cuisines',y='aggregate_rating', color='cuisines')
        fig.update_xaxes(title_text='Categorias de Culinária')  # Renomeia o eixo X
        fig.update_yaxes(title_text='Avaliação Agregada Média')  # Renomeia o eixo Y
        st.plotly_chart(fig, use_container_width=True)

        
        
        
        
        
        
        
        
        
        
        
    with col2:
        st.header('top 10 piores tipos de culinaria')
        df_grouped = df.loc[:,['cuisines','aggregate_rating']].groupby('cuisines').mean().sort_values(by='aggregate_rating',ascending=True).reset_index()
        df_grouped = df_grouped.head(11)
        fig = px.bar(df_grouped,x='cuisines',y='aggregate_rating',color='cuisines')
        fig.update_xaxes(title_text='Categorias de Culinária')  # Renomeia o eixo X
        fig.update_yaxes(title_text='Avaliação Agregada Média')  # Renomeia o eixo Y
        st.plotly_chart(fig, use_container_width=True)

        
        
        
        
## deixar mais bonito no Home.py

#libraries

import plotly.express as px
import pandas as pd
import inflection
import streamlit as st



df = pd.read_csv('dataset/zomato.csv')
    
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
    
    
    
    
st.set_page_config(page_title='main page', page_icon='🏙️',layout='wide')    
    
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

st.title('🏙️ Visão Cidades 🏙️ ')

with st.container():
    st.subheader('Top 10 cidades com mais restaurantes')
    df_grouped = df.loc[:,['city','restaurant_id']].groupby('city').count().sort_values(by='restaurant_id',ascending=False).reset_index()
    df_grouped = df_grouped.head(31)
    fig = px.bar(df_grouped,x='city',y='restaurant_id', color='city')
    fig.update_xaxes(title_text='Países')
    fig.update_yaxes(title_text='quantidade de restaurantes')
    st.plotly_chart(fig,use_container_width=True)

    
    
    
    
    
    
    
    
    
    
    
    
    
with st.container():
    col1,col2 = st.columns(2)
    with col1:
        st.subheader('top 10 cidades que possui mais restaurantes com melhores nota média')
        df_grouped = df.loc[df['aggregate_rating'] >= 4,['aggregate_rating','city']].groupby(['city']).count().sort_values(by='aggregate_rating',ascending=False).reset_index()
        df_grouped = df_grouped.head(11)
        fig=px.bar(df_grouped,x='city',y='aggregate_rating', color='city')
        fig.update_xaxes(title_text='Países')
        fig.update_yaxes(title_text='quantidade de restaurantes')
        st.plotly_chart(fig,use_container_width=True)


        
        
        
        
        
    with col2:
        st.subheader('top 10 cidades que possui mais restaurantes com piores nota média')
        df_grouped = df.loc[df['aggregate_rating'] <= 2.5,['aggregate_rating','city']].groupby(['city']).count().sort_values(by='aggregate_rating',ascending=False).reset_index()
        df_grouped = df_grouped.head(11)
        fig=px.bar(df_grouped,x='city',y='aggregate_rating', color='city')
        fig.update_xaxes(title_text='Países')
        fig.update_yaxes(title_text='quantidade de restaurantes')
        st.plotly_chart(fig,use_container_width=True)
        
        
        
        
        
        
        
        
        
        
with st.container():
    st.header('quantidade de tipos de culinária distinta em cada cidade')
    df_grouped = df.loc[:,['cuisines','city']].groupby('city').nunique().sort_values(by='cuisines',ascending=False)
    df_grouped.columns =['quantidade']
    st.dataframe(df_grouped)
        

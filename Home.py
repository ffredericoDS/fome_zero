import streamlit as st
from PIL import Image
st.set_page_config(
    page_title='Home',
    page_icon='🎲'
)



st.sidebar.markdown(' # Fome zero')
st.sidebar.markdown('## Descubra o melhor restaurante para você')
st.sidebar.markdown("""----""")

st.markdown(
    """
    # Fome zero Dashboard
    O projeto 'Fome Zero' é uma plataforma desenvolvida com o objetivo de acompanhar as métricas de crescimento dos restaurantes.
    Diante do cenário atual dos dados, surge a necessidade de uma ferramenta que permita analisar e comparar diferentes aspectos dos
    estabelecimentos gastronômicos para que você possa escolher a melhor opção para você.

    ## Como utilizar este Growth Dashboard?
    - **Visão main page**:
        - Métricas gerais do dashboard
    
    - **Visão contries**:
        - Métricas gerais por países
        

    - **Visão cities**:
        - Métricas gerais das cidades

    - **Visão cuisines**:
        - Métricas gerais por culinarias

    ## ASK FOR HELP
    Você pode entrar em contato com o nosso time de Data Science:
    - gmail: frederico.pereira020@gmail.com
    """
)


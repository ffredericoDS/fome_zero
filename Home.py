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
    O fome zero foi construído para acompanhar as métricas de crescimento dos restaurantes.

    ## Como utilizar este Growth Dashboard?
    - **Visão main page**:
        - Métricas gerais do dashboard
    
    - **Visão contries**:
        - Métricas gerais por cidade
        

    - **Visão cities**:
        - Métricas gerais das cidades

    - **Visão cuisines**:
        - Métricas gerais das culinarias

    ## ASK FOR HELP
    Você pode entrar em contato com o nosso time de Data Science:
    - gmail: frederico.pereira020@gmail.com
    """
)


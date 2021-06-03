import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
st.set_page_config(layout="wide")
import plotly.graph_objects as go

pd.options.display.float_format = "{:,.2f}".format


@st.cache(suppress_st_warning=True)
def load_df(df_index):
    """
    Loads files from df directory into Pandas DataFrame according to positional index, df_index, from 0 to 11.
    """
    list_dfs = [
        'df1_especialidades.ftd'
        , 'df2_tipos_dados.ftd'
        , 'df3_conhecimentos.ftd'
        , 'df4_excel.ftd'
        , 'df5_sql.ftd'
        , 'df6_python.ftd'
        , 'df7_outra_linguagem.ftd'
        , 'df8_impacto.ftd'
        , 'df9_dificuldade.ftd'
        , 'df9a_bibliotecas.ftd'
        , 'df9b_algoritmos.ftd'
        , 'df9c_ia.ftd'
        ]

    df_name = list_dfs[df_index]

    df = pd.read_feather('data/df/' + df_name)

    return df

@st.cache(suppress_st_warning=True)
def plot(df=None):
    """
    Generates a bar plot with the DataFrame df loaded by the load_df function  
    """
    fig = px.bar(data_frame=df, x=df.columns[0], y=df.columns[1], width=1300, height=500)
    fig.update_layout(font=dict(size=18))

    return fig

 
list_topics = [ # list of topics that appear as options in the selection box that spawns the generation of bar plots related to the topics  
    'Especialidades dos profissionais'
    , 'Tipos de dados dados com os quais trabalham'
    , 'Conhecimentos requeridos/úteis no trabalho'
    , 'Nível de conhecimento de Excel'
    , 'Nível de conhecimento de Sql'
    , 'Nível de conhecimento de Python'
    , 'Conhece outra linguagem de programação'
    , 'Percepção de nível de impacto que aprender python teve/teria'
    , 'Percepção de dificuldade para aprendizado de Python'
    , 'Tipos de pacotes da ecossistema Python que conhece'
    , 'Famílias de algoritmos que conhece'
    , 'Reconhece que a IA terá elevado impacto no Planejamento Urbano e Regional'
    ]

st.markdown(
    f"<h1 style='text-align: left; color: black;'>DataProficiency App</h1>", unsafe_allow_html=True
)

Topic = st.selectbox(
    label="Tópico",
    options =list_topics,
    help='Tópico cujas respostas devem ser carregadas'
)

dict_dfs = {index:load_df(df_index=index) for index in range(12)} # loading every Pandas DataFrame as value in a dictionary. The keys are indexes from 0 to 11

index_topic = list_topics.index(Topic) # uses the Topic selected from the selectbox to get the corresponding index in the list_topics

fig = plot(df=dict_dfs[index_topic]) # uses the index related to the topic selected on the selection box to choose a DataFrame from dictionary to be ploted 

st.plotly_chart(fig) # show the plot on the webapp layout
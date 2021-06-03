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
    Under development
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
        , 'df9a_bibliotecas.ftd'
        , 'df9b_algoritmos.ftd'
        , 'df9c_ia.ftd'
        , 'df9_dificuldade.ftd'
        ]

    df_name = list_dfs[df_index]

    df = pd.read_feather('data/df/' + df_name)

    return df

@st.cache(suppress_st_warning=True)
def plot(df=None):
    """
    """
    fig = px.bar(data_frame=df, x=df.columns[0], y=df.columns[1], width=1300, height=500)
    fig.update_layout(font=dict(size=18))

    return fig

list_topics = [
    'Especialidades'
    , 'Tipos de dados_dados'
    , 'Conhecimentos'
    , 'Excel'
    , 'Sql'
    , 'Python'
    , 'Outra Linguagem'
    , 'Impacto'
    , 'Bibliotecas'
    , 'Algoritmos'
    , 'IA'
    , 'Dificuldade'
    ]

#dfs 
#df1_especialidades = load_df(df_index=0)
#df2_tipos_dados = load_df(df_index=1)
#df3_conhecimentos = load_df(df_index=2)
#df4_excel = load_df(df_index=3)
#df5_sql = load_df(df_index=4)
#df6_python = load_df(df_index=5)
#df7_outra_linguagem = load_df(df_index=6)
#df8_impacto = load_df(df_index=7)
#df10_bibliotecas = load_df(df_index=8)
#df11_algoritmos = load_df(df_index=9)
#df12_ia = load_df(df_index=10)
#df13_dificuldade = load_df(df_index=1)

st.markdown(
    f"<h1 style='text-align: left; color: black;'>EvalApp - Urbtec</h1>", unsafe_allow_html=True
)

Topic = st.selectbox(
    label="Tópico",
    options =list_topics,
    help='Tópico cujas respostas devem ser carregadas'
)

dict_dfs = {index:load_df(df_index=index) for index in range(12)}

index_topic = list_topics.index(Topic)

#st.markdown(
#    f"<h2 style='text-align: left; color: black;'>{municipio_name} </h2>", unsafe_allow_html=True
#)

fig = plot(df=dict_dfs[index_topic])

st.plotly_chart(fig)
# importing packages
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
st.set_page_config(layout="wide")
from PIL import Image
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import geopandas as gpd
import plotly.io as pio
import app_functions as app
pd.options.display.float_format = "{:,.2f}".format


# SideBar Options
df_territory = app.load_df_territory()
uf = st.sidebar.selectbox(label='UF', options=df_territory.uf.unique())
options = app.filter_municipalities_by_uf(uf=uf, df=df_territory)
municipio = st.sidebar.selectbox(label='Município', options=options)
cod_municipio = app.get_cod_municipio(df=df_territory, uf=uf, municipio=municipio)
municipio_name = app.load_mun_name(cod_municipio=cod_municipio)


st.markdown(f"<h1 style='text-align: right; color: black;'>PopApp</h1>", unsafe_allow_html=True)
st.markdown(f'## {municipio}')

df_urbrur_growth = app.load_urbrur_data()

fig_urbrur_growth, ano_min, ano_max = app.plot_urbrur_growth(df=df_urbrur_growth, cod_municipio=cod_municipio)

urbanization_index = app.get_urbanization_index(df=df_urbrur_growth, cod_municipio=cod_municipio)

df_projection = app.load_projection_data()

subplots = app.subplot_pop_growth(df_urbrur=df_urbrur_growth, df_projection=df_projection, cod_municipio=cod_municipio)
st.plotly_chart(subplots, use_container_width=True)


df_estrutura_etaria_f, df_estrutura_etaria_m = app.load_age_groups()

fig_age_groups, year = app.plot_pop_pyramid(df_estrutura_etaria_f=df_estrutura_etaria_f, df_estrutura_etaria_m=df_estrutura_etaria_m, cod_municipio=cod_municipio, year=2010)

c1, c2 = st.beta_columns(2)

c1.plotly_chart(fig_age_groups, use_container_width=True)

st.markdown(f"**`O índice de urbanização do município é {urbanization_index}`**")


if uf == 'PB':
    gdf1 = app.load_sector_geodataframe(uf=uf, cod_municipio=cod_municipio)

    fig_map1 = app.plot_density(gdf=gdf1)

    c2.plotly_chart(fig_map1, use_container_width=True)

if cod_municipio == 4106902:
    st.markdown(f"<h2 style='text-align: left; color: black;'>Populacão por Setores Censitários</h2>", unsafe_allow_html=True)
    fig_map = app.load_plotly_map('data/json/curitiba.json')
    st.plotly_chart(fig_map)
elif cod_municipio == 4125506:
    st.markdown(f"<h2 style='text-align: left; color: black;'>População por Setores Censitários</h2>", unsafe_allow_html=True)
    fig_map = app.load_plotly_map('data/json/sjp.json')
    st.plotly_chart(fig_map)


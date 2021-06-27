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

pd.options.display.float_format = "{:,.2f}".format


@st.cache(suppress_st_warning=True)
def subplot_pop_growth(df_urbrur=None, df_projection=None, cod_municipio=4125506):
    """
    Under development
    """

    df_urbrur = df_urbrur.loc[df_urbrur["Código"] == cod_municipio]
    df_pop_total = df_urbrur[df_urbrur['Situação'] == 'Total']
    df_pop_urbana = df_urbrur[df_urbrur['Situação'] == 'Urbana']
    df_pop_rural = df_urbrur[df_urbrur['Situação'] == 'Rural']

    df_projection = df_projection.loc[df_projection["Código"] == cod_municipio]
    df_projection = df_projection.sort_values(by='Ano')

    subplots = make_subplots(
        rows=1
        , cols=2
        , shared_xaxes=True
        , shared_yaxes=True
        , horizontal_spacing=0.06        
        , subplot_titles=("1970 e 2010", "2010 a 2040"))
    subplots.append_trace(go.Scatter(x=df_pop_total['Ano'], y=df_pop_total['População'], name='Total'), row=1, col=1)
    subplots.append_trace(go.Scatter(x=df_pop_urbana['Ano'], y=df_pop_urbana['População'], name='Urbana'), row=1, col=1)
    subplots.append_trace(go.Scatter(x=df_pop_rural['Ano'], y=df_pop_rural['População'], name='Rural'), row=1, col=1)
    subplots.append_trace(go.Scatter(x=df_projection['Ano'], y=df_projection['População'], name='Projetada'), row=1, col=2)
    subplots.update_layout(width=1200, height=500, title_text='<b>Crescimento Demográfico<b>')
    subplots.update_layout(font=dict(size=10))
    subplots.update_layout(margin=dict(l=0, r=0, b=0, t=50))
    

#    ano_min = df['Ano'].min()
#    ano_max = df['Ano'].max()

    return subplots


@st.cache(suppress_st_warning=True)
def load_mun_name(cod_municipio=4125506):
    municipios = pd.read_csv('data/territorio/municipios_brasileiros.csv', sep=';')
    
    name_municipio = municipios[municipios['cod'] == cod_municipio]['municipio'].values[0]

    return name_municipio



@st.cache(suppress_st_warning=True)
def load_urbrur_data():
    """
    Loads data from the file pop_urbano_rural_total_70_10.CSV into a Pandas DataFrame. Treats the data so it can be used as an argument to devise a line plot with the plot_urbrur_growth function.
    pop_urbano_rural_total_70_10.CSV must be in the folder data/pop/.
    """

    df = pd.read_csv(
        "data/pop/pop_urbano_rural_total_70_10.CSV",
        sep=";",
        dtype={
            "codmun": np.int32,
            "nomemun": "object",
            "ano": np.int32,
            "Total": np.int32,
            "Urbana": np.int32,
            "Rural": np.int32,
        },
    )
    df = df.melt(id_vars=["codmun", "nomemun", "ano"])
    df.columns = ["Código", "Município", "Ano", "Situação", "População"]

    return df


@st.cache(suppress_st_warning=True)
def plot_urbrur_growth(df=None, cod_municipio=4125506):
    """
    Generates a line plot of the rural, urban an total population of the selected municipality.
    The df argument must be the Pandas DataFrame generated by the function load_urbrur_data.
    cod_municipio must be an integer representing the IBGE code for the municipality of interest.
    """

    df = df.loc[df["Código"] == cod_municipio]
    fig = px.line(data_frame=df, x="Ano", y="População", color="Situação", width=1300, height=400, title='Crescimento Populacional entre 1970 e 2010')
    fig.update_layout(font=dict(size=18))
    ano_min = df['Ano'].min()
    ano_max = df['Ano'].max()

    return fig, ano_min, ano_max


@st.cache(suppress_st_warning=True)
def load_projection_data():
    """
    Loads projection data into a Pandas DataFrame to be used as an argument in the plot_projection function.

    """

    dict_types = {
        "codmun": np.int32,
        "nomemun": "object",
        "2010": np.int32,
        "2020": np.int32,
        "2030": np.int32,
        "2040": np.int32,
    }
    df = pd.read_csv(
        "data/pop/pop_projetada_ipardes_consolidada.csv", sep=";", dtype=dict_types
    )
    df = df.melt(id_vars=["codmun", "nomemun"])
    df.columns = ["Código", "Município", "Ano", "População"]

    return df


@st.cache(suppress_st_warning=True)
def plot_projection(df=None, cod_municipio=4125506):
    """
    Generates a line plot of the population projecte to the next decades by the IPARDES.
    The df argument must be the Pandas DataFrame generated by the load_projection_data function.
    cod_municipio must be an integer representing the IBGE code for the municipality of interest.

    """
    df = df.loc[df["Código"] == cod_municipio]
    df = df.sort_values(by="Ano")
    proj_max = df['Ano'].max()


    fig = px.line(data_frame=df, x="Ano", y="População", width=1300, height=400)

    return fig, proj_max


@st.cache(suppress_st_warning=True)
def get_urbanization_index(df, cod_municipio):
    """
    Returns the urbanization index for the municipality whose IBGE code is provided in cod_municipio.
    The df argument must be the Pandas DataFrame generated by the function load_urbrur_data.
    """

    df = df.loc[(df["Código"] == cod_municipio) & (df["Ano"] == df["Ano"].max())]
    urban_pop = df.loc[df["Situação"] == "Urbana"]["População"].values
    total_pop = df.loc[df["Situação"] == "Total"]["População"].values
    urbanization_index = urban_pop / total_pop * 100

    return round(urbanization_index[0], 2)


@st.cache(suppress_st_warning=True)
def load_age_groups():

    dtypes = {
        "codmun": np.int32,
        "sexo": "category",
        "0 a 4 anos": np.int32,
        "5 a 9 anos": np.int32,
        "10 a 14 anos": np.int32,
        "15 a 19 anos": np.int32,
        "20 a 24 anos": np.int32,
        "25 a 29 anos": np.int32,
        "30 a 34 anos": np.int32,
        "35 a 39 anos": np.int32,
        "40 a 44 anos": np.int32,
        "45 a 49 anos": np.int32,
        "50 a 54 anos": np.int32,
        "55 a 59 anos": np.int32,
        "60 a 64 anos": np.int32,
        "65 a 69 anos": np.int32,
        "70 a 74 anos": np.int32,
        "75 a 79 anos": np.int32,
        "80 anos ou mais": np.int32,
    }

    df_estrutura_etaria = pd.read_csv("data/pop/estruturaetaria.csv", sep=";")

    df_estrutura_etaria = df_estrutura_etaria.melt(id_vars=["codmun", "sexo"])

    df_estrutura_etaria.columns = ["Código", "Sexo", "Faixa", "População"]
    
    df_estrutura_etaria_f = df_estrutura_etaria[df_estrutura_etaria['Sexo'] == 'Feminino']
    df_estrutura_etaria_m = df_estrutura_etaria[df_estrutura_etaria['Sexo'] == 'Masculino']

    return df_estrutura_etaria_f, df_estrutura_etaria_m


@st.cache(suppress_st_warning=True)
def plot_pop_pyramid(df_estrutura_etaria_f, df_estrutura_etaria_m, cod_municipio, year):
    df_estrutura_etaria_f = df_estrutura_etaria_f[df_estrutura_etaria_f['Código'] == cod_municipio]
    df_estrutura_etaria_m = df_estrutura_etaria_m[df_estrutura_etaria_m['Código'] == cod_municipio]

    fig = make_subplots(rows=1, cols=2, shared_yaxes=True, shared_xaxes=True, horizontal_spacing=0.0)

    sub0 = px.bar(data_frame=df_estrutura_etaria_f, y='Faixa', x='População', color='Sexo', orientation='h', color_discrete_map={'Feminino':'rgb(228, 26,28)'}, barmode='overlay')

    sub0.update_layout(xaxis_autorange='reversed')

    sub1 = px.bar(data_frame=df_estrutura_etaria_m, y='Faixa', x='População', orientation='h', color='Sexo', barmode='overlay')

    fig.add_traces(sub0['data'][0], rows=1, cols=1);
    fig.add_traces(sub1['data'][0], rows=1, cols=2);
    fig.data[0].showlegend= False
    fig.data[1].showlegend= False
    fig.layout.barmode = 'overlay'
    fig.layout.xaxis.autorange = 'reversed'
    fig.layout.xaxis.title.text = 'Feminino'
    fig.layout.xaxis2.title.text = 'Masculino'

    fig.layout.title.text = f'<b>Pirâmide Etária<b>'
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=40), width=1075, height=400)
    fig.layout.title.font.size = 25

    return fig, year



@st.cache(suppress_st_warning=True)
def load_geo_dataframe(cod_municipio=4125506):
    
    if str(cod_municipio)[:2] == '41':
        file = 'data/territorio/setores_2010_pb.ftd'
    elif str(cod_municipio)[:2] == '25':
        file = 'data/territorio/setores_2010_pr.ftd'
    else:
        file = None
    
    if file != None:
        return gpd.read_feather(file)


@st.cache(suppress_st_warning=True)
def plot_density_map(gdf, cod_municipio):

    gdf = gdf.loc[gdf["CD_GEOCODI"] == cod_municipio]

    long = gdf.centroid.x[0]
    lat = gdf.centroid.y[0]

    px.choropleth_mapbox(
        data_frame=gdf
        , geojson=gdf.geometry
    #    , featureidkey=gdf.index
        , locations=gdf.index
        , color='População'
        , hover_name='CD_GEOCODI'
        , hover_data=None
        , zoom=11
        ,center={"lat": lat, "lon": long}
        , mapbox_style="carto-positron"
        , title=None
        , template=None
        , width=None
        , height=None
        , opacity=0.1
    )

    fig.update_layout(title_text='<b>Pirâmide Etária<b>', font=dict(size=18))

    return fig, year

@st.cache(suppress_st_warning=True)
def load_df_territory():
    df_territory = pd.read_csv('data/territorio/municipios_brasileiros.csv', sep=';')
    return df_territory

@st.cache(suppress_st_warning=True)
def filter_municipalities_by_uf(uf):
    options = df_territory.municipio.loc[df_territory.uf == uf].values
    return options

df_territory = load_df_territory()

uf = st.sidebar.selectbox(label='UF', options=df_territory.uf.unique())

options = filter_municipalities_by_uf(uf=uf)

municipio = st.sidebar.selectbox(label='Município', options=options)

@st.cache(suppress_st_warning=True)
def get_cod_municipio(uf, municipio):
    cod_municipio = df_territory.loc[(df_territory.uf == uf) & (df_territory.municipio == municipio)]['cod'].values[0]
    return cod_municipio

cod_municipio = get_cod_municipio(uf=uf, municipio=municipio)


municipio_name = load_mun_name(cod_municipio=cod_municipio)

#image = Image.open('imagens/urbtec.png')
#st.image(image)
st.markdown(
    f"<h1 style='text-align: right; color: black;'>PopApp</h1>", unsafe_allow_html=True
)
st.markdown(f'## {municipio}')
#st.markdown(
#    f"<h2 style='text-align: left; color: black;'>{municipio_name} </h2>", unsafe_allow_html=True
#)


df_urbrur_growth = load_urbrur_data()

fig_urbrur_growth, ano_min, ano_max = plot_urbrur_growth(df=df_urbrur_growth, cod_municipio=cod_municipio)

#st.markdown(f'## **Crescimento Populacional entre {ano_min} e {ano_max}**')
#st.plotly_chart(fig_urbrur_growth)

urbanization_index = get_urbanization_index(
    df=df_urbrur_growth, cod_municipio=cod_municipio
)

df_projection = load_projection_data()

subplots = subplot_pop_growth(df_urbrur=df_urbrur_growth, df_projection=df_projection, cod_municipio=cod_municipio)
st.plotly_chart(subplots)

'''
subplots.layout
'''

#fig_projection, proj_max = plot_projection(df=df_projection, cod_municipio=cod_municipio)

#st.markdown(f'## **Projeção Populacional até {proj_max}**')
#st.plotly_chart(fig_projection)

#df_age_groups = load_age_groups()

df_estrutura_etaria_f, df_estrutura_etaria_m = load_age_groups()

fig_age_groups, year = plot_pop_pyramid(df_estrutura_etaria_f=df_estrutura_etaria_f, df_estrutura_etaria_m=df_estrutura_etaria_m, cod_municipio=cod_municipio, year=2010)

#st.markdown(f'## **Pirâmide Etária em {year}**')
st.plotly_chart(fig_age_groups)

st.markdown(f"**`O índice de urbanização do município é {urbanization_index}`**")


@st.cache(suppress_st_warning=True)
def load_plotly_map(file):
    return pio.read_json(file)

@st.cache(suppress_st_warning=True)
def load_sector_geodataframe(uf,cod_municipio):
    cod_municipio = str(cod_municipio)
    gdf = pd.read_pickle(f'https://github.com/augustogeog/python_demo/blob/30b1ec2dfccfc435b14f3708cd3d021b7c1637f3/data/territorio/setores2010/{uf}/{cod_municipio}/{cod_municipio}.zip?raw=true')
    return gdf



if uf == 'PB':
    gdf1 = load_sector_geodataframe(uf=uf, cod_municipio=cod_municipio)
    lon = gdf1.dissolve(by='NM_MUNICIP').centroid.x[0]
    lat = gdf1.dissolve(by='NM_MUNICIP').centroid.y[0]

    fig_map = px.choropleth_mapbox(
        data_frame=gdf1
        , geojson=gdf1.geometry
    #    , featureidkey=gdf.index
        , locations=gdf1.index
        , color='Pop/ha'
    #    , hover_name='CD_GEOCODI'
        , hover_data=None
        , zoom=11
        ,center={"lat": lat, "lon": lon}
        , mapbox_style="carto-positron"
        , title=None
        , template=None
        , width=None
        , height=None
        , opacity=0.3
        )
    st.plotly_chart(fig_map, use_container_width=True)

if cod_municipio == 4106902:
    st.markdown(f"<h2 style='text-align: left; color: black;'>Populacão por Setores Censitários</h2>", unsafe_allow_html=True)
    fig_map = load_plotly_map('data/json/curitiba.json')
    st.plotly_chart(fig_map)
elif cod_municipio == 4125506:
    st.markdown(f"<h2 style='text-align: left; color: black;'>População por Setores Censitários</h2>", unsafe_allow_html=True)
    fig_map = load_plotly_map('data/json/sjp.json')
    st.plotly_chart(fig_map)


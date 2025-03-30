import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import json
import altair as alt

Anio = [2023, 2024]

st.set_page_config(page_title='Censo Bovino - Tablero',
                page_icon=':ox:',
                layout='wide')

st.sidebar.header("Año")
AnioSeleccionado = st.sidebar.selectbox('Seleccione un año',
                            Anio, index=1)
st.sidebar.markdown('---')

st.title(f'Tablero {AnioSeleccionado}')
st.markdown('---')

@st.cache_data
def load_data(AnioSeleccionado):
    df=pd.read_excel(
        io=f'CENSOS-BOVINOS-{AnioSeleccionado}-Final.xlsx',
        #io='CENSOS-BOVINOS-2023-Final.xlsx',
        engine='openpyxl',
        sheet_name='BOVINOS Y PREDIOS',
        skiprows=4,
        usecols='A:Q',
        #nrows=1121,
    )

    df['DEPARTAMENTO'] = df['DEPARTAMENTO'].replace('NARIÑO', 'NARINO')
    
    Totales = ['TERNERAS < 1 AÑO',
            'TERNEROS < 1 AÑO',
            'HEMBRAS 1 - 2 AÑOS',
            'MACHOS 1 - 2 AÑOS',
            'HEMBRAS 2 - 3 AÑOS',
            'MACHOS 2 - 3 AÑOS',
            'HEMBRAS > 3 AÑOS',
            'MACHOS > 3 AÑOS',
            'TOTAL BOVINOS',
            ' No DE FINCAS 1 A 50',
            ' No DE FINCAS 51 A 100',
            ' No DE FINCAS 101 A 500',
            ' No DE FINCAS 501 O MAS',
            'TOTAL FINCAS CON BOVINOS'
            ]

    for Total in Totales:
        df[Total + '/Dep']= df.groupby('DEPARTAMENTO')[Total].transform('sum')

    df.sort_values(by='DEPARTAMENTO', inplace=True)

    return df

df = load_data(AnioSeleccionado)


st.sidebar.header("Variables")

columnas = [col for col in df.columns if col not in ['DEPARTAMENTO',
                                                    'MUNICIPIO',
                                                    'CODIGO MUNICIPIO',
                                                    'TERNERAS < 1 AÑO',
                                                    'TERNEROS < 1 AÑO',
                                                    'HEMBRAS 1 - 2 AÑOS',
                                                    'MACHOS 1 - 2 AÑOS',
                                                    'HEMBRAS 2 - 3 AÑOS',
                                                    'MACHOS 2 - 3 AÑOS',
                                                    'HEMBRAS > 3 AÑOS',
                                                    'MACHOS > 3 AÑOS',
                                                    'TOTAL BOVINOS',
                                                    ' No DE FINCAS 1 A 50',
                                                    ' No DE FINCAS 51 A 100',
                                                    ' No DE FINCAS 101 A 500',
                                                    ' No DE FINCAS 501 O MAS',
                                                    'TOTAL FINCAS CON BOVINOS',
                                                    ]]

variables = st.sidebar.selectbox('Seleccione una variable a mapear',
                                columnas,
                                index=8)

variables2 = st.sidebar.selectbox('Seleccione una variable para comparar',
                                columnas,
                                index=8)

with open ('Colombia.json') as response:
    Departamentos = json.load(response)

locs = df['DEPARTAMENTO']

for Departamento in Departamentos['features']:
    Departamento['id'] = Departamento['properties']['NOMBRE_DPT']
mapa = go.Figure(go.Choroplethmapbox(
                    geojson=Departamentos,
                    locations=locs,
                    z=df[variables],
                    colorscale='prgn_r',
                    colorbar_title=f'{variables}',
                    hovertemplate='%{z:.4s} <extra>%{location}</extra>',
                    ))
mapa.update_layout(mapbox_style="carto-positron",
                        mapbox_zoom=4.8,
                        height=750,
                        margin=dict(
                            l=10,
                            r=10,
                            b=10,
                            t=10,
                            pad=5
                            ),
                        
                        paper_bgcolor='rgba(50, 50, 50, 0.5)',
                        mapbox_center = {"lat": 4.270868, "lon": -74.2973328})

#------------------------------------------------------------------------------

#--------------------------------------------------------------------------------

st.plotly_chart(mapa,
                use_container_width=True,
                config={'displaylogo': False})
st.markdown('---')

# Sección de grafico de barras
Grafico1 = go.FigureWidget()
Grafico1.add_scatter(x=df['DEPARTAMENTO'].unique(),
                    y=df[variables].unique(),
                    name=variables,
                    mode='lines+markers',
                    )

Grafico1.add_bar(x=df['DEPARTAMENTO'].unique(),
                y=df[variables2].unique(),
                name=variables2,
                )

Grafico1.update_layout(
    title=f'{variables} vs. {variables2}',
    margin=dict(
        l=10,
        r=10,
        b=10,
        t=40,
        pad=5
    ),
    paper_bgcolor='rgba(50, 50, 50, 0.5)',
    separators='.',
    hovermode='x unified',
)

Grafico1.update_traces(hovertemplate='%{y:.4s}')

st.plotly_chart(Grafico1, use_container_width=True, config={'displaylogo': False})
st.markdown('---')

dfBovinos=df.drop(['MUNICIPIO',
            'CODIGO MUNICIPIO',
            'TERNERAS < 1 AÑO',
            'TERNEROS < 1 AÑO',
            'HEMBRAS 1 - 2 AÑOS',
            'MACHOS 1 - 2 AÑOS',
            'HEMBRAS 2 - 3 AÑOS',
            'MACHOS 2 - 3 AÑOS',
            'HEMBRAS > 3 AÑOS',
            'MACHOS > 3 AÑOS',
            'TOTAL BOVINOS',
            ' No DE FINCAS 1 A 50',
            ' No DE FINCAS 51 A 100',
            ' No DE FINCAS 101 A 500',
            ' No DE FINCAS 501 O MAS',
            'TOTAL FINCAS CON BOVINOS',
            ' No DE FINCAS 1 A 50/Dep',
            ' No DE FINCAS 51 A 100/Dep',
            ' No DE FINCAS 101 A 500/Dep',
            ' No DE FINCAS 501 O MAS/Dep',
            'TOTAL FINCAS CON BOVINOS/Dep',
            'TOTAL BOVINOS/Dep'
            ], axis=1)

dfBovinos.drop_duplicates(inplace=True)

dfBovinos.set_index('DEPARTAMENTO', inplace=True)

dfBovinos = dfBovinos.transpose()

dfBovinos.columns = dfBovinos.columns.astype(str)

st.dataframe(dfBovinos.style.format("{:.0f}",thousands='.'))

dfFincas=df.drop(['MUNICIPIO',
            'CODIGO MUNICIPIO',
            'TERNERAS < 1 AÑO',
            'TERNEROS < 1 AÑO',
            'HEMBRAS 1 - 2 AÑOS',
            'MACHOS 1 - 2 AÑOS',
            'HEMBRAS 2 - 3 AÑOS',
            'MACHOS 2 - 3 AÑOS',
            'HEMBRAS > 3 AÑOS',
            'MACHOS > 3 AÑOS',
            'TOTAL BOVINOS',
            ' No DE FINCAS 1 A 50',
            ' No DE FINCAS 51 A 100',
            ' No DE FINCAS 101 A 500',
            ' No DE FINCAS 501 O MAS',
            'TOTAL FINCAS CON BOVINOS',
            'TOTAL BOVINOS/Dep',
            'TERNERAS < 1 AÑO/Dep',
            'TERNEROS < 1 AÑO/Dep',
            'HEMBRAS 1 - 2 AÑOS/Dep',
            'MACHOS 1 - 2 AÑOS/Dep',
            'HEMBRAS 2 - 3 AÑOS/Dep',
            'MACHOS 2 - 3 AÑOS/Dep',
            'HEMBRAS > 3 AÑOS/Dep',
            'MACHOS > 3 AÑOS/Dep',
            'TOTAL FINCAS CON BOVINOS/Dep'
            ], axis=1)

dfFincas.drop_duplicates(inplace=True)

dfFincas.set_index('DEPARTAMENTO', inplace=True)

dfFincas = dfFincas.transpose()

dfFincas.columns = dfFincas.columns.astype(str)

st.dataframe(dfFincas.style.format("{:.0f}", thousands='.'))

st.markdown('---')

Departamentos=st.sidebar.selectbox('Seleccione un departamento', dfBovinos.columns)
st.sidebar.markdown('---')

Grafico2 = px.pie(dfBovinos,
                names=dfBovinos.index,
                values=Departamentos,
                height=350,
                )

Grafico2.update_layout(
    title=f'Distribución censo bovinos en {Departamentos}',
    margin=dict(
        l=10,
        r=10,
        b=10,
        t=40,
        pad=5
    ),
    paper_bgcolor='rgba(50, 50, 50, 0.5)',
)

Grafico3 = px.pie(dfFincas,
                names=dfFincas.index,
                values=Departamentos,
                height=350,
                )

Grafico3.update_layout(
    title=f'Distribución censo fincas en {Departamentos}',
    margin=dict(
        l=10,
        r=10,
        b=10,
        t=40,
        pad=5
    ),
    paper_bgcolor='rgba(50, 50, 50, 0.5)',
)

Columna1, Columna2 = st.columns(2)

with Columna1:
    st.header('Animales por Dpto.')
    st.plotly_chart(Grafico2, use_container_width=True, config={'displaylogo': False})
    st.markdown('---')

with Columna2:
    st.header('Fincas por Dpto.')
    st.plotly_chart(Grafico3, use_container_width=True, config={'displaylogo': False})
    st.markdown('---')

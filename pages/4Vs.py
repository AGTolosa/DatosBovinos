import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import json
import altair as alt

Anio = [2023, 2024]

st.set_page_config(page_title='Censo Bovino - Comparativa por años',
                page_icon=':ox:',
                layout='wide')

st.sidebar.header("Año 1")
AnioSeleccionado1 = st.sidebar.selectbox('Seleccione año 1',
                            Anio, index=0)

st.sidebar.header("Año 2")
AnioSeleccionado2 = st.sidebar.selectbox('Seleccione año 2',
                            Anio, index=1)
st.sidebar.markdown('---')

st.title(f'{AnioSeleccionado1} Vs {AnioSeleccionado2}')
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

df1 = load_data(AnioSeleccionado1)

df2 = load_data(AnioSeleccionado2)






st.sidebar.header("Variables")

columnas = [col for col in df1.columns if col not in ['DEPARTAMENTO',
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


#Sección de mapas
Columna3, Columna4 = st.columns(2)
##Mapa 1
with Columna3:
    st.header(f'Mapa {AnioSeleccionado1}')
    
    with open ('Colombia.json') as response:
        Departamentos = json.load(response)

    locs = df1['DEPARTAMENTO']

    for Departamento in Departamentos['features']:
        Departamento['id'] = Departamento['properties']['NOMBRE_DPT']
    mapa = go.Figure(go.Choroplethmapbox(
                        geojson=Departamentos,
                        locations=locs,
                        z=df1[variables],
                        colorscale='prgn_r',
                        colorbar_title=f'{variables}',
                        hovertemplate='%{z:.4s} <extra>%{location}</extra>',
                        ))
    mapa.update_layout(mapbox_style="carto-positron",
                            mapbox_zoom=4.4,
                            height=700,
                            margin=dict(
                                l=10,
                                r=10,
                                b=10,
                                t=10,
                                pad=5
                                ),
                            
                            paper_bgcolor='rgba(50, 50, 50, 0.5)',
                            mapbox_center = {"lat": 4.570868, "lon": -74.2973328})

    st.plotly_chart(mapa,
                    use_container_width=True,
                    config={'displaylogo': False})

##Mapa 2
with Columna4:
    st.header(f'Mapa {AnioSeleccionado2}')
    with open ('Colombia.json') as response:
        Departamentos = json.load(response)

    locs = df2['DEPARTAMENTO']

    for Departamento in Departamentos['features']:
        Departamento['id'] = Departamento['properties']['NOMBRE_DPT']
    mapa = go.Figure(go.Choroplethmapbox(
                        geojson=Departamentos,
                        locations=locs,
                        z=df2[variables],
                        colorscale='prgn_r',
                        colorbar_title=f'{variables}',
                        hovertemplate='%{z:.4s} <extra>%{location}</extra>',
                        ))
    mapa.update_layout(mapbox_style="carto-positron",
                            mapbox_zoom=4.4,
                            height=700,
                            margin=dict(
                                l=10,
                                r=10,
                                b=10,
                                t=10,
                                pad=5
                                ),
                            
                            paper_bgcolor='rgba(50, 50, 50, 0.5)',
                            mapbox_center = {"lat": 4.570868, "lon": -74.2973328})

    st.plotly_chart(mapa,
                    use_container_width=True,
                    config={'displaylogo': False})

st.markdown('---')


#Sección graficos de barras.
#Grafico Año 1
Grafico1 = go.FigureWidget()
Grafico1.add_scatter(x=df1['DEPARTAMENTO'].unique(),
                    y=df1[variables].unique(),
                    name=variables,
                    mode='lines+markers',
                    )

Grafico1.add_bar(x=df1['DEPARTAMENTO'].unique(),
                y=df1[variables2].unique(),
                name=variables2,
                )

Grafico1.update_layout(
    title=f'Año 1: {variables} vs. {variables2}',
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

# Grafico Año 2
Grafico2 = go.FigureWidget()
Grafico2.add_scatter(x=df2['DEPARTAMENTO'].unique(),
                    y=df2[variables].unique(),
                    name=variables,
                    mode='lines+markers',
                    )

Grafico2.add_bar(x=df2['DEPARTAMENTO'].unique(),
                y=df2[variables2].unique(),
                name=variables2,
                )

Grafico2.update_layout(
    title=f'Año 2: {variables} vs. {variables2}',
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

Grafico2.update_traces(hovertemplate='%{y:.4s}')

st.plotly_chart(Grafico2, use_container_width=True, config={'displaylogo': False})
st.markdown('---')


# Sección de tablas
st.header(f'Censo bovino {AnioSeleccionado1}')

dfBovinos1=df1.drop(['MUNICIPIO',
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

dfBovinos1.drop_duplicates(inplace=True)

dfBovinos1.set_index('DEPARTAMENTO', inplace=True)

dfBovinos1 = dfBovinos1.transpose()

dfBovinos1.columns = dfBovinos1.columns.astype(str)

st.dataframe(dfBovinos1.style.format("{:.0f}",thousands='.'))


st.header(f'Censo bovino {AnioSeleccionado2}')


dfBovinos2=df2.drop(['MUNICIPIO',
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

dfBovinos2.drop_duplicates(inplace=True)

dfBovinos2.set_index('DEPARTAMENTO', inplace=True)

dfBovinos2 = dfBovinos2.transpose()

dfBovinos2.columns = dfBovinos2.columns.astype(str)

st.dataframe(dfBovinos2.style.format("{:.0f}",thousands='.'))


st.subheader(f'Censo fincas {AnioSeleccionado1}')


dfFincas1=df1.drop(['MUNICIPIO',
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

dfFincas1.drop_duplicates(inplace=True)

dfFincas1.set_index('DEPARTAMENTO', inplace=True)

dfFincas1 = dfFincas1.transpose()

dfFincas1.columns = dfBovinos1.columns.astype(str)

st.dataframe(dfFincas1.style.format("{:.0f}", thousands='.'))


st.subheader(f'Censo fincas {AnioSeleccionado2}')


dfFincas2=df2.drop(['MUNICIPIO',
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

dfFincas2.drop_duplicates(inplace=True)

dfFincas2.set_index('DEPARTAMENTO', inplace=True)

dfFincas2 = dfFincas2.transpose()

dfFincas2.columns = dfFincas2.columns.astype(str)

st.dataframe(dfFincas2.style.format("{:.0f}", thousands='.'))


st.markdown('---')


# Sección de gráficos de pastel
# Se toman los nombres de los departamentos a partir de un solo dataframe, ya que
# a traves del tiempo, estos no cambian de nombre, siendo los mismos en ambos años.
Departamentos=st.sidebar.selectbox('Seleccione un departamento', dfBovinos1.columns)
st.sidebar.markdown('---')

Grafico5 = px.pie(dfBovinos1,
                names=dfBovinos1.index,
                values=Departamentos,
                height=350,
                )

Grafico5.update_layout(
    title=f'Distribución censo bovinos en {Departamentos} Año {AnioSeleccionado1}',
    margin=dict(
        l=10,
        r=10,
        b=10,
        t=40,
        pad=5
    ),
    paper_bgcolor='rgba(50, 50, 50, 0.5)',
)


Grafico6 = px.pie(dfBovinos2,
                names=dfBovinos2.index,
                values=Departamentos,
                height=350,
                )

Grafico6.update_layout(
    title=f'Distribución censo bovinos en {Departamentos} Año {AnioSeleccionado2}',
    margin=dict(
        l=10,
        r=10,
        b=10,
        t=40,
        pad=5
    ),
    paper_bgcolor='rgba(50, 50, 50, 0.5)',
)


Grafico7 = px.pie(dfFincas1,
                names=dfFincas1.index,
                values=Departamentos,
                height=350,
                )

Grafico7.update_layout(
    title=f'Distribución censo fincas en {Departamentos} Año {AnioSeleccionado1}',
    margin=dict(
        l=10,
        r=10,
        b=10,
        t=40,
        pad=5
    ),
    paper_bgcolor='rgba(50, 50, 50, 0.5)',
)



Grafico8 = px.pie(dfFincas2,
                names=dfFincas2.index,
                values=Departamentos,
                height=350,
                )

Grafico8.update_layout(
    title=f'Distribución censo fincas en {Departamentos} Año {AnioSeleccionado2}',
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
    st.plotly_chart(Grafico5, use_container_width=True, config={'displaylogo': False})
    st.plotly_chart(Grafico6, use_container_width=True, config={'displaylogo': False})
    st.markdown('---')

with Columna2:
    st.header('Fincas por Dpto.')
    st.plotly_chart(Grafico7, use_container_width=True, config={'displaylogo': False})
    st.plotly_chart(Grafico8, use_container_width=True, config={'displaylogo': False})
    st.markdown('---')

import streamlit as st
import pandas as pd
import sweetviz as sv

Anio = [2023, 2024]

st.set_page_config(page_title='Censo Bovino - Datos',
                page_icon=':ox:',
                layout='wide')

st.title('Datos')
st.markdown('---')

st.sidebar.header("Año")
AnioSeleccionado = st.sidebar.selectbox('Seleccione año:',
                            Anio, index=0)

@st.cache_data
def load_data(AnioSeleccionado):
    df= pd.read_excel(
        io=f'CENSOS-BOVINOS-{AnioSeleccionado}-Final.xlsx',
        #io='CENSOS-BOVINOS-2023-Final.xlsx',
        engine='openpyxl',
        sheet_name='Tabla_Departamentos',
        skiprows=4,
        usecols='A:O',
        nrows=35,
        thousands='.'
        )

    return df
    
df = load_data(AnioSeleccionado)

st.dataframe(df.style.format(thousands='.'))
st.markdown('---')

st.sidebar.header('Variables')
variables = st.sidebar.multiselect(
    'Seleccione las variables a analizar. En cero generará un analisis exploratorio de todos los datos.',
    df.columns.tolist(),
    placeholder='Cero',
)

st.sidebar.write('Cantidad seleccionada: ', variables.__len__())

def eda():
    variables = sv.FeatureConfig(force_text=["DEPARTAMENTO"])
    analisis = sv.analyze(df, feat_cfg=variables)
    analisis.show_html('Reporte.html',
                        layout='vertical',
                        )
    sv.config_parser.read('override.ini')
    st.download_button('Descargar Reporte',
                    data=open('Reporte.html', 'rb').read(),
                    file_name='Reporte.html')
    return analisis

def filtrado():
    df_filtrado = df[variables]
    analisis_filtrado = sv.analyze(df_filtrado)
    analisis_filtrado.show_html('Reporte Personalizado.html',
                                layout='vertical',
                                )
    sv.config_parser.read('override.ini')
    st.download_button('Descargar Reporte Personalizado',
                    data=open('Reporte Personalizado.html', 'rb').read(),
                    file_name='Reporte Personalizado.html'
                    )
    return analisis_filtrado

def ejecutar():
    if len(variables) == 0:
        eda()
    else:
        filtrado()

st.sidebar.button('Analizar datos', on_click=ejecutar, help='Genera el analisis exploratorio de las variables seleccionadas.')
st.sidebar.markdown('---')

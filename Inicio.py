import streamlit as st

st.set_page_config(page_title='Censo Bovino',
                page_icon=':ox:',
                layout='wide')

st.title("Datos Bovinos")
st.markdown('---')

st.sidebar.success(":arrow_up_small: Elija una sección y un año para empezar:")
st.sidebar.markdown("---")

st.subheader("Fuente de los datos originales:")
st.markdown('Censo bovino [ICA](https://www.ica.gov.co/areas/pecuaria/servicios/epidemiologia-veterinaria/censos-2016/censo-2018)')

st.subheader("Codigo fuente del proyecto:")
st.markdown('Github [AGTolosa](https://github.com/AGTolosa/DatosBovinos.git)')

st.subheader("Uso:")
st.write('Proporciona una visión resumida de los Censos realizados al hato bovino Colombiano a partir del año 2023.\n'
        '### Tablero\n'
        '- Análisis gráfico y comparativo de los datos.\n'
        '- _Seleccionar una variable a mapear:_ Muestra la distribución de la variable por departamento.\n'
        '- _Seleccione una variable para comparar:_ Compara gráficamente la variable mapeada, con una variable adicional.\n'
        '- _Seleccione un departamento:_ Muestra la distribución de los datos en el departamento seleccionado.\n'
        '### Datos\n'
        'Análisis exploratorio de los datos.\n'
        '- _Variables:_ generará un análisis exploratorio de las variables seleccionadas; en caso de no seleccionar ninguna,\n'
        'el análisis se ejecutara sobre todas las variables.\n'
        '- _Descargar Reporte:_ Descarga un archivo html con el análisis exploratorio de los datos.\n'
        '### Vs\n'
        'Comparativa entre años.\n'
        '- Seleccione los años para los que quiere ver un analisis comparativo.\n'
        '- Seleccione las caracteristicas que quiere comparar.\n')
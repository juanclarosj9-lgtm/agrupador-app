import streamlit as st
import pandas as pd

st.set_page_config(page_title="Agrupador Global", page_icon="📊")

st.title("🌍 Agrupador de Datos Global")
st.write("Sube tu archivo CSV y agrupa los datos al instante.")

uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.write("Vista previa de tus datos:")
    st.dataframe(df.head())
    
    columnas = df.columns.tolist()
    opcion = st.selectbox("¿Por qué columna quieres agrupar?", columnas)
    
    if st.button("🚀 Agrupar Datos"):
        resultado = df.groupby(opcion).size().reset_index(name='Total')
        
        st.success("¡Listo! Estos son tus resultados:")
        st.dataframe(resultado)
        st.bar_chart(resultado.set_index(opcion))
else:
    st.info("Esperando que subas un archivo...")
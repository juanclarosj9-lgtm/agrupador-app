import streamlit as st
import pandas as pd
import io

# 1. Mejorar la apariencia visual (Idea 4)
st.set_page_config(
    page_title="📊 Agrupador Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌍 Agrupador de Datos Pro")
st.write("Sube tu CSV, filtra, agrupa, analiza y descarga los resultados.")

# Barra lateral para controles
with st.sidebar:
    st.header("⚙️ Configuración")
    uploaded_file = st.file_uploader("📂 Elige un archivo CSV", type="csv")

# 2. Filtros previos (Idea 3)
if uploaded_file is not None:
    # Leemos los datos y los guardamos en session_state para no perderlos al recargar
    if 'df' not in st.session_state:
        st.session_state.df = pd.read_csv(uploaded_file)
    
    df = st.session_state.df
    st.success(f"✅ Archivo cargado: {len(df)} filas leídas.")

    # Filtros
    st.subheader("🔍 Filtros")
    col1, col2 = st.columns(2)
    
    with col1:
        filtro_columna = st.multiselect("Filtrar por columna:", df.columns.tolist())
    
    if filtro_columna:
        with col2:
            valores_filtro = st.multiselect(
                "Selecciona valores:", 
                df[filtro_columna[0]].unique().tolist()
            )
        
        # Aplicamos el filtro
        if valores_filtro:
            df_filtrado = df[df[filtro_columna[0]].isin(valores_filtro)]
            st.info(f"Mostrando {len(df_filtrado)} filas filtradas.")
        else:
            df_filtrado = df
    else:
        df_filtrado = df

    # 3. Que el usuario elija qué calcular (Idea 2)
    st.subheader("🧮 Agrupación y Análisis")
    
    opcion = st.selectbox("Agrupar por:", df_filtrado.columns.tolist(), key="group_col")
    
    # Buscamos columnas numéricas
    columnas_numericas = df_filtrado.select_dtypes(include=['number']).columns.tolist()
    
    if columnas_numericas:
        columna_valor = st.selectbox("Analizar columna numérica:", columnas_numericas)
        operacion = st.selectbox("¿Qué cálculo quieres?", ["Suma", "Promedio", "Máximo", "Mínimo", "Contar"])
    else:
        columna_valor = None
        operacion = "Contar"
        st.warning("No se encontraron columnas numéricas. Se hará un conteo.")

    if st.button("🚀 Ejecutar Agrupación"):
        if columna_valor:
            if operacion == "Suma":
                resultado = df_filtrado.groupby(opcion)[columna_valor].sum().reset_index()
            elif operacion == "Promedio":
                resultado = df_filtrado.groupby(opcion)[columna_valor].mean().reset_index()
            elif operacion == "Máximo":
                resultado = df_filtrado.groupby(opcion)[columna_valor].max().reset_index()
            elif operacion == "Mínimo":
                resultado = df_filtrado.groupby(opcion)[columna_valor].min().reset_index()
            else:
                resultado = df_filtrado.groupby(opcion)[columna_valor].count().reset_index()
        else:
            # Si no hay numéricas, solo contamos
            resultado = df_filtrado.groupby(opcion).size().reset_index(name='Total')

        st.success("¡Resultados listos!")
        
        # 5. Guardar preferencias entre sesiones (Idea 5)
        st.session_state.resultado = resultado
        st.session_state.opcion = opcion

    # Mostrar resultados si existen
    if 'resultado' in st.session_state:
        resultado = st.session_state.resultado
        opcion = st.session_state.opcion
        
        st.subheader("📊 Resultados")
        st.dataframe(resultado, use_container_width=True)
        
        # Gráfico
        st.subheader("📈 Gráfico Visual")
        st.bar_chart(resultado.set_index(opcion))
        
        # 1. Botón para descargar (Idea 1)
        csv = resultado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar resultados como CSV",
            data=csv,
            file_name='resultados_agrupados.csv',
            mime='text/csv'
        )ÚseloControl + Shift + m para alternar el enfoquetab de movimiento de la tecla. Alternativamente, úselo para pasar al siguiente elemento interactivo de la página.esctab

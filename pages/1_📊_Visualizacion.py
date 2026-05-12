import streamlit as st
import sys
import os
import plotly.express as px
import pandas as pd

# Agregamos el directorio raíz al path para poder importar desde 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_processor import cargar_datos_estudiantes, aplicar_filtros_globales, verificar_contrasena

st.set_page_config(page_title="Vista General", page_icon="📊", layout="wide")

# Validar contraseña
verificar_contrasena()

st.title("📊 Vista General y Asistencia")
st.markdown("Visión demográfica y comportamiento general de estudio de los encuestados.")

# Llamamos a la función cacheada y aplicamos filtros
with st.spinner('Cargando datos desde el archivo CSV...'):
    df = cargar_datos_estudiantes()
    df = aplicar_filtros_globales(df)

st.subheader("Métricas Generales")

# Validamos la cantidad exacta de encuestados contando los IDs únicos para evitar duplicados
# o filas vacías que Pandas haya podido leer por error.
total_encuestados = df['ID'].nunique() if 'ID' in df.columns else len(df)
st.metric("Total de Estudiantes Encuestados", total_encuestados)

st.divider()

st.subheader("📅 Evolución de Respuestas en el Tiempo")
if 'Fecha_Respuesta' in df.columns:
    df_fechas = df.copy()
    # Extraemos solo la fecha (ignorando la hora) para agrupar por día
    df_fechas['Fecha_Respuesta'] = pd.to_datetime(df_fechas['Fecha_Respuesta'], errors='coerce').dt.date
    timeline_data = df_fechas['Fecha_Respuesta'].dropna().value_counts().reset_index()
    timeline_data.columns = ['Fecha', 'Respuestas']
    timeline_data = timeline_data.sort_values('Fecha')
    if not timeline_data.empty:
        fig_timeline = px.area(timeline_data, x='Fecha', y='Respuestas', markers=True, 
                               color_discrete_sequence=['#636EFA'], title="Cantidad de encuestas respondidas por día")
        st.plotly_chart(fig_timeline, use_container_width=True)

st.divider()

# Gráficos de barra nativos de Streamlit
st.subheader("Distribución de los Estudiantes y Frecuencia")
c1, c2 = st.columns(2)

with c1:
    if 'Sede' in df.columns:
        data_sede = df['Sede'].dropna().value_counts().reset_index()
        data_sede.columns = ['Sede', 'Cantidad']
        data_sede = data_sede.sort_values('Cantidad', ascending=False)
        fig_sede = px.bar(data_sede, x='Sede', y='Cantidad', text_auto=True, 
                          title="Cantidad de Encuestados por Sede", color='Sede')
        fig_sede.update_traces(textposition="outside")
        st.plotly_chart(fig_sede, use_container_width=True)

with c2:
    if 'Frecuencia_Asistencia' in df.columns:
        data_frec = df['Frecuencia_Asistencia'].dropna().value_counts().reset_index()
        data_frec.columns = ['Frecuencia', 'Cantidad']
        data_frec = data_frec.sort_values('Cantidad', ascending=False)
        fig_frec = px.bar(data_frec, x='Frecuencia', y='Cantidad', text_auto=True, 
                          title="Frecuencia de Asistencia a Ayudantías")
        fig_frec.update_traces(textposition="outside")
        st.plotly_chart(fig_frec, use_container_width=True)

st.divider()

st.subheader("Alternativas de Estudio (cuando no asisten)")
if 'Alternativas_Estudio' in df.columns:
    # Al ser respuesta múltiple separada por ';', separamos las cadenas y las contamos
    alt_series = df['Alternativas_Estudio'].dropna().astype(str).str.split(';').explode().str.strip()
    alt_series = alt_series[alt_series != '']
    data_alt = alt_series.value_counts().reset_index()
    data_alt.columns = ['Alternativa', 'Cantidad']
    data_alt = data_alt.sort_values('Cantidad', ascending=True)
    fig_alt = px.bar(data_alt, y='Alternativa', x='Cantidad', text_auto=True, 
                     orientation='h', title="Herramientas de estudio alternativas")
    fig_alt.update_traces(textposition="outside")
    st.plotly_chart(fig_alt, use_container_width=True)

st.divider()

st.subheader("Vista Previa de la Base de Datos")
st.dataframe(df, use_container_width=True)
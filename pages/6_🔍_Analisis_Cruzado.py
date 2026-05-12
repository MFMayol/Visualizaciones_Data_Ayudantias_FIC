import streamlit as st
import sys
import os
import plotly.express as px
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_processor import cargar_datos_estudiantes, aplicar_filtros_globales, verificar_contrasena

st.set_page_config(page_title="Análisis Cruzado", page_icon="🔍", layout="wide")

# Validar contraseña
verificar_contrasena()

st.title("🔍 Análisis Cruzado Avanzado")
st.markdown("Cruces de variables para entender mejor el comportamiento y las tendencias segmentadas.")

df = cargar_datos_estudiantes()
df = aplicar_filtros_globales(df)

st.subheader("1. Frecuencia de Asistencia por Sede")
if 'Sede' in df.columns and 'Frecuencia_Asistencia' in df.columns:
    cross_freq_sede = df.groupby(['Sede', 'Frecuencia_Asistencia']).size().reset_index(name='Cantidad')
    fig_freq = px.bar(cross_freq_sede, x='Sede', y='Cantidad', color='Frecuencia_Asistencia', 
                      barmode='stack', text_auto=True, title="Distribución de Asistencia según la Sede")
    st.plotly_chart(fig_freq, use_container_width=True)

st.divider()

st.subheader("2. Modalidad Preferida por Sede")
if 'Sede' in df.columns and 'Modalidad_Preferida' in df.columns:
    cross_mod_sede = df.groupby(['Sede', 'Modalidad_Preferida']).size().reset_index(name='Cantidad')
    fig_mod = px.bar(cross_mod_sede, x='Sede', y='Cantidad', color='Modalidad_Preferida', 
                     barmode='group', text_auto=True, title="Qué formato prefieren en cada campus")
    st.plotly_chart(fig_mod, use_container_width=True)

st.divider()

st.subheader("3. Nivel de Asistencia vs Utilidad Percibida Promedio")
if 'Frecuencia_Asistencia' in df.columns and 'Utilidad' in df.columns:
    utilidad_media = df.groupby('Frecuencia_Asistencia')['Utilidad'].mean().reset_index()
    utilidad_media['Utilidad_Texto'] = utilidad_media['Utilidad'].round(2).astype(str)
    fig_util = px.line(utilidad_media, x='Frecuencia_Asistencia', y='Utilidad', markers=True, text='Utilidad_Texto',
                       title="¿A mayor asistencia, encuentran más útiles las ayudantías?",
                       labels={'Utilidad': 'Promedio de Utilidad (Rango 1 al 5)'})
    fig_util.update_traces(textposition="top center")
    st.plotly_chart(fig_util, use_container_width=True)

st.divider()

st.subheader("4. Horario Preferido por Sede")
if 'Sede' in df.columns and 'Horario_Preferido' in df.columns:
    # Filtramos la opción "Otros" para mantener los gráficos limpios
    df_horario = df[(df['Sede'] != 'Otros') & (df['Horario_Preferido'] != 'Otros')]
    cross_horario_sede = df_horario.groupby(['Sede', 'Horario_Preferido']).size().reset_index(name='Cantidad')
    fig_horario = px.bar(cross_horario_sede, x='Sede', y='Cantidad', color='Horario_Preferido', 
                         barmode='group', text_auto=True, title="Qué horario prefieren en cada campus")
    st.plotly_chart(fig_horario, use_container_width=True)

st.divider()

st.subheader("5. Modalidad vs Frecuencia de Asistencia")
if 'Modalidad_Preferida' in df.columns and 'Frecuencia_Asistencia' in df.columns:
    df_mod_frec = df[(df['Modalidad_Preferida'] != 'Otros') & (df['Frecuencia_Asistencia'] != 'Otros')]
    cross_mod_frec = df_mod_frec.groupby(['Frecuencia_Asistencia', 'Modalidad_Preferida']).size().reset_index(name='Cantidad')
    fig_mod_frec = px.bar(cross_mod_frec, x='Frecuencia_Asistencia', y='Cantidad', color='Modalidad_Preferida', 
                          barmode='stack', text_auto=True, title="Relación entre la asistencia actual y la modalidad preferida")
    st.plotly_chart(fig_mod_frec, use_container_width=True)

st.divider()

st.subheader("6. Matriz de Correlación de Evaluaciones (Heatmap)")
st.markdown("Analiza qué tanto se relacionan las calificaciones entre sí. Valores cercanos a 1 indican una fuerte correlación positiva.")

metricas_num = ['Utilidad', 'Claridad', 'Comodidad', 'Preparacion']
if set(metricas_num).issubset(df.columns):
    df_corr = df[metricas_num].copy()
    for col in metricas_num:
        df_corr[col] = pd.to_numeric(df_corr[col], errors='coerce')
    corr_matrix = df_corr.dropna().corr()
    fig_corr = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='RdBu_r', 
                         aspect="auto", title="Mapa de Calor de Correlaciones")
    st.plotly_chart(fig_corr, use_container_width=True)

st.divider()

st.subheader("7. Comparación de Calidad por Sede (Gráfico de Radar)")
st.markdown("Compara el rendimiento promedio de los ayudantes en las distintas sedes bajo los 4 pilares de evaluación.")

if set(metricas_num).issubset(df.columns) and 'Sede' in df.columns:
    # Filtramos valores 'Otros' en Sede
    df_radar = df[df['Sede'] != 'Otros'].copy()
    for col in metricas_num:
        df_radar[col] = pd.to_numeric(df_radar[col], errors='coerce')
    
    # Agrupamos por sede y calculamos promedios
    radar_data = df_radar.groupby('Sede')[metricas_num].mean().reset_index()
    # Transformamos el dataframe al formato requerido por Plotly Express (Melt)
    radar_melted = radar_data.melt(id_vars='Sede', var_name='Métrica', value_name='Promedio')
    
    # Creamos el gráfico de radar
    if not radar_melted.empty:
        fig_radar = px.line_polar(radar_melted, r='Promedio', theta='Métrica', color='Sede', 
                                  line_close=True, range_r=[0, 5], 
                                  title="Perfil de Evaluación Promedio por Sede")
        fig_radar.update_traces(fill='toself')
        st.plotly_chart(fig_radar, use_container_width=True)
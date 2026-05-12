import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_processor import cargar_datos_estudiantes, aplicar_filtros_globales, verificar_contrasena

st.set_page_config(page_title="Evaluación", page_icon="⭐", layout="wide")

# Validar contraseña
verificar_contrasena()

st.title("⭐ Evaluación de los Ayudantes")
st.markdown("Análisis de la percepción de los estudiantes sobre la calidad de las ayudantías.")

df = cargar_datos_estudiantes()
df = aplicar_filtros_globales(df)

st.subheader("Promedios de Evaluación (Rango 1 al 5)")
cols = st.columns(5)
metricas = ['Utilidad', 'Claridad', 'Comodidad', 'Preparacion', 'Alineacion_Clases']

for i, col_name in enumerate(metricas):
    if col_name in df.columns:
        # Convertimos a numérico en caso de que existan strings vacíos
        promedio = pd.to_numeric(df[col_name], errors='coerce').mean()
        cols[i].metric(col_name.replace('_', ' '), round(promedio, 2))

st.divider()

st.subheader("Calidad y Criterios")
c1, c2 = st.columns(2)

with c1:
    if 'Diferencias_Calidad' in df.columns:
        data_diff = df['Diferencias_Calidad'].dropna().value_counts().reset_index()
        data_diff.columns = ['Respuesta', 'Cantidad']
        fig_diff = px.pie(data_diff, names='Respuesta', values='Cantidad', 
                          title="¿Se notan diferencias de calidad entre ayudantes?", hole=0.4)
        fig_diff.update_traces(textinfo='percent+value')
        st.plotly_chart(fig_diff, use_container_width=True)

with c2:
    if 'Resolucion_Problemas' in df.columns:
        data_res = df['Resolucion_Problemas'].dropna().value_counts().reset_index()
        data_res.columns = ['Resolución', 'Cantidad']
        data_res = data_res.sort_values('Cantidad', ascending=True)
        fig_res = px.bar(data_res, y='Resolución', x='Cantidad', text_auto=True, 
                         orientation='h', title="Resolución ante problemas con correcciones")
        fig_res.update_traces(textposition="outside")
        st.plotly_chart(fig_res, use_container_width=True)

st.divider()

st.subheader("Distribución de las Calificaciones")
if set(metricas).issubset(df.columns):
    df_melted = df.melt(value_vars=metricas, var_name='Métrica', value_name='Puntuación')
    df_melted['Puntuación'] = pd.to_numeric(df_melted['Puntuación'], errors='coerce')
    df_melted = df_melted.dropna()
    
    fig_box = px.box(df_melted, x='Métrica', y='Puntuación', color='Métrica', points="all",
                     title="Dispersión de Notas asignadas a los Ayudantes (Boxplot)")
    st.plotly_chart(fig_box, use_container_width=True)
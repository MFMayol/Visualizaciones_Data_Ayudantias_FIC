import streamlit as st
import sys
import os
import plotly.express as px
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_processor import cargar_datos_docentes, aplicar_filtros_globales, verificar_contrasena

st.set_page_config(page_title="Coordinación Docente", page_icon="🤝", layout="wide")
verificar_contrasena()

st.title("🤝 Coordinación y Relación Docente-Ayudante")
st.markdown("Análisis detallado de cómo se coordinan los profesores con sus ayudantes y los obstáculos que enfrentan.")

df = cargar_datos_docentes()

if df.empty:
    st.warning("No se encontró el archivo `BD_Docentes.csv` en la carpeta `data`. Asegúrate de subirlo.")
    st.stop()

df = aplicar_filtros_globales(df)

st.subheader("1. Claridad de Roles y Frecuencia de Coordinación")
c1, c2 = st.columns(2)
with c1:
    if 'Claridad_Roles' in df.columns:
        data_roles = df['Claridad_Roles'].value_counts().reset_index()
        data_roles.columns = ['Claridad de Roles', 'Cantidad']
        fig_roles = px.pie(data_roles, names='Claridad de Roles', values='Cantidad', title="Claridad de roles del equipo docente", hole=0.4)
        st.plotly_chart(fig_roles, use_container_width=True)

with c2:
    if 'Coordinacion' in df.columns:
        data_coord = df['Coordinacion'].value_counts().reset_index()
        data_coord.columns = ['Frecuencia', 'Cantidad']
        fig_coord = px.bar(data_coord, x='Frecuencia', y='Cantidad', title="Frecuencia de Coordinación Real", text_auto=True)
        st.plotly_chart(fig_coord, use_container_width=True)

st.divider()

st.subheader("2. Pautas y Materiales")
c3, c4 = st.columns(2)
with c3:
    if 'Anticipacion_Materiales' in df.columns:
        data_ant = df['Anticipacion_Materiales'].value_counts().reset_index()
        data_ant.columns = ['Anticipación', 'Cantidad']
        fig_ant = px.bar(data_ant, x='Cantidad', y='Anticipación', orientation='h', title="Anticipación en entrega de materiales", text_auto=True)
        st.plotly_chart(fig_ant, use_container_width=True)

with c4:
    if 'Pauta_Comun' in df.columns:
        fig_pauta = px.pie(df, names='Pauta_Comun', title="Uso de Pauta Común (Correctores)")
        st.plotly_chart(fig_pauta, use_container_width=True)

st.divider()

st.subheader("3. Principales Obstáculos de Coordinación")
if 'Obstaculos_Coordinacion' in df.columns:
    obstaculos = df['Obstaculos_Coordinacion'].astype(str).str.split(';').explode().str.strip()
    obstaculos = obstaculos[(obstaculos != 'Otros') & (obstaculos != '')] 
    data_obs = obstaculos.value_counts().reset_index()
    data_obs.columns = ['Obstáculo', 'Cantidad']
    fig_obs = px.bar(data_obs, x='Cantidad', y='Obstáculo', orientation='h', title="Obstáculos reportados (Respuesta múltiple)", text_auto=True)
    st.plotly_chart(fig_obs, use_container_width=True)
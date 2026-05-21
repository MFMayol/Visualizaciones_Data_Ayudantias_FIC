import streamlit as st
import sys
import os
import plotly.express as px
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_processor import cargar_datos_docentes, aplicar_filtros_globales, verificar_contrasena

st.set_page_config(page_title="Vista Docentes", page_icon="👨‍🏫", layout="wide")
verificar_contrasena()

st.title("👨‍🏫 Vista General de Docentes")
st.markdown("Análisis de las respuestas y percepciones del equipo docente respecto a las ayudantías de sus cursos.")

df = cargar_datos_docentes()

if df.empty:
    st.warning("No se encontró el archivo `BD_Docentes.csv` en la carpeta `data`. Asegúrate de subirlo.")
    st.stop()

df = aplicar_filtros_globales(df)

st.subheader("Métricas Generales")
total_docentes = df['ID'].nunique() if 'ID' in df.columns else len(df)
st.metric("Total de Docentes Encuestados", total_docentes)

st.divider()

st.subheader("📅 Evolución de Respuestas y Top Cursos")
c0_1, c0_2 = st.columns(2)
with c0_1:
    if 'Fecha_Respuesta' in df.columns:
        df_fechas = df.copy()
        df_fechas['Fecha_Respuesta'] = pd.to_datetime(df_fechas['Fecha_Respuesta'], errors='coerce').dt.date
        timeline_data = df_fechas['Fecha_Respuesta'].dropna().value_counts().reset_index()
        timeline_data.columns = ['Fecha', 'Respuestas']
        timeline_data = timeline_data.sort_values('Fecha')
        if not timeline_data.empty:
            fig_timeline = px.area(timeline_data, x='Fecha', y='Respuestas', markers=True, 
                                   color_discrete_sequence=['#FF7F0E'], title="Respuestas de Docentes por Día")
            st.plotly_chart(fig_timeline, use_container_width=True)

with c0_2:
    if 'Curso' in df.columns:
        data_curso = df['Curso'].value_counts().reset_index().head(10)  # Top 10 para no saturar
        data_curso.columns = ['Curso', 'Cantidad']
        fig_curso = px.bar(data_curso, x='Cantidad', y='Curso', orientation='h', 
                           title="Top 10 Cursos con más participación", text_auto=True)
        fig_curso.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_curso, use_container_width=True)

st.divider()

c1, c2 = st.columns(2)
with c1:
    if 'Sede' in df.columns:
        fig_sede = px.pie(df, names='Sede', title="Distribución de Docentes por Sede", hole=0.3)
        st.plotly_chart(fig_sede, use_container_width=True)

with c2:
    if 'Modalidad' in df.columns:
        data_mod = df['Modalidad'].value_counts().reset_index()
        data_mod.columns = ['Modalidad', 'Cantidad']
        fig_mod = px.bar(data_mod, x='Modalidad', y='Cantidad', title="Modalidad predominante de la ayudantía", text_auto=True)
        st.plotly_chart(fig_mod, use_container_width=True)

st.divider()

st.subheader("Percepción del Valor Académico y Alineación")
c3, c4 = st.columns(2)
with c3:
    if 'Valor_Academico' in df.columns:
        data_valor = df['Valor_Academico'].value_counts().reset_index()
        data_valor.columns = ['Valor Académico', 'Cantidad']
        fig_valor = px.bar(data_valor, x='Valor Académico', y='Cantidad', title="Valor Académico Percibido", text_auto=True)
        st.plotly_chart(fig_valor, use_container_width=True)

with c4:
    if 'Alineacion' in df.columns:
        fig_alineacion = px.pie(df, names='Alineacion', title="¿Qué tan alineados están los objetivos de clase?", hole=0.3)
        st.plotly_chart(fig_alineacion, use_container_width=True)

st.divider()

st.subheader("Utilidad Percibida y Factores de Valor")
c4_1, c4_2 = st.columns(2)
with c4_1:
    if 'Utilidad_Actual' in df.columns:
        data_util = df['Utilidad_Actual'].value_counts().reset_index()
        data_util.columns = ['Utilidad en Formato Actual', 'Cantidad']
        fig_util = px.pie(data_util, names='Utilidad en Formato Actual', values='Cantidad', title="Utilidad del formato actual", hole=0.3)
        st.plotly_chart(fig_util, use_container_width=True)

with c4_2:
    if 'Factores_Valor' in df.columns:
        factores = df['Factores_Valor'].astype(str).str.split(';').explode().str.strip()
        factores = factores[(factores != 'Otros') & (factores != '')]
        data_factores = factores.value_counts().reset_index()
        data_factores.columns = ['Factor', 'Cantidad']
        fig_factores = px.bar(data_factores, x='Cantidad', y='Factor', orientation='h', title="¿Qué factores dan valor a la ayudantía?", text_auto=True)
        st.plotly_chart(fig_factores, use_container_width=True)

st.divider()

st.subheader("Roles y Asistencia Estimada")
c5, c6 = st.columns(2)
with c5:
    if 'Asistencia_Estimada' in df.columns:
        data_asist = df['Asistencia_Estimada'].value_counts().reset_index()
        data_asist.columns = ['Asistencia Estimada', 'Cantidad']
        fig_asist = px.pie(data_asist, names='Asistencia Estimada', values='Cantidad', title="Asistencia estimada por los docentes", hole=0.4)
        st.plotly_chart(fig_asist, use_container_width=True)

with c6:
    if 'Roles_Ayudantia' in df.columns:
        roles = df['Roles_Ayudantia'].astype(str).str.split(';').explode().str.strip()
        roles = roles[(roles != 'Otros') & (roles != '')]
        data_roles = roles.value_counts().reset_index()
        data_roles.columns = ['Rol Principal', 'Cantidad']
        fig_roles = px.bar(data_roles, x='Cantidad', y='Rol Principal', orientation='h', title="Principales roles de la ayudantía", text_auto=True)
        st.plotly_chart(fig_roles, use_container_width=True)

st.divider()

st.subheader("Claridad y Percepción de Mejoras")
c7, c8 = st.columns(2)
with c7:
    if 'Claridad_Objetivo' in df.columns:
        data_claridad = df['Claridad_Objetivo'].value_counts().reset_index()
        data_claridad.columns = ['Claridad del Objetivo', 'Cantidad']
        fig_claridad = px.pie(data_claridad, names='Claridad del Objetivo', values='Cantidad', title="¿Qué tan claro está el objetivo para los alumnos?", hole=0.3)
        st.plotly_chart(fig_claridad, use_container_width=True)

with c8:
    if 'Mejora_Valor_Academico' in df.columns:
        mejoras = df['Mejora_Valor_Academico'].astype(str).str.split(';').explode().str.strip()
        mejoras = mejoras[(mejoras != 'Otros') & (mejoras != '')]
        data_mejoras = mejoras.value_counts().reset_index()
        data_mejoras.columns = ['Mejora Sugerida', 'Cantidad']
        fig_mejoras = px.bar(data_mejoras, x='Cantidad', y='Mejora Sugerida', orientation='h', title="¿Qué mejoraría el valor académico?", text_auto=True)
        st.plotly_chart(fig_mejoras, use_container_width=True)
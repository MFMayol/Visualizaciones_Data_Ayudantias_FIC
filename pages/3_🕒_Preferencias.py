import streamlit as st
import sys
import os
import plotly.express as px

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_processor import cargar_datos_estudiantes, aplicar_filtros_globales

st.set_page_config(page_title="Preferencias", page_icon="🕒", layout="wide")
st.title("🕒 Preferencias y Formatos")
st.markdown("Modalidades, horarios y razones para la baja asistencia a las ayudantías.")

df = cargar_datos_estudiantes()
df = aplicar_filtros_globales(df)

st.subheader("Formatos de Ayudantía Ideales")
c1, c2 = st.columns(2)

with c1:
    if 'Modalidad_Preferida' in df.columns:
        data_mod = df['Modalidad_Preferida'].dropna().value_counts().reset_index()
        data_mod.columns = ['Modalidad', 'Cantidad']
        fig_mod = px.pie(data_mod, names='Modalidad', values='Cantidad', 
                         title="Modalidad Preferida", hole=0.3)
        fig_mod.update_traces(textinfo='percent+value')
        st.plotly_chart(fig_mod, use_container_width=True)

with c2:
    if 'Horario_Preferido' in df.columns:
        data_hor = df['Horario_Preferido'].dropna().value_counts().reset_index()
        data_hor.columns = ['Horario', 'Cantidad']
        data_hor = data_hor.sort_values('Cantidad', ascending=False)
        fig_hor = px.bar(data_hor, x='Horario', y='Cantidad', text_auto=True, 
                         title="Horario Preferido", color='Horario')
        fig_hor.update_traces(textposition="outside")
        st.plotly_chart(fig_hor, use_container_width=True)

st.divider()

st.subheader("Razones y Formatos de Aprendizaje")
c3, c4 = st.columns(2)

with c3:
    if 'Formato_Aprendizaje' in df.columns:
        data_form = df['Formato_Aprendizaje'].dropna().value_counts().reset_index()
        data_form.columns = ['Formato', 'Cantidad']
        data_form = data_form.sort_values('Cantidad', ascending=True)
        fig_form = px.bar(data_form, y='Formato', x='Cantidad', text_auto=True, 
                          orientation='h', title="Formato que más ayuda a aprender")
        fig_form.update_traces(textposition="outside")
        st.plotly_chart(fig_form, use_container_width=True)

with c4:
    if 'Razones_No_Asistencia' in df.columns:
        razones = df['Razones_No_Asistencia'].dropna().astype(str).str.split(';').explode().str.strip()
        razones = razones[razones != '']
        data_razones = razones.value_counts().reset_index()
        data_razones.columns = ['Razón', 'Cantidad']
        data_razones = data_razones.sort_values('Cantidad', ascending=True)
        fig_razones = px.bar(data_razones, y='Razón', x='Cantidad', text_auto=True, 
                             orientation='h', title="Razones principales para NO asistir")
        fig_razones.update_traces(textposition="outside")
        st.plotly_chart(fig_razones, use_container_width=True)
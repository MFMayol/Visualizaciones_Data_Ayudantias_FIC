import streamlit as st
import sys
import os
import plotly.express as px

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_processor import cargar_datos_estudiantes, aplicar_filtros_globales

st.set_page_config(page_title="Participación", page_icon="🎓", layout="wide")
st.title("🎓 Participación como Ayudante")
st.markdown("Perspectiva de los estudiantes sobre postular y ejercer como ayudantes de la universidad.")

df = cargar_datos_estudiantes()
df = aplicar_filtros_globales(df)

st.subheader("Experiencia Previa y Barreras")
c1, c2 = st.columns(2)

with c1:
    if 'Ha_Sido_Ayudante' in df.columns:
        data_ha_sido = df['Ha_Sido_Ayudante'].dropna().value_counts().reset_index()
        data_ha_sido.columns = ['Respuesta', 'Cantidad']
        fig_ha_sido = px.pie(data_ha_sido, names='Respuesta', values='Cantidad', 
                             title="¿Has sido ayudante alguna vez?", hole=0.4, color='Respuesta')
        fig_ha_sido.update_traces(textinfo='percent+value')
        st.plotly_chart(fig_ha_sido, use_container_width=True)

with c2:
    if 'Razones_No_Ayudante' in df.columns:
        # Extraer las respuestas múltiples
        motivos = df['Razones_No_Ayudante'].dropna().astype(str).str.split(';').explode().str.strip()
        motivos = motivos[motivos != '']
        data_motivos = motivos.value_counts().reset_index()
        data_motivos.columns = ['Razón', 'Cantidad']
        data_motivos = data_motivos.sort_values('Cantidad', ascending=True)
        
        fig_motivos = px.bar(data_motivos, y='Razón', x='Cantidad', text_auto=True, 
                             orientation='h', title="Razones por las que NO han sido ayudantes")
        fig_motivos.update_traces(textposition="outside")
        st.plotly_chart(fig_motivos, use_container_width=True)
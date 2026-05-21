import streamlit as st
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_processor import cargar_datos_docentes, aplicar_filtros_globales, verificar_contrasena

st.set_page_config(page_title="Comentarios Docentes", page_icon="💬", layout="wide")
verificar_contrasena()

st.title("💬 Comentarios y Análisis Abierto (Docentes)")
st.markdown("Explora de forma dinámica las fortalezas, debilidades y oportunidades de mejora indicadas por los profesores.")

df = cargar_datos_docentes()

if df.empty:
    st.warning("No se encontró el archivo `BD_Docentes.csv` en la carpeta `data`. Asegúrate de subirlo.")
    st.stop()

df = aplicar_filtros_globales(df)

def generar_nube_y_comentarios(columna, titulo_nube):
    if columna in df.columns:
        comentarios = df[df[columna] != 'Otros'][columna].dropna().astype(str).tolist()
        comentarios = [c for c in comentarios if len(c.strip()) > 5]
        
        if comentarios:
            with st.expander(f"Ver respuestas completas ({len(comentarios)})"):
                for c in comentarios:
                    st.info(f'"{c}"')
            
            texto_completo = " ".join(comentarios)
            if len(texto_completo.strip()) > 10:
                stopwords_es = set(STOPWORDS)
                stopwords_es.update([
                    "que", "de", "la", "el", "en", "y", "a", "los", "se", "del", "las", "un", "una", 
                    "con", "para", "por", "no", "como", "es", "o", "mas", "ms", "lo", "pero", 
                    "si", "al", "su", "porque", "sea", "sean", "hay", "muy", "son", "est", "esta", 
                    "este", "todo", "todas", "todos", "te", "me", "le", "nos", "sus", "hacer", "ya", 
                    "cuando", "eso", "esas", "esos", "tambien", "tambin", "nada", "tiene", "tienen"
                ])
                
                st.markdown(f"**☁️ {titulo_nube}**")
                wordcloud = WordCloud(width=800, height=350, background_color='white', stopwords=stopwords_es, colormap='inferno').generate(texto_completo)
                fig, ax = plt.subplots(figsize=(10, 4.5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
        else:
            st.write("No hay comentarios disponibles en esta sección.")

tab1, tab2, tab3 = st.tabs(["Fortalezas y Debilidades", "Estándar vs Flexible", "Mejoras Inmediatas"])
with tab1:
    generar_nube_y_comentarios('Fortalezas_Debilidades', "Nube de Palabras: Fortalezas y Debilidades")
with tab2:
    generar_nube_y_comentarios('Estandar_Minimo', "Nube de Palabras: Estándar Mínimo vs Flexible")
with tab3:
    generar_nube_y_comentarios('Mejora_Inmediata', "Nube de Palabras: Oportunidades de Mejora Inmediata")
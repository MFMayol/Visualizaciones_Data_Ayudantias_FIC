import streamlit as st
import sys
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_processor import cargar_datos_estudiantes, aplicar_filtros_globales, verificar_contrasena

st.set_page_config(page_title="Comentarios", page_icon="💬", layout="wide")

# Validar contraseña
verificar_contrasena()

st.title("💬 Comentarios y Sugerencias Abiertas")
st.markdown("Explora de forma dinámica lo que los estudiantes expresaron en las preguntas de desarrollo.")

df = cargar_datos_estudiantes()
df = aplicar_filtros_globales(df)

st.subheader("📊 Tasa de Respuesta en Preguntas Abiertas")
col_m1, col_m2, col_m3 = st.columns(3)

def calcular_tasa(columna):
    if columna in df.columns:
        respuestas = len(df[df[columna] != 'Otros'])
        total = len(df)
        return f"{(respuestas/total)*100:.1f}%" if total > 0 else "0%"
    return "0%"

col_m1.metric("Lo más importante", calcular_tasa('Importante_Ayudantia'))
col_m2.metric("Qué cambiarían", calcular_tasa('Cambiar_Ayudantia'))
col_m3.metric("Comentarios Generales", calcular_tasa('Comentarios_Generales'))

st.divider()

st.subheader("🔍 Buscador de Comentarios")
busqueda = st.text_input("Ingresa una palabra clave para buscar en las respuestas (ej. 'horario', 'presencial'):")
if busqueda:
    for col, titulo in [('Importante_Ayudantia', 'Lo más importante'), ('Cambiar_Ayudantia', 'Lo que cambiarían'), ('Comentarios_Generales', 'Comentarios Generales')]:
        if col in df.columns:
            resultados = df[(df[col] != 'Otros') & (df[col].astype(str).str.contains(busqueda, case=False, na=False))][col].tolist()
            if resultados:
                with st.expander(f"Resultados en '{titulo}' ({len(resultados)} encontrados)"):
                    for r in resultados:
                        st.markdown(f"- {r}")
                        
st.divider()

def mostrar_todos_los_comentarios(columna, titulo):
    st.subheader(titulo)
    if columna in df.columns:
        # Excluimos la etiqueta 'Otros' para no ensuciar la visualización
        comentarios = df[df[columna] != 'Otros'][columna].dropna().astype(str).tolist()
        # Filtrar posibles respuestas muy cortas (ej. '.', 'no', 'nada')
        comentarios = [c for c in comentarios if len(c.strip()) > 5]
        if comentarios:
            with st.container(height=400):
                for c in comentarios:
                    st.info(f'"{c}"')
        else:
            st.write("No hay comentarios disponibles para esta sección.")

def mostrar_wordcloud(columna, titulo):
    st.subheader(titulo)
    if columna in df.columns:
        textos = df[df[columna] != 'Otros'][columna].dropna().astype(str).tolist()
        texto_completo = " ".join(textos)
        if len(texto_completo.strip()) > 10:
            stopwords_es = set(STOPWORDS)
            stopwords_es.update([
                "que", "de", "la", "el", "en", "y", "a", "los", "se", "del", "las", "un", "una", 
                "con", "para", "por", "no", "como", "es", "o", "mas", "ms", "ms", "lo", "pero", 
                "si", "al", "su", "porque", "sea", "sean", "hay", "muy", "son", "est", "esta", 
                "este", "todo", "todas", "todos", "te", "me", "le", "nos", "sus", "hacer", "ya", 
                "cuando", "eso", "esas", "esos", "tambien", "tambin", "nada", "tiene", "tienen"
            ])
            wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords_es, colormap='viridis').generate(texto_completo)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
        else:
            st.write("No hay suficientes palabras para generar la nube.")

st.header("💬 Todos los Comentarios")
c1, c2 = st.columns(2)

with c1:
    mostrar_todos_los_comentarios('Importante_Ayudantia', "¿Qué es lo más importante en una ayudantía?")

with c2:
    mostrar_todos_los_comentarios('Cambiar_Ayudantia', "Si pudieras cambiar UNA cosa, ¿qué sería?")

mostrar_todos_los_comentarios('Comentarios_Generales', "Comentarios Adicionales y Contexto")

st.divider()
st.header("☁️ Nubes de Palabras (Temas recurrentes)")
tab1, tab2, tab3 = st.tabs(["Lo más importante", "Lo que cambiarían", "Comentarios Generales"])

with tab1:
    mostrar_wordcloud('Importante_Ayudantia', "Conceptos Clave: Lo más importante")
with tab2:
    mostrar_wordcloud('Cambiar_Ayudantia', "Conceptos Clave: Lo que cambiarían")
with tab3:
    mostrar_wordcloud('Comentarios_Generales', "Conceptos Clave: Comentarios Generales")
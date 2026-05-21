import streamlit as st
from src.data_processor import verificar_contrasena, cargar_datos_estudiantes, cargar_datos_docentes

# Configuración inicial de la página (debe ser el primer comando de Streamlit)
st.set_page_config(
    page_title="Proyecto Ayudantías",
    page_icon="🏠",
    layout="wide"
)

# Validar contraseña antes de continuar
verificar_contrasena()

# Cargar datos para mostrar un resumen rápido en la portada
df = cargar_datos_estudiantes()
df_docentes = cargar_datos_docentes()
total_encuestados = df['ID'].nunique() if 'ID' in df.columns else len(df)
total_docentes = df_docentes['ID'].nunique() if not df_docentes.empty and 'ID' in df_docentes.columns else len(df_docentes)

st.title("🏠 Dashboard: Proyecto Ayudantías")
st.markdown("---")

st.markdown("""
Bienvenido a la plataforma interactiva de análisis de ayudantías. Este dashboard ha sido diseñado para transformar las respuestas de los estudiantes en **insights accionables** que permitan mejorar la calidad, asistencia y formato de las sesiones de apoyo académico.
""")

st.subheader("💡 Resumen Rápido")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Estudiantes Encuestados", total_encuestados)
col2.metric("Docentes Encuestados", total_docentes)
if 'Sede' in df.columns:
    top_sede = df[df['Sede'] != 'Otros']['Sede'].mode()[0]
    col3.metric("Sede más participativa (Est.)", top_sede)
if 'Frecuencia_Asistencia' in df.columns:
    top_frec = df[df['Frecuencia_Asistencia'] != 'Otros']['Frecuencia_Asistencia'].mode()[0]
    col4.metric("Asistencia Común (Est.)", top_frec)

st.markdown("---")

st.subheader("📌 Índice de Navegación")
st.markdown("👈 Utiliza el **menú lateral izquierdo** para explorar a fondo cada una de las secciones:")

c1, c2 = st.columns(2)

with c1:
    st.info("**1. 📊 Vista General**\n\nResumen demográfico, asistencia general y uso de herramientas de estudio alternativas.")
    st.success("**2. ⭐ Evaluación**\n\nAnálisis profundo de las notas asignadas a los ayudantes (Claridad, Utilidad, Comodidad) y dispersión.")
    st.warning("**3. 🕒 Preferencias**\n\nEstudio detallado sobre los horarios, modalidades (online vs presencial) y formatos ideales.")
    st.error("**4. 🎓 Participación**\n\nBarreras y motivaciones de los alumnos para postularse como futuros ayudantes.")
    st.info("**5. 💬 Comentarios (Est.)**\n\nBuscador interactivo y nubes de palabras para entender conceptos y quejas recurrentes.")

with c2:
    st.success("**6. 🔍 Análisis Cruzado**\n\nCruces de variables avanzados (Ej. Modalidad vs Frecuencia) y Mapas de Calor de correlaciones.")
    st.warning("**7. 🤖 Machine Learning**\n\nModelos de K-Means Clustering y PCA para descubrir perfiles ocultos de los estudiantes.")
    st.info("**8. 👨‍🏫 Docentes General**\n\nVisión de los académicos sobre el valor, alineación y modalidades de las ayudantías.")
    st.error("**9. 🤝 Coordinación**\n\nEstudio detallado sobre la comunicación, preparación y obstáculos con los ayudantes.")
    st.success("**10. 💬 Comentarios Docentes**\n\nAnálisis cualitativo y nubes de palabras de fortalezas y oportunidades de mejora.")

st.divider()
st.caption("🚀 Sistema de Visualización de Datos desarrollado con Streamlit y Python.")
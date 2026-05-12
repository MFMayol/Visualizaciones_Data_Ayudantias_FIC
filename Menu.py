import streamlit as st

# Configuración inicial de la página (debe ser el primer comando de Streamlit)
st.set_page_config(
    page_title="Proyecto Ayudantías",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Bienvenido al Proyecto Ayudantías")

st.markdown("""
Esta es la página principal de la aplicación interactiva para visualizar y analizar los datos de las encuestas de ayudantías.

👈 **Utiliza el menú lateral para navegar a las distintas páginas de la aplicación.**

### ¿Qué encontrarás aquí?
En esta plataforma podrás explorar las respuestas de los estudiantes, analizar métricas de asistencia, motivos por los cuales asisten o no, la percepción sobre la calidad de los ayudantes y las modalidades preferidas.
""")

st.info("Ve a la sección **1 📊 Visualizacion** en la barra lateral para interactuar con la base de datos.")
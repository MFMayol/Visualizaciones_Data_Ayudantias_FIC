import pandas as pd
import os
import streamlit as st

@st.cache_data
def cargar_datos_estudiantes():
    """
    Carga la base de datos de estudiantes desde la carpeta 'data'.
    Usa cache para evitar recargar el archivo en cada interacción.
    """
    # Obtenemos la ruta absoluta del directorio actual (src)
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    # Subimos un nivel y entramos a data
    ruta_archivo = os.path.join(directorio_actual, '..', 'data', 'BD_Estudiantes.csv')
    
    # Leemos el archivo considerando el separador ';' y el formato de caracteres
    df = pd.read_csv(ruta_archivo, sep=';', encoding='latin-1')
    
    # Renombramos algunas columnas clave usando palabras contenidas en ellas para 
    # evitar problemas con los caracteres especiales o mal codificados ().
    nuevos_nombres = {}
    for col in df.columns:
        col_lower = col.lower()
        if 'sede' in col_lower: nuevos_nombres[col] = 'Sede'
        elif 'hora de inicio' in col_lower: nuevos_nombres[col] = 'Fecha_Respuesta'
        elif 'frecuencia asistes' in col_lower: nuevos_nombres[col] = 'Frecuencia_Asistencia'
        elif 'utilidad real' in col_lower: nuevos_nombres[col] = 'Utilidad'
        elif 'comodidad' in col_lower and 'preguntas' in col_lower: nuevos_nombres[col] = 'Comodidad'
        elif 'claridad' in col_lower: nuevos_nombres[col] = 'Claridad'
        elif 'preparaci' in col_lower and 'evaluaciones' in col_lower: nuevos_nombres[col] = 'Preparacion'
        elif 'modalidad te sirve' in col_lower: nuevos_nombres[col] = 'Modalidad_Preferida'
        elif 'horario es m' in col_lower: nuevos_nombres[col] = 'Horario_Preferido'
        elif 'diferencias grandes' in col_lower: nuevos_nombres[col] = 'Diferencias_Calidad'
        elif 'sido ayudante' in col_lower and 'uai' in col_lower: nuevos_nombres[col] = 'Ha_Sido_Ayudante'
        elif 'formato de ayudant' in col_lower and 'aprender' in col_lower: nuevos_nombres[col] = 'Formato_Aprendizaje'
        elif 'razones por la que no asistes' in col_lower: nuevos_nombres[col] = 'Razones_No_Asistencia'
        elif 'utilizas para estudiar' in col_lower: nuevos_nombres[col] = 'Alternativas_Estudio'
        elif 'alineada sientes' in col_lower: nuevos_nombres[col] = 'Alineacion_Clases'
        elif 'problemas con una correcci' in col_lower: nuevos_nombres[col] = 'Resolucion_Problemas'
        elif 'no has sido ayudante' in col_lower: nuevos_nombres[col] = 'Razones_No_Ayudante'
        elif 'importante que deber' in col_lower: nuevos_nombres[col] = 'Importante_Ayudantia'
        elif 'cambiar una sola cosa' in col_lower: nuevos_nombres[col] = 'Cambiar_Ayudantia'
        elif 'comentarios sobre las ayudantias' in col_lower: nuevos_nombres[col] = 'Comentarios_Generales'
        
    df.rename(columns=nuevos_nombres, inplace=True)
    
    # Rellenar los valores nulos (vacíos/sin responder) con la etiqueta "Otros"
    # Convertimos el DataFrame a 'object' primero para evitar advertencias de incompatibilidad de tipos
    df = df.astype(object).fillna("Otros")

    return df

def aplicar_filtros_globales(df):
    """Agrega filtros interactivos en la barra lateral para todas las páginas."""
    st.sidebar.header("🌍 Filtros Globales")
    if 'Sede' in df.columns:
        sedes = df['Sede'].dropna().unique().tolist()
        sede_seleccionada = st.sidebar.multiselect("Filtrar por Sede", sedes, default=sedes)
        df = df[df['Sede'].isin(sede_seleccionada)]
        
    # Añadir botón de exportación en la barra lateral
    st.sidebar.divider()
    st.sidebar.header("💾 Exportar Datos")
    # utf-8-sig es ideal para que Excel lea correctamente los tildes y caracteres especiales
    csv = df.to_csv(index=False, sep=';').encode('utf-8-sig')
    st.sidebar.download_button(
        label="📥 Descargar CSV Filtrado",
        data=csv,
        file_name="datos_ayudantias_filtrados.csv",
        mime="text/csv",
    )

    return df

def verificar_contrasena():
    """Valida que el usuario tenga la contraseña correcta antes de mostrar el contenido."""
    def password_entered():
        # AQUÍ DEFINES TU CONTRASEÑA:
        if st.session_state["password"] == "UAI":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Eliminar contraseña por seguridad
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.title("🔒 Acceso Restringido")
    st.text_input(
        "Por favor, introduce la contraseña para acceder al Dashboard:",
        type="password",
        on_change=password_entered,
        key="password"
    )
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("😕 Contraseña incorrecta.")
    
    st.stop()  # Detiene la ejecución de la página si no se ha introducido la clave
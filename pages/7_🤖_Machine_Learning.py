import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px

# Importamos librerías de Machine Learning
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_processor import cargar_datos_estudiantes, aplicar_filtros_globales

st.set_page_config(page_title="Machine Learning", page_icon="🤖", layout="wide")
st.title("🤖 Machine Learning: Segmentación de Estudiantes")
st.markdown("""
Esta página utiliza aprendizaje automático no supervisado (**K-Means Clustering**) para encontrar perfiles o "grupos" ocultos de estudiantes basándose en cómo evaluaron a los ayudantes.

### 🧠 ¿Cómo funciona este modelo?
Para lograr esta visualización, el sistema realiza automáticamente los siguientes pasos:
1. **Selección y Limpieza**: Extrae las evaluaciones numéricas (1 al 5) de **Utilidad, Claridad, Comodidad y Preparación**, excluyendo aquellas filas vacías.
2. **Estandarización de Datos**: Escala matemáticamente las notas para que el algoritmo interprete correctamente las distancias entre respuestas y evite sesgos numéricos.
3. **K-Means Clustering**: Un algoritmo de agrupamiento analiza todas las encuestas e identifica a estudiantes con patrones de respuesta similares. (Puedes ajustar la cantidad de grupos en la barra lateral).
4. **Reducción de Dimensionalidad (PCA)**: Dado que estamos analizando 4 métricas al mismo tiempo (4 dimensiones), aplicamos **Análisis de Componentes Principales (PCA)** para comprimir la información en 2 y 3 dimensiones. Esto nos permite visualizar las agrupaciones espacialmente y entender qué variables influyen más en las diferencias entre estudiantes.
""")

df = cargar_datos_estudiantes()
df = aplicar_filtros_globales(df)

st.divider()

# 1. Seleccionamos las columnas numéricas que usará el modelo
metricas_ml = ['Utilidad', 'Claridad', 'Comodidad', 'Preparacion']

if set(metricas_ml).issubset(df.columns):
    # Preparamos los datos: Convertir a numérico (ignorando "Otros") y eliminar valores nulos
    df_ml = df[metricas_ml].copy()
    for col in metricas_ml:
        df_ml[col] = pd.to_numeric(df_ml[col], errors='coerce')
    
    # Conservamos los ndices originales para luego cruzar con los datos originales
    df_ml = df_ml.dropna()
    
    if len(df_ml) > 10:
        st.sidebar.markdown("### ⚙️ Hiperparámetros del Modelo")
        n_clusters = st.sidebar.slider("Número de Perfiles (Clusters)", min_value=2, max_value=5, value=3)
        
        # 2. Estandarizamos los datos (buena prctica en Machine Learning)
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df_ml)
        
        # 3. Entrenamos el modelo K-Means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
        df_ml['Cluster'] = kmeans.fit_predict(df_scaled)
        df_ml['Cluster'] = df_ml['Cluster'].astype(str) # Convertir a texto para plotly
        
        st.subheader("💡 Perfiles Encontrados (Centroides)")
        st.markdown("Cada barra representa la calificación promedio que ese grupo le otorgó a los ayudantes.")
        
        # Agrupamos por cluster para ver qu define a cada grupo
        perfiles = df_ml.groupby('Cluster').mean().reset_index()
        perfiles_melted = perfiles.melt(id_vars='Cluster', var_name='Métrica', value_name='Promedio')
        
        fig_perfiles = px.bar(perfiles_melted, x='Métrica', y='Promedio', color='Cluster', 
                              barmode='group', title="Análisis de los Perfiles de Estudiantes")
        st.plotly_chart(fig_perfiles, use_container_width=True)
        
        st.divider()
        
        st.subheader("🌌 Visualización Avanzada con PCA")
        st.markdown("Explora las agrupaciones de estudiantes proyectadas en múltiples dimensiones y analiza el peso estadístico de cada métrica.")
        
        # 4. Reducción de dimensionalidad para visualizar en 2D y 3D
        pca = PCA(n_components=3)
        pca_results = pca.fit_transform(df_scaled)
        
        df_ml['PCA1'] = pca_results[:, 0]
        df_ml['PCA2'] = pca_results[:, 1]
        df_ml['PCA3'] = pca_results[:, 2]

        tab_2d, tab_3d, tab_analisis = st.tabs(["Gráfico 2D", "Gráfico 3D (Interactivo)", "Análisis de Componentes (Pesos)"])
        
        with tab_2d:
            fig_pca2d = px.scatter(df_ml, x='PCA1', y='PCA2', color='Cluster', size_max=10, 
                                   title="Mapa Espacial 2D de los Perfiles", opacity=0.8)
            fig_pca2d.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')))
            st.plotly_chart(fig_pca2d, use_container_width=True)
            
        with tab_3d:
            fig_pca3d = px.scatter_3d(df_ml, x='PCA1', y='PCA2', z='PCA3', color='Cluster',
                                      title="Proyección Espacial 3D (Gira el gráfico con el mouse)", opacity=0.8)
            fig_pca3d.update_traces(marker=dict(size=6, line=dict(width=1, color='DarkSlateGrey')))
            st.plotly_chart(fig_pca3d, use_container_width=True)
            
        with tab_analisis:
            c_pca1, c_pca2 = st.columns(2)
            with c_pca1:
                var_exp = pca.explained_variance_ratio_ * 100
                df_var = pd.DataFrame({'Componente': ['PC1', 'PC2', 'PC3'], 'Varianza Explicada (%)': var_exp})
                fig_var = px.bar(df_var, x='Componente', y='Varianza Explicada (%)', text_auto='.1f', title="Varianza retenida por Componente")
                st.plotly_chart(fig_var, use_container_width=True)
            with c_pca2:
                loadings = pd.DataFrame(pca.components_.T, columns=['PC1', 'PC2', 'PC3'], index=metricas_ml)
                fig_loadings = px.imshow(loadings, text_auto=".2f", color_continuous_scale='RdBu_r', aspect='auto', title="Peso de las Variables originales en cada Componente")
                st.plotly_chart(fig_loadings, use_container_width=True)
    else:
        st.warning("No hay suficientes datos válidos para entrenar el modelo (mínimo 10 encuestas numéricas).")
import streamlit as st
import requests

# Configuración de la página
st.set_page_config(page_title="Búsqueda Semántica con IA", page_icon="🔍", layout="wide")

# URL de tu API (usaremos localhost si corres local, o el nombre del contenedor en Docker)
API_URL = "http://localhost:8000"

st.title(" Motor de Búsqueda Semántica con Inteligencia Artificial")
st.markdown("Sube tus documentos y haz preguntas en lenguaje natural. La IA encontrará las respuestas basándose en el contexto.")

# BARRA LATERAL: Subida de Documentos
with st.sidebar:
    st.header(" Tus Documentos")
    archivo_subido = st.file_uploader("Sube un archivo PDF", type=["pdf"])
    
    if st.button("Procesar e Indexar PDF"):
        if archivo_subido is not None:
            with st.spinner('Extrayendo texto y generando embeddings...'):
                try:
                    # Preparamos el archivo para enviarlo a la API
                    files = {"file": (archivo_subido.name, archivo_subido.getvalue(), "application/pdf")}
                    response = requests.post(f"{API_URL}/upload", files=files)
                    
                    if response.status_code == 200:
                        st.success(f"¡Éxito! {archivo_subido.name} indexado correctamente.")
                    else:
                        st.error(f"Error de la API: {response.json().get('detail')}")
                except Exception as e:
                    st.error(f"No se pudo conectar con la API. ¿Está encendida? Detalle: {e}")
        else:
            st.warning("Por favor, selecciona un archivo primero.")


# PANTALLA PRINCIPAL: Buscador
st.divider()
st.subheader(" Hazle una pregunta a tus documentos")

pregunta = st.text_input("Ejemplo: ¿Cuáles son las responsabilidades del puesto?")

if st.button("Buscar con IA"):
    if pregunta:
        with st.spinner('Buscando en la base de datos vectorial...'):
            try:
                payload = {"query": pregunta, "top_k": 3}
                response = requests.post(f"{API_URL}/search", json=payload)
                
                if response.status_code == 200:
                    resultados = response.json().get("results", [])
                    
                    if not resultados:
                        st.info("No se encontró información relevante para tu pregunta.")
                    else:
                        for i, res in enumerate(resultados):
                            with st.expander(f" Resultado {i+1} (Fuente: {res['metadata'].get('source', 'Desconocida')})", expanded=True):
                                st.write(res['content'])
                else:
                    st.error(f"Error al buscar: {response.json().get('detail')}")
            except Exception as e:
                st.error(f"No se pudo conectar con la API. Detalle: {e}")
    else:
        st.warning("Escribe una pregunta para buscar.")
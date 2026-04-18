# AI Semantic Document Search

Este proyecto es un motor de búsqueda semántica y procesamiento de lenguaje natural (NLP) diseñado para operar íntegramente de forma local. Permite la ingesta de documentos en formato PDF, la generación de embeddings mediante modelos de código abierto y la recuperación de información basada en el contexto, eliminando la dependencia de servicios de pago externos y garantizando la privacidad de los datos.

## Arquitectura del Sistema

El sistema implementa una arquitectura modular siguiendo principios de Clean Architecture, separando la interfaz de usuario, la lógica de red y el motor de procesamiento de datos.

```text
[Flujo de Datos]
Usuario (Interfaz) -> Carga de PDF -> Extracción de Texto (PyPDF)
Texto Extraido -> Generación de Vectores (HuggingFace MiniLM-L6-v2)
Vectores -> Almacenamiento y Persistencia (ChromaDB)
Consulta del Usuario -> Vectorización de Consulta -> Búsqueda de Similitud (Coseno)
```

## Características Técnicas

* **Operación Local Privada:** Procesamiento de embeddings realizado en el host local mediante `sentence-transformers`. No se envían datos a APIs externas.
* **Procesamiento de PDF en Memoria:** Extracción de texto utilizando flujos de bytes (`io.BytesIO`) para evitar escrituras innecesarias en disco y mejorar la velocidad de respuesta.
* **Búsqueda por Similitud Semántica:** Recuperación de fragmentos de información basada en el significado latente del texto en lugar de coincidencias exactas de palabras clave.
* **Entorno Contenerizado:** Configuración completa mediante Docker y Docker Compose para asegurar la reproducibilidad del entorno en cualquier sistema.
* **Interfaz de Usuario Funcional:** Frontend interactivo desarrollado en Streamlit que facilita la interacción con el backend de FastAPI.

## Stack Tecnológico

* **Backend:** FastAPI, Uvicorn, Pydantic (Validación de datos).
* **Inteligencia Artificial:** LangChain, HuggingFace, Sentence-Transformers.
* **Base de Datos de Vectores:** ChromaDB.
* **Frontend:** Streamlit.
* **Infraestructura:** Docker, Docker Compose.

---

## Guía de Inicio Rápido con Docker

La implementación mediante contenedores es el método recomendado para asegurar que todas las dependencias funcionen correctamente.

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/semantic-search-pro.git](https://github.com/tu-usuario/semantic-search-pro.git)
   cd semantic-search-pro
   ```

2. **Desplegar los servicios:**
   ```bash
   docker-compose up --build
   ```
   *Nota: Durante el primer despliegue, el sistema descargará el modelo de lenguaje desde HuggingFace (aproximadamente 80MB).*

3. **Direcciones de acceso:**
   * **Interfaz de Usuario:** `http://localhost:8501`
   * **Documentación de API (Swagger):** `http://localhost:8000/docs`

---

## Instalación para Desarrollo Local

Si prefiere ejecutar el proyecto fuera de un contenedor:

1. **Configurar el entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: .\venv\Scripts\activate
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuración de variables de entorno:**
   Copie el contenido de `.env.example` a un nuevo archivo llamado `.env`.

4. **Ejecución de los servicios:**
   * **Iniciar Backend:** `uvicorn src.main:app --reload --port 8000`
   * **Iniciar Frontend:** `streamlit run src/frontend/app.py`

## Estructura del Proyecto

* `src/main.py`: Punto de entrada de la API y definición de rutas.
* `src/services/ai_service.py`: Lógica de carga de modelos y generación de embeddings.
* `src/services/document_parser.py`: Utilidades de extracción de texto de archivos binarios.
* `src/database/vector_store.py`: Gestión de la conexión y consultas a ChromaDB.
* `src/frontend/app.py`: Interfaz gráfica de usuario.
* `tests/`: Suite de pruebas unitarias para validación de servicios y endpoints.

## Decisiones de Ingeniería

* **Elección de ChromaDB:** Se seleccionó por su capacidad de operar en modo embebido, lo que simplifica la infraestructura al no requerir un servidor de base de datos independiente.
* **Optimización de Embeddings:** El modelo `all-MiniLM-L6-v2` ofrece un equilibrio óptimo entre precisión semántica y bajo consumo de recursos (CPU/RAM).
* **Manejo de Concurrencia:** El uso de FastAPI con programación asíncrona permite que el servidor gestione múltiples solicitudes de carga y búsqueda de forma eficiente.


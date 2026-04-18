# run_demo.py
from src.database.vector_store import VectorDB

def main():
    print(" Iniciando el motor de búsqueda semántica...\n")
    
    # 1. Inicializar la base de datos (y descargar el modelo de IA si es la primera vez)
    print(" Cargando modelo de Inteligencia Artificial y ChromaDB...")
    db = VectorDB()
    
    # 2. Ingestar datos de prueba
    print("\n Indexando documentos de prueba...")
    documentos = [
        {"texto": "Python fue creado por Guido van Rossum y lanzado en 1991.", "fuente": "historia_python.txt"},
        {"texto": "Docker permite empaquetar aplicaciones en contenedores ligeros.", "fuente": "manual_docker.pdf"},
        {"texto": "La búsqueda semántica entiende el contexto en lugar de buscar palabras exactas.", "fuente": "ia_conceptos.md"},
        {"texto": "El aguacate es una fruta rica en grasas saludables.", "fuente": "nutricion.csv"}
    ]
    
    for doc in documentos:
        db.add_document(text=doc["texto"], metadata={"source": doc["fuente"]})
    print(" 4 documentos indexados correctamente.")

    # 3. Hacer una búsqueda semántica
    pregunta = "¿Quién inventó el lenguaje Python?"
    print(f"\n Realizando consulta: '{pregunta}'")
    
    resultados = db.search(query=pregunta, top_k=1)
    
    # 4. Mostrar resultados
    print("\n RESULTADO DE LA IA:")
    for res in resultados:
        print(f"   -> Texto encontrado: '{res.page_content}'")
        print(f"   -> Fuente original: {res.metadata.get('source')}\n")

if __name__ == "__main__":
    main()
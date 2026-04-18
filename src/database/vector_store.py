import os
from langchain_community.vectorstores import Chroma
from src.services.ai_service import EmbeddingService

class VectorDB:
    def __init__(self):
        # Instanciamos nuestro servicio de embeddings
        self.embed_service = EmbeddingService().embeddings
        
        # Usamos una variable de entorno para la ruta (definida en docker-compose)
        self.persist_directory = os.getenv("CHROMA_DB_PATH", "./chroma_data")
        
        # Inicializamos ChromaDB
        self.db = Chroma(
            embedding_function=self.embed_service,
            persist_directory=self.persist_directory
        )

    def add_document(self, text: str, metadata: dict = None):
        """Convierte el texto a vector y lo guarda persistente en disco."""
        # Chroma se encarga de usar el embed_service automáticamente aquí
        self.db.add_texts(texts=[text], metadatas=[metadata] if metadata else None)

    def search(self, query: str, top_k: int = 3):
        """Busca los 'top_k' documentos más similares a la consulta."""
        return self.db.similarity_search(query, k=top_k)
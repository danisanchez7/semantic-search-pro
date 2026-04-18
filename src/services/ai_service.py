from langchain_community.embeddings import HuggingFaceEmbeddings

class EmbeddingService:
    def __init__(self):
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.embeddings = HuggingFaceEmbeddings(model_name=self.model_name)

    def generate_vector(self, text: str):
        """Transforma un texto en una lista de números (embedding)"""
        return self.embeddings.embed_query(text)
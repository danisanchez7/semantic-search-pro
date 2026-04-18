from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from src.database.vector_store import VectorDB
from src.services.document_parser import DocumentParser # <-- IMPORTANTE: Nueva importación

app = FastAPI(
    title="Semantic Search API",
    description="Motor de búsqueda semántica con IA Open Source y ChromaDB",
    version="1.0.0"
)

db = VectorDB()

class DocumentInput(BaseModel):
    text: str
    source: str = "unknown"

class SearchQuery(BaseModel):
    query: str
    top_k: int = 3

@app.get("/")
def health_check():
    return {"status": "ok", "message": "API corriendo correctamente"}

# --- Endpoint Antiguo (Para texto manual) ---
@app.post("/ingest")
def ingest_document(doc: DocumentInput):
    try:
        db.add_document(text=doc.text, metadata={"source": doc.source})
        return {"message": "Documento indexado con éxito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==========================================
# NUEVO: Endpoint para subir PDFs Reales
# ==========================================
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Sube un archivo PDF, extrae su texto y lo indexa en la base de datos."""
    
    # 1. Validar que sea un PDF
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Actualmente solo soportamos archivos .pdf")
    
    try:
        # 2. Leer el archivo de forma asíncrona (no bloquea el servidor)
        contenido_bytes = await file.read()
        
        # 3. Extraer el texto usando nuestro parser
        texto_extraido = DocumentParser.parse_pdf(contenido_bytes)
        
        # 4. Validar que el PDF no estuviera vacío o fuera pura imagen (sin OCR)
        if not texto_extraido:
            raise HTTPException(status_code=400, detail="No se pudo extraer texto. Asegúrese de que el PDF no sea una imagen escaneada.")
        
        # 5. Ingestar el texto en la Base de Datos Vectorial
        db.add_document(text=texto_extraido, metadata={"source": file.filename})
        
        return {
            "message": "Archivo procesado e indexado con éxito",
            "filename": file.filename,
            "caracteres_extraidos": len(texto_extraido)
        }
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# --- Endpoint de Búsqueda ---
@app.post("/search")
def search_documents(query: SearchQuery):
    try:
        results = db.search(query=query.query, top_k=query.top_k)
        return {
            "results": [
                {"content": r.page_content, "metadata": r.metadata} 
                for r in results
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
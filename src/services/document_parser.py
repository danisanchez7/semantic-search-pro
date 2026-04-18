import io
from pypdf import PdfReader

class DocumentParser:
    """Clase encargada de extraer texto de diferentes formatos de archivo."""

    @staticmethod
    def parse_pdf(file_bytes: bytes) -> str:
        """
        Toma los bytes de un archivo PDF en memoria y devuelve todo su texto.
        """
        try:
            # Usamos io.BytesIO para leer el PDF directamente desde la memoria
            # sin tener que guardarlo físicamente en el disco del servidor.
            lector_pdf = PdfReader(io.BytesIO(file_bytes))
            
            texto_completo = ""
            for pagina in lector_pdf.pages:
                texto_extraido = pagina.extract_text()
                if texto_extraido:
                    texto_completo += texto_extraido + "\n"
            
            # Limpiamos espacios en blanco redundantes a los lados
            return texto_completo.strip()
            
        except Exception as e:
            # Si el PDF está corrupto o protegido con contraseña, lo capturamos
            raise ValueError(f"Error al procesar el PDF: {str(e)}")
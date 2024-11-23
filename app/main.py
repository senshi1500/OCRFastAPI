from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pytesseract
from app.api.OCR import process_image
from fastapi import Request

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Cambia esto según tu instalación
# pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract' # Para el contenedor de docker

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, lang_html: str = "es"):
    """Vista principal de la application"""
    try:
        return templates.TemplateResponse(f"upload_{lang_html}.html", {"request": request, "extracted_text": None})
    except Exception as e:
        return HTMLResponse(content=f"Error: {str(e)}", status_code=500)


@app.post("/v1/ocr", response_class=HTMLResponse)
async def ocr(request: Request, lang_html: str = "es", image: UploadFile = File(...)):
    """
        Realiza OCR en la imagen proporcionada y devuelve el texto extraído.

        Args:
            request (Request): La solicitud HTTP.
            lang_html (str): El idioma para la plantilla HTML.
            image (UploadFile): La imagen a procesar.

        Returns:
            HTMLResponse: La respuesta HTML con el texto extraído.
        """

    # Realizar OCR
    extracted_text = await process_image(image)
    return templates.TemplateResponse(f"base_{lang_html}.html", {"request": request, "extracted_text": extracted_text})


# Ruta para descargar el texto
@app.get("/download")
async def download_text(edited_text: str):
    """
    Descarga el texto del input del HTML en un archivo .txt

    edited_text: cadena de caracteres que proviene del textarea del HTML
    """
    # Guardar el texto en un archivo temporal
    file_path = "texto_guardado.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(edited_text)

    # Proporcionar el archivo para descargar
    return FileResponse(file_path, media_type='text/plain', filename='texto_guardado.txt')


@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request, lang_html: str = "es"):
    """Vista secundaria de la aplicacion con el texto extraído y pegado en el textarea"""
    return templates.TemplateResponse(f"upload_{lang_html}.html", {"request": request})


@app.post("/upload")
async def upload_file(request: Request):
    """Sube la imagen del input file al backend para que lo analise en OCR"""
    form = await request.form()
    file = form.get("file")
    # Aquí puedes manejar el archivo subido
    return {"filename": file.filename}

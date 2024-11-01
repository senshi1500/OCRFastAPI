from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pytesseract
from PIL import Image
import cv2
import numpy as np
from fastapi import Request

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Cambia esto según tu instalación
# pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract' # Para el contenedor de docker

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request, "extracted_text": None})


@app.post("/ocr")
async def ocr(request: Request, image: UploadFile = File(...)):
    # Leer la imagen
    image_data = await image.read()
    image_np = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Realizar OCR
    extracted_text = pytesseract.image_to_string(gray, lang='spa')  # Cambia 'spa' por 'eng' si es en inglés

    return templates.TemplateResponse("upload.html", {"request": request, "extracted_text": extracted_text})


# Ruta para descargar el texto
@app.get("/download")
async def download_text(edited_text: str):
    # Guardar el texto en un archivo temporal
    file_path = "texto_guardado.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(edited_text)

    # Proporcionar el archivo para descargar
    return FileResponse(file_path, media_type='text/plain', filename='texto_guardado.txt')

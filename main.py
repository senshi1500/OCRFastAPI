from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
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
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

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

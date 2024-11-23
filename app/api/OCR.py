# api/OCR.py
from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pytesseract
import cv2
import numpy as np

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

async def process_image(image: UploadFile):
    image_data = await image.read()
    image_np = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(gray, lang='spa')


@router.post("/v1/ocr", response_class=HTMLResponse)
async def ocr(request: Request, lang_html: str = "es", image: UploadFile = File(...)):
    """Realiza OCR en la imagen proporcionada y devuelve el texto extraído."""
    extracted_text = await process_image(image)
    return templates.TemplateResponse(f"base_{lang_html}.html", {"request": request, "extracted_text": extracted_text})

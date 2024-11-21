# api/OCR.py
from fastapi import UploadFile
import pytesseract
import cv2
import numpy as np


async def process_image(image: UploadFile):
    image_data = await image.read()
    image_np = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(gray, lang='spa')

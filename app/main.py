from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.OCR import router as ocr_router
from app.api.routes import router as app_router
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Montar routers
app.include_router(ocr_router, prefix="/ocr", tags=["OCR"])
app.include_router(app_router, tags=["App"])

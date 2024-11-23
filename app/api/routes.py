from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, lang_html: str = "es"):
    """Vista principal de la aplicación."""
    return templates.TemplateResponse(f"upload_{lang_html}.html", {"request": request, "extracted_text": None})


@router.get("/download")
async def download_text(edited_text: str):
    """Descarga el texto del input del HTML en un archivo .txt."""
    file_path = "texto_guardado.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(edited_text)
    return FileResponse(file_path, media_type='text/plain', filename='texto_guardado.txt')


@router.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request, lang_html: str = "es"):
    """Vista secundaria de la aplicación con el texto extraído."""
    return templates.TemplateResponse(f"upload_{lang_html}.html", {"request": request})


@router.post("/upload")
async def upload_file(request: Request):
    """Sube la imagen del input file al backend para que lo analice en OCR."""
    form = await request.form()
    file = form.get("file")
    return {"filename": file.filename}

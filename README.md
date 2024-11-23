# OCR FastAPI

OCR FastAPI es una aplicación que permite realizar reconocimiento óptico de caracteres (OCR) a partir de imágenes. Solo
necesitas cargar una imagen y el sistema devolverá el texto contenido en ella.

## Características

- **Carga de imágenes**: Permite cargar imágenes desde tu dispositivo.
- **Reconocimiento de texto**: Utiliza tecnología OCR para extraer texto de imágenes.
- **API RESTful**: Interfaz fácil de usar para interactuar con la aplicación.

## Requisitos

Asegúrate de tener los siguientes requisitos antes de ejecutar la aplicación:

- Python 3.12 o superior
- Docker (opcional, si deseas ejecutar la aplicación en un contenedor)

## Instalación

1. **Clona el repositorio**:

   ```bash
   git clone https://github.com/tu-usuario/ocr-fastapi.git

### Entrar al directorio

    cd OCRFasatAPI

### Instalar las librerias

    pip install -r requirements.txt

### Levantar en local con uvicorn

    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

### Conctruir y Levantar el docker compose

    docker-compose up --build

## Uso

Para poder entender de mejor manera el funcionamiento este proyeyo es recomendable abrirr la ruta que se encuentra en
http://localhost:8000/docs

## Agradecimientos

* Madflows:
  https://uiverse.io/Madflows/fresh-fireant-15
* Yaya12085:
  https://uiverse.io/Yaya12085/tender-moose-95

## Lisecia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
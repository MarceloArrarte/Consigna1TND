import azure.functions as func
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

mock_news = [
  {
    "id": 1,
    "title": "Avances en inteligencia artificial revolucionan la industria tecnológica",
    "source": "TechNews",
    "publishedAt": "2025-08-23T10:30:00Z",
    "url": "#",
  },
  {
    "id": 2,
    "title": "Nueva política económica impulsa el crecimiento del sector empresarial",
    "source": "Economía Hoy",
    "publishedAt": "2025-08-23T09:15:00Z",
    "url": "#",
  },
  {
    "id": 3,
    "title": "Descubrimiento científico podría cambiar el tratamiento de enfermedades",
    "source": "Ciencia y Salud",
    "publishedAt": "2025-08-23T08:45:00Z",
    "url": "#",
  },
  {
    "id": 4,
    "title": "Cambios climáticos afectan la agricultura mundial según nuevo estudio",
    "source": "Verde Noticias",
    "publishedAt": "2025-08-23T07:20:00Z",
    "url": "#",
  },
  {
    "id": 5,
    "title": "Innovaciones en energías renovables prometen un futuro sostenible",
    "source": "Energía Limpia",
    "publishedAt": "2025-08-23T06:00:00Z",
    "url": "#",
  },
]

@app.route(route="GetNews")
def GetNews(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    return func.HttpResponse(
        json.dumps(mock_news, ensure_ascii=False),
        mimetype="application/json",
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "http://localhost:3000"
        }
    )


@app.route(route="LogAccess")
def LogAccess(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    return func.HttpResponse(
        json.dumps({"message": "Access logged"}, ensure_ascii=False),
        mimetype="application/json",
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "http://localhost:3000"
        }
    )
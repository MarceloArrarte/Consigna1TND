import logging
import azure.functions as func
import requests
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('GetNews HTTP trigger processed a request.')

    try:
        API_KEY = "TU_API_KEY"
        url = f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()

        return func.HttpResponse(
            json.dumps(response.json()),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Request failed: {str(e)}")
        logging.exception("Stacktrace completo:")
        return func.HttpResponse(
            "Algo ha fallado en el servidor",
            status_code=500
        )

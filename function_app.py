import azure.functions as func
import logging
import json
import os
import requests
import copy
from azure.data.tables import TableServiceClient
from azure.core.exceptions import ResourceExistsError
from datetime import datetime
import uuid

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# trigger pipeline

connection_string = os.environ["DEPLOYMENT_STORAGE_CONNECTION_STRING"]
table_name =  os.environ["AZURE_STORAGE_TABLE"]

# Inicializo cliente de servicio
table_service = TableServiceClient.from_connection_string(conn_str=connection_string)

# Crear tabla si no existe
try:
    table_client = table_service.create_table_if_not_exists(table_name=table_name)
except ResourceExistsError:
    # La tabla existe, entonces la recuperamos
    table_client = table_service.get_table_client(table_name)


API_KEY = os.environ.get("NEWS_API_KEY", "no-key")
new_object = {
              "id": None,
              "source": None,
              "author": None,
              "title": None,
              "description": None,
              "url": None,
              "urlToImg": None,
              "publishedAt": None
          }

#@app.function_name(name="GetNews")
@app.route(route="GetNews", methods=['GET'])
def GetNews(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        url = f"https://newsapi.org/v2/everything?q=hotels&apiKey={API_KEY}"


        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Esto lanza excepción si no es 200

        data = response.json()
        
        articles = data['articles']
        
        # Restablecemos variables de interes
        new_id = 1
        news = []

        # Iteramos para conseguir los datos de cada item
        for new in articles:
          article = copy.deepcopy(new_object)
          
          article['id'] = new_id
          article['source'] = new['source']['name']
          article['author'] = new['author']
          article['title'] = new['title']
          article['description'] = new['description']
          article['url'] = new['url']
          article['urlToImage'] = new['urlToImage']
          article['publishedAt'] = new['publishedAt']
          
          new_id +=1  
          news.append(article)

        return func.HttpResponse(
            json.dumps(news),
            status_code=200,
            mimetype="application/json",
             headers={
                  "Access-Control-Allow-Origin": "*",
                  "Access-Control-Allow-Methods": "GET, OPTIONS",
                  "Access-Control-Allow-Headers": "Content-Type"
              }
        )

    except requests.exceptions.RequestException as e:
        logging.error("Request failed: %s", str(e))
        logging.exception("Stacktrace completo del error:")

        return func.HttpResponse(
            "Algo ha fallado en el servidor",
            status_code=500,
            mimetype="text/plain"
        )

    
    
    

#@app.function_name(name="LogAccess")
@app.route(route="LogAccess", methods=['POST'])
def LogAccess(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        if not table_client:
            return func.HttpResponse(
                "No hay cliente de tabla configurado.",
                status_code=500
            )

        forwarded_for = req.headers.get("x-forwarded-for")
        if forwarded_for:
            # puede traer varias IP separadas por coma, tomamos la primera
            client_ip = forwarded_for.split(",")[0].strip()
        else:
            # fallback si por alguna razón no está
            client_ip = req.headers.get("REMOTE_ADDR", "unknown")
            
        entity = {
            "PartitionKey": "Logs",
            "RowKey": str(uuid.uuid4()),
            "Timestamp": datetime.utcnow().isoformat(),
            "Level": "Information",
            "Message": "Se solicitaron noticias",
            "IP": client_ip
        }

        table_client.create_entity(entity=entity)

        return func.HttpResponse(
            json.dumps({"message": "Access logged"}, ensure_ascii=False),
            mimetype="application/json",
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*"
            }
        )
        
    except requests.exceptions.RequestException as e:
        logging.error("Request failed: %s", str(e))
        logging.exception("Stacktrace completo del error:")

        return func.HttpResponse(
            "Algo ha fallado en el servidor",
            status_code=500,
            mimetype="text/plain"
        )

      

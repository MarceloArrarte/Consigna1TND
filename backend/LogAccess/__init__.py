import logging
import azure.functions as func
from azure.data.tables import TableClient
from datetime import datetime
import uuid
import os
import json

connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
table_client = TableClient.from_connection_string(
    conn_str=connection_string, table_name="Logs"
)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('LogAccess HTTP trigger processed a request.')

    try:
        entity = {
            "PartitionKey": "Logs",
            "RowKey": str(uuid.uuid4()),
            "Timestamp": datetime.utcnow().isoformat(),
            "Level": "Information",
            "Message": "Se solicitó acceso a GetNews"
        }

        table_client.create_entity(entity=entity)

        return func.HttpResponse(
            json.dumps({"message": "Access logged"}, ensure_ascii=False),
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

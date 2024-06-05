#v3

# This is a HTTP trigger function which writes visitir count+1 to Azure CosmosDB using Azure-cosmos SDK.

import azure.functions as func
from azure.cosmos import CosmosClient
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

ENDPOINT=None
DB_NAME="ToDoList"
CONTAINER_NAME="Items"
CONN_STRING="AccountEndpoint=https:==;" # hardcoded
SQL_QUERY='SELECT * FROM c WHERE c.id = "visitors"'
PARTITION_KEY="count"

@app.route(route=ENDPOINT)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    client = CosmosClient.from_connection_string(conn_str=CONN_STRING)
    
    database = client.get_database_client(DB_NAME)
    container = database.get_container_client(CONTAINER_NAME)

    
    try:
        for item in container.query_items(
            query=SQL_QUERY,
            enable_cross_partition_query=True):
            logging.info(f'Query result is: {json.dumps(item, indent=True)}')

        item["count"] = item["count"]+1
        logging.info(f'Updated result is: {json.dumps(item, indent=True)}')
        container.replace_item(item=item, body=item)
        return func.HttpResponse(f"Count is uploaded succesfully!")
    
    except ValueError:
        return func.HttpResponse(
                    "something went wrong from server. Please check internal function logs",
                    status_code=400)


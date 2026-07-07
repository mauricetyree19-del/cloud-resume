import azure.functions as func
import json
import os
from azure.cosmos import CosmosClient

app = func.FunctionApp()

@app.route(route="visitorCounter", auth_level=func.AuthLevel.ANONYMOUS)
def visitorCounter(req: func.HttpRequest) -> func.HttpResponse:

    endpoint = os.environ["COSMOS_ENDPOINT"]
    key = os.environ["COSMOS_KEY"]
    database_name = os.environ["COSMOS_DATABASE"]
    container_name = os.environ["COSMOS_CONTAINER"]

    client = CosmosClient(endpoint, key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    try:
        item = container.read_item(
            item="visitorCount",
            partition_key="visitorCount"
        )
    except:
        item = {
            "id": "visitorCount",
            "count": 0
        }
        container.create_item(item)

    item["count"] += 1

    container.upsert_item(item)

    return func.HttpResponse(
        json.dumps({"count": item["count"]}),
        mimetype="application/json",
        status_code=200
    )
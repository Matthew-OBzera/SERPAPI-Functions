import logging

import azure.functions as func

import json
# SerpApi search
from serpapi import GoogleSearch

def main(req: func.HttpRequest, msg: func.Out[func.QueueMessage]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body_bytes = req.get_body()
    req_body = req_body_bytes.decode("utf-8")

    logging.info(f"Request: {req_body}")

    content = json.loads(req_body)

    keywords = content["keyword"]
    device = content["gl"]
    gl = content["gl"]
    hl = content["hl"]

    processKeywords(keywords, device, gl, hl)
    return func.HttpResponse(
        "This HTTP triggered function executed successfully.",
        status_code=200
    )

def processKeywords(keyword, device = 'desktop', gl = 'us', hl = 'en'):
    # SerpApi search
    search = GoogleSearch({
        "engine" : "google",
        "gl" : gl,
        "hl" : hl,
        "device" : device,
        "async": True,
        "api_key": ""
    })
    result = search.get_dict()
    msg.set(result['search_metadata']['id'])

    print("wait until all search statuses are cached or success")

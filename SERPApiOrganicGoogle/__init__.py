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

    keyword = content["keyword"]
    device = content["device"]
    gl = content["gl"]
    hl = content["hl"]

    processKeywords(msg, keyword, device, gl, hl)
    return func.HttpResponse(
        "This HTTP triggered function executed successfully.",
        status_code=200
    )

def processKeywords(msg, keyword, device = 'desktop', gl = 'us', hl = 'en'):
    # SerpApi search
    search = GoogleSearch({
        "q" : keyword, 
        "engine" : "google",
        "gl" : gl,
        "hl" : hl,
        "device" : device,
        "async": True,
        "api_key": "22cf33864512bf7f490a937d3aed585f0c6ebf76a40c48dfdf3c9c203d29d52f"
    })
    result = search.get_dict()
    msg.set(result['search_metadata']['id'])

    print("wait until all search statuses are cached or success")

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

    keywords = content["keywords"]
    location = content["location"]
    device = content["gl"]
    gl = content["gl"]
    hl = content["hl"]

    return func.HttpResponse(
        "This HTTP triggered function executed successfully.",
        status_code=200
    )

def processKeywords(keywords, location, device, gl, hl):
    # SerpApi search
    search = GoogleSearch({
        "engine" : "google",
        "location": location,
        "gl" : gl,
        "hl" : hl,
        "device" : device,
        "async": True,
        "api_key": ""
    })

    # loop through a list of companies
    for keyword in keywords:
        print("execute async search: q = " + keyword)
        search.params_dict["q"] = keyword
        result = search.get_dict()
        if "error" in result:
            print("error: ", result["error"])
            continue
        # add search to the search_queue
        msg.set(result['search_metadata']['id'])

    print("wait until all search statuses are cached or success")

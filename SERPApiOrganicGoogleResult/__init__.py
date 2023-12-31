import logging

import azure.functions as func

# regular expression library
import re
# SerpApi search
from serpapi import GoogleSearch

def main(msg: func.QueueMessage, remsg: func.Out[func.QueueMessage]) -> None:
    search_id = msg.get_body().decode('utf-8')
    logging.info('Python queue trigger function processed a queue item: %s', search_id)
    # retrieve search from the archive - blocker
    print(search_id + ": get search from archive")
    search_archived = GoogleSearch({"api_key": "22cf33864512bf7f490a937d3aed585f0c6ebf76a40c48dfdf3c9c203d29d52f"}).get_search_archive(search_id, 'json')
    print(search_id + ": status = " +
          search_archived['search_metadata']['status'])

    # check status
    if re.search('Cached|Success',
                 search_archived['search_metadata']['status']):
        print(search_id + ": search done with q = " +
              search_archived['search_parameters']['q'])
    else:
        remsg.set(search_id)

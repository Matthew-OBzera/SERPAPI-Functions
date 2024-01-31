import logging

import azure.functions as func

# regular expression library
import re
# Postgres connection
import psycopg2
# SerpApi search
from serpapi import GoogleSearch

def main(msg: func.QueueMessage, remsg: func.Out[func.QueueMessage]) -> None:
      search_id = msg.get_body().decode('utf-8')
      logging.info('Python queue trigger function processed a queue item: %s', search_id)
      print(search_id + ": get search from archive")
      search_archived = GoogleSearch({"api_key": "22cf33864512bf7f490a937d3aed585f0c6ebf76a40c48dfdf3c9c203d29d52f"}).get_search_archive(search_id, 'json')
      print(search_id + ": status = " +
            search_archived['search_metadata']['status'])

      # check status
      if re.search('Cached|Success', search_archived['search_metadata']['status']):
            try:
                  connection = psycopg2.connect(user="bptmvnlomyctqd",
                                                password="ebf458d508c74de58143d9946eecc86b159d9835129a876e1f98bf77f0358349",
                                                host="ec2-54-164-138-85.compute-1.amazonaws.com",
                                                port="5432",
                                                database="df77hp04j8rqui")
                  cursor = connection.cursor()
                  
                  postgres_insert_query = """ INSERT INTO SERPAPIGOOGLERESULTS (KEYWORD, RESULT, DATE) VALUES (%s,%s,%s)"""
                  record_to_insert = (search_archived['search_parameters']['q'], search_archived, search_archived['search_metadata']['processed_at'])
                  cursor.execute(postgres_insert_query, record_to_insert)

                  connection.commit()
                  count = cursor.rowcount
                  print(count, "Record inserted successfully into mobile table")

            except (Exception, psycopg2.Error) as error:
                  print("Failed to insert record into mobile table", error)

            finally:
            # closing database connection.
                  if connection:
                        cursor.close()
                        connection.close()
                        print("PostgreSQL connection is closed")
                        remsg.set(search_id)

      else:
            remsg.set(search_id)

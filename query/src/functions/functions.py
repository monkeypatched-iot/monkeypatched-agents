import asyncio
import base64
import json
import re
from neomodel import db
from src.tools.redis import RedisDB
from src.tools.nats import publish_event
from src.utils.graph import connection


redis = RedisDB()

answers = [] 

def ExecuteQuery(query,question):
    if query != "query":
        try:
            # Run the query to match nodes with no relationships
            # Execute the query via the Neo4j connection
            result = connection.query(str(query))
            if len(answers)>0:
                answers.pop()
            answers.append({"answer":result[0][0]})
            print(answers)
            NotifyBot(query,question)
        except Exception as e:
            print(f"Error occurred: {e}")

def NotifyBot(query,question):
    if query != "query":
        try:
            result = asyncio.run(publish_event("answers", answers))
            match = re.search(r"question='(.*?)'", question)

            if match:
                extracted_question = match.group(1)
                redis.put(extracted_question,json.dumps(answers[0]),0)
            

            else:
                print("No question found.")


        except Exception as e:
            print(f"An error occurred: {e}")


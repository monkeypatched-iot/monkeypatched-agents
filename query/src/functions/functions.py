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
            if result[0][0] is not None:
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
                ttl_seconds = 3600  # 1 hour TTL

                # Check if the key exists
                if redis.get(extracted_question) is not None:
                    redis.set(extracted_question, json.dumps(answers[0]), ex=ttl_seconds)  # Update with TTL
                else:
                    redis.set(extracted_question, json.dumps(answers[0]), ex=ttl_seconds)  # Insert with TTL

                redis.expire(extracted_question, 3600)  # Set TTL if needed

            else:
                print("No question found.")

        except Exception as e:
            print(f"An error occurred: {e}")


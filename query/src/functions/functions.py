import asyncio
from neomodel import db
from src.tools.nats import publish_event
from src.utils.graph import connection


answers = [] 

def ExecuteQuery(query):
    if query != "query":
        try:
            # Run the query to match nodes with no relationships
            # Execute the query via the Neo4j connection
            result = connection.query(str(query))
            answers.append({"answer":result[0][0]})
            
        except Exception as e:
            print(f"Error occurred: {e}")


def NotifyBot(query):
    try:
        result = asyncio.run(publish_event("answers", answers))
    except Exception as e:
        print(f"An error occurred: {e}")


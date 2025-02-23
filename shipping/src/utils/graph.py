# Define connection details
from src.tools.neo4j import Neo4jGraphDB


from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


# Create an instance of the connection
connection = Neo4jGraphDB(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)


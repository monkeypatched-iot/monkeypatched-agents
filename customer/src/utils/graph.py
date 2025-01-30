# Define connection details
from src.tools.neo4j import Neo4jGraphDB


URI = "neo4j://localhost:7687"  # Change to your Neo4j instance URI
USERNAME = "neo4j"             # Replace with your username
PASSWORD = "neo4jpassword"     # Replace with your password

# Create an instance of the connection
connection = Neo4jGraphDB(URI, USERNAME, PASSWORD)


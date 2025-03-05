import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
import qdrant_client
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance


load_dotenv()  # Load variables from .env

QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = os.getenv("QDRANT_PORT")

# Initialize Qdrant client
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


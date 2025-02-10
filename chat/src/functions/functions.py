
from datetime import datetime
import json
import os
import random
import boto3
import botocore
from dotenv import load_dotenv
from fastapi import HTTPException, UploadFile
import pandas as pd
from requests import post
from src.dao.orders.details import OrderDetails
from src.dao.components.details import ComponentDetails
from src.dao.customers.details import CustomerDetails
from src.dao.suppliers.details import SupplierDetails
from src.dao.product.details import ProductDetails
from src.dao.document.metadata import DocumentMetadata
from src.helpers.helper import read_file, upload_to_s3
from src.utils.graph import connection
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import requests
from fastapi import File
from fastapi.datastructures import UploadFile

load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET")

# Retrieve environment variables

# Session state tracking
session_state = {}

CSV_API_BASE_URL = os.getenv("CSV_API_BASE_URL")
PDF_API_BASE_URL = os.getenv("PDF_API_BASE_URL")
WORD_API_BASE_URL = os.getenv("WORD_API_BASE_URL")
DOCUMENT_METADATA_API = os.getenv("DOCUMENT_METADATA_API")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

DOCUMENT_SYNCH_API = os.getenv("DOCUMENT_SYNCH_API")


# Initialize AWS S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

Document = connection.create_node(DocumentMetadata)

def upload_document(message,session_state):
    return "Please specify the file type (if applicable, e.g., csv)."

def handle_doc_type(message,session_state):
    session_state["doc_type"] = message.lower()
    return "Please specify the file type (if applicable, e.g., csv)."

def handle_doc_subtype(message,session_state):
    session_state["doc_subtype"] = message
    return "Please specify the document author."

def handle_author(message,session_state):
    session_state["author"] = message
    return "Please provide the document type ( if applicable , eg invoice,customers)."

def handle_tags(message,session_state):
    session_state["tags"] = message
    return "Please specify the document status (e.g., draft, finalized, reviewed)."

def handle_status(message,session_state):
    session_state["status"] = message
    return "Please specify the ID type (eg product_id etc.)."

def handle_id_type(message,session_state):
    session_state["id_type"] = message
    return f"Please provide the {message}."

def handle_id_value(message,session_state):
    session_state["id_value"] = message
    return "Please provide the full file path."

def handle_file_name(message,session_state):
    session_state["file_name"] = message
    return "Uploaded your document."

def GetProductDetailsFromGraph(product_id):
    """Fetch product details from the knowledge graph."""
    if not product_id:
        print("Invalid product_id provided")
        return None

    print(f"Getting product details for ID: {product_id}")
    try:
        product = ProductDetails.nodes.get_or_none(product_id=product_id)
        if product:
            print(f"Product found: {product}")
            return product
        print(f"No product found with product_id: {product_id}")
    except Exception as e:
        print(f"Error fetching product details: {e}", exc_info=True)

    return None


def GetOrderDetailsFromGraph(order_id):
    """Fetch order details from the knowledge graph."""
    if not order_id:
        print("Invalid order_id provided")
        return None

    print(f"Getting order details for ID: {order_id}")
    try:
        order = OrderDetails.nodes.get_or_none(order_id=order_id)
        if order:
            print(f"Order found: {order}")
            return order
        print(f"No order found with order_id: {order_id}")
    except Exception as e:
        print(f"Error fetching order details: {e}", exc_info=True)

    return None


def GetCustomerDetailsFromGraph(customer_id):
    """Fetch customer details from the knowledge graph."""
    if not customer_id:
        print("Invalid customer_id provided")
        return None

    print(f"Getting customer details for ID: {customer_id}")
    try:
        customer = CustomerDetails.nodes.get_or_none(customer_id=customer_id)
        if customer:
            print(f"Customer found: {customer}")
            return customer
        print(f"No customer found with customer_id: {customer_id}")
    except Exception as e:
        print(f"Error fetching customer details: {e}", exc_info=True)

    return None


def GetProductDetailsFromGraph(product_id):
    """Fetch product details from the knowledge graph."""
    if not product_id:
        print("Invalid product_id provided")
        return None

    print(f"Getting product details for ID: {product_id}")
    try:
        product = ProductDetails.nodes.get_or_none(product_id=product_id)
        if product:
            print(f"Product found: {product}")
            return product
        print(f"No product found with product_id: {product_id}")
    except Exception as e:
        print(f"Error fetching product details: {e}", exc_info=True)

    return None


def GetComponentDetailsFromGraph(component_id):
    """Fetch component details from the knowledge graph."""
    if not component_id:
        print("Invalid component_id provided")
        return None

    print(f"Getting component details for ID: {component_id}")
    try:
        component = ComponentDetails.nodes.get_or_none(part_id=component_id)
        if component:
            print(f"Component found: {component}")
            return component
        print(f"No component found with component_id: {component_id}")
    except Exception as e:
        print(f"Error fetching component details: {e}", exc_info=True)

    return None


def GetSupplierDetailsFromGraph(supplier_id):
    """Fetch supplier details from the knowledge graph."""
    if not supplier_id:
        print("Invalid supplier_id provided")
        return None

    print(f"Fetching supplier details for ID: {supplier_id}")
    try:
        supplier_details = SupplierDetails.nodes.get_or_none(supplier_id=supplier_id)
        if supplier_details:
            print(f"Supplier details found: {supplier_details}")
            return supplier_details
        print(f"No supplier details found for supplier_id: {supplier_id}")
    except Exception as e:
        print(f"Error fetching supplier details: {e}", exc_info=True)

    return None

def get_data_from_s3(file_path: str):  # Example: "data/my_data.csv"
    """Reads data from an S3 file and returns it as JSON."""
    try:
        obj = s3_client.get_object(Bucket=S3_BUCKET, Key=file_path)
        data = obj["Body"].read()

        # Determine file type and parse accordingly
        if file_path.endswith(".csv"):
            df = pd.read_csv(data)  # Or pd.read_csv(io.BytesIO(data)) for in-memory
        elif file_path.endswith((".xls", ".xlsx")):
            df = pd.read_excel(data)  # Or pd.read_excel(io.BytesIO(data))
        elif file_path.endswith(".json"):
            import json
            return json.loads(data.decode('utf-8')) # Directly return JSON data
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # Convert DataFrame to JSON (more flexible for complex data)
        json_data = df.to_dict(orient="records")  # List of dictionaries
        return json_data

    except Exception as e:
        print(f"Error reading from S3: {e}")  # For debugging
        raise HTTPException(status_code=500, detail=f"Error reading from S3: {e}")
    
def s3_data_to_fastapi_file(data, filename, content_type):
    """
    Converts S3 data to a FastAPI File object.

    Args:
        data (BytesIO): Contents of the object as a BytesIO stream.
        filename (str): Name of the file.
        content_type (str): MIME type of the file.

    Returns:
        UploadFile: FastAPI File object.
    """
    return UploadFile(filename=filename, content=data, media_type=content_type)


def handle_upload(file_path: str, session_state: dict) -> list:
    """
    Handles file upload and metadata creation.

    Args:
    file_path (str): The local file path.
    session_state (dict): The session state.

    Returns:
    list: A list of history items.
    """
    history = []

    # Validate file path
    if not os.path.exists(file_path):
        history.append({"role": "assistant", "content": "Error uploading file. File not found. ❌"})
        return history

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
    except Exception as e:
        history.append({"role": "assistant", "content": f"Error reading CSV file: {str(e)} ❌"})
        return history
    
    try:
        # Convert DataFrame to CSV in memory
        content = df.to_csv(index=False)
    except Exception as e:
        history.append({"role": "assistant", "content": f"Error converting DataFrame to CSV: {str(e)} ❌"})
        return history
    
    try:
        # Upload to S3
        upload_to_s3(content, f"uploads/{session_state['doc_subtype']}/{session_state['file_name']}")
    except NoCredentialsError:
        history.append({"role": "assistant", "content": "AWS credentials not available ❌"})
        return history
    except botocore.exceptions.ClientError as e:
        history.append({"role": "assistant", "content": f"Error uploading to S3: {str(e)} ❌"})
        return history
    except Exception as e:
        history.append({"role": "assistant", "content": f"Unexpected error during S3 upload: {str(e)} ❌"})
        return history
    
    try:
        # Get data from S3
        data = get_data_from_s3(f"uploads/{session_state['doc_subtype']}/{session_state['file_name']}")
        file = s3_data_to_fastapi_file(data, f"uploads/{session_state['doc_subtype']}/{session_state['file_name']}", "text/csv")
    except requests.exceptions.RequestException as e:
        history.append({"role": "assistant", "content": f"Error getting data from S3: {str(e)} ❌"})
        return history
    except Exception as e:
        history.append({"role": "assistant", "content": f"Unexpected error while processing S3 data: {str(e)} ❌"})
        return history
    
    try:
        # Post file to API
        success = post(f"{DOCUMENT_SYNCH_API}/v1/file/upload/type/{session_state['doc_subtype']}/subtype/none", file)
    except Exception as e:
        history.append({"role": "assistant", "content": f"Error uploading file via API: {str(e)} ❌"})
        return history
    
    if success:
        try:
            # Create metadata
            metadata = {
                "document_id": f"DOC{random.randint(0, 100000)}",
                "title": session_state["file_name"],
                "author": session_state.get("author", ""),
                "created_at": datetime.utcnow().isoformat() + "Z",
                "modified_at": datetime.utcnow().isoformat() + "Z",
                "file_type": session_state["doc_subtype"],
                "document_url": f"https://{S3_BUCKET}.s3express-use1-az4.us-east-1.amazonaws.com/uploads/csv/{session_state['file_name']}",
                "tags": [session_state.get("tags")],
                session_state.get("id_type", "product_id"): session_state.get("id_value", ""),
                "status": session_state.get("status", ""),
            }
        except Exception as e:
            history.append({"role": "assistant", "content": f"Error creating metadata: {str(e)} ❌"})
            return history
        
        try:
            # Post metadata to API
            response = post(f"{DOCUMENT_METADATA_API}/documents/", json.dumps(metadata))
        except Exception as e:
            history.append({"role": "assistant", "content": f"Error posting metadata: {str(e)} ❌"})
            return history
        
        if response:
            try:
                # Add node to Neo4j database
                document = connection.add(Document(**metadata))
            except Exception as e:
                history.append({"role": "assistant", "content": f"Error adding document node to database: {str(e)} ❌"})
                return history
            
            try:
                # Connect document to related entity
                id_type = session_state.get("id_type", "product_id")
                id_value = session_state.get("id_value", "")
                entity_map = {
                    "product_id": GetProductDetailsFromGraph,
                    "order_id": GetOrderDetailsFromGraph,
                    "component_id": GetComponentDetailsFromGraph,
                    "customer_id": GetCustomerDetailsFromGraph,
                    "supplier_id": GetSupplierDetailsFromGraph,
                }
                
                if id_type in entity_map:
                    entity = entity_map[id_type](id_value)
                    if entity is not None:
                        try:
                            getattr(document, id_type.split('_')[0]).connect(entity)
                        except Exception as e:
                            history.append({"role": "assistant", "content": f"Error connecting document to {id_type}: {str(e)} ❌"})
            except Exception as e:
                history.append({"role": "assistant", "content": f"Unexpected error while connecting document: {str(e)} ❌"})
        
        history.append({"role": "assistant", "content": f"File '{session_state['file_name']}' uploaded successfully! ✅"})
    else:
        history.append({"role": "assistant", "content": "Error uploading file. ❌"})
    
    return history

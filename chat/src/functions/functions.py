
from datetime import datetime
import json
import os
import random
from dotenv import load_dotenv
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

load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET")

# Retrieve environment variables

# Session state tracking
session_state = {}

CSV_API_BASE_URL = os.getenv("CSV_API_BASE_URL")
PDF_API_BASE_URL = os.getenv("PDF_API_BASE_URL")
WORD_API_BASE_URL = os.getenv("WORD_API_BASE_URL")
DOCUMENT_METADATA_API = os.getenv("DOCUMENT_METADATA_API")

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
        
        # Convert DataFrame to CSV in memory
        content = df.to_csv(index=False)
        
        # Upload to S3
        success = upload_to_s3(content, f"uploads/{session_state['doc_subtype']}/{session_state['file_name']}")
        
        if success:
            # Create metadata
            metadata = {
                "document_id": f"DOC" + str(random.randint(0, 100000)),
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
            
            # Post metadata to API
            response = post(f"{DOCUMENT_METADATA_API}/documents/", json.dumps(metadata))
            
            if response:
                try:
                    # Add node to Neo4j database
                    document = connection.add(Document(**metadata))
                    
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
                                print(f"Connected document to {id_type}")
                            except Exception as e:
                                print(f"Error connecting document to {id_type}: {str(e)}")
                                history.append({"role": "assistant", "content": f"Error uploading file: {str(e)} ❌"})
                    
                    history.append({"role": "assistant", "content": f"File '{session_state['file_name']}' uploaded successfully! ✅"})
                except Exception as e:
                    print(f"Error adding document node to Neo4j database: {str(e)}")
                    history.append({"role": "assistant", "content": f"Error uploading file: {str(e)} ❌"})
            else:
                history.append({"role": "assistant", "content": "Error uploading file. ❌"})
    except Exception as e:
        history.append({"role": "assistant", "content": f"Error uploading file: {str(e)} ❌"})
    
    return history

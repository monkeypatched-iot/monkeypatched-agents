import json
from dotenv import load_dotenv
import os
from src.tools.nats import publish_event
from src.dao.pricing import ProductPricing
from src.dao.inventory import ProductInventory
from src.dao.metadata import ProductMetadata
from src.dao.details import ProductDetails
from src.tools.requests import get
from src.utils.graph import connection


load_dotenv()  # Load variables from .env

BASE_URL = os.getenv("API_BASE_URL")

Product = connection.create_node(ProductDetails)
Metadata = connection.create_node(ProductMetadata)
Inventory = connection.create_node(ProductInventory)
Pricing = connection.create_node(ProductPricing)

product_aggregate = {}

def GetProductDetails(product_id):
    print(product_id)
    if product_id != "product_id":

        response = get(f"{BASE_URL}/v1/product/details/{product_id}")
     
        print(response)

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")
 
        product_details_dict = json.loads(json_string)

       # Step 2: Convert string to JSON (Python dictionary)
        product_aggregate["details"] = product_details_dict
        connection.add(ProductDetails(**product_details_dict))

        print(product_details_dict)

def GetProductMetadata(product_id):
    if product_id != "product_id":

        response = get(f"{BASE_URL}/v1/product/metadata/{product_id}")

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        product_metadata_dict = json.loads(json_string)

        product_aggregate["metadata"] = product_metadata_dict
        connection.add(ProductMetadata(**product_metadata_dict))

        print(product_metadata_dict)

def GetProductInventory(product_id):
    if product_id != "product_id":
        print("get the product inventory")

        response = get(f"{BASE_URL}/v1/product/inventory/{product_id}")

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        product_inventory_dict = json.loads(json_string)

        product_aggregate["inventory"] = product_inventory_dict
        connection.add(ProductInventory(**product_inventory_dict))

        print(product_inventory_dict)

def GetProductPricing(product_id):
    if product_id != "product_id":

        response = get(f"{BASE_URL}/v1/product/pricing/{product_id}")

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        product_pricing_dict = json.loads(json_string)

        product_aggregate["pricing"] = product_pricing_dict
        connection.add(ProductPricing(**product_pricing_dict))

        print(product_pricing_dict)

def GetProductDetailsFromGraph(product_id):
    if product_id != "product_id":
        print('Getting product details for ID:', product_id)

        try:
            # Check if the product exists
            product = ProductDetails.nodes.get_or_none(product_id=product_id)
            if product:
                print(f"Product found: {product}")
                return product
            else:
                print(f"No product found with product_id: {product_id}")
                return None  # Return None if no product found

        except Exception as e:
            print(f"Error fetching product details: {e}")
            return None

def GetProductMetadataFromGraph(product_id):
    if product_id != "product_id":
        print('Getting product metadata for ID:', product_id)

        try:
            # Check if the product metadata exists
            metadata = ProductMetadata.nodes.get_or_none(product_id=product_id)
            if metadata:
                print(f"Product Metadata found: {metadata}")
                return metadata
            else:
                print(f"No metadata found for product_id: {product_id}")
                return None  # Return None if no metadata found

        except Exception as e:
            print(f"Error fetching product metadata: {e}")
            return None

def GetProductInventoryFromGraph(product_id):
    if product_id != "product_id":
        print('Getting product inventory for ID:', product_id)

        try:
            # Check if the product inventory exists
            inventory = ProductInventory.nodes.get_or_none(product_id=product_id)
            if inventory:
                print(f"Product Inventory found: {inventory}")
                return inventory
            else:
                print(f"No inventory found for product_id: {product_id}")
                return None  # Return None if no inventory found

        except Exception as e:
            print(f"Error fetching product inventory: {e}")
            return None

def GetProductPricingFromGraph(product_id):
    if product_id != "product_id":
        print('Getting product pricing for ID:', product_id)

        try:
            # Check if the product pricing exists
            pricing = ProductPricing.nodes.get_or_none(product_id=product_id)
            if pricing:
                print(f"Product Pricing found: {pricing}")
                return pricing
            else:
                print(f"No pricing found for product_id: {product_id}")
                return None  # Return None if no pricing found

        except Exception as e:
            print(f"Error fetching product pricing: {e}")
            return None

def publish_product():
    try:
        # Ensure it's a dictionary before converting it to JSON
        if not isinstance(product_aggregate, dict):
            raise ValueError("product_aggregate must be a dictionary")

        # Convert to JSON string before sending
        product_json = {"product": product_aggregate}

        # Publish event to Kafka
        publish_event("product", product_json)

        print("Product data published successfully.")

    except Exception as e:
        print(f"Error publishing product data: {e}")

def AddProduct(product_id):
    if product_id != "product_id":
        print("Adding a new product...")
        publish_product()  # Publish event

        # Retrieve existing product details, metadata, inventory, and pricing information
        product = GetProductDetailsFromGraph(product_id)
        metadata = GetProductMetadataFromGraph(product_id)
        inventory = GetProductInventoryFromGraph(product_id)
        pricing = GetProductPricingFromGraph(product_id)

        # Retry if not exists
        if not product:
            product = GetProductDetails(product_id)
        if not metadata:
            metadata = GetProductMetadata(product_id)
        if not inventory:
            inventory = GetProductInventory(product_id)
        if not pricing:
            pricing = GetProductPricing(product_id)

        # Connect relationships
        if product:
            if metadata:
                product.metadata.connect(metadata)
            if inventory:
                product.inventory.connect(inventory)
            if pricing:
                product.pricing.connect(pricing)

            print(f"Product {product_id} added successfully.")
            return json.dumps({"message": f"Product {product_id} added successfully."})
        
        return json.dumps({"error": "No product data found"})

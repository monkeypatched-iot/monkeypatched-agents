import json
from dotenv import load_dotenv
import os
from src.tools.requests import get

load_dotenv()  # Load variables from .env

BASE_URL = os.getenv("API_BASE_URL")

print(BASE_URL)

def GetProductDetails(product_id,location_id):
    if product_id != "product_id":
        print(product_id,location_id)
        print("getting product details!")

        response = get(f"{BASE_URL}/v1/product/details/{product_id}")

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        product_dict = json.loads(json_string)

        print(product_dict)

def GetProductMetadata(product_id,location_id):
    if product_id != "product_id":
        print(product_id,location_id)
        print("get product metadata")

        response = get(f"{BASE_URL}/v1/product/metadata/{product_id}")

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        product_metadata_dict = json.loads(json_string)

        print(product_metadata_dict)

def GetProductInventory(product_id,location_id):
    if product_id != "product_id":
        print(product_id,location_id)
        print("get the product inventory")

        response = get(f"{BASE_URL}/v1/product/inventory/{product_id}")

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        product_inventory_dict = json.loads(json_string)

        print(product_inventory_dict)

def GetProductPricing(product_id,location_id):
    if product_id != "product_id":
        print(product_id,location_id)
        print("get the product pricing")

        response = get(f"{BASE_URL}/v1/product/pricing/{product_id}")

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        product_pricing_dict = json.loads(json_string)

        print(product_pricing_dict)

def AddProduct(product_id,location_id):
    if product_id != "product_id":
        print(product_id,location_id)
        print(" adding the product")
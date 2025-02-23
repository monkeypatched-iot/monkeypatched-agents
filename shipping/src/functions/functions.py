import json
from requests import get

from dotenv import load_dotenv
import os

from src.dao.details import ShippingProviderDetails
from src.dao.metadata import ShippingProviderMetadata
from src.utils.graph import connection
from src.tools.nats import publish_event

load_dotenv()  # Load variables from .env

BASE_URL = os.getenv("API_BASE_URL")

shipping_provider_aggregate = {}

def GetShippingProviderDetails(provider_id):
   if provider_id != "provider_id":
    print("Getting Shipping Provider details...")

    # Fetch Shipping Provider details
    response = get(f"{BASE_URL}/v1/shipping_provider/{provider_id}")

    # Step 1: Decode binary to string
    json_string = response.content.decode("utf-8")

    # Step 2: Convert string to JSON (Python dictionary)
    shipping_provider_dict = json.loads(json_string)

    # Print order details for debugging
    print(shipping_provider_dict)

    # Save data to the node
    shipping_provider_aggregate["details"] = shipping_provider_dict
    connection.add(ShippingProviderDetails(**shipping_provider_dict))

    # Return shipping provider details
    return shipping_provider_dict


def GetShippingProviderMetadata(provider_id):
    if provider_id != "provider_id":
        print("Getting the Shipping Provider data...")

        # Fetch Shipping Provider metadata
        response = get(f"{BASE_URL}/v1/shipping_provider/shipping_metadata/{provider_id}")

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        shipping_provider_metadata = json.loads(json_string)

        # Print order metadata for debugging
        print(shipping_provider_metadata)

        # Save data to the node
        shipping_provider_aggregate["metadata"] = shipping_provider_metadata
        connection.add(ShippingProviderMetadata(**shipping_provider_metadata))

        # Return shipping provider metadata
        return shipping_provider_metadata


def publish_shipping_provider():
    try:
        # Ensure it's a dictionary before converting it to JSON
        if not isinstance(shipping_provider_aggregate, dict):
            raise ValueError("shipping_provider_aggregate must be a dictionary")

        # Convert to JSON string before sending
        shipping_provider_json = {"shipping_provider": shipping_provider_aggregate}

        # Publish event to Kafka
        publish_event("shipping_provider", shipping_provider_json)

        print("Shipping Provider data published successfully.")

    except Exception as e:
        print(f"Error publishing Shipping Provider data: {e}")


def GetShippingProviderDetailsFromGraph(provider_id):
    if provider_id != "provider_id":
        print('Getting Shipping Provider details for ID:', provider_id)

        try:
            # Check if the Shipping Provider exists
            shipping_provider = ShippingProviderDetails.nodes.get_or_none(provider_id=provider_id)
            if shipping_provider:
                print(f"Shipping Provider found: {shipping_provider}")
                return shipping_provider
            else:
                print(f"No Shipping Provider found with provider_id: {provider_id}")
                return None  # Return None if no shipping provider found

        except Exception as e:
            print(f"Error fetching Shipping Provider details: {e}")
            return None


def GetShippingProviderMetadataFromGraph(provider_id):
    if provider_id != "provider_id":
        print('Getting shipping_provider metadata for ID:', provider_id)

        try:
            # Check if the metadata exists for the Shipping Provider
            metadata = ShippingProviderMetadata.nodes.get_or_none(provider_id=provider_id)
            if metadata:
                print(f"Shipping Provider metadata found: {metadata}")
                return metadata
            else:
                print(f"No Shipping Provider metadata found with provider_id: {provider_id}")
                return None

        except Exception as e:
            print(f"Error fetching Shipping Provider metadata: {e}")
            return None


def AddShippingProvider(provider_id):
    if provider_id != "provider_id":
        print("adding a new Shipping Provider")
        publish_shipping_provider()

        # Retrieve existing Shipping Provider details and metadata
        shippingProvider = GetShippingProviderDetailsFromGraph(provider_id)
        metadata = GetShippingProviderMetadataFromGraph(provider_id)
    
        # retry if not exists 
        if not shippingProvider:  
            shippingProvider = GetShippingProviderDetails(provider_id)

        if not metadata:
            metadata = GetShippingProviderMetadata(provider_id)
        
        # add to Shipping Provider 
        if shippingProvider:
            if metadata:
                shippingProvider.metadata.connect(metadata)

            print(f"Shipping Provider {provider_id} added successfully.") 
            return json.dumps({"message": f"Shipping Provider {provider_id} added successfully."})

        return json.dumps({"error": "No Shipping Provider data found"})

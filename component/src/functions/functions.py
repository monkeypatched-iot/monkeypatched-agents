import json
from requests import get

from dotenv import load_dotenv
import os

from src.tools.kafka import publish_event
from src.dao.details import ComponentDetails
from src.dao.metadata import ComponentMetadata
from src.dao.inventory import ComponentInventory
from src.dao.pricing import ComponentPricing
from src.tools.requests import get
from src.utils.graph import connection

load_dotenv()  # Load variables from .env

BASE_URL = os.getenv("API_BASE_URL")

component_aggregate = {}

def GetComponentDetails(component_id):
     if component_id != "component_id":
        print("getting componeent details")

        response = get(f"{BASE_URL}/v1/component/details/{component_id}")

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        component_dict = json.loads(json_string)

        print(component_dict)

        component_aggregate["details"] = component_dict

        connection.add(ComponentDetails(**component_dict))

        
 
def GetComponentMetadata(component_id):
    if component_id != "component_id":
        print("getting the component data")

        response = get(f"{BASE_URL}/v1/component/metadata/{component_id}")

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        component_metadata_dict = json.loads(json_string)

        print(component_metadata_dict)

        component_aggregate["metadata"] = component_metadata_dict

        connection.add(ComponentMetadata(**component_metadata_dict))


def GetComponentInventory(component_id):
    if component_id != "component_id":
        print("getting component inventory")

        response = get(f"{BASE_URL}/v1/component/inventory/{component_id}")

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        component_inventory_dict = json.loads(json_string)

        print(component_inventory_dict)

        component_aggregate["inventory"] = component_inventory_dict

        connection.add(ComponentInventory(**component_inventory_dict))
        
def GetComponentPaymentInformation(component_id):
    if component_id != "component_id":
        print("getting the payment information")

        response = get(f"{BASE_URL}/v1/component/pricing/{component_id}")

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        component_pricing_dict = json.loads(json_string)

        print(component_pricing_dict)

        component_aggregate["pricing"] = component_pricing_dict

        connection.add(ComponentPricing(**component_pricing_dict))

def GetComponentDetailsFromGraph(component_id):
    if component_id != "component_id":
        print('Getting component details for ID:', component_id)
        try:
            component = ComponentDetails.nodes.get_or_none(part_id=component_id)
            if component:
                print(f"Component found: {component}")
                return component
            print(f"No component found with component_id: {component_id}")
        except Exception as e:
            print(f"Error fetching component details: {e}")
    return None

def GetComponentMetadataFromGraph(component_id):
    if component_id != "component_id":
        print('Getting component metadata for ID:', component_id)
        try:
            metadata = ComponentMetadata.nodes.get_or_none(part_id=component_id)
            if metadata:
                print(f"Component metadata found: {metadata}")
                return metadata
            print(f"No component metadata found with component_id: {component_id}")
        except Exception as e:
            print(f"Error fetching component metadata: {e}")
    return None

def GetComponentInventoryFromGraph(component_id):
    if component_id != "component_id":
        print('Getting component inventory for ID:', component_id)
        try:
            inventory = ComponentInventory.nodes.get_or_none(part_id=component_id)
            if inventory:
                print(f"Component inventory found: {inventory}")
                return inventory
            print(f"No component inventory found with component_id: {component_id}")
        except Exception as e:
            print(f"Error fetching component inventory: {e}")
    return None

def GetComponentPaymentInfoFromGraph(component_id):
    if component_id != "component_id":
        print('Getting component payment info for ID:', component_id)
        try:
            payment_info = ComponentPricing.nodes.get_or_none(part_id=component_id)
            if payment_info:
                print(f"Component payment info found: {payment_info}")
                return payment_info
            print(f"No component payment info found with component_id: {component_id}")
        except Exception as e:
            print(f"Error fetching component payment info: {e}")
    return None

def publish_component(component_aggregate):
    try:
        if not isinstance(component_aggregate, dict):
            raise ValueError("component_aggregate must be a dictionary")

        component_json = {"component": component_aggregate}

        # Publish event to Kafka
        publish_event("component", component_json)

        print("Component data published successfully.")

    except Exception as e:
        print(f"Error publishing component data: {e}")

def AddComponent(component_id):
    if component_id != "component_id":
        print("Adding a new component...")

        publish_component(component_aggregate)

        # Retrieve existing component details, metadata, inventory, and payment information
        component = GetComponentDetailsFromGraph(component_id)
        metadata = GetComponentMetadataFromGraph(component_id)
        inventory = GetComponentInventoryFromGraph(component_id)
        pricing = GetComponentPaymentInfoFromGraph(component_id)

        # Retry if not exists
        if not component:
            component = GetComponentDetails(component_id)

        if not pricing:
            pricing = GetComponentPaymentInformation(component_id)

        if not metadata:
            metadata = GetComponentMetadata(component_id)
        
        if not inventory:
            inventory = GetComponentInventory(component_id)

        # Add to component
        if component:
            if metadata:
                component.metadata.connect(metadata)
            if inventory:
                component.inventory.connect(inventory)
            if pricing:
                component.pricing.connect(pricing)

            print(f"Component {component_id} added successfully.") 

  
            return json.dumps({"message": "Component added successfully"})
        
        return json.dumps({"error": "Component could not be added due to missing data"})

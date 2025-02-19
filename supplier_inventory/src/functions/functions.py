import asyncio
import json
import logging
import os

from dotenv import load_dotenv
from src.tools.nats import publish_event
from src.dao.locations import SupplierLocation
from src.dao.inventory import SupplierInventory
from src.tools.requests import get
from src.utils.graph import connection


load_dotenv()  # Load variables from .env

SUPPLIER_BASE_URL = os.getenv("SUPPLIER_BASE_URL")
BASE_URL = os.getenv("API_BASE_URL")

component_inventory = []

def update_supplier_inventory(item_id: str, supplier_id: str, updated_data: dict):
    """
    Updates the supplier inventory based on item_id and supplier_id.
    :param item_id: The ID of the item in inventory.
    :param supplier_id: The ID of the supplier.
    :param updated_data: A dictionary containing the fields to be updated.
    :return: The updated SupplierInventory node.
    """
    try:
        # Find the existing inventory node based on item_id and supplier_id
        inventory_node = SupplierInventory.nodes.get(item_id=item_id, supplier_id=supplier_id)
        
        # Loop through the keys in the updated_data dictionary to update the properties
        for field, value in updated_data.items():
            # Make sure that the field exists in the model before updating
            if hasattr(inventory_node, field):
                setattr(inventory_node, field, value)
            else:
                print(f"Field '{field}' does not exist on the SupplierInventory model.")
        
        # Save the updated node to the database
        inventory_node.save()

        print(f"Updated inventory for item_id: {item_id}, supplier_id: {supplier_id}")

        return inventory_node  # Return the updated node for further processing (optional)

    except SupplierInventory.DoesNotExist:
        print(f"Supplier inventory not found for item_id: {item_id}, supplier_id: {supplier_id}")
        return None  # If the node doesn't exist, return None

    except Exception as e:
        print(f"Error updating inventory: {e}")
        return None

def GetSupplierInventory(supplier_id):
    if supplier_id != "supplier_id":
        print("getting the supplier inventory")
        response = get(f"{SUPPLIER_BASE_URL}/v1/supplier/{supplier_id}/inventory-info/")
        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")
        # Step 2: Convert string to JSON (Python dictionary)
        supplier_inventory_dict = json.loads(json_string)

        connection.add(SupplierInventory(**supplier_inventory_dict[0]))

        return supplier_inventory_dict

def GetSupplierLocationsFromGraph(supplier_id):
    """Fetches supplier locations from the graph based on supplier_id."""
    if not supplier_id:  # Handles None, empty strings
        logging.warning("Invalid supplier_id provided")
        return None
    
    logging.info(f"Fetching supplier locations for ID: {supplier_id}")
    try:
        supplier_locations = SupplierLocation.nodes.get_or_none(supplier_id=supplier_id)
        if supplier_locations:
            logging.info(f"Supplier locations found: {supplier_locations}")
            return supplier_locations
        logging.info(f"No supplier locations found for supplier_id: {supplier_id}")
    except Exception as e:
        logging.error(f"Error fetching supplier locations: {e}", exc_info=True)

    return None

def GetSupplierInventoryFromGraph(supplier_id):
    if not supplier_id:  # Handles None, empty strings
        logging.warning("Invalid supplier_id provided")
        return None
    
    logging.info(f"Fetching supplier inventory for ID: {supplier_id}")
    try:
        supplier_inventory = SupplierInventory.nodes.get_or_none(supplier_id=supplier_id)
        if supplier_inventory:
            logging.info(f"Supplier inventory found: {supplier_inventory}")
            return supplier_inventory
        logging.info(f"No supplier inventory found for supplier_id: {supplier_id}")
    except Exception as e:
        logging.error(f"Error fetching supplier inventory: {e}", exc_info=True)
    return None


def get_component_inventory(component_id, supplier_id):
    """Retrieves the component inventory."""
    print(f"get_component_inventory called with component_id: {component_id} and supplier_id: {supplier_id}")
    if component_id != "component_id":

        try:
            response = get(f"{BASE_URL}/v1/suppliers/inventory/{supplier_id}/locations")
            
            # Step 1: Decode binary to string
            json_string = response.content.decode("utf-8")

            # Step 2: Convert string to JSON (Python dictionary)
            location_ids = json.loads(json_string)
            
            for location_id in location_ids:
                location_node = GetSupplierLocationsFromGraph(supplier_id)
                if location_node:
                    location_metadata = location_node.__dict__
                    if location_metadata.get("location_id") == location_id:
                        response = get(f"{BASE_URL}/v1/suppliers/inventory/{supplier_id}/locations/{location_id}/items/{component_id}")
                        supplier_inventory_dict = json.loads(response.content.decode("utf-8"))
                        component_inventory.append(supplier_inventory_dict)

        except Exception as e:
            logging.error(f"Error retrieving component inventory: {e}", exc_info=True)

    else:
        logging.warning(f"Invalid component_id provided: {component_id}")
    return


def get_component_inventory_metadata(component_id, supplier_id):
    """Retrieves metadata for the component inventory."""
    print(f"get_component_inventory_metadata called with component_id: {component_id} and supplier_id: {supplier_id}")
    if component_id != "component_id":
        for component in component_inventory:
                # create node for the inventory
                response = GetSupplierInventory(supplier_id)
                response[0]['current_stock'] =  component["quantity"]
                update_supplier_inventory(response[0]["item_id"],supplier_id,response[0])

def add_component_inventory(component_id, supplier_id):
    """Adds new components to the inventory."""

    if component_id != "component_id":
        print(f"add_component_inventory called with component_id: {component_id} and supplier_id: {supplier_id}")
        # get the supplier location node 
        supplier_location = GetSupplierLocationsFromGraph(supplier_id)

        # get the inventory node 
        supplier_inventory = GetSupplierInventoryFromGraph(supplier_id)

        supplier_location.inventory.connect(supplier_inventory)

def add_inventory_notification(component_id, supplier_id):
    """Sends a notification about inventory updates."""
    print(f"add_inventory_notification called with component_id: {component_id} and supplier_id: {supplier_id}")
    try:
        component_json = {"component": component_id,"supplier":supplier_id,"action":"inventory updated"}
        asyncio.run(publish_event("component", component_json))
        print(f"Component Inventory  for {component_id}  retrived for supplier {supplier_id} .")

    except Exception as e:
        print(f"Error publishing component data: {e}")
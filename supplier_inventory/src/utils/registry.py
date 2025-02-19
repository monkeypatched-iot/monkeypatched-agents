from src.functions.functions import (
    get_component_inventory,
    get_component_inventory_metadata,
    add_component_inventory,
    add_inventory_notification
)

function_registry = {
    "GetComponentInventory": get_component_inventory,
    "GetComponentInventoryMetadata": get_component_inventory_metadata,
    "AddComponentInventory": add_component_inventory,
    "AddInventoryNotification": add_inventory_notification
}

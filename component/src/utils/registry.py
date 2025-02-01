from src.functions.functions import AddComponent, GetComponentDetails, GetComponentInventory, GetComponentMetadata, GetComponentPaymentInformation


function_registry = {
    "GetComponentDetails":GetComponentDetails,
    "GetComponentMetadata":GetComponentMetadata,
    "GetComponentInventory":GetComponentInventory,
    "GetComponentPaymentInformation":GetComponentPaymentInformation,
    "AddComponent":AddComponent
}
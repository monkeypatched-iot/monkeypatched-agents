from src.functions.functions import AddComponent, GetComponentDetails, GetComponentMetadata, GetComponentMetrics, GetComponentPaymentInformation


function_registry = {
    "GetComponentDetails":GetComponentDetails,
    "GetComponentMetadata":GetComponentMetadata,
    "GetComponentMetrics":GetComponentMetrics,
    "GetComponentPaymentInformation":GetComponentPaymentInformation,
    "AddComponent":AddComponent
}
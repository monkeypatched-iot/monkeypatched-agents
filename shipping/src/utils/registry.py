from src.functions.functions import AddShippingProvider, GetShippingProviderDetails, GetShippingProviderMetadata


function_registry = {
    "GetShippingProviderDetails": GetShippingProviderDetails,
    "GetShippingProviderMetadata": GetShippingProviderMetadata,
    "AddShippingProvider": AddShippingProvider
}

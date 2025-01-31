from src.functions.functions import AddOrder, GetOrderDetails, GetOrderMetadata, GetOrderMetrics, GetOrderPaymentInformation, GetOrderShippingInformation


function_registry = {
    "GetOrderDetails": GetOrderDetails,
    "GetOrderMetadata": GetOrderMetadata,
    "GetOrderMetrics": GetOrderMetrics,
    "GetOrderPaymentInformation": GetOrderPaymentInformation,
    "GetOrderShippingInformation": GetOrderShippingInformation,
    "AddOrder": AddOrder
}

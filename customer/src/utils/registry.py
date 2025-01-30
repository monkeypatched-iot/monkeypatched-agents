from  src.functions.functions import AddCustomer, GetCustomerDetails, GetCustomerMetadata, GetCustomerMetrics, GetCustomerPaymentInformation

function_registry = {
    "GetCustomerDetails":GetCustomerDetails,
    "GetCustomerMetadata":GetCustomerMetadata,
    "GetCustomerMetrics":GetCustomerMetrics,
    "GetCustomerPaymentInformation":GetCustomerPaymentInformation,
    "AddCustomer":AddCustomer
}
from src.functions.functions import (
    GetSupplierDetails, 
    GetSupplierFinance,
    GetSupplierLocations, 
    GetSupplierCapabilities,
    GetSupplierCertifications,
    GetSupplierQuality,
    AddSupplier
)


function_registry = {
    "GetSupplierDetails":GetSupplierDetails,
    "GetSupplierLocations":GetSupplierLocations,
    "GetSupplierFinance":GetSupplierFinance,
    "GetSupplierCapabilities":GetSupplierCapabilities,
    "GetSupplierCertifications":GetSupplierCertifications,
    "GetSupplierQuality":GetSupplierQuality,
    "AddSupplier":AddSupplier
}
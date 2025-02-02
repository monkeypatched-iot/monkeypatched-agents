from src.functions.functions import (
    GetSupplierDetails, 
    GetSupplierFinance, 
    GetSupplierInventory,
    GetSupplierLocations, 
    GetSupplierPricing,
    GetSupplierCapabilities,
    GetSupplierCertifications,
    GetSupplierQuality,
    GetSupplierShipping,
    AddSupplier
)


function_registry = {
    "GetSupplierDetails":GetSupplierDetails,
    "GetSupplierLocations":GetSupplierLocations,
    "GetSupplierInventory":GetSupplierInventory,
    "GetSupplierPricing":GetSupplierPricing,
    "GetSupplierFinance":GetSupplierFinance,
    "GetSupplierCapabilities":GetSupplierCapabilities,
    "GetSupplierCertifications":GetSupplierCertifications,
    "GetSupplierQuality":GetSupplierQuality,
    "GetSupplierShipping":GetSupplierShipping,
    "AddSupplier":AddSupplier
}
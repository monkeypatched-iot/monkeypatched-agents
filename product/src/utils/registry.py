from  src.functions.functions import GetProductDetails, GetProductMetadata, GetProductInventory, GetProductPricing, AddProduct

function_registry = {
    "GetProductDetails":GetProductDetails,
    "GetProductMetadata":GetProductMetadata,
    "GetProductInventory":GetProductInventory,
    "GetProductPricing":GetProductPricing,
    "AddProduct":AddProduct
}
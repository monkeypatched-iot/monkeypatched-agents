

from src.functions.functions import ConnectComponentToProduct, ConnectCustomertoOrder, ConnectOrderToProduct, ConnectComponentsToSuppliers, UpdateInventory


function_registry = {
   "ConnectCustomertoOrder":ConnectCustomertoOrder,
   "ConnectOrderToProduct":ConnectOrderToProduct,
   "ConnectComponentToProduct":ConnectComponentToProduct,
   "ConnectComponentsToSuppliers":ConnectComponentsToSuppliers,
   "UpdateInventory":UpdateInventory
}
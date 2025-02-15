

from src.functions.functions import ConnectComponentToProduct, ConnectCustomertoOrder, ConnectOrderToProduct, ConnectComponentsToSuppliers, Notify


function_registry = {
   "ConnectCustomerToOrder":ConnectCustomertoOrder,
   "ConnectOrderToProduct":ConnectOrderToProduct,
   "ConnectComponentToProduct":ConnectComponentToProduct,
   "ConnectComponentsToSuppliers":ConnectComponentsToSuppliers,
   "Notify":Notify
}

from src.dao.suppliers.details import SupplierDetails
from src.dao.components.details import ComponentDetails
from src.dao.products.details import ProductDetails
from src.dao.orders.details import OrderDetails
from src.dao.customers.details import CustomerDetails

def GetOrderDetailsFromGraph(order_id):
    if order_id != "order_id":
        print('Getting order details for ID:', order_id)

        try:
            # Check if the order exists
            order = OrderDetails.nodes.get_or_none(order_id=order_id)
            if order:
                print(f"Order found: {order}")
                return order
            else:
                print(f"No order found with order_id: {order_id}")
                return None  # Return None if no order found

        except Exception as e:
            print(f"Error fetching order details: {e}")
            return None

def GetCustomerDetailsFromGraph(customer_id):
    if customer_id != "customer_id":
        print('Getting customer details for ID:', customer_id)

        try:
            # Check if the customer exists
            customer = CustomerDetails.nodes.get_or_none(customer_id=customer_id)
            if customer:
                print(f"Customer found: {customer}")
                return customer
            else:
                print(f"No customer found with customer_id: {customer_id}")
                return None  # Return None if no customer found

        except Exception as e:
            print(f"Error fetching customer details: {e}")
            return None

def GetProductDetailsFromGraph(product_id):
    if product_id != "product_id":
        print('Getting product details for ID:', product_id)

        try:
            # Check if the product exists
            product = ProductDetails.nodes.get_or_none(product_id=product_id)
            if product:
                print(f"Product found: {product}")
                return product
            else:
                print(f"No product found with product_id: {product_id}")
                return None  # Return None if no product found

        except Exception as e:
            print(f"Error fetching product details: {e}")
            return None

def GetComponentDetailsFromGraph(component_id):
    if component_id != "component_id":
        print('Getting component details for ID:', component_id)
        try:
            component = ComponentDetails.nodes.get_or_none(part_id=component_id)
            if component:
                print(f"Component found: {component}")
                return component
            print(f"No component found with component_id: {component_id}")
        except Exception as e:
            print(f"Error fetching component details: {e}")
    return None

def GetSupplierDetailsFromGraph(supplier_id):
    if not supplier_id:  # Handles None, empty strings
        print("Invalid supplier_id provided")
        return None
    
    print(f"Fetching supplier details for ID: {supplier_id}")
    try:
        supplier_details = SupplierDetails.nodes.get_or_none(supplier_id=supplier_id)
        if supplier_details:
            print(f"Supplier details found: {supplier_details}")
            return supplier_details
        print(f"No supplier details found for supplier_id: {supplier_id}")
    except Exception as e:
        print(f"Error fetching supplier details: {e}", exc_info=True)

    return None


def ConnectCustomertoOrder(customer_id,order_id,products):
    if customer_id != "customer_id":
        print("connecting the customer to order")
        order = GetOrderDetailsFromGraph(order_id)
        customer =  GetCustomerDetailsFromGraph(customer_id)
        customer.order.connect(order)

def ConnectOrderToProduct(customer_id,order_id,products):
    print("connect the order to the products")
    if customer_id != "customer_id":
        order = GetOrderDetailsFromGraph(order_id)
        for product in products:
            product_id = product["id"]
            product = GetProductDetailsFromGraph(product_id)
            order.product.connect(product)


def ConnectComponentToProduct(customer_id,order_id,products):
    if customer_id != "customer_id":
        print("connect the compponent to the product")
        for product in products:
                product_id = product["id"]
                product = GetProductDetailsFromGraph(product_id)
                # todo: get the components for the producct from the bom service
                response = {"product_id":"PRD12345","components":[{"component_id":"P12345"}]}
                components = response["components"]
                for component in components:
                    part = GetComponentDetailsFromGraph(component["component_id"])
                    product.part.connect(part)

def ConnectComponentsToSuppliers(customer_id,order_id,products):
      if customer_id != "customer_id":
        print("connect the compponent to the product")
        for product in products:
                # todo: get the components for the producct from the bom service
                response = {"product_id":"PRD12345","components":[{"component_id":"P12345"}]}
                components = response["components"]
                for component in components:
                    part = GetComponentDetailsFromGraph(component["component_id"])
                    # todo: get the supplier for the components
                    response = {"component_id":"PRD12345","suppliers":[{"supplier_id":"S12345"}]}
                    suppliers = response["suppliers"]
                    for supplier in suppliers:
                        current_supplier = GetSupplierDetailsFromGraph(supplier["supplier_id"])
                        part.supplier.connect(current_supplier)

def Notify(customer_id,order_id,products):
    print("update the inventory")
   




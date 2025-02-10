import json
import os

from dotenv import load_dotenv
from src.tools.kafka import publish_event
from src.tools.requests import get
from src.dao.suppliers.details import SupplierDetails
from src.dao.components.details import ComponentDetails
from src.dao.products.details import ProductDetails
from src.dao.orders.details import OrderDetails
from src.dao.customers.details import CustomerDetails


load_dotenv()  # Load variables from .env

BASE_URL = os.getenv("API_BASE_URL")


def GetOrderDetailsFromGraph(order_id):
    """Fetch order details from the knowledge graph."""
    if not order_id:
        print("Invalid order_id provided")
        return None

    print(f"Getting order details for ID: {order_id}")
    try:
        order = OrderDetails.nodes.get_or_none(order_id=order_id)
        if order:
            print(f"Order found: {order}")
            return order
        print(f"No order found with order_id: {order_id}")
    except Exception as e:
        print(f"Error fetching order details: {e}", exc_info=True)

    return None


def GetCustomerDetailsFromGraph(customer_id):
    """Fetch customer details from the knowledge graph."""
    if not customer_id:
        print("Invalid customer_id provided")
        return None

    print(f"Getting customer details for ID: {customer_id}")
    try:
        customer = CustomerDetails.nodes.get_or_none(customer_id=customer_id)
        if customer:
            print(f"Customer found: {customer}")
            return customer
        print(f"No customer found with customer_id: {customer_id}")
    except Exception as e:
        print(f"Error fetching customer details: {e}", exc_info=True)

    return None


def GetProductDetailsFromGraph(product_id):
    """Fetch product details from the knowledge graph."""
    if not product_id:
        print("Invalid product_id provided")
        return None

    print(f"Getting product details for ID: {product_id}")
    try:
        product = ProductDetails.nodes.get_or_none(product_id=product_id)
        if product:
            print(f"Product found: {product}")
            return product
        print(f"No product found with product_id: {product_id}")
    except Exception as e:
        print(f"Error fetching product details: {e}", exc_info=True)

    return None


def GetComponentDetailsFromGraph(component_id):
    """Fetch component details from the knowledge graph."""
    if not component_id:
        print("Invalid component_id provided")
        return None

    print(f"Getting component details for ID: {component_id}")
    try:
        component = ComponentDetails.nodes.get_or_none(part_id=component_id)
        if component:
            print(f"Component found: {component}")
            return component
        print(f"No component found with component_id: {component_id}")
    except Exception as e:
        print(f"Error fetching component details: {e}", exc_info=True)

    return None


def GetSupplierDetailsFromGraph(supplier_id):
    """Fetch supplier details from the knowledge graph."""
    if not supplier_id:
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


def ConnectCustomertoOrder(customer_id, order_id, products):
    """Connect a customer to an order."""
    if customer_id != "customer_id":
        if not customer_id or not order_id:
            print("Invalid customer_id or order_id")
            return

        print("Connecting the customer to order...")
        order = GetOrderDetailsFromGraph(order_id)
        customer = GetCustomerDetailsFromGraph(customer_id)

        if order and customer:
            customer.order.connect(order)
            print(f"Customer {customer_id} connected to order {order_id}")
        else:
            print("Failed to connect customer to order.")


def ConnectOrderToProduct(customer_id, order_id, products):
    """Connect an order to products."""

    if customer_id != "customer_id":
        if not order_id or not products:
            print("Invalid order_id or products")
            return

        print("Connecting order to products...")
        order = GetOrderDetailsFromGraph(order_id)

        if order:
            for product in products:
                product_id = product["id"]
                product_obj = GetProductDetailsFromGraph(product_id)
                if product_obj:
                    order.product.connect(product_obj)
                    print(f"Product {product_id} connected to order {order_id}")
        else:
            print("Failed to connect order to products.")


def ConnectComponentToProduct(customer_id, order_id, products):
    """Connect components to products."""
    if customer_id != "customer_id":

        if not products:
            print("Invalid products")
            return

        print("Connecting components to products...")
        for product in products:
            product_id = product["id"]
            product_obj = GetProductDetailsFromGraph(product_id)

            if product_obj:
                
                response = get(f"{BASE_URL}/v1/bill-of-materials/{product_id}")

                json_string = response.content.decode("utf-8")

                component_dict = json.loads(json_string)

                components = component_dict["components"]

                for component in components:
                    part = GetComponentDetailsFromGraph(component["component_id"])
                    if part:
                        product_obj.part.connect(part)
                        print(f"Component {component['component_id']} connected to product {product_id}")


def ConnectComponentsToSuppliers(customer_id, order_id, products):
    """Connect components to suppliers."""
    if customer_id != "customer_id":

        if not products:
            print("Invalid products")
            return

        for product in products:
            product_id = product["id"]

            response = get(f"{BASE_URL}/v1/bill-of-materials/{product_id}")

            json_string = response.content.decode("utf-8")

            component_dict = json.loads(json_string)

            components = component_dict["components"]

            for component in components:
                part = GetComponentDetailsFromGraph(component["component_id"])
                if part:
                    component_id = component["component_id"]

                    response = get(f"{BASE_URL}/v1/component-suppliers/{component_id}")

                    json_string = response.content.decode("utf-8")

                    supplier_dict = json.loads(json_string)
                        
                    suppliers = supplier_dict["suppliers"]

                    for supplier in suppliers:
                        current_supplier = GetSupplierDetailsFromGraph(supplier["supplier_id"])
                        if current_supplier:
                            part.supplier.connect(current_supplier)
                            print(f"Component {component['component_id']} connected to supplier {supplier['supplier_id']}")


def Notify(customer_id, order_id, products):
    """Send a notification event."""
    print("Updating the inventory and notifying...")
    if not customer_id or not order_id:
        print("Invalid customer_id or order_id")
        return

    publish_event("message", json.dumps({"message": "Knowledge graph updated successfully!"}))
    print("Knowledge graph updated successfully.")

import json
from requests import get

from dotenv import load_dotenv
import os

from src.dao.details import OrderDetails
from src.dao.metadata import OrderMetadata
from src.dao.metrics import OrderMetrics
from src.dao.payment import OrderPayment
from src.dao.shipping import OrderShipping
from src.utils.graph import connection
from src.tools.kafka import publish_event

load_dotenv()  # Load variables from .env

BASE_URL = os.getenv("API_BASE_URL")

order_aggregate = {}

def GetOrderDetails(order_id):
   if order_id != "order_id":
    print("Getting order details...")

    # Fetch order details
    response = get(f"{BASE_URL}/v1/order/details/{order_id}")

    # Step 1: Decode binary to string
    json_string = response.content.decode("utf-8")

    # Step 2: Convert string to JSON (Python dictionary)
    order_dict = json.loads(json_string)

    # Print order details for debugging
    print(order_dict)

    # Save data to the node
    order_aggregate["details"] = order_dict
    connection.add(OrderDetails(**order_dict))

    # Return order details
    return order_dict

def GetOrderMetadata(order_id):
    if order_id != "order_id":
        print("Getting the Order data...")

        # Fetch order metadata
        response = get(f"{BASE_URL}/v1/order/metadata/{order_id}")

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        order_metadata = json.loads(json_string)

        # Print order metadata for debugging
        print(order_metadata)

        # Save data to the node
        order_aggregate["metadata"] = order_metadata
        connection.add(OrderMetadata(**order_metadata))

        # Return order metadata
        return order_metadata


def GetOrderMetrics(order_id):
    if order_id != "order_id":
        print("Getting Order metrics...")

        # Fetch order metrics
        response = get(f"{BASE_URL}/v1/order/metrics/{order_id}")

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        order_metrics = json.loads(json_string)

        # Print order metrics for debugging
        print(order_metrics)

        # Save data to the node
        order_aggregate["metrics"] = order_metrics
        connection.add(OrderMetrics(**order_metrics))

        # Return order metrics
        return order_metrics

def GetOrderPaymentInformation(order_id):
    if order_id != "order_id":
        print("Getting the payment information...")

        # Fetch payment information
        response = get(f"{BASE_URL}/v1/order/payments/{order_id}")

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        payment_info = json.loads(json_string)

        # Print payment information for debugging
        print(payment_info)

        # Save data to the node
        order_aggregate["payments"] = payment_info
        connection.add(OrderPayment(**payment_info))

        # Return payment information
        return payment_info


def GetOrderShippingInformation(order_id):
    if order_id != "order_id":
        print("Getting the shipping information...")

        # Fetch shipping information
        response = get(f"{BASE_URL}/v1/order/shipping/{order_id}")

        # Step 1: Decode binary to string
        json_string = response.content.decode("utf-8")

        # Step 2: Convert string to JSON (Python dictionary)
        shipping_info = json.loads(json_string)

        # Print shipping information for debugging
        print(shipping_info)

        # Save data to the node
        order_aggregate["shipping"] = shipping_info
        connection.add(OrderShipping(**shipping_info))

        # Return shipping information
        return shipping_info

def publish_order():
    try:
        # Ensure it's a dictionary before converting it to JSON
        if not isinstance(order_aggregate, dict):
            raise ValueError("order_aggregate must be a dictionary")

        # Convert to JSON string before sending
        order_json = {"order": order_aggregate}

        # Publish event to Kafka
        publish_event("order", order_json)

        print("Order data published successfully.")

    except Exception as e:
        print(f"Error publishing order data: {e}")

def publish_order():
    try:
        # Ensure it's a dictionary before converting it to JSON
        if not isinstance(order_aggregate, dict):
            raise ValueError("order_aggregate must be a dictionary")

        # Convert to JSON string before sending
        order_json = {"order": order_aggregate}

        # Publish event to Kafka
        publish_event("order", order_json)

        print("Order data published successfully.")

    except Exception as e:
        print(f"Error publishing order data: {e}")


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


def GetOrderMetadataFromGraph(order_id):
    if order_id != "order_id":
        print('Getting order metadata for ID:', order_id)

        try:
            # Check if the metadata exists for the order
            metadata = OrderMetadata.nodes.get_or_none(order_id=order_id)
            if metadata:
                print(f"Order metadata found: {metadata}")
                return metadata
            else:
                print(f"No order metadata found with order_id: {order_id}")
                return None

        except Exception as e:
            print(f"Error fetching order metadata: {e}")
            return None


def GetOrderMetricsFromGraph(order_id):
    if order_id != "order_id":
        print('Getting order metrics for ID:', order_id)

        try:
            # Check if the order metrics exist
            metrics = OrderMetrics.nodes.get_or_none(order_id=order_id)
            if metrics:
                print(f"Order metrics found: {metrics}")
                return metrics
            else:
                print(f"No order metrics found with order_id: {order_id}")
                return None

        except Exception as e:
            print(f"Error fetching order metrics: {e}")
            return None


def GetOrderPaymentInfoFromGraph(order_id):
    if order_id != "order_id":
        print('Getting order payment info for ID:', order_id)

        try:
            # Check if the order payment info exists
            payment_info = OrderPayment.nodes.get_or_none(order_id=order_id)
            if payment_info:
                print(f"Order payment info found: {payment_info}")
                return payment_info
            else:
                print(f"No order payment found with order_id: {order_id}")
                return None

        except Exception as e:
            print(f"Error fetching order payment: {e}")
            return None


def GetOrderShippingInfoFromGraph(order_id):
    if order_id != "order_id":
        print('Getting order shipping info for ID:', order_id)

        try:
            # Check if the order shipping info exists
            shipping_info = OrderShipping.nodes.get_or_none(order_id=order_id)
            if shipping_info:
                print(f"Order shipping info found: {shipping_info}")
                return shipping_info
            else:
                print(f"No order shipping info found with order_id: {order_id}")
                return None

        except Exception as e:
            print(f"Error fetching order shipping info: {e}")
            return None


def AddOrder(order_id):
    if order_id != "order_id":
        print("adding a new order")
        publish_order()

        # Retrieve existing order details, metadata, metrics, and payment information
        order = GetOrderDetailsFromGraph(order_id)
        metadata = GetOrderMetadataFromGraph(order_id)
        metrics = GetOrderMetricsFromGraph(order_id)
        payments = GetOrderPaymentInfoFromGraph(order_id)
        shipping = GetOrderShippingInfoFromGraph(order_id)
    
        # retry if not exists 
        if not order:  
            order = GetOrderDetails(order_id)

        if not payments:
            payments = GetOrderPaymentInformation(order_id)

        if not metadata:
            metadata = GetOrderMetadata(order_id)
        
        if not payments:
            payments = GetOrderPaymentInformation(order_id)

        # add to order 
        if metadata:
            order.metadata.connect(metadata)
        if metrics:
            order.metrics.connect(metrics)
        if payments:
            order.payment.connect(payments)
        if shipping:
            order.shipping.connect(shipping)

        print(f"Order {order_id} added successfully.") 

        return json.dumps({"error": "No order payment data found"})

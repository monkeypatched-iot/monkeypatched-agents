import json
from requests import get

from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

BASE_URL = os.getenv("API_BASE_URL")

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
    # order_aggregate["details"] = order_dict
    # connection.add(Order(**order_dict))

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
        #order_aggregate["metadata"] = order_metadata
        #connection.add(OrderMetadata(**order_metadata))

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
        #order_aggregate["metrics"] = order_metrics
        #connection.add(OrderMetrics(**order_metrics))

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
        # order_aggregate["payments"] = payment_info
        # connection.add(OrderPayments(**payment_info))

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
        # order_aggregate["shipping"] = shipping_info
        # connection.add(OrderShipping(**shipping_info))

        # Return shipping information
        return shipping_info


def AddOrder(order_id):
    if order_id != "order_id":
        print("adding a new Order")
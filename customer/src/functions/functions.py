from src.dao.metadata import CustomerMetadata
from src.dao.metrics import CustomerOrderMetrics
from src.dao.payment import CustomerPaymentData
from src.tools.requests import get
from src.tools.nats import publish_event
from src.utils.graph import connection
from src.dao.details import CustomerDetails
import json

from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

BASE_URL = os.getenv("API_BASE_URL")

Customer = connection.create_node(CustomerDetails)
Metadata = connection.create_node(CustomerMetadata)
Metrics = connection.create_node(CustomerOrderMetrics)
Payments = connection.create_node(CustomerPaymentData)

customer_aggregate = {}

def GetCustomerDetails(customer_id):
    if customer_id != "customer_id":
        print('getting customer details')
        print("Received keyword arguments:", customer_id)

        try:
            response = get(f"{BASE_URL}/v1/customer/details/{customer_id}")
            
            # Step 1: Decode binary to string
            json_string = response.content.decode("utf-8")

            # Step 2: Convert string to JSON (Python dictionary)
            customer_dict = json.loads(json_string)

            print(customer_dict)

            # save data to the node 
            customer_aggregate["details"] = customer_dict
            connection.add(Customer(**customer_dict))

            return customer_dict

        except Exception as e:
            print(f"Error while fetching customer details: {e}")


def GetCustomerMetadata(customer_id):
    if customer_id != "customer_id":
        print('getting customer metadata')
        print("Received keyword arguments:", customer_id)
        
        try:
            response = get(f"{BASE_URL}/v1/customer/metadata/{customer_id}")
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            
            # Step 1: Decode binary to string
            json_string = response.content.decode("utf-8")

             # Step 2: Convert string to JSON (Python dictionary)
            customer_metadata_dict = json.loads(json_string)

            print(customer_metadata_dict)
            customer_aggregate["metadata"] = customer_metadata_dict

            # save data to the node 
            connection.add(Metadata(**customer_metadata_dict))

            print(customer_metadata_dict)

            
        except Exception as e:
            print(f"Error while fetching customer metadata: {e}")


def GetCustomerMetrics(customer_id):
    if customer_id != "customer_id":
        print('getting customer retention metrics')
        print("Received keyword arguments:", customer_id)
        
        try:
            response = get(f"{BASE_URL}/v1/customer/metrics/{customer_id}")
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            
            # Step 1: Decode binary to string
            json_string = response.content.decode("utf-8")

            # Step 2: Convert string to JSON (Python dictionary)
            customer_metric_dict = json.loads(json_string)

            print(customer_metric_dict)

            customer_aggregate["metrics"] = customer_metric_dict
            # save data to the node 
            connection.add(Metrics(**customer_metric_dict))

        except Exception as e:
            print(f"Error while fetching customer retention metrics: {e}")


def GetCustomerPaymentInformation(customer_id):
    if customer_id != "customer_id":
        print('getting customer payments')
        print("Received keyword arguments:", customer_id)
        
        try:
            response = get(f"{BASE_URL}/v1/customer/payment-data/{customer_id}")
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

            # todo: use this data to create a customer-payment node in neo4j

            # Step 1: Decode binary to string
            json_string = response.content.decode("utf-8")

            # Step 2: Convert string to JSON (Python dictionary)
            customer_payment_info_dict = json.loads(json_string)

            print(customer_payment_info_dict)

            # save data to the node 
            customer_aggregate["payment_info"] = customer_payment_info_dict
            connection.add(Payments(**customer_payment_info_dict))

            return customer_payment_info_dict

        except Exception as e:
            print(f"Error while fetching customer payments: {e}")

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

def GetCustomerMetadataFromGraph(customer_id):
    if customer_id != "customer_id":
        print('Getting customer metadata for ID:', customer_id)

        try:
            # Check if the metadata exists for the customer
            metadata = CustomerMetadata.nodes.get_or_none(customer_id=customer_id)
            if metadata:
                print(f"Customer metadata found: {metadata}")
                return metadata
            else:
                print(f"No customer metadata found with customer_id: {customer_id}")
                return None

        except Exception as e:
            print(f"Error fetching customer metadata: {e}")
            return None

def GetCustomerMetricsFromGraph(customer_id):
    if customer_id != "customer_id":
        print('Getting customer metrics for ID:', customer_id)

        try:
            # Check if the customer metrics exist
            metrics = CustomerOrderMetrics.nodes.get_or_none(customer_id=customer_id)
            if metrics:
                print(f"Customer metrics found: {metrics}")
                return metrics
            else:
                print(f"No customer metrics found with customer_id: {customer_id}")
                return None

        except Exception as e:
            print(f"Error fetching customer metrics: {e}")
            return None

def GetCustomerPaymentInfoFromGraph(customer_id):
    if customer_id != "customer_id":
        print('Getting customer payment info for ID:', customer_id)

        try:
            # Check if the customer payment info exists
            payment_info = CustomerPaymentData.nodes.get_or_none(customer_id=customer_id)
            if payment_info:
                print(f"Customer payment info found: {payment_info}")
                return payment_info
            else:
                print(f"No customer payment found with customer_id: {customer_id}")
                return None

        except Exception as e:
            print(f"Error fetching customer payment: {e}")
            return None

def publish_customer():
    try:
        # Ensure it's a dictionary before converting it to JSON
        if not isinstance(customer_aggregate, dict):
            raise ValueError("customer_aggregate must be a dictionary")

        # Convert to JSON string before sending
        customer_json ={"customer": customer_aggregate}

        # Publish event to Kafka
        publish_event("customer",customer_json)

        print("Customer data published successfully.")

    except Exception as e:
        print(f"Error publishing customer data: {e}")

def AddCustomer(customer_id):
    if customer_id != "customer_id":
        print("adding a new customer")
        publish_customer()

        # Retrieve existing customer details, metadata, metrics, and payment information
        customer = GetCustomerDetailsFromGraph(customer_id)
        metadata = GetCustomerMetadataFromGraph(customer_id)
        metrics = GetCustomerMetricsFromGraph(customer_id)
        payments = GetCustomerPaymentInfoFromGraph(customer_id)
 
        # retry  if not exists 
        if not customer:  
            customer = GetCustomerDetails(customer_id)

        if not payments:
            payments = GetCustomerPaymentInformation(customer_id)

        if not metadata:
            metadata = GetCustomerMetadata(customer_id)
        
        if not payments:
            payments = GetCustomerPaymentInformation(customer_id)

        # add to customer 
        if metadata:
            customer.metadata.connect(metadata)
        if metrics:
            customer.metrics.connect(metrics)
        if payments:
            customer.payment.connect(payments)

        print(f"Customer {customer_id} added successfully.") 
 
        return json.dumps({"error": "No customer payment data found"})
    
 

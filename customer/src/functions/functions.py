from src.dao.metadata import CustomerMetadata
from src.dao.metrics import CustomerOrderMetrics
from src.dao.payment import CustomerPaymentData
from src.tools.requests import get
from src.utils.graph import connection
from src.dao.details import CustomerDetails
import json

Customer = connection.create_node(CustomerDetails)
Metadata = connection.create_node(CustomerMetadata)
Metrics = connection.create_node(CustomerOrderMetrics)
Payments = connection.create_node(CustomerPaymentData)

def GetCustomerDetails(customer_id):
    if customer_id != "customer_id":
        print('getting customer details')
        print("Received keyword arguments:", customer_id)

        try:
            response = get(f"http://localhost:8000/v1/customer/details/{customer_id}")
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

            # Step 1: Decode binary to string
            json_string = response.content.decode("utf-8")

            # Step 2: Convert string to JSON (Python dictionary)
            customer_dict = json.loads(json_string)

            print(customer_dict)

            # save data to the node 
        
            customer = connection.add(Customer(**customer_dict))

        except Exception as e:
            print(f"Error while fetching customer details: {e}")


def GetCustomerMetadata(customer_id):
    if customer_id != "customer_id":
        print('getting customer metadata')
        print("Received keyword arguments:", customer_id)
        
        try:
            response = get(f"http://localhost:8000/v1/customer/metadata/{customer_id}")
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            
            # Step 1: Decode binary to string
            json_string = response.content.decode("utf-8")

             # Step 2: Convert string to JSON (Python dictionary)
            customer_metadata_dict = json.loads(json_string)

            print(customer_metadata_dict)

            # save data to the node 
            metadata = connection.add(Metadata(**customer_metadata_dict))

            
        except Exception as e:
            print(f"Error while fetching customer metadata: {e}")


def GetCustomerMetrics(customer_id):
    if customer_id != "customer_id":
        print('getting customer retention metrics')
        print("Received keyword arguments:", customer_id)
        
        try:
            response = get(f"http://localhost:8000/v1/customer/metrics/{customer_id}")
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            
            # Step 1: Decode binary to string
            json_string = response.content.decode("utf-8")

            # Step 2: Convert string to JSON (Python dictionary)
            customer_metric_dict = json.loads(json_string)

            print(customer_metric_dict)

            # save data to the node 
            metric = connection.add(Metrics(**customer_metric_dict))

        except Exception as e:
            print(f"Error while fetching customer retention metrics: {e}")


def GetCustomerPaymentInformation(customer_id):
    if customer_id != "customer_id":
        print('getting customer payments')
        print("Received keyword arguments:", customer_id)
        
        try:
            response = get(f"http://localhost:8000/v1/customer/payment-data/{customer_id}")
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

            # todo: use this data to create a customer-payment node in neo4j

            # Step 1: Decode binary to string
            json_string = response.content.decode("utf-8")

            # Step 2: Convert string to JSON (Python dictionary)
            customer_payment_info_dict = json.loads(json_string)

            print(customer_payment_info_dict)

            # save data to the node 
            payment_info = connection.add(Payments(**customer_payment_info_dict))

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

def AddCustomer(customer_id):
    if customer_id != "customer_id":
        print("adding a new customer")

        # Retrieve existing customer details, metadata, metrics, and payment information
        customer = GetCustomerDetailsFromGraph(customer_id)
        metadata = GetCustomerMetadataFromGraph(customer_id)
        metrics = GetCustomerMetricsFromGraph(customer_id)
        payments = GetCustomerPaymentInfoFromGraph(customer_id)

        # Add customer only if they don't already exist
        if not customer:  # If customer doesn't exist, proceed to create and link
            customer_dict = GetCustomerDetails(customer_id)
            customer = connection.add(CustomerDetails(**customer_dict))

        if metadata:
            customer.metadata.connect(metadata)
        if metrics:
            customer.metrics.connect(metrics)
        if payments:
            customer.payment.connect(payments)

        print(f"Customer {customer_id} added successfully.")
        
        
    





# todo: create an aggregate object and save it to vector db

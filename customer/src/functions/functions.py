from src.tools.requests import get

def GetCustomerDetails(customer_id):
    if customer_id != "customer_id":
        print('getting customer details')
        print("Received keyword arguments:", customer_id)

        try:
            response = get(f"http://localhost:8000/v1/customer/details/{customer_id}")
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            print(response.content)
            # todo: use this data to create a customer node in neo4j
        except Exception as e:
            print(f"Error while fetching customer details: {e}")


def GetCustomerMetadata(customer_id):
    if customer_id != "customer_id":
        print('getting customer metadata')
        print("Received keyword arguments:", customer_id)
        
        try:
            response = get(f"http://localhost:8000/v1/customer/metadata/{customer_id}")
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            print(response.content)
            # todo: use this data to create a customer-metadata node in neo4j
        except Exception as e:
            print(f"Error while fetching customer metadata: {e}")


def GetCustomerMetrics(customer_id):
    if customer_id != "customer_id":
        print('getting customer retention metrics')
        print("Received keyword arguments:", customer_id)
        
        try:
            response = get(f"http://localhost:8000/v1/customer/metrics/{customer_id}")
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            print(response.content)
            # todo: use this data to create a customer-metrics node in neo4j
        except Exception as e:
            print(f"Error while fetching customer retention metrics: {e}")


def GetCustomerPaymentInformation(customer_id):
    if customer_id != "customer_id":
        print('getting customer payments')
        print("Received keyword arguments:", customer_id)
        
        try:
            response = get(f"http://localhost:8000/v1/customer/payment-data/{customer_id}")
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            print(response.content)
            # todo: use this data to create a customer-payment node in neo4j
        except Exception as e:
            print(f"Error while fetching customer payments: {e}")

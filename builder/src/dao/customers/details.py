from neomodel import StructuredNode, StringProperty, EmailProperty, UniqueIdProperty
from src.utils.graph import connection
from src.dao.customers.metadata import CustomerMetadata
from src.dao.customers.metrics import CustomerOrderMetrics
from src.dao.customers.payment import CustomerPaymentData
from src.dao.orders.details import OrderDetails

# CustomerDetails Model using neomodel
class CustomerDetails(StructuredNode):
    # Unique identifier for the customer
    uid = UniqueIdProperty()
    
    # Customer details fields
    customer_id = StringProperty(unique_index=True)
    company_name = StringProperty(required=True)
    contact_name = StringProperty(required=True)
    job_title = StringProperty(required=True)
    email_address = EmailProperty(required=True)
    phone_number = StringProperty(required=True)
    mobile_number = StringProperty(required=True)
    billing_address = StringProperty(required=True)
    shipping_address = StringProperty(required=True)
    industry_type = StringProperty(required=True)
    company_size = StringProperty(required=True)
    preferred_communication_method = StringProperty(required=True)

    # Relationship to CustomerMetadata (HAS relationship)
    metadata = connection.create_relationship_to('CustomerMetadata','HAS_A')
    metrics =  connection.create_relationship_to('CustomerOrderMetrics','HAS_A')
    payment =  connection.create_relationship_to('CustomerPaymentData','HAS_A')
    order =  connection.create_relationship_to('OrderDetails','HAS_MANY')

    

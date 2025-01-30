from neomodel import StructuredNode, StringProperty, FloatProperty

class CustomerPaymentData(StructuredNode):
    # Required properties
    customer_id = StringProperty(unique_index=True)
    payment_terms = StringProperty(required=True)
    tax_identification_number = StringProperty(required=True)
    credit_limit = FloatProperty(required=True)
    payment_method = StringProperty(required=True)
    currency = StringProperty(required=True)
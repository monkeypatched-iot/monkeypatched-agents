from neomodel import StructuredNode, StringProperty
from src.utils.graph import connection
from src.dao.orders.metadata import OrderMetadata
from src.dao.orders.metrics import OrderMetrics
from src.dao.orders.payment import OrderPayment
from src.dao.orders.shipping import OrderShipping
from src.dao.product.details import ProductDetails

class OrderDetails(StructuredNode):
    order_id = StringProperty(required=True, unique=True)
    order_date = StringProperty(required=True)
    order_status = StringProperty(required=True)
    order_type = StringProperty(required=True)
    priority_level = StringProperty(default=None)
    shipping_method = StringProperty(default=None)
    payment_method = StringProperty(required=True)

    metadata = connection.create_relationship_to('OrderMetadata','HAS_A')
    metrics =  connection.create_relationship_to('OrderMetrics','HAS_A')
    payment =  connection.create_relationship_to('OrderPayment','HAS_A')
    shipping =  connection.create_relationship_to('OrderShipping','HAS_A')
    product =  connection.create_relationship_to('ProductDetails','HAS_MANY')


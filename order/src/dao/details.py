from neomodel import StructuredNode, StringProperty, DateTimeProperty, Optional
from datetime import datetime, timezone

def datetime_now():
    return datetime.now(timezone.utc)

class OrderDetailsModel(StructuredNode):
    order_id = StringProperty(required=True, unique=True)
    order_date = DateTimeProperty(default=datetime_now)
    order_status = StringProperty(required=True)
    order_type = StringProperty(required=True)
    priority_level = StringProperty(default=None)
    shipping_method = StringProperty(default=None)
    payment_method = StringProperty(required=True)

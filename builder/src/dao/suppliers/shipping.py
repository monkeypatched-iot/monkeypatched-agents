from neomodel import StructuredNode, StringProperty, FloatProperty, IntegerProperty, BooleanProperty, ArrayProperty
from typing import List, Optional

class SupplierShipping(StructuredNode):
    supplier_id = StringProperty(required=True)
    item_id = StringProperty(required=True)
    location_id = StringProperty(required=True)
    shipping_method = StringProperty(required=True)
    shipping_carrier = StringProperty(required=True)
    shipping_terms = StringProperty(required=True)
    origin_address = StringProperty(required=True)
    destination_address = StringProperty(required=True)
    average_transit_time_days = IntegerProperty(required=True)
    shipping_cost = FloatProperty(required=True)
    shipping_currency = StringProperty(required=True)
    packaging_type = StringProperty(required=True)
    max_weight_per_shipment = FloatProperty(required=True)
    max_volume_per_shipment = FloatProperty(required=True)
    tracking_available = BooleanProperty(required=True)
    tracking_url = StringProperty()
    preferred_delivery_time = StringProperty(required=True)
    insurance_provided = BooleanProperty(required=True)
    insurance_coverage_amount = FloatProperty()
    freight_class = StringProperty()
    customs_clearance_included = BooleanProperty(required=True)
    customs_documentation = ArrayProperty(required=True)  # List of strings for required customs documentation
    last_shipping_date = StringProperty()  # Store as ISO 8601 string
    remarks = StringProperty()

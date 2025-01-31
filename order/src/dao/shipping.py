from neomodel import StructuredNode, StringProperty, DateTimeProperty, FloatProperty

class ShippingInformation(StructuredNode):
    order_id = StringProperty(required=True)
    shipping_id = StringProperty(required=True)
    shipping_address = StringProperty(required=True)
    shipping_date = DateTimeProperty(required=True)
    expected_delivery_date = DateTimeProperty(required=True)
    shipping_method = StringProperty(required=True)
    tracking_number = StringProperty(required=True)
    carrier_name = StringProperty(required=True)
    shipment_status = StringProperty(required=True)
    weight = FloatProperty(required=True)
    shipping_cost = FloatProperty(required=True)
    insurance_details = StringProperty(required=True)
    remarks = StringProperty(required=True)

from neomodel import StructuredNode, StringProperty, FloatProperty, BooleanProperty, ArrayProperty

class ShippingProviderMetadata(StructuredNode):
    provider_id = StringProperty(required=True, unique=True)
    base_shipping_rate = FloatProperty(default=None)
    cost_per_kg = FloatProperty(default=None)
    cost_per_km = FloatProperty(default=None)
    surcharge_details = StringProperty(default=None)
    fleet_details = ArrayProperty(StringProperty(), default=None)
    average_delivery_time = StringProperty(default=None)
    pricing_model = StringProperty(default=None)
    insurance_offered = BooleanProperty(default=None)
    remarks = StringProperty(default=None)
    category = StringProperty(required=True)
    capabilities = StringProperty(required=True)
    description = StringProperty(required=True)
    key_features = ArrayProperty(StringProperty(), required=True)
    certifications = ArrayProperty(StringProperty(), default=None)
    remarks = StringProperty(default=None)

from neomodel import StructuredNode, StringProperty, FloatProperty

class ProductPricing(StructuredNode):
    product_id = StringProperty(unique_index=True, required=True)
    base_price = FloatProperty(required=True)
    discount_rate = FloatProperty()
    tax_rate = FloatProperty(required=True)
    currency = StringProperty(required=True)
    effective_price = FloatProperty(required=True)

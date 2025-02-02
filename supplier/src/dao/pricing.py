from neomodel import StructuredNode, StringProperty, FloatProperty, IntegerProperty

class SupplierPricing(StructuredNode):
    supplier_id = StringProperty(required=True)
    item_id = StringProperty(required=True)
    location_id = StringProperty(required=True)
    item_name = StringProperty(required=True)
    unit_price = FloatProperty(required=True)
    currency = StringProperty(required=True)
    pricing_tier = StringProperty(required=True)
    discount_rate = FloatProperty(required=True)
    net_unit_price = FloatProperty(required=True)
    quantity_range = StringProperty(required=True)
    pricing_validity_start = StringProperty(required=True)  # Store as ISO 8601 string
    pricing_validity_end = StringProperty(required=True)  # Store as ISO 8601 string
    price_adjustment_terms = StringProperty(required=True)
    tax_rate = FloatProperty(required=True)
    tax_amount = FloatProperty(required=True)
    total_unit_cost = FloatProperty(required=True)
    shipping_cost_per_unit = FloatProperty(required=True)
    total_landed_cost = FloatProperty(required=True)
    payment_terms = StringProperty(required=True)
    minimum_order_quantity = IntegerProperty(required=True)
    price_escalation_clause = StringProperty()
    currency_exchange_rate = FloatProperty()
    custom_pricing_notes = StringProperty()

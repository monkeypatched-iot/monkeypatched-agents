from neomodel import StructuredNode, StringProperty, FloatProperty

class ComponentPricingDetails(StructuredNode):
    part_id = StringProperty(required=True)
    unit_price = FloatProperty(required=True)
    total_price = FloatProperty(required=True)
    discount = StringProperty(required=True)
    net_price = FloatProperty(required=True)
    tax_rate = FloatProperty(required=True)
    tax_amount = FloatProperty(required=True)
    final_price = FloatProperty(required=True)

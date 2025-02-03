from neomodel import StructuredNode, StringProperty, FloatProperty, BooleanProperty

class OrderMetadata(StructuredNode):
    order_id = StringProperty(required=True, unique=True)
    customer_segment = StringProperty(default=None)
    sales_region = StringProperty(default=None)
    salesperson = StringProperty(default=None)
    sales_channel = StringProperty(default=None)
    customs_declaration_id = StringProperty()
    
    total_sales_value = FloatProperty(gt=0)
    discount_applied = FloatProperty(default=0.0, ge=0)
    net_sales_value = FloatProperty(required=True, gt=0)
    tax_amount = FloatProperty(default=0.0, ge=0)
    shipping_charges = FloatProperty(default=0.0, ge=0)
    total_revenue = FloatProperty(required=True, gt=0)
    
    commission_rate = FloatProperty(default=0.0, ge=0, le=100)
    commission_amount = FloatProperty(default=0.0, ge=0)
    promo_code_used = BooleanProperty(default=False)
    promo_code_value = FloatProperty(default=0.0, ge=0)
    
    upsell_or_cross_sell = StringProperty(default=None)
    refund_amount = FloatProperty(default=0.0, ge=0)
from neomodel import StructuredNode, StringProperty, IntegerProperty, FloatProperty, BooleanProperty

class ProductInventory(StructuredNode):
    product_id = StringProperty(unique_index=True, required=True)
    available_stock = IntegerProperty(required=True)
    reorder_level = IntegerProperty(required=True)
    backorder_allowed = BooleanProperty(required=True)
    economic_order_quantity = FloatProperty()
    reorder_point = IntegerProperty()
    safety_stock_level = IntegerProperty()
    inventory_turnover = FloatProperty()
    stockout_rate = FloatProperty()
    demand_forecast_accuracy = FloatProperty()

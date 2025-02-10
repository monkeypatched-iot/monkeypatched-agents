from neomodel import StructuredNode, StringProperty, IntegerProperty, FloatProperty, BooleanProperty

class ComponentInventory(StructuredNode):
    part_id = StringProperty(required=True)
    available_stock = IntegerProperty(required=True)
    reorder_level = IntegerProperty(required=True)
    backorder_allowed = BooleanProperty(required=True)
    economic_order_quantity = FloatProperty(required=True)
    reorder_point = IntegerProperty(required=True)
    safety_stock_level = IntegerProperty(required=True)
    inventory_turnover = FloatProperty(required=True)
    stockout_rate = FloatProperty(required=True)
    demand_forecast_accuracy = FloatProperty(required=True)

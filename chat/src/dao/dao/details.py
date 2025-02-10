from neomodel import StructuredNode, StringProperty, FloatProperty, ArrayProperty,JSONProperty,UniqueIdProperty
from src.utils.graph import connection
from src.dao.inventory import ProductInventory
from monkeypatched_chat.src.dao.document.metadata import ProductMetadata
from src.dao.pricing import ProductPricing

class ProductDetails(StructuredNode):
    uid = UniqueIdProperty()
    
    product_id = StringProperty(unique_index=True, required=True)
    product_name = StringProperty(required=True)
    product_category = StringProperty(required=True)
    product_type = StringProperty(required=True)
    product_dimensions = StringProperty(required=True)
    weight = FloatProperty(required=True)
    product_price = FloatProperty(required=True)
    manufacturer = StringProperty(required=True)
    product_description = StringProperty(required=True)
    product_features = JSONProperty(required=True)
    material_composition = StringProperty()
    power_requirements = StringProperty()
    color_options = ArrayProperty()
    environmental_impact = StringProperty()
    safety_features = StringProperty()

    # Relationship to CustomerMetadata (HAS relationship)
    inventory = connection.create_relationship_to('ProductInventory','HAS_A')
    metadata =  connection.create_relationship_to('ProductMetadata','HAS_A')
    pricing =  connection.create_relationship_to('ProductPricing','HAS_A')

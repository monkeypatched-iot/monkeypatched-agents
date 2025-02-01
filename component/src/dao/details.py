from neomodel import StructuredNode, StringProperty, FloatProperty, BooleanProperty
from src.dao.metadata import ComponentMetadata
from src.dao.inventory import ComponentInventory
from src.dao.pricing import ComponentPricing
from src.utils.graph import connection

class ComponentDetails(StructuredNode):
    part_id = StringProperty(required=True)
    part_name = StringProperty(required=True)
    part_category = StringProperty(required=True)
    part_type = StringProperty(required=True)
    part_description = StringProperty(required=True)
    hsn_code = StringProperty(required=True)
    material_composition = StringProperty(required=True)
    part_dimensions = StringProperty(required=True)
    unit_of_measure = StringProperty(required=True)
    weight = FloatProperty(required=True)
    part_number = StringProperty(required=True)
    batch_number = StringProperty(required=True)
    quality_control_batch = StringProperty(required=True)
    part_lifecycle_status = StringProperty(required=True)
    part_testing_date = StringProperty(required=True)
    part_testing_results = StringProperty(required=True)
    part_warranty = StringProperty(required=True)
    part_customization = BooleanProperty(required=True)

    metadata = connection.create_relationship_to('ComponentMetadata','HAS_A')
    inventory =  connection.create_relationship_to('ComponentInventory','HAS_A')
    pricing =  connection.create_relationship_to('ComponentPricing','HAS_A')

from neomodel import StructuredNode, StringProperty, DateTimeProperty

class ComponentMetadata(StructuredNode):
    part_id = StringProperty(required=True)
    certification_details = StringProperty(required=True)
    production_batch_id = StringProperty(required=True)
    material_origin = StringProperty(required=True)
    environmental_rating = StringProperty(required=True)
    warranty_terms = StringProperty(required=True)
    last_updated = DateTimeProperty(required=True)
    remarks = StringProperty(required=True)

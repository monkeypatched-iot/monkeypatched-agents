from neomodel import StructuredNode, StringProperty, FloatProperty
from src.utils.graph import connection
from src.dao.metadata import ShippingProviderMetadata

class ShippingProviderDetails(StructuredNode):
    provider_id = StringProperty(required=True, unique=True)
    provider_name = StringProperty(required=True, unique=True)
    contact_number = StringProperty(required=True)
    email_address = StringProperty(required=True)
    address = StringProperty(default=None)
    service_areas = StringProperty(default=None)
    available_services = StringProperty(required=True)
    rating = FloatProperty(required=True)
    website_url = StringProperty(required=True)

    metadata = connection.create_relationship_to('ShippingProviderMetadata','HAS_A')


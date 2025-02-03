from neomodel import StructuredNode, StringProperty, EmailProperty, DateTimeProperty, IntegerProperty, ArrayProperty, RelationshipFrom
from typing import List, Optional
import datetime
from src.utils.graph import connection

# CustomerMetadata Model using neomodel
class CustomerMetadata(StructuredNode):
    # Properties
    customer_id = StringProperty(unique_index=True)
    account_manager = StringProperty(required=True)
    special_requirements = StringProperty(required=True)
    warranty_information = StringProperty(required=True)
    support_contact = EmailProperty(required=True)
    notes_comments = StringProperty(required=True)
    preferred_shipping_method = StringProperty(required=True)
    lead_time = IntegerProperty(required=True)
    region = StringProperty(required=True)
    account_status = StringProperty(required=True)
    customer_since = StringProperty(required=True)
    social_media_handles = ArrayProperty()
    shipping_contact_name = StringProperty(required=True)
    shipping_contact_number = StringProperty(required=True)
    
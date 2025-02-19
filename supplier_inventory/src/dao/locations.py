from neomodel import StructuredNode, StringProperty, IntegerProperty, FloatProperty
from src.utils.graph import connection
from src.dao.inventory import SupplierInventory

class SupplierLocation(StructuredNode):
    supplier_id = StringProperty(required=True, unique_index=True)
    item_id = StringProperty(required=True)
    location_id = StringProperty(required=True, unique_index=True)
    location_name = StringProperty(required=True)
    address_line_1 = StringProperty(required=True)
    address_line_2 = StringProperty()
    city = StringProperty(required=True)
    state_province = StringProperty(required=True)
    country = StringProperty(required=True)
    postal_code = StringProperty(required=True)
    contact_number = StringProperty(required=True)
    email_address = StringProperty(required=True)
    facility_type = StringProperty(required=True)
    operational_hours = StringProperty(required=True)
    primary_function = StringProperty(required=True)
    geographical_coordinates = StringProperty(required=True)
    annual_production_capacity = IntegerProperty()
    employee_count = IntegerProperty(required=True)
    certifications = StringProperty()  # Convert list to a comma-separated string if needed
    storage_capacity = FloatProperty()
    key_contact_person = StringProperty(required=True)
    key_contact_role = StringProperty(required=True)
    remarks = StringProperty()

    inventory = connection.create_relationship_to('SupplierInventory', 'HAS')
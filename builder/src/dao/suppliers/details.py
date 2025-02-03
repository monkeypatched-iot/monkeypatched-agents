from neomodel import StructuredNode, StringProperty, BooleanProperty, IntegerProperty, FloatProperty, ArrayProperty
from src.utils.graph import connection
from src.dao.suppliers.shipping import SupplierShipping
from src.dao.suppliers.quality import SupplierQuality
from src.dao.suppliers.inventory import SupplierInventory
from src.dao.suppliers.locations import SupplierLocation
from src.dao.suppliers.pricing import SupplierPricing
from src.dao.suppliers.finances import SupplierFinancials
from src.dao.suppliers.capablities import SupplierCapabilities
from src.dao.suppliers.certifications import SupplierCertifications

class SupplierDetails(StructuredNode):
    supplier_id = StringProperty(required=True, unique_index=True)
    supplier_name = StringProperty(required=True)
    supplier_type = StringProperty(required=True)
    address = StringProperty(required=True)
    city = StringProperty(required=True)
    state_region = StringProperty(required=True)
    country = StringProperty(required=True)
    postal_code = StringProperty(required=True)
    contact_name = StringProperty(required=True)
    contact_email = StringProperty(required=True)
    contact_phone = StringProperty(required=True)
    website = StringProperty()
    tax_id = StringProperty(required=True)
    payment_terms = StringProperty(required=True)
    currency = StringProperty(required=True)
    lead_time_days = IntegerProperty(required=True)
    annual_spend = FloatProperty(required=True)
    approval_status = StringProperty(required=True)
    risk_rating = IntegerProperty(required=True)
    certifications = ArrayProperty(StringProperty(), required=True)
    industry = StringProperty(required=True)
    past_performance_score = FloatProperty(required=True)
    preferred_supplier = BooleanProperty(required=True)
    last_order_date = StringProperty()
    remarks = StringProperty()

    # Relationships
    certifications = connection.create_relationship_to('SupplierCertifications', 'HAS')
    locations = connection.create_relationship_to('SupplierLocation', 'HAS')
    inventory = connection.create_relationship_to('SupplierInventory', 'HAS')
    pricing = connection.create_relationship_to('SupplierPricing', 'HAS')
    finance = connection.create_relationship_to('SupplierFinancials', 'HAS')
    quality = connection.create_relationship_to('SupplierQuality', 'HAS')
    capabilities = connection.create_relationship_to('SupplierCapabilities', 'HAS')
    shipping = connection.create_relationship_to('SupplierShipping', 'HAS')


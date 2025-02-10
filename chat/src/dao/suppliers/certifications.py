from neomodel import StructuredNode, StringProperty, BooleanProperty

class SupplierCertifications(StructuredNode):
    supplier_id = StringProperty(required=True, unique_index=True)
    certification_name = StringProperty(required=True)
    certification_type = StringProperty(required=True)
    issuing_authority = StringProperty(required=True)
    certification_number = StringProperty()
    issue_date = StringProperty(required=True)
    expiry_date = StringProperty()
    renewal_required = BooleanProperty(required=True)
    renewal_frequency = StringProperty()
    scope_of_certification = StringProperty(required=True)
    audit_required = BooleanProperty(required=True)
    last_audit_date = StringProperty()
    next_audit_date = StringProperty()
    certification_status = StringProperty(required=True)
    certificate_document = StringProperty()
    remarks = StringProperty()

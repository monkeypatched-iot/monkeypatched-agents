from neomodel import StructuredNode, StringProperty, FloatProperty, IntegerProperty, BooleanProperty, ArrayProperty
from typing import List

class SupplierQuality(StructuredNode):
    supplier_id = StringProperty(required=True)
    item_id = StringProperty(required=True)
    location_id = StringProperty(required=True)
    quality_rating = FloatProperty(required=True)
    defect_rate = FloatProperty(required=True)
    on_time_delivery_rate = FloatProperty(required=True)
    return_rate = FloatProperty(required=True)
    non_conformance_reports = IntegerProperty(required=True)
    iso_certifications = ArrayProperty(required=True)  # List of strings for ISO certifications
    quality_audit_compliance_rate = FloatProperty(required=True)
    inspection_pass_rate = FloatProperty(required=True)
    warranty_claims_rate = FloatProperty(required=True)
    supplier_quality_manager = StringProperty(required=True)
    corrective_action_turnaround_time = IntegerProperty(required=True)
    customer_complaint_rate = FloatProperty(required=True)
    continuous_improvement_programs = BooleanProperty(required=True)
    last_quality_audit_date = StringProperty(required=True)  # Store as ISO 8601 string
    next_quality_audit_date = StringProperty(required=True)  # Store as ISO 8601 string
    inspection_process_details = StringProperty()
    first_pass_yield = FloatProperty(required=True)
    material_traceability = BooleanProperty(required=True)
    adherence_to_specifications = FloatProperty(required=True)
    remarks = StringProperty()

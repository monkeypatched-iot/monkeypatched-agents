import json
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import re
import json
import logging
from neomodel import db

from  src.api.steps import execute_query_for_knowledge_graph_helper

load_dotenv()  # Load variables from .env

logging.basicConfig(level=logging.INFO)

OLAMMA_BASE_URL = os.getenv("OLAMMA_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

def ask_question_from_knowledge_graph_helper(question):

    prompt_template = PromptTemplate(input_variables=["question"], template="""
    
    human:
    You are neo4j expert that generates cypher queries from natural language  

    You have access to a graph database with the following entities in it  
        ComponentDetails 
        ComponentPricing 
        ComponentMetadata 
        ComponentDetails 
        ComponentInventory
    represented by the neomodel below 

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

    class ComponentMetadata(StructuredNode):
        part_id = StringProperty(required=True)
        certification_details = StringProperty(required=True)
        production_batch_id = StringProperty(required=True)
        material_origin = StringProperty(required=True)
        environmental_rating = StringProperty(required=True)
        warranty_terms = StringProperty(required=True)
        last_updated = StringProperty(required=True)
        remarks = StringProperty(required=True)

    class ComponentPricing(StructuredNode):
        part_id = StringProperty(required=True)
        unit_price = FloatProperty(required=True)
        total_price = FloatProperty(required=True)
        discount = StringProperty(required=True)
        net_price = FloatProperty(required=True)
        tax_rate = FloatProperty(required=True)
        tax_amount = FloatProperty(required=True)
        final_price = FloatProperty(required=True)     

    Where the Component Details is linked to all other entities the structure of each of the entities is given by the pydantic models Below  

    Each of these components must have a supplier where the supplier entities are given below 

    SupplierCapabilities
    SupplierCertifications
    SupplierDetails
    SupplierFinancials
    SupplierLocation
    SupplierQuality
    SupplierShipping

    described by the neo model given below 


    class SupplierCapabilities(StructuredNode):
        supplier_id = StringProperty(unique_index=True, required=True)
        core_competencies = ArrayProperty(StringProperty(), required=True)
        production_capacity = IntegerProperty(required=True)
        capacity_unit = StringProperty(required=True)
        lead_time = IntegerProperty(required=True)
        technology_capability = ArrayProperty(StringProperty(), required=True)
        certifications = ArrayProperty(StringProperty(), required=True)
        quality_control_measures = StringProperty(required=True)
        rad_capabilities = BooleanProperty(required=True)
        customization_capability = BooleanProperty(required=True)
        geographical_reach = ArrayProperty(StringProperty(), required=True)
        material_expertise = ArrayProperty(StringProperty(), required=True)
        sustainability_practices = StringProperty()
        subcontracting_capability = BooleanProperty(required=True)
        maintenance_services = BooleanProperty(required=True)
        packaging_capabilities = StringProperty(required=True)
        export_compliance = BooleanProperty(required=True)
        testing_facilities = BooleanProperty(required=True)
        automation_level = StringProperty(required=True)
        employee_count = IntegerProperty(required=True)
        partnership_initiatives = StringProperty()
        innovation_awards = ArrayProperty(StringProperty())
        remarks = StringProperty()

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
        finance = connection.create_relationship_to('SupplierFinancials', 'HAS')
        quality = connection.create_relationship_to('SupplierQuality', 'HAS')
        capabilities = connection.create_relationship_to('SupplierCapabilities', 'HAS')
        

    class SupplierFinancials(StructuredNode):
        supplier_id = StringProperty(required=True, unique_index=True)
        annual_revenue = FloatProperty(required=True)
        currency = StringProperty(required=True)
        net_profit_margin = FloatProperty(required=True)
        operating_costs = FloatProperty(required=True)
        debt_to_equity_ratio = FloatProperty(required=True)
        credit_rating = StringProperty(required=True)
        payment_terms = StringProperty(required=True)
        outstanding_balance = FloatProperty(required=True)
        overdue_invoices = IntegerProperty(required=True)
        average_payment_delay_days = IntegerProperty(required=True)
        financial_health_score = FloatProperty(required=True)
        bank_name = StringProperty()
        bank_account_number = StringProperty()
        tax_identification_number = StringProperty()
        audited_financials = BooleanProperty(required=True)
        last_audit_date = StringProperty()
        profitability_trends = StringProperty(required=True)
        liquidity_ratio = FloatProperty(required=True)
        payment_methods_accepted = ArrayProperty(StringProperty())
        tax_compliance_status = BooleanProperty(required=True)
        remarks = StringProperty()
    from neomodel import StructuredNode, StringProperty, IntegerProperty, FloatProperty

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


    class SupplierShipping(StructuredNode):
        supplier_id = StringProperty(required=True)
        item_id = StringProperty(required=True)
        location_id = StringProperty(required=True)
        shipping_method = StringProperty(required=True)
        shipping_carrier = StringProperty(required=True)
        shipping_terms = StringProperty(required=True)
        origin_address = StringProperty(required=True)
        destination_address = StringProperty(required=True)
        average_transit_time_days = IntegerProperty(required=True)
        shipping_cost = FloatProperty(required=True)
        shipping_currency = StringProperty(required=True)
        packaging_type = StringProperty(required=True)
        max_weight_per_shipment = FloatProperty(required=True)
        max_volume_per_shipment = FloatProperty(required=True)
        tracking_available = BooleanProperty(required=True)
        tracking_url = StringProperty()
        preferred_delivery_time = StringProperty(required=True)
        insurance_provided = BooleanProperty(required=True)
        insurance_coverage_amount = FloatProperty()
        freight_class = StringProperty()
        customs_clearance_included = BooleanProperty(required=True)
        customs_documentation = ArrayProperty(required=True)  # List of strings for required customs documentation
        last_shipping_date = StringProperty()  # Store as ISO 8601 string
        remarks = StringProperty()
                                     
        here is an example goww ro do this 
                                     
        Questtion : what is the part number for Steel Gear ?
        Answer : MATCH (c:ComponentDetails)
                WHERE c.part_name = 'steel gear'
                RETURN c.part_number
                                     
        Question: what is the part id for Steel Gear?
        Answer:MATCH (c:ComponentDetails)-[:HAS_A]->(m:ComponentMetadata)
                WHERE c.part_name = 'Steel Gear'
                RETURN c.part_id
                                     
        Question: what suppliers provide for Steel Gear?
        Answer: MATCH (c:ComponentDetails)-[:HAS_A]->(m:ComponentMetadata)
                MATCH (s:SupplierDetails)-[:HAS_A]->(c)
                WHERE c.part_name = 'Steel Gear'
                RETURN s.supplier_name
                                     
        Question: what is my current inventory for Steel Gear?
        Answer: MATCH (c:ComponentDetails)-[:HAS_A]->(i:ComponentInventory)
                WHERE c.part_name = 'Steel Gear'
                RETURN i.available_stock
                    
        Question: what is the name of the supplier that suppliers Steel Gear?
                  MATCH (c:ComponentDetails)-[:HAS_A]->(i:SupplierDetails)
                  RETURN i.supplier_name
                                     
        Question: what is the location of the supplier?
                  MATCH (s:SupplierDetails)-[:HAS]->(l:SupplierLocation)
                  WHERE s.supplier_id = 'SUP-001'
                  RETURN l.location_name
            
        Question : what is the current stock at the location ?
                MATCH (s:SupplierDetails)-[:HAS]->(l:SupplierLocation)
                MATCH (l:SupplierLocation) -[:HAS]->(i:SupplierInventory)
                WHERE s.supplier_id = 'SUP-001' AND i.item_id = 'ITEM-1234'
                RETURN i.current_stock
                                     
        Question : what are the capablities of the supplier with id SUP-001
                   MATCH (s:SupplierDetails)-[:HAS]->(c:SupplierCapabilities)
                   WHERE s.supplier_id = 'SUP-001'
                   RETURN c
                
                                                    
        Response Format:  
            return the response in the exact format below:
                                                
           <answer>

    generate the cypher query to answer the {question} following the given examples guidelines  strictly
                                     
    Guldelines
        - doc not make any assumptions about the data strictly use the text above   
        - use the fields given in the neo model only
        - use the entity names provided above  neo model only
        - do not change the case of the letters in the question from uppercase to lowercase 
        - do not use alias
        - when asking for part id return the part_id
        - do not return any extra text like ```cypher and ```
        - also do not return any exlainations or any other text other than the query
        - use a HAS_A relationship in reults for edges
        - if the edge is for Supplier* use a HAS relationship in results for edges
        - when asked about total price return the total_price from ComponentPricing
        - when asked about capablities use SupplierCapablities
        - when asked about supplier rename the edge as HAS strictly do not add any other text 
        - please return the answers in the correct cypher syntax
        - also replace SupplierCapablities ith SupplierCapabilities
        - always surround the answer with <answer></answer>
                                     

                                                           
    """)

    model = OllamaLLM(model=MODEL_NAME, temperature=0.1 , base_url= OLAMMA_BASE_URL)

    chain = prompt_template | model

    # Invoke the chain with the Component_id parameter
    response = chain.invoke({"question": question})   

    # print(response)

    # Regex to extract text between <answer> and </answer>
    pattern = r'<answer>\s*(.*?)\s*</answer>'

    # Find all matches
    matches = re.findall(pattern, response, re.DOTALL)  # re.DOTALL allows . to match newlines


    # Print the matched content
    for match in matches:
        print(match)
        execute_query_for_knowledge_graph_helper(match)
   
    
    return True
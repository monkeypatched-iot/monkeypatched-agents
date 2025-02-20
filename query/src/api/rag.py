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

from src.api.steps import execute_query_for_knowledge_graph_helper

load_dotenv()  # Load variables from .env

logging.basicConfig(level=logging.INFO)

OLAMMA_BASE_URL = os.getenv("OLAMMA_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

def ask_question_from_knowledge_graph_helper(question):

    prompt_template = PromptTemplate(input_variables=["question"], template="""
    
     
    human:
    You are neo4j expert that generates cypher queries from natural language  

  Entities and Their Fields:

    1. ComponentDetails:
            part_id
            part_name
            part_category
            part_type
            part_description
            hsn_code
            material_composition
            part_dimensions
            unit_of_measure
            weight
            part_number
            batch_number
            quality_control_batch
            part_lifecycle_status
            part_testing_date
            part_testing_results
            part_warranty
            part_customization
            Relationships:
                HAS_A to ComponentMetadata, ComponentInventory, ComponentPricing

    2. ComponentInventory:
            part_id
            available_stock
            reorder_level
            backorder_allowed
            economic_order_quantity
            reorder_point
            safety_stock_level
            inventory_turnover
            stockout_rate
            demand_forecast_accuracy

    3. ComponentPricing:
            part_id
            unit_price
            total_price
            discount
            net_price
            tax_rate
            tax_amount
            final_price

    4. SupplierDetails:
            supplier_id
            supplier_name
            supplier_type
            address
            city
            state_region
            country
            postal_code
            contact_name
            contact_email
            contact_phone
            website
            tax_id
            payment_terms
            currency
            lead_time_days
            annual_spend
            approval_status
            risk_rating
            certifications
            industry
            past_performance_score
            preferred_supplier
            last_order_date
            Relationships:
                HAS to SupplierCapabilities, SupplierCertifications, SupplierLocation, SupplierFinancials, SupplierQuality

    5. SupplierCapabilities:
            supplier_id
            core_competencies
            production_capacity
            capacity_unit
            lead_time
            technology_capability
            certifications
            quality_control_measures
            rad_capabilities
            customization_capability
            geographical_reach
            material_expertise
            sustainability_practices
            subcontracting_capability
            maintenance_services
            packaging_capabilities
            export_compliance
            testing_facilities
            automation_level
            employee_count
            partnership_initiatives
            innovation_awards
            remarks

    6. SupplierCertifications:
            supplier_id
            certification_name
            certification_type
            issuing_authority
            certification_number
            issue_date
            expiry_date
            renewal_required
            renewal_frequency
            scope_of_certification
            audit_required
            last_audit_date
            next_audit_date
            certification_status
            certificate_document
            remarks

    7. SupplierLocation:
            supplier_id
            item_id
            location_id
            location_name
            address_line_1
            address_line_2
            city
            state_province
            country
            postal_code
            contact_number
            email_address
            facility_type
            operational_hours
            primary_function
            geographical_coordinates
            annual_production_capacity
            employee_count
            certifications
            storage_capacity
            key_contact_person
            key_contact_role
            remarks

    8. SupplierQuality:
            supplier_id
            item_id
            location_id
            quality_rating
            defect_rate
            on_time_delivery_rate
            return_rate
            non_conformance_reports
            iso_certifications
            quality_audit_compliance_rate
            inspection_pass_rate
            warranty_claims_rate
            supplier_quality_manager
            corrective_action_turnaround_time
            customer_complaint_rate
            continuous_improvement_programs
            last_quality_audit_date
            next_quality_audit_date
            inspection_process_details
            first_pass_yield
            material_traceability
            adherence_to_specifications
            remarks

    9. SupplierShipping:
            supplier_id
            item_id
            location_id
            shipping_method
            shipping_carrier
            shipping_terms
            origin_address
            destination_address
            average_transit_time_days
            shipping_cost
            shipping_currency
            packaging_type
            max_weight_per_shipment
            max_volume_per_shipment
            tracking_available
            tracking_url
            preferred_delivery_time
            insurance_provided
            insurance_coverage_amount
            freight_class
            customs_clearance_included
            customs_documentation
            last_shipping_date
            remarks

    10. OrderDetails:
            order_id
            order_date
            order_status
            order_type
            priority_level
            shipping_method
            payment_method
            Relationships:
                HAS_A to OrderMetrics
                HAS_A to OrderPayment
                HAS_A to OrderShipping

    11. OrderMetadata:
            order_id
            customer_segment
            sales_region
            salesperson
            sales_channel
            customs_declaration_id
            total_sales_value
            discount_applied
            net_sales_value
            tax_amount
            shipping_charges
            total_revenue
            commission_rate
            commission_amount
            promo_code_used
            promo_code_value
            upsell_or_cross_sell
            refund_amount

    12. OrderMetrics:
            order_id
            returns_exchanges_requested
            backordered_items
            shipping_tracking_number
            order_fulfillment_location
            customs_clearance_status
            order_handling_time
            shipping_status
            order_delivery_time
            customer_feedback_score
            order_quality_rating
            failed_delivery_attempts
            damage_defect_rate
            order_resolution_time
            customer_service_interaction_count
            order_accuracy_rate
            late_shipment_rate
            customer_loyalty_index
            order_fulfillment_time
            lead_time_variability
            cycle_time_for_time_sensitive_orders
            missed_priority_order_rate
            backlogged_order_rate
            critical_path_completion_rate
            order_cycle_time
            order_fill_rate
            perfect_order_rate

    13. OrderPayment:
            order_id
            order_payment_status
            payment_method
            payment_terms
            order_payment_due_date
            payment_received_date
            payment_amount
            outstanding_payment_amount
            payment_overdue_amount
            early_payment_discount
            late_payment_penalty
            credit_limit_utilization
            customer_payment_history
            payment_dispute_status
            payment_risk_rating
            payment_processing_time
            payment_approval_status

    14. OrderShipping:
            order_id
            shipping_id
            shipping_address
            shipping_date
            expected_delivery_date
            shipping_method
            tracking_number
            carrier_name
            shipment_status
            weight
            shipping_cost
            insurance_details
            remarks

    15. CustomerDetails:
            uid
            customer_id
            company_name
            contact_name
            job_title
            email_address
            phone_number
            mobile_number
            billing_address
            shipping_address
            industry_type
            company_size
            preferred_communication_method
            Relationships:
                HAS_A to CustomerMetadata
                HAS_A to CustomerOrderMetrics
                HAS_A to CustomerPaymentData

    16. CustomerMetadata:
            customer_id
            account_manager
            special_requirements
            warranty_information
            support_contact
            notes_comments
            preferred_shipping_method
            lead_time
            region
            account_status
            customer_since
            social_media_handles
            shipping_contact_name
            shipping_contact_number
                                     
    17. CustomerOrderMetrics:

            customer_id
            profit_per_order
            revenue_per_order
            cost_to_serve_per_order
            customer_lifetime_value
            return_on_fulfillment_cost
            gross_profit_margin
            inventory_turnover_ratio
            order_profitability_index
            average_order_value
            customer_retention_rate
            order_fill_rate
            on_time_delivery_rate
            order_cycle_time
            late_order_rate
            perfect_order_rate
            return_rate
            backorder_rate
            order_accuracy_rate
            first_time_fill_rate
            customer_satisfaction_score
            order_margin_per_unit
            cost_of_goods_sold
            order_processing_time
                                     
    18. CustomerPaymentData:

            customer_id
            payment_terms
            tax_identification_number
            credit_limit
            payment_method
            currency
                                     
    19. ProductInventory:

            product_id
            available_stock
            reorder_level
            backorder_allowed
            economic_order_quantity
            reorder_point
            safety_stock_level
            inventory_turnover
            stockout_rate
            demand_forecast_accuracy
    
     20. ProductMetadata:

            product_id
            ce_certification
            product_certifications
            product_lifecycle_stage
            product_warranty_coverage
            release_date
            product_lead_time
            minimum_production_capacity
            maximum_production_capacity
            serial_number
            part_number
            batch_number
            hsn_number
            lot_number
            production_date
            expiration_date
            quality_control_batch
            manufacturing_location
            product_testing_date
            product_testing_results
            customer_order_reference
            shipment_tracking_number
            return_exchange_reference
            return_rate_for_product
                                     
    21. ProductPricing:

            product_id
            base_price
            discount_rate
            tax_rate
            currency
            effective_price
                                     
        here is an example to do this 
                                     
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
                
                                                    
        Please generate the response in the exact format below, ensuring no deviations in structure:

        <answer>Your response here</answer>

        Strictly adhere to this format without adding any extra text, explanations, or special characters.

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
                                                           
    """)

    model = OllamaLLM(model=MODEL_NAME, temperature=0.1 , base_url= OLAMMA_BASE_URL)

    chain = prompt_template | model

    # Invoke the chain with the Component_id parameter
    response = chain.invoke({"question": question})   

    print(response)

    pattern = r'<answer>\s*(.*?)\s*</answer>'


    # Find all matches
    matches = re.findall(pattern, response, re.DOTALL)  # re.DOTALL allows . to match newlines


    # Print the matched content
    for match in matches:
        print(match)
        execute_query_for_knowledge_graph_helper(match)
   
    
    return True
   
    
    return True
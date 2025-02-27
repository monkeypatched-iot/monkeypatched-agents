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

entities = """
        ComponentDetails:
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

        ComponentInventory:
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

        ComponentPricing:
                part_id
                unit_price
                total_price
                discount
                net_price
                tax_rate
                tax_amount
                final_price

        SupplierDetails:
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

        SupplierCapabilities:
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

        SupplierCertifications:
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

        SupplierLocation:
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

        SupplierQuality:
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

        SupplierShipping:
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

        OrderDetails:
                order_id
                order_date
                order_status
                order_type
                priority_level
                shipping_method
                payment_method

        OrderMetadata:
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

        OrderMetrics:
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

        OrderPayment:
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

        OrderShipping:
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

        CustomerDetails:
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

        CustomerMetadata:
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

        CustomerOrderMetrics:
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

        CustomerPaymentData:
                customer_id
                payment_terms
                tax_identification_number
                credit_limit
                payment_method
                currency

        ProductInventory:
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

        ProductMetadata:
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

        ProductPricing:
                product_id
                base_price
                discount_rate
                tax_rate
                currency
                effective_price
"""

relationships = """ 

     CustomerDetails
        HAS_A → CustomerMetadata
        HAS_A → CustomerOrderMetrics
        HAS_A → CustomerPaymentData
        HAS_MANY → OrderDetails

     OrderDetails
        HAS_A → OrderMetrics
        HAS_A → OrderPayment
        HAS_A → OrderShipping

   
"""

def ask_question_from_knowledge_graph_helper(question):
    prompt_template = PromptTemplate(
        input_variables=["entities", "relationships", "question"],
        template="""
                Instruction: you are a tool to create a cypher queries given the nodes in a neo4j graph database and the relationship between them
                the entities for the neo4j schema are defined as {entities}
                and the relationships are defined as {relationships}
                you are to convert questions asked to cypher queries that are compatible with neo4j
                do not make any assumptions about the data strictly use the text above   
                strictly use the entity names and field names as provided in the entities
                think step by step how you will generate the query to answer the question asked given the above entities and relationships
                do not make any assumptions 
                do not generate a sql query  
                and answer the given {question} only
                for customer use customer_id as id
                do not add  new line charachter in the query
                please respond without using any newline characters (\n)
                follow the below steps to consturct the query 
                   if looking for information about the customer start with the CustomerDetails
                   if not found in CustomerDetails look in CustomerMetadata

                   look for industry type in CustomerDetails
                   look for company size in CustomerDetails
                   look for job title in CustomerDetails
                   look for preferred communication method in CustomerDetails
                   look for billing address in CustomerDetails
                   look for company name in CustomerDetails
                   look for phone number in CustomerDetails

                   look for the account manager in CustomerMetadata
                   look for the account status in CustomerMetadata
                   look for the warranty information in CustomerMetadata
                   look for the lead time in CustomerMetadata
                   do not rename lead_time to product_lead_time
                   look for preferred shipping method ins CustomerMetadata

                   when getting payment information make sure that a HAS_A relationship exists between CustomerDetails and CustomerPaymentData
                   look for currency in CustomerPaymentData
                   look for payment terms in CustomerPaymentData
                   for credit limit look in the CustomerPaymentData

                   when getting customer order metrics information make sure that a HAS_A relationship exists between CustomerDetails and CustomerOrderMetrics
                   look for the average order value in the CustomerOrderMetrics
                   look for the backorder rate in the CustomerOrderMetrics
                   look for cost to serve per order in CustomerOrderMetrics
                   look for customer lifetime value in CustomerOrderMetrics
                   look for customer retention rate in CustomerOrderMetrics
                   look for customer satisfaction rate CustomerOrderMetrics
                   look for first time fill rate in CustomerOrderMetrics
                   look for gross profit margin in CustomerOrderMetrics
                   look for inventory turnover ratio in CustomerOrderMetrics
                   look for late order rate in CustomerOrderMetrics
                   look for order accuracy rate in CustomerOrderMetrics
                   look for order cycle time in CustomerOrderMetrics
                   look for order fill rate in CustomerOrderMetrics
                   look for order margin per unit in CustomerOrderMetrics
                   look for order processing in CustomerOrderMetrics
                   look for order profitability index in CustomerOrderMetrics
                   look for perfect order rate	in CustomerOrderMetrics
                   look for profit per order in CustomerOrderMetrics
                   look for return on fulfillment cost in CustomerOrderMetrics
                   look for return rate	in CustomerOrderMetrics	
                   look for revenue per order in CustomerOrderMetrics
                   look for on time delivery rate in CustomerOrderMetrics

                   when answering questions about order details where order id is known use the OrderDetails where the CustomerDetails HAS_MANY OrderDetails
                   look for order status in OrderDetails
                   look for order type in OrderDetails and return the order type only
                   look for priority level in OrderDetails and return the order type only
                 
                   when answering questions about order payment where the order id is known use the OrderPayment where the OrderDetails HAS_A OrderPayment
                   if asked about order payment due date use order_payment_due_date
                   look for credit limit utilization in OrderPayment
                   look for customer payment history in OrderPayment strictly
                   look for early payment discount in OrderPayment strictly
                   look for late payment penalty in OrderPayment strictly
                   look for the order payment due date in OrderPayment strictly
                   look for the order payment status in OrderPayment strictly
                   look for outstanding payment amount in OrderPayment
                   look for payment amount in OrderPayment
                   look for payment approval status in OrderPayment
                   look for payment dispute status in OrderPayment
                   look for payment method in OrderPayment
                   look for payment overdue amount in OrderPayment
                   look for payment processing time in OrderPayment
                   look for payment recieved date in OrderPayment
                   look for payment risk rating in OrderPayment

                   validate and correct the generated cypher query
                   the arrow (`→`) symbol should be replaced with the correct relationship notation `-[]->`.
                
                Return the response in the below response Format exactly:  
                      <answer>cypher query</answer>

                Examples: Here are a few examples of generated Cypher statements for particular questions:

                # Question: Hi monkeypatched who is the account manager for customer with id CUST12345?
                # Answer: MATCH (customer:CustomerDetails)-[:HAS_A]->(metadata:CustomerMetadata) WHERE customer.customer_id = 'CUST12345' RETURN metadata.account_manager

                # Question: Hi monkeypatched what is the preffered shipping method for customer with id CUST12345 ?
                # Answer: MATCH (customer:CustomerDetails)-[:HAS_A]->(metadata:CustomerMetadata) WHERE customer.customer_id = 'CUST12345' RETURN metadata.account_manager

                # Question: Hi monkeypatched what is the company size for customer with id CUST12345 ?
                # Answer: MATCH (customer:CustomerDetails) WHERE customer.customer_id = 'CUST12345' RETURN customer.company_size

                # Question: Hi monkeypatched what is the company name for customer with id CUST12345 ?
                # Answer: MATCH (customer:CustomerDetails) WHERE customer.customer_id = 'CUST12345' RETURN customer.company_name

                # Question: Hi monkeypatched what is the email address for Jhon Doe ?
                # Answer: MATCH (c:CustomerDetails) WHERE c.contact_name = 'Jhon Doe' RETURN c.email_address

                # Question: Hi monkeypatched what is the mobile number for customer with id CUST12345 ?
                # Answer: MATCH (c:CustomerDetails) WHERE  c.customer_id ='CUST12345' RETURN c.mobile_number

                # Question: Hi monkeypatched what is the phone number for customer with id CUST12345 ?
                # Answer: MATCH (c:CustomerDetails) WHERE  c.customer_id ='CUST12345' RETURN c.phone_number

                # Question: Hi monkeypatched what are the notes comments for customer with id CUST12345 ?
                # Answer: MATCH (customer:CustomerDetails)-[:HAS_A]->(metadata:CustomerMetadata) WHERE customer.customer_id = 'CUST12345' RETURN m.notes_comments

                # Question: hi monkeypatched what orders do we have for customer with id CUST12345 ?
                # Answer: MATCH (customer:CustomerDetails)-[:HAS_MANY]->(order:OrderDetails) WHERE customer.customer_id = 'CUST12345' RETURN order.order_id

                # Question: hi monkeypatched what special requirements do do we have for customer with id CUST12345 ?
                # Answer: MATCH (customer:CustomerDetails)-[:HAS_A]->(metadata:CustomerMetadata) WHERE customer.customer_id = 'CUST12345' RETURN m.special_Requirements

                # Question: hi monkeypatched what are the payment terms for customer with customer id CUST12345
                # Answer: MATCH (customer:CustomerDetails)-[:HAS_A]->(metadata:CustomerMetadata) WHERE customer.customer_id = 'CUST12345' RETURN m.special_Requirements

                # Question: hi monkeypatched what is the credit limit utilization for order with id ORD98765
                # Answer: MATCH (o:OrderDetails)-[:HAS_A]->(p:OrderPayment) WHERE o.order_id = 'ORD98765' RETURN p.credit_limit_utilization

                # Question: hi monkeypatched what is the customer order history for order with id ORD98765
                # Answer: MATCH (o:OrderDetails)-[:HAS_A]->(p:OrderPayment) WHERE o.order_id = 'ORD98765' RETURN p.customer_order_history

                # Question: hi monkeypatched what is the order payment status for order with id ORD98765
                # Answer: MATCH (o:OrderDetails)-[:HAS_A]->(p:OrderPayment) WHERE o.order_id = 'ORD98765' RETURN p.order_payment_status
                
                # Question: hi monkeypatched what is the customer segment for order with id ORD98765
                # Answer : MATCH (o:OrderDetails)-[:HAS_A]->(m:OrderMetadata) WHERE o.order_id = 'ORD98765' RETURN m.customer_segment

                # Question: hi monkeypatched what is the customs declaration id for order with id ORD98765
                # Answer : MATCH (o:OrderDetails)-[:HAS_A]->(m:OrderMetadata) WHERE o.order_id = 'ORD98765' RETURN m.customs_declaration_id

                # Question: hi monkeypatched what is discount applied for order with id ORD98765
                # Answer : MATCH (o:OrderDetails)-[:HAS_A]->(m:OrderMetadata) WHERE o.order_id = 'ORD98765' RETURN m.discount_applied
        
        """
    )

    model = OllamaLLM(model=MODEL_NAME, temperature=0.3, base_url=OLAMMA_BASE_URL)
    chain = prompt_template | model

    # Invoke the chain with the Component_id parameter
    try:
        response = chain.invoke({"entities": entities, "relationships": relationships, "question": question})
    except Exception as e:
        print(e)

    print(response)

    pattern = r'<answer>\s*(.*?)\s*</answer>'

    # Find all matches
    matches = re.findall(pattern, response, re.DOTALL)  # re.DOTALL allows . to match newlines

    if len(matches) == 0:
        pattern = r'cypher\n([\s\S]*?)\n'
        matches = re.findall(pattern, response, re.DOTALL)  # re.DOTALL allows . to match newlines

    # Print the matched content
    for match in matches:
        print(match)
        execute_query_for_knowledge_graph_helper(match, question)


    return True

prompt = """
  Task:Generate Cypher statement to query a graph database.
  Instructions:
  Use only the provided relationship types and properties in the schema.
  Do not use any other relationship types or properties that are not provided.
  Do not add new line charachter in the query
  Never generate SQL query
  Do not make any assumptions 
  Do not use uid in the queries
  Do not replace the lot number with batch number
  STRICTLY Look for the given field in the node that contains the field only for example industry type in CustomerDetails DO NOT look in CustomerMetdata especially for CUST-1
  STRICLY look in pricing if thhe question is about product pricing
  STRICTLY use the product nodes if the product id is given
  STRICTLY use the component nodes if the component id is given
  STRICTLY Do not make any assumptions if a field is in ComponentDetails do not use ComponentMetadata or any other node

  Schema Details (ESCAPED):
  CustomerDetails: {{customer_id,company_size,job_title,phone_number,industry_type,billing_address,company_name,contact_name,email_address,mobile_number,preferred_communication_method,shipping_address}}
  CustomerMetadata: {{customer_id,account_manager,account_status,customer_since,lead_time,notes_comments,preferred_shipping_method,region,shipping_contact_name,shipping_contact_number,social_media_handles,special_requirements,support_contact,warranty_information}}
  CustomerPaymentData: {{customer_id,credit_limit,currency,payment_method,payment_terms,tax_identification_number}}
  CustomerOrderMetrics: {{customer_id,average_order_value,backorder_rate,cost_of_goods_sold,cost_to_serve_per_order,customer_lifetime_value,customer_retention_rate,customer_satisfaction_score,first_time_fill_rate,gross_profit_margin,inventory_turnover_ratio,late_order_rate,on_time_delivery_rate,order_accuracy_rate,order_cycle_time,order_fill_rate,order_margin_per_unit,order_processing_time,order_profitability_index,perfect_order_rate,profit_per_order,return_on_fulfillment_cost,return_rate,revenue_per_order}}
  OrderDetails: {{order_date,order_id,order_status,order_type,payment_method,priority_level,shipping_method}}
  OrderMetadata: {{order_id,commission_amount,commission_rate,customer_segment,customs_declaration_id,discount_applied,net_sales_value,promo_code_used,promo_code_value,refund_amount,sales_channel,sales_region,salesperson,shipping_charges,tax_amount,total_revenue,total_sales_value,upsell_or_cross_sell}}
  OrderPayment: {{order_id,credit_limit_utilization,customer_payment_history,early_payment_discount,late_payment_penalty,order_payment_due_date,order_payment_status,outstanding_payment_amount,payment_amount,payment_approval_status,payment_dispute_status,payment_method,payment_overdue_amount,payment_processing_time,payment_received_date,payment_risk_rating,payment_terms}}
  OrderShipping: {{order_id,carrier_name,expected_delivery_date,insurance_details,remarks,shipment_status,shipping_address,shipping_cost,shipping_date,shipping_id,shipping_method,tracking_number,weight}}
  ProductDetails: {{product_id,product_name,product_price,product_type,product_category,product_description,product_dimensions,product_features,safety_features,manufacturer,material_composition,power_requirements,color_options,environmental_impact,weight}}
  ProductMetadata: {{product_id,batch_number,ce_certification,customer_order_reference,expiration_date,hsn_number,lot_number,manufacturing_location,maximum_production_capacity,minimum_production_capacity,part_number,product_certifications,product_lead_time,product_lifecycle_stage,product_testing_date,product_testing_results,product_warranty_coverage,production_date,quality_control_batch,release_date,return_exchange_reference,return_rate_for_product,serial_number,shipment_tracking_number}}
  ProductPricing: {{product_id,base_price,currency,discount_rate,effective_price,tax_rate}}
  ProductInventory: {{product_id,available_stock,backorder_allowed,demand_forecast_accuracy,economic_order_quantity,inventory_turnover,reorder_level,reorder_point,safety_stock_level,stockout_rate}}
  ComponentDetails:{{part_id,part_name,part_number,part_type,part_category,part_description,material_composition,part_dimensions,weight,unit_of_measure,part_customization,part_lifecycle_status,part_testing_date,part_testing_results,part_warranty,quality_control_batch,batch_number,hsn_code}}
  ComponentPricing: {{part_id,unit_price,total_price,discount,net_price,tax_rate,tax_amount,final_price}}
  ComponentInventory: {{part_id,available_stock,backorder_allowed,demand_forecast_accuracy,economic_order_quantity,inventory_turnover,reorder_level,reorder_point,safety_stock_level,stockout_rate}}
  ComponentMetadata: {{part_id,certification_details,environmental_rating,last_updated,material_origin,production_batch_id,remarks,warranty_terms}}
  Relationships: 
  - (CustomerDetails)-[:HAS_A]->(CustomerMetadata)
  - (CustomerDetails)-[:HAS_A]->(CustomerPaymentData)
  - (CustomerDetails)-[:HAS_A]->(CustomerOrderMetrics)
  - (CustomerDetails)-[:HAS_MANY]->(OrderDetails)
  - (OrderDetails)-[:HAS_A]->(OrderMetadata)
  - (OrderDetails)-[:HAS_A]->(OrderPayment)
  - (OrderDetails)-[:HAS_A]->(OrderShipping)
  - (OrderDetails)-[:HAS_MANY]->(ProductDetails)
  - (ProductDetails)-[:HAS_A]->(ProductMetadata)
  - (ProductDetails)-[:HAS_A]->(ProductPricing)
  - (ProductDetails)-[:HAS_A]->(ProductInventory)
  - (ProductDetails)-[:HAS_A]->(ComponentDetails)
  - (ComponentDetails)-[:HAS_A]->(ComponentPricing)
  - (ComponentDetails)-[:HAS_A]->(ComponentInventory)
  - (ComponentDetails)-[:HAS_A]->(ComponentMetadata)

  Note: Do not include any explanations or apologies in your responses.
  Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
  Do not include any text except the generated Cypher statement.
  If asked about component id use the part id
  Return the response in the below response Format exactly:  
    <answer>cypher query</answer>

  The question is:
  {question}

  Examples:
  # Question: Company size for CUST-1?
  <answer>MATCH (c:CustomerDetails) WHERE c.customer_id = 'CUST' RETURN c.company_size</answer>

  # Question: what is the industry type for CUST-1?
  <answer>MATCH (c:CustomerDetails) WHERE c.customer_id = 'CUST-1' RETURN c.industry_type</answer>

  # Question:  account manager for customer with id CUST-1?
  <answer>MATCH (customer:CustomerDetails)-[:HAS_A]->(metadata:CustomerMetadata) WHERE customer.customer_id = 'CUST-1' RETURN metadata.account_manager</answer>

  # Question: customer with id CUST-1 has been a customer since?
  <answer>MATCH (customer:CustomerDetails)-[:HAS_A]->(metadata:CustomerMetadata) WHERE customer.customer_id = 'CUST-1' RETURN metadata.customer_since</answer>

  # Question: credit limit for CUST-1?
  <answer>MATCH (c:CustomerDetails)-[:HAS_A]->(p:CustomerPaymentData) WHERE c.customer_id = 'ORD98765' RETURN p.credit_limit</answer>

  # Question: average order value for CUST-1?
  <answer>MATCH (c:CustomerDetails)-[:HAS_A]->(o:CustomerOrderMetrics) WHERE c.customer_id = 'CUST-1' RETURN o.average_order_value</answer>

  # Question: order status for order ORD98765
  <answer>MATCH (order:OrderDetails) WHERE order.order_id = 'ORD98765' RETURN order.order_status</answer>

  # Question: batch number for product
  <answer>MATCH (p:ProductDetails)-[:HAS_A]->(m:ProductMetadata) WHERE p.product_id = 'PRODUCT_ID' RETURN m.batch_number</answer>

  # Question: get lotnumber of product
  <answer>MATCH (p:ProductDetails)-[:HAS_A]->(m:ProductMetadata) WHERE p.product_id = 'PRODUCT_ID' RETURN m.lot_number</answer>

  # Question: what is the product testing result for product with id PRD-001
  <answer>MATCH (p:ProductDetails)-[:HAS_A]->(m:ProductMetadata) WHERE p.product_id = 'PRD-001' RETURN m.product_testing_results</answer>

  # Question: what is the product warranty coverage for product with id PRD-001
  <answer>MATCH (p:ProductDetails)-[:HAS_A]->(m:ProductMetadata) WHERE p.product_id = 'PRD-001' RETURN m.product_warranty_coverage</answer>
  
  # Question: what is the product warranty coverage for product with id PRD-001
  <answer>MATCH (p:ProductDetails)-[:HAS_A]->(m:ProductMetadata) WHERE p.product_id = 'PRD-001' RETURN m.product_warranty_coverage</answer>

  # Question: what is the discount rate for PRD-001
  <answer>MATCH (p:ProductDetails)-[:HAS_A]->(pr:ProductPricing) WHERE p.product_id = 'PRD-001' RETURN pr.discount_rate</answer>

  # Question: is backorder allowed for product 
  <answer>MATCH (p:ProductDetails)-[:HAS_A]->(i:ProductInventory) WHERE p.product_id = 'PRD-001' RETURN i.backorder_allowed</answer>

  # Question: is the name of the component with id
  <answer>MATCH (p:ComponentDetails) WHERE p.part_id = 'PRT-002' RETURN p.part_name</answer>

  # Question: the material composition for component with id PRT-001 ?
  <answer>MATCH (p:ProductDetails) WHERE p.product_id = 'PRT-001' RETURN p.material_composition</answer>

  # Question: what is the part lifecycle status for component ?
  <answer>MATCH (pp:ComponentDetails) WHERE pp.part_id = 'PRT-001' RETURN pp.part_lifecycle_status</answer>

  # Question: what is the part testing results for component ?
  <answer>MATCH (pp:ComponentDetails) WHERE pp.part_id = 'PRT-001' RETURN pp.part_testing_results</answer>

  # Question: get the part warranty for component ?
  <answer>MATCH (p:ComponentDetails) WHERE p.part_id = 'PART_ID' RETURN p.part_warranty</answer>

"""

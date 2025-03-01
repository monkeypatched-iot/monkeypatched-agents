prompt = """
  Task:Generate Cypher statement to query a graph database.
  Instructions:
  Use only the provided relationship types and properties in the schema.
  Do not use any other relationship types or properties that are not provided.
  Do not add new line charachter in the query
  Never generate SQL query
  Do not make any assumptions 
  STRICTLY Look for the given field in the node that contains the field only for example industry type in CustomerDetails DO NOT look in CustomerMetdata

  Schema Details (ESCAPED):
  CustomerDetails: {{customer_id,company_size,job_title,phone_number,industry_type,billing_address,company_name,contact_name,email_address,mobile_number,preferred_communication_method,shipping_address,uid}}
  CustomerMetadata: {{customer_id,account_manager,account_status,customer_since,lead_time,notes_comments,preferred_shipping_method,region,shipping_contact_name,shipping_contact_number,social_media_handles,special_requirements,support_contact,warranty_information}}
  CustomerPaymentData: {{customer_id,credit_limit,currency,payment_method,payment_terms,tax_identification_number}}
  CustomerOrderMetrics: {{customer_id,average_order_value,backorder_rate,cost_of_goods_sold,cost_to_serve_per_order,customer_lifetime_value,customer_retention_rate,customer_satisfaction_score,first_time_fill_rate,gross_profit_margin,inventory_turnover_ratio,late_order_rate,on_time_delivery_rate,order_accuracy_rate,order_cycle_time,order_fill_rate,order_margin_per_unit,order_processing_time,order_profitability_index,perfect_order_rate,profit_per_order,return_on_fulfillment_cost,return_rate,revenue_per_order}}
  OrderDetails: {{order_date,order_id,order_status,order_type,payment_method,priority_level,shipping_method}}
  OrderMetadata: {{order_id,commission_amount,commission_rate,customer_segment,customs_declaration_id,discount_applied,net_sales_value,promo_code_used,promo_code_value,refund_amount,sales_channel,sales_region,salesperson,shipping_charges,tax_amount,total_revenue,total_sales_value,upsell_or_cross_sell}}
  OrderPayment: {{order_id,credit_limit_utilization,customer_payment_history,early_payment_discount,late_payment_penalty,order_payment_due_date,order_payment_status,outstanding_payment_amount,payment_amount,payment_approval_status,payment_dispute_status,payment_method,payment_overdue_amount,payment_processing_time,payment_received_date,payment_risk_rating,payment_terms}}
  OrderShipping: {{order_id,carrier_name,expected_delivery_date,insurance_details,remarks,shipment_status,shipping_address,shipping_cost,shipping_date,shipping_id,shipping_method,tracking_number,weight}}
  Relationships: 
  - (CustomerDetails)-[:HAS_A]->(CustomerMetadata)
  - (CustomerDetails)-[:HAS_A]->(CustomerPaymentData)
  - (CustomerDetails)-[:HAS_A]->(CustomerOrderMetrics)
  - (CustomerDetails)-[:HAS_MANY]->(OrderDetails)
  - (OrderDetails)-[:HAS_A]->(OrderMetadata)
  - (OrderDetails)-[:HAS_A]->(OrderPayment)
  - (OrderDetails)-[:HAS_A]->(OrderShipping)
  
  Note: Do not include any explanations or apologies in your responses.
  Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
  Do not include any text except the generated Cypher statement.


  Return the response in the below response Format exactly:  
    <answer>cypher query</answer>

  The question is:
  {question}

  Examples:
  # Question: Company size for CUST12345?
  <answer>MATCH (c:CustomerDetails) WHERE c.customer_id = 'CUST12345' RETURN c.company_size</answer>

  # Question:  account manager for customer with id CUST12345?
  <answer>MATCH (customer:CustomerDetails)-[:HAS_A]->(metadata:CustomerMetadata) WHERE customer.customer_id = 'CUST12345' RETURN metadata.account_manager</answer>

  # Question: customer with id CUST12345 has been a customer since?
  <answer>MATCH (customer:CustomerDetails)-[:HAS_A]->(metadata:CustomerMetadata) WHERE customer.customer_id = 'CUST12345' RETURN metadata.customer_since</answer>

  # Question: credit limit for CUST12345?
  <answer>MATCH (c:CustomerDetails)-[:HAS_A]->(p:CustomerPaymentData) WHERE c.customer_id = 'ORD98765' RETURN p.credit_limit</answer>

  # Question: average order value for CUST12345?
  <answer>MATCH (c:CustomerDetails)-[:HAS_A]->(o:CustomerOrderMetrics) WHERE c.customer_id = 'CUST12345' RETURN o.average_order_value</answer>

  # Question: order status for orde ORD98765
  <answer>MATCH (order:OrderDetails) WHERE order.order_id = 'ORD98765' RETURN order.order_status</answer>

"""

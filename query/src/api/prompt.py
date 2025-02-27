prompt = """
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

                follow the below steps to construct the query 
                   
                the following fieds are in the CustomerDetails
                   look for industry type in CustomerDetails
                   look for company size in CustomerDetails
                   look for job title in CustomerDetails
                   look for preferred communication method in CustomerDetails
                   look for billing address in CustomerDetails
                   look for company name in CustomerDetails
                   look for phone number in CustomerDetails

                the following fieds are in the CustomerMetadata where CustomerDetails HAS_A CustomerMetadata
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

                   validate and correct the generated cypher query
                   the arrow (`→`) symbol should be replaced with the correct relationship notation `-[]->`.
                

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

                # Question: hi monkeypatched what are the payment terms for customer with customer id CUST12345
                # Answer: MATCH (customer:CustomerDetails)-[:HAS_A]->(metadata:CustomerMetadata) WHERE customer.customer_id = 'CUST12345' RETURN m.payment_terms

            Return the response in the below response Format exactly:  
                <answer>cypher query</answer>
        """

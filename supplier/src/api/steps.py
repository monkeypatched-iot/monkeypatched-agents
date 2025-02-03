from fastapi import FastAPI
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import re
import json
import logging
from src.utils.invoker import invoke
from neomodel import db

def create_supplier_nodes_in_knowledge_graph_helper(supplier_id,location_id,item_id):
    prompt_template = PromptTemplate(input_variables=["parameters"], template="""
        Human: 
        You are a system that aggregates data from multiple APIs and constructs a knowledge graph based on the retrieved information. To accomplish this, follow the steps outlined below:

        Steps:

        1️. Retrieve Supplier Details  
        - **Step:** 1  
        - **Action:** GetSupplierDetails (parameters: {parameters})
                                    
        2. Retrieve Supplier Locations  
        - **Step:** 2  
        - **Action:** GetSupplierLocations (parameters: {parameters})

        3. Retrieve Supplier Inventory  
        - **Step:** 3  
        - **Action:** GetSupplierInventory (parameters: {parameters})

        4. Retrieve Supplier Pricing
        - **Step:** 4  
        - **Action:** GetSupplierPricing (parameters: {parameters})
                                    
        5. Retrieve Supplier Finance
        - **Step:** 5  
        - **Action:** GetSupplierFinance (parameters: {parameters})

        6. Retrieve Supplier Capabilities  
        - **Step:** 6  
        - **Action:** GetSupplierCapabilities (parameters: {parameters})
                                    
        7. Retrieve Supplier Certifications  
        - **Step:** 7  
        - **Action:** GetSupplierCertifications (parameters: {parameters})
                                    
        8. Retrieve Supplier Quality  
        - **Step:** 8  
        - **Action:** GetSupplierQuality (parameters: {parameters})
                                    
        9. Retrieve Supplier Shipping 
        - **Step:** 9  
        - **Action:** GetSupplierShipping (parameters: {parameters})                      
                                        
        10. Add Supplier
        - **Step:** 10
        - **Action:** AddSupplier (parameters: {parameters}) 
                                        

        Response Format:  
        For each step, return the response in the exact format below:
                                            
        step: [Step Number]  
        action: [Action Name] 
        parameters: {parameters}
            
                                    
        Guidelines:  
        - Execute step by step use only the steps given above
        - Ensure each step is clearly labeled with "step:" and "action:" and "paramaters".
        - do not add any other keys other than step,action and parameters to parameters
        - do not change the action names
        - return answer as json string                                          
        - Maintain the given response structure for consistency.  
        - Execute the steps sequentially.
        - maintain the order of the steps
        - do not add response
        - ignore first line
                                                                                    
        """)

    model = OllamaLLM(model="deepseek-r1:1.5b",temperature=0.0)

    chain = LLMChain(prompt=prompt_template, llm=model)

    #pass all params hereS
    parameters_json = json.dumps({"supplier_id": supplier_id,"location_id":location_id,"item_id":item_id})

    query = {"parameters": parameters_json}

    # Invoke the chain with the Supplier_id parameter
    response = chain.run(query)   

    print(response)

    # Improved regex to correctly match standalone JSON objects
    pattern = re.compile(r"\{(?:[^{}]|(?:\{[^{}]*\}))*\}", re.DOTALL)

    # Extract valid JSON objects
    matches = pattern.findall(response)

    # Convert extracted matches into proper JSON format
    steps= []
    for match in matches:
        try:
            # Stripping unnecessary newlines or spaces
            cleaned_match = match.strip()

            steps.append(json.loads(cleaned_match))

        except json.JSONDecodeError as e:
                print(f"JSON Decode Error: {e}\nProblematic JSON:\n{cleaned_match}")

    for step in steps:
        print(step)
        if "parameters" in step.keys() and "action" in step.keys():
            
                # get the parameters
                arguments = step["parameters"]

                # get the functions
                function_name = step["action"]
                            
                # If the arguments are a dictionary, pass them as keyword arguments
                if isinstance(arguments, dict):
                    result = invoke(function_name, **arguments)
                if isinstance(arguments, str):
                    result = invoke(function_name, arguments)
                else:
                    # Otherwise pass them as positional arguments
                    result = invoke(function_name, *arguments)
                        

def delete_orphan_nodes():
    try:
        # Run the query to match nodes with no relationships
        query = """
        MATCH (n)
        WHERE NOT (n)-[]-()
        DELETE n
        """
        # Execute the query via the Neo4j connection
        db.cypher_query(query, {})
        print("Orphan nodes deleted successfully.")
    except Exception as e:
        print(f"Error occurred: {e}")
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from pydantic import BaseModel
import re
import json
import logging
from src.utils.invoker import invoke

logging.basicConfig(level=logging.INFO)

app = FastAPI()



# @app.get("/v1/customer/metadata/{customer_id}")
def create_customer_nodes_in_knowledge_graph_helper(customer_id:str):

    prompt_template = PromptTemplate(input_variables=["parameters"], template="""
    YHuman: 
    You are a system that aggregates data from multiple APIs and constructs a knowledge graph based on the retrieved information. To accomplish this, follow the steps outlined below:

    Steps:

    1️. Retrieve Customer Details  
    - **Step:** 1  
    - **Action:** GetCustomerDetails (parameters: {parameters})

    2️. Retrieve Customer Metadata  
    - **Step:** 2  
    - **Action:** GetCustomerMetadata (parameters: {parameters})

    3️. Retrieve Customer Retention & Satisfaction Metrics  
    - **Step:** 3  
    - **Action:** GetCustomerMetrics (parameters: {parameters})

    4️. Retrieve Customer Payment Information  
    - **Step:** 4  
    - **Action:** GetCustomerPaymentInformation (parameters: {parameters}) 

    Response Format:  
    For each step, return the response in the exact format below:
                                        
    step: [Step Number]  
    action: [Action Name] 
    parameters: {parameters}

    Guidelines:  
    - Ensure each step is clearly labeled with "step:" and "action:" and "paramaters".
    - return answer as json string                                          
    - Maintain the given response structure for consistency.  
    - Execute the steps sequentially.
    - Always return the same response
                                                                                
    """)

    model = OllamaLLM(model="deepseek-r1:1.5b",temperature=0.0)

    chain = LLMChain(prompt=prompt_template, llm=model)
    #pass all params hereS
    parameters_json = json.dumps({"customer_id": customer_id})

    query = {"parameters": parameters_json}

    # Invoke the chain with the customer_id parameter
    response = chain.run(query)

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
        if "parameters" in step.keys():
        
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
                    
        else:
            # Call function without parameters
            function_name = step["action"]
            result = invoke(function_name)
            logging.info(f"Result from invoking {function_name} without parameters: {result}")
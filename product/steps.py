import re
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langchain.chains import LLMChain
import json
from neomodel import db

from src.utils.invoker import invoke
from src.utils.logger import logging

prompt_template = PromptTemplate(input_variables=["parameters"], template="""
    Human: 
    You are a system that aggregates data from multiple APIs and constructs a knowledge graph based on the retrieved information. To accomplish this, follow the steps outlined below:

    Steps:

    1️. Retrieve Product Details  
    - **Step:** 1  
    - **Action:** GetProductDetails (parameters: {parameters})

    2️. Retrieve Product Metadata  
    - **Step:** 2  
    - **Action:** GetProductMetadata (parameters: {parameters})

    3️. Retrieve Product Inventory 
    - **Step:** 3  
    - **Action:** GetProductInventory (parameters: {parameters})

    4️. Retrieve Product Pricing 
    - **Step:** 4  
    - **Action:** GetProductPricing (parameters: {parameters}) 
                                     
    5. Add a Product
    - **Step:** 5 
    - **Action:** AddProduct (parameters: {parameters}) 

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
    - Do not add extra parameters 
                                                                                
    """)

model = OllamaLLM(model="deepseek-r1:1.5b",temperature=0.0)

chain = LLMChain(prompt=prompt_template, llm=model)
    
#pass all params hereS
parameters_json = json.dumps({"product_id": "PRD12345","location_id":"LOC12345"})

query = {"parameters": parameters_json}

# Invoke the chain with the customer_id parameter
response = chain.run(query)

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
    if 'parameters' in step.keys():
        print(step)

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
        print(step)
        # function_name = step["action"]
        # result = invoke(function_name)
        logging.info(f"Result from invoking {function_name} without parameters: {result}")

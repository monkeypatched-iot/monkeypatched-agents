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
from src.utils.invoker import invoke

load_dotenv()  # Load variables from .env

logging.basicConfig(level=logging.INFO)

OLAMMA_BASE_URL = os.getenv("OLAMMA_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")


def create_inventory_nodes_in_knowledge_graph_helper(component_id,supplier_id):
   
    prompt_template = PromptTemplate(input_variables=["parameters"], template="""
        Human: 
        You are a system that aggregates data from multiple APIs and constructs a knowledge graph based on the retrieved information. To accomplish this, follow the steps outlined below:

        Steps:

        1️. Get the Component Inventory 
        - **Step:** 1  
        - **Action:** GetComponentInventory (parameters: {parameters})

        2️. Retrieve Component Inventory Metadata
        - **Step:** 2  
        - **Action:** GetComponentInventoryMetadata (parameters: {parameters})

        3. Retrieve Add Inventory  
        - **Step:** 3  
        - **Action:** AddComponentInventory (parameters: {parameters}) 
                                        
        4. Send A notification
        - **Step:** 4 
        - **Action:** AddInventoryNotification (parameters: {parameters}) 

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
        - do not change the action names
        - please return a json strictly
        - do not add extra lines 
        - return all steps
                                                                                                             
        """)
    
    # Initialize Ollama model
    model = OllamaLLM(model=MODEL_NAME, temperature=0.0 , base_url= OLAMMA_BASE_URL)


    chain = prompt_template | model
    #pass all params hereS
    parameters_json = json.dumps({"component_id": component_id,"supplier_id":supplier_id})

    query = {"parameters": parameters_json}

    # Invoke the chain with the Component_id parameter
    response = chain.invoke(query)   

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
        if "parameters" in step.keys() and "component_id" not in step.keys():
            
                # get the parameters
                arguments = step["parameters"]

                # get the functions
                function_name = step["action"].replace(" ", "")
                            
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
                print("Action key is missing!")

# executes the cypher query and returns the reult back to chatbot

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import re
import json
import logging
from src.utils.invoker import invoke
from neomodel import db

load_dotenv()  # Load variables from .env

logging.basicConfig(level=logging.INFO)

OLAMMA_BASE_URL = os.getenv("OLAMMA_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

def execute_query_for_knowledge_graph_helper(query,question):

    prompt_template = PromptTemplate(input_variables=["parameters"], template="""
        system: 
        You are a system that aggregates data from multiple APIs and constructs a knowledge graph based on the retrieved information. To accomplish this, follow the steps outlined below:

     
            ### Steps:

            1️ **Execute Query**
            - **Step:** 1  
            - **Action:** ExecuteQuery  
            - **Parameters:** {parameters}  

        Response Format:  
        For each step, return the response as a json in the exact format below:
                                            
        step: [Step Number]  
        action: [Action Name] 
        parameters: {parameters}
                                     
        Guidelines:  
        - Ensure each step is clearly labeled with "step:" and "action:" and "paramaters".
        - STRICTLY return answer as json string                                          
        - Maintain the given response structure for consistency.  
        - Execute the steps sequentially.
        - Always return the same response
        - do not change the action names
        - execute all steps in order 
        - do not make any assumptions
        
                                                                                    
        """)
    
    # Initialize Ollama model
    model = OllamaLLM(model=MODEL_NAME, temperature=0.0 , base_url= OLAMMA_BASE_URL)

    chain = prompt_template | model

    data = {"query": str(query),"question":str(question)}

    # Invoke the chain with the Component_id parameter
    response = chain.invoke(json.dumps(data))   

    print(response)

    # Improved regex to correctly match standalone JSON objects
    pattern = re.compile(r'```json(.*?)```', re.DOTALL)

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
        print(step.keys())
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

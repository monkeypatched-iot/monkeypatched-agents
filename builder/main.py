from fastapi import FastAPI
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import re
import json
import logging

from neomodel import db

prompt_template = PromptTemplate(input_variables=["parameters"], template="""
    Human: 
                                 
    1️. Connect the customer
    - **Step:** 1  
    - **Action:** ConnectCustomertoOrder (parameters: {parameters})
                                 
    2. Connect the order
    - **Step:** 2  
    - **Action:** ConnectOrderToProduct (parameters: {parameters})                       
                                 
    3. Connect the components
    - **Step:** 3  
    - **Action:** ComponentToProduct (parameters: {parameters})
                                                   
    4. Connect component to suppliers
    - **Step:** 4  
    - **Action:** ConnetComponentsToSuppliers (parameters: {parameters})
                            
    Guidelines:  
    - Execute step by step use only the steps given above
    - Ensure each step is clearly labeled with "step:" and "action:" and "paramaters".
    - do not add any other keys other than step,action and parameters to parameters
    - do not change the action names
    - do not miss any steps
    - return a as json string                                          
    - Maintain the given response structure for consistency.  
    - Execute the steps sequentially.
    - maintain the order of the steps
    - do not add response
    - ignore first line
                                                                                
    """)

model = OllamaLLM(model="deepseek-r1:1.5b",temperature=0.0)

chain = LLMChain(prompt=prompt_template, llm=model)

parameters ={
    "customer_id": "CUST12345", 
    "order_id":"ORD12345",
    "products":[
        {
            "id":"P12345",
            "qty":"1"
        }
    ]
}

query = {"parameters":parameters}

# Invoke the chain with the Supplier_id parameter
response = chain.run(query)   

print(response)

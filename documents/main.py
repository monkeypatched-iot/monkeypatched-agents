import ast
from fastapi import FastAPI, File, UploadFile
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import re
import json
from neomodel import db
from src.utils.invoker import invoke
from src.tools.requests import post_file

from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

CSV_API_BASE_URL = os.getenv("CSV_API_BASE_URL")
PDF_API_BASE_URL = os.getenv("PDF_API_BASE_URL")


app = FastAPI()

def index_given_document_helper(document_type:str,file: UploadFile = File(...)):
    prompt_template = PromptTemplate(input_variables=["parameters"], template="""
        Human: 
        You are a system that indexes the uploaded documents to the LLM. To accomplish this, follow the steps outlined below:

        Steps:

        1. Index the document  
        - **Step:** 1 
        - **Action:** IndexDocument (parameters: {parameters})

        2. Ask for Document Metadata
        - **Step:** 2 
        - **Action:** SendDocumentUploadNotification (parameters: {parameters})

     Response Format:  
        For each step, return the response in the exact format below:
                                            
        step: [Step Number]  
        action: [Action Name] 
        parameters: {parameters}
                                    
    Guidelines:  
        - Execute step by step use only the steps given above
        - Always use double quotation
        - Ensure each step is clearly labeled with "step:", "action:", and "parameters".
        - Return as JSON string 
        - Do not add any other keys other than step, action, and parameters to parameters
        - Do not change the action names
        - Do not miss any steps                                         
        - Maintain the given response structure for consistency  
        - Execute the steps sequentially.
        - Maintain the order of the steps
                                                                                    
        """)

    model = OllamaLLM(model="deepseek-r1:1.5b",temperature=0.0)

    chain = LLMChain(prompt=prompt_template, llm=model)
    #pass all params hereS
    parameters_json = json.dumps({"type": document_type,"file_name":file.filename})

    query = {"parameters": parameters_json}

    # Invoke the chain with the Order_id parameter
    response = chain.run(query)   

    print(response)

    pattern = r"action:\s*(\S+)\s*parameters:\s*(\{.*\})"

     # Find all matches in the text
    matches = re.findall(pattern, response)

    # Convert extracted matches into proper JSON format (as Python objects)
    extracted_data = []
    for match in matches:
        action = match[0]
        parameters = ast.literal_eval(match[1])  # Safely convert the string representation to a dictionary
        extracted_data.append({
            "action": action,
            "parameters": parameters
        })

    steps = extracted_data

    if len(steps) == 0 :
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
        
        # Function to delete orphan nodes
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


 
@app.post("/v1/file/upload/type/{type}/subtype/{subtype}")
async def upload_file(type:str,subtype:str,file: UploadFile = File(...)):

    if type == "csv" and subtype == "none":

        response = post_file(f"{CSV_API_BASE_URL}/v1/csv/upload",file)

        json_string = response.content.decode("utf-8")

        response_dict = json.loads(json_string)
        
        if response_dict["message"]:

            index_given_document_helper(type,file)
    
    if type == "pdf" and subtype == "document":

        response = post_file(f"{PDF_API_BASE_URL}/v1/pdf/upload/{subtype}",file)

        json_string = response.content.decode("utf-8")

        response_dict = json.loads(json_string)

        if response_dict["message"] == 'Uploaded successfully':
            
            index_given_document_helper(type,file)

    
    if type == "docx" and subtype == "word":

        response = post_file(f"{PDF_API_BASE_URL}/v1/docx/upload",file)

        json_string = response.content.decode("utf-8")

        response_dict = json.loads(json_string)

        index_given_document_helper(type,file)

    if type == "image" and subtype == "jpeg":

        response = post_file(f"{PDF_API_BASE_URL}/v1/upload/image",file)

        json_string = response.content.decode("utf-8")


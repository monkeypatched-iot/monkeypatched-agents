from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import re
import ast  # To safely convert the string representation of a dictionary to an actual dictionary

from neomodel import db
from src.vo.graph import KnowledgeGraphRequest
from src.utils.invoker import invoke

def create_knowledge_graph_helper(request: KnowledgeGraphRequest):
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
        - **Action:** ConnectComponentToProduct (parameters: {parameters})
                                                    
        4. Connect component to suppliers
        - **Step:** 4  
        - **Action:** ConnectComponentsToSuppliers (parameters: {parameters})
                                    
        5. Update the inventory
        - **Step:** 5 
        - **Action:** Notify (parameters: {parameters})


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

    # Initialize LLM
    model = OllamaLLM(model="deepseek-r1:1.5b", temperature=0.0)
    chain = LLMChain(prompt=prompt_template, llm=model)

    # Parameters
    parameters = request.dict()

    query = {"parameters": parameters}

    # Invoke the chain with the parameters
    response = chain.run(query)   
    print(response)

    # Regex pattern to extract action and parameters
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


import json
import os
import re
import logging
from dotenv import load_dotenv
from neomodel import db
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from src.api import  prompt
from src.tools.open_router import post_to_llm
from src.api.steps import execute_query_for_knowledge_graph_helper
from langchain.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Environment variables
OLAMMA_BASE_URL = os.getenv("OLAMMA_BASE_URL", "http://localhost:5000")
MODEL_NAME = os.getenv("MODEL_NAME", "default-model-name")
MODE = os.getenv("MODE", "local")

# Compile regex patterns
ANSWER_PATTERN = re.compile(r'<answer>\s*(.*?)\s*</answer>', re.DOTALL)
CYPHER_PATTERN = re.compile(r'cypher\n([\s\S]*?)\n', re.DOTALL)
ANSWER_TEXT_PATTERN = re.compile(r'\*\*Answer\*\*\s*(.*?)\s*(?=(\*\*|$))', re.DOTALL)

def extract_matches(response, patterns):
    for pattern in patterns:
        matches = pattern.findall(response)
        if matches:
            return matches
    return []

def process_response(response, question):
    matches = extract_matches(response, [ANSWER_PATTERN, CYPHER_PATTERN, ANSWER_TEXT_PATTERN])
    if matches is None:
        execute_query_for_knowledge_graph_helper(response, question)

    for match in matches:
        if isinstance(match, tuple):
            match = match[0]  # Extract the first group if the pattern uses groups
        logging.info(f"Executing match: {match}")
        execute_query_for_knowledge_graph_helper(match, question)

def handle_local_model(question, prompt_template):
    # Only proceed if 'monkeypatched' is in the question
    model = OllamaLLM(model=MODEL_NAME, temperature=0.3, base_url=OLAMMA_BASE_URL)
    if hasattr(question, 'question') and "monkeypatched" in str(question.question):
        chain = prompt_template | model
        logging.info(f"Using local model with question: {question.question}")
        return chain.invoke({"question": question.question})
    else:
        logging.info("Skipping local model due to absence of 'monkeypatched' in the question.")

        # Define the chat prompt template
        chat_prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            ("user", "{question}"),  # Placeholder for the user's question
            ("assistant", "Sure, here is the information you requested."),
        ])

        # Create a chain using the template and model
        chain = chat_prompt_template | model

        # Invoke the model with the formatted question
        response = chain.invoke({"question": question.question})

        return response


def handle_open_router(question, prompt_template):
    # Only proceed if 'monkeypatched' is in the question
    if hasattr(question, 'question') and "monkeypatched" in str(question.question):
        logging.info("Using Open Router for request")
        formatted_prompt = prompt_template.format(question=question)
        response = post_to_llm(formatted_prompt)
        return json.loads(response.content.decode('utf-8'))
    else:
        response = post_to_llm(question.question)
        return json.loads(response.content.decode('utf-8'))

def ask_question_from_knowledge_graph_helper(question):
    prompt_template = PromptTemplate(input_variables=["question"], template=prompt.prompt)
    try:
        response = None
        
        if MODE == "local":
            response = handle_local_model(question, prompt_template)
        if not response:  # If no response from local model, try Open Router
            response_data = handle_open_router(question, prompt_template)
            if response_data:
                response_text = response_data["choices"][0]["message"]["content"]
                logging.info(f"Open Router response: {response_text}")
                response = response_text
        
        if response:  # Process response if available
            process_response(response, question)
        else:
            logging.info("No response generated due to absence of 'monkeypatched' keyword.")
    
    except Exception as e:
        logging.error(f"Error occurred while processing question: {e}")



import json
import os
import re
import logging
from dotenv import load_dotenv
from neomodel import db
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from src.api import entities, relationships, prompt
from src.tools.open_router import post_to_llm
from src.api.steps import execute_query_for_knowledge_graph_helper

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Environment variables
OLAMMA_BASE_URL = os.getenv("OLAMMA_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
MODE = os.getenv("MODE")

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
    for match in matches:
        if isinstance(match, tuple):
            match = match[0]  # Extract the first group if the pattern uses groups
        logging.info(f"Executing match: {match}")
        execute_query_for_knowledge_graph_helper(match, question)


def ask_question_from_knowledge_graph_helper(question):
    prompt_template = PromptTemplate(
        input_variables=["entities", "relationships", "question"],
        template=prompt.prompt
    )
    try:
        if MODE == "local":
            model = OllamaLLM(model=MODEL_NAME, temperature=0.3, base_url=OLAMMA_BASE_URL)
            chain = prompt_template | model
            response = chain.invoke({"entities": entities.entities, "relationships": relationships.relationships, "question": question})
            logging.info(response)
            process_response(response, question)
        else:
            logging.info("Using Open Router")
            formatted_prompt = prompt_template.format(entities=entities.entities, relationships=relationships.relationships, question=question)
            response = post_to_llm(formatted_prompt)
            decoded_response = json.loads(response.content.decode('utf-8'))
            response_text = decoded_response["choices"][0]["message"]["content"]
            logging.info(response_text)
            process_response(response_text, question)
    except Exception as e:
        logging.error(f"Error occurred: {e}")

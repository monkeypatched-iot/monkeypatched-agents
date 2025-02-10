

import json
from langchain_ollama import OllamaLLM
from requests import post

from dotenv import load_dotenv
import os

from src.tools.kafka import publish_event


load_dotenv()  # Load variables from .env

CSV_API_BASE_URL = os.getenv("CSV_API_BASE_URL")
PDF_API_BASE_URL = os.getenv("PDF_API_BASE_URL")

def IndexDocument(type,file_name):
    print(type,file_name)
    if type != "type":
        if type == "csv":
            print("calls csv the document indexing endpoint")
            response = post(f"{CSV_API_BASE_URL}/v1/csv/add",json.dumps({"file_name": file_name}))
            print(response.content)
        if type == "pdf":
            print("calls pdf the document indexing endpoint")
            response = post(f"{PDF_API_BASE_URL}/v1/pdf/add",json.dumps({"file_name": file_name}))
            print(response.content)
        if type == "docx":
            print("calls docx the document indexing endpoint")
            response = post(f"{WORD_API_BASE_URL}/v1/docx/add",json.dumps({"file_name": file_name}))
            print(response.content)


def SendDocumentUploadNotification(type,file_name):
    if type != "type":
        print(type,file_name)
        print("sends user notification to add document metadata")

        # send the returned content to chatbot

        # 1. send a  prompt to the human by posting to chat app asking for document metadata
        # 2. get the posted body from the chat box 
        # 3. add the node to the graph

        # publish_event("messager",f"file with filename {file_name} added to the LLM please add the metadata to add it to the graph")


def AddMetadata(type,file_name):
    print("human in loop agent to ask for documnent metadata")

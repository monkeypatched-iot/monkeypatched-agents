

import json
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
            response = post(f"{PDF_API_BASE_URL}/v1/docx/add",json.dumps({"file_name": file_name}))
            print(response.content)


def SendDocumentUploadNotification(type,file_name):
    if type != "type":
        print(type,file_name)
        print("sends user notification to add document metadata")
        publish_event("messager",f"file with filename {file_name} added to the LLM please add the metadata to add it to the grapg")
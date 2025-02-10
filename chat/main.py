import os
import boto3
import gradio as gr
from dotenv import load_dotenv
from requests import post
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate


from src.functions.functions import handle_doc_type
from src.functions.functions import handle_upload
from src.functions.functions import handle_file_name
from src.functions.functions import handle_id_value
from src.functions.functions import handle_id_type
from src.functions.functions import handle_status
from src.functions.functions import handle_author
from src.functions.functions import handle_doc_subtype
from src.functions.functions import handle_tags
from src.helpers.helper import check_substring

# Load environment variables
load_dotenv()

# Retrieve environment variables
S3_BUCKET = os.getenv("S3_BUCKET")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
CSV_API_BASE_URL = os.getenv("CSV_API_BASE_URL")
PDF_API_BASE_URL = os.getenv("PDF_API_BASE_URL")
WORD_API_BASE_URL = os.getenv("WORD_API_BASE_URL")
DOCUMENT_METADATA_API = os.getenv("DOCUMENT_METADATA_API")

# Initialize AWS S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# Initialize LLM Model
model = OllamaLLM(model="deepseek-r1:1.5b", temperature=0.0)

# Session state tracking

# todo: this should be in redis 

session_state = {}

steps_state = []

# Generate LLM response
def generate_completion(message):
    """Uses LLM to generate a response."""

    response = model.invoke(ChatPromptTemplate.from_template("{message}").format(message=message))
    print("LLM Response:", response)

    if message == "upload document": 
        
        # todo add more combinations here to enable the document upload

        if check_substring(response, "attach files directly"):
            print("Substring found! Resetting session state.")
            steps_state.append("csv file")
            return handle_doc_type(message,session_state)
        else:
            print("Substring not found.")
            return response.content if hasattr(response, "content") else str(response)
    elif message == "csv" :
        prev = steps_state.pop()
        if prev == "csv file":
            steps_state.append(message)
            return handle_doc_subtype(message,session_state)
        else:
            print("Substring not found.")
            return response.content if hasattr(response, "content") else str(response)
    elif message in ["Prashun Javeri"]:

        # todo: names must come from valid user list

        prev = steps_state.pop()
        if prev == "csv":
            steps_state.append("author")
            return handle_author(message,session_state)
        else:
            print("Substring not found.")
            return response.content if hasattr(response, "content") else str(response)
        

    elif message in ["documents","invoice"]:
        
        # todo: need a list of document types

        prev = steps_state.pop()
        if prev == "author":
            steps_state.append("tags")
            return handle_tags(message,session_state)
        else:
            print("Substring not found.")
            return response.content if hasattr(response, "content") else str(response)
        

    elif message in ["draft","finalized","reviewed"]:
        prev = steps_state.pop()
        if prev == "tags":
            steps_state.append("status")
            return handle_status(message,session_state)
        else:
            print("Substring not found.")
            return response.content if hasattr(response, "content") else str(response)
        

    elif message in ["product_id","cusomer_id","order_id","component_id","supplier_id"]: 

        prev = steps_state.pop()
        if prev == "status":
            steps_state.append("id_type")
            return handle_id_type(message,session_state)
        else:
            print("Substring not found.")
            return response.content if hasattr(response, "content") else str(response)
        
    elif check_substring(message, "PRD") or check_substring(message, "CUST")  or check_substring(message, "ORD") or  check_substring(message, "PART") or check_substring(message, "SUP"): 

        prev = steps_state.pop()
        if prev == "id_type":
            steps_state.append("id_value")
            return handle_id_value(message,session_state)
        else:
            print("Substring not found.")
            return response.content if hasattr(response, "content") else str(response)
    elif check_substring(message, "/"):
        prev = steps_state.pop()
        if prev == "id_value":
            print(session_state)
            return handle_file_name(message,session_state)
        else:
            print("Substring not found.")
            return response.content if hasattr(response, "content") else str(response)
        
    else:
        print("Substring not found.")
        return response.content if hasattr(response, "content") else str(response)

def chatbot_response(message, history, file):
    """Handles chatbot message and visibility of file upload."""

    # Generate chatbot response
    response = generate_completion(message)

    # Update chatbot history
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response})

    print(session_state)
    if "file_name" in session_state.keys() and session_state["file_name"] :
        if session_state["doc_type"] == "upload document" and session_state["doc_subtype"] == "csv" :
         handle_upload(session_state["file_name"],session_state)

    return history

# Custom CSS for styling
custom_css = """
    body { background-color: #343541; color: #ffffff; font-family: Arial, sans-serif; }
    .gradio-container { max-width: 800px; margin: auto; padding: 20px; }
    .chatbot .message { border-radius: 10px; padding: 10px; margin: 5px 0; }
    .chatbot .user { background-color: #0a84ff; color: white; }
    .chatbot .ai { background-color: #3a3b44; }
    .gradio-button { background-color: #0a84ff; color: white; border-radius: 5px; margin-top: 10px; }
    #logo {  background-color: red; border-width: 0px; display: block;width:100%;height:100%; margin:0px;}
    .gradio-container > *:not(img) { margin-top: 20px; }  # Adds margin-top to all elements except the logo
    .svelte-dpdy90 { border: none;}
"""

with gr.Blocks(css=custom_css) as app:
    gr.Image("log.png", elem_id="logo", show_label=False, show_download_button=False, show_fullscreen_button=False)
    gr.Markdown("# Your manufacturing chatbot")
    chatbot = gr.Chatbot(elem_id="chatbot", type='messages')  # Set type to 'messages'
    msg_input = gr.Textbox(label="Type your message...")
    send_button = gr.Button("Send", elem_id="send-button")
    send_button.click(chatbot_response, [msg_input, chatbot], chatbot)
    upload_button = gr.File(label="Upload File", visible=False)  # Initially hidden

app.launch(share=True)  # Optionally, set share=True for a public link

import asyncio
import json
import logging
import os
import re
import time
from dotenv import load_dotenv
import gradio as gr
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate

from src.tools.redis import RedisDB
from src.tools.nats import subscribe_event
from src.tools.requests import post

load_dotenv()  # Load variables from .env

logging.basicConfig(level=logging.INFO)

OLAMMA_BASE_URL = os.getenv("OLAMMA_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
BASE_API_URL = os.getenv("BASE_API_URL")

redis = RedisDB()

def responder(message, history):
    """Handles chatbot message and visibility of file upload."""

    print(message)

     # Initialize Ollama model
    model = OllamaLLM(model=MODEL_NAME, temperature=0.0 , base_url=OLAMMA_BASE_URL)

    response = model.invoke(ChatPromptTemplate.from_template("{message}").format(message=message))

    print("LLM Response:", response)

    if re.search(r"\bmonkeypatched\b", message, re.IGNORECASE):  
        print("hold on let me think!")
        response = re.sub(r"\bhi monkeypatched\b", "", message, flags=re.IGNORECASE)  # Case-insensitive replacement
        response = post(BASE_API_URL, {"question": message})
        time.sleep(5)
        data = redis.get(message)
        print(data)

        if data is not None:
            # Convert byte strings to regular strings
            decoded_data = {key.decode(): value.decode() if isinstance(value, bytes) else value for key, value in data.items()}

            print(decoded_data)

            completion_data = json.loads(decoded_data['completion'])

            # Extract the answer
            answer = completion_data.get('answer')

            # Output the answer
            print(answer)
            response = str(answer)

            if answer is None:
               response = "answer not found" 

        else:
            response = "answer not found"

 
    else:
        print("Substring not found.")
   

    # Update chatbot history
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response})

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
    send_button.click(responder, [msg_input, chatbot], chatbot)
    # upload_button = gr.File(label="Upload File", visible=False)  # Initially hidden

app.launch(share=True)  # Optionally, set share=True for a public link

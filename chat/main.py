import asyncio
import json
import logging
import os
import re
import time
from dotenv import load_dotenv
import gradio as gr
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import ChatPromptTemplate

from src.tools.redis import RedisDB
from src.tools.nats import subscribe_event
from src.tools.requests import post

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)

# Configuration
OLAMMA_BASE_URL = os.getenv("OLAMMA_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
BASE_API_URL = os.getenv("BASE_API_URL")

redis = RedisDB()
def responder(message, history):
    """Handles chatbot responses and manages Redis cache."""

    print(f"User message: {message}")

    # Default response
    response = "I couldn't understand that."

    # Check if the message exists in Redis cache
    data = redis.get(message)

    if data is not None:
        try:
            # Convert byte keys and values to string
            converted_data = {key.decode(): value.decode() for key, value in data.items()}
            converted_data["completion"] = json.loads(converted_data["completion"])
            # Extract answer and ensure it's a string
            response = str(converted_data["completion"].get('answer', "answer not found"))
            print(f"Cache hit: {response}")

        except Exception as e:
            print(f"Error processing Redis data: {e}")
            response = "Error retrieving cached data."
    
    else:
        print("Cache miss: Generating response with LLM")

        # Initialize Ollama model
        model = OllamaLLM(model=MODEL_NAME, temperature=0.0, base_url=OLAMMA_BASE_URL)

        try:
            response = model.invoke(ChatPromptTemplate.from_template("{message}").format(message=message))
            response = str(response)  # Ensure response is a string
            print(f"LLM Response: {response}")

        except Exception as e:
            print(f"Error with LLM: {e}")
            response = "I couldn't generate a response."

        # If message contains "monkeypatched", fetch data from external API
        if re.search(r"\bmonkeypatched\b", message, re.IGNORECASE):
            print("Hold on, let me think!")
            
            res = post(BASE_API_URL, {"question": message})
            print(res.content.decode('utf-8'))
            time.sleep(40)  # Give time for API to process

            # Re-check Redis for the answer
            data = redis.get(message)
            print(data)

            if data:
                try:
                    decoded_data = {key.decode(): value.decode() if isinstance(value, bytes) else value for key, value in data.items()}
                    completion_data = json.loads(decoded_data['completion'])
                    response = str(completion_data.get('answer', "answer not found"))  # Ensure response is a string
                    print(f"API Retrieved Answer: {response}")

                except Exception as e:
                    print(f"Error processing API data: {e}")
                    response = "Error retrieving API response."
            else:
                response = "answer not found"

    # Ensure response is always a string
    response = str(response)

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
    #logo { background-color: red; border-width: 0px; display: block; width:100%; height:100%; margin:0px; }
    .gradio-container > *:not(img) { margin-top: 20px; }
    .svelte-dpdy90 { border: none; }
"""

# Gradio UI
with gr.Blocks(css=custom_css) as app:
    gr.Image("log.png", elem_id="logo", show_label=False, show_download_button=False, show_fullscreen_button=False)
    gr.Markdown("# Your Manufacturing Chatbot")
    chatbot = gr.Chatbot(elem_id="chatbot", type='messages')  # Set type to 'messages'
    msg_input = gr.Textbox(label="Type your message...")
    send_button = gr.Button("Send", elem_id="send-button")
    send_button.click(responder, [msg_input, chatbot], chatbot)

app.launch(share=True)  # Set share=True for a public link if needed

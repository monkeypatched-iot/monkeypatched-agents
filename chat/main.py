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
from src.tools.nats import publish_event, subscribe_event, history_queue
from src.tools.requests import post

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)

# Configuration
OLAMMA_BASE_URL = os.getenv("OLAMMA_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
BASE_API_URL = os.getenv("BASE_API_URL")


gradio_history = []

redis = RedisDB()


# Function to get history from the queue and format for Gradio
async def gradio_interface():
    """Fetch history from the queue to display in Gradio."""
    history = []
    global history_queue

    # Fetch messages from the queue and return them
    while not history_queue.empty():
        role, content = await history_queue.get()
        history.append(f"{role.capitalize()}: {content}")
    
    return "\n".join(history)

async def responder(message, history):
    await publish_event("messages", message)
    user = await history_queue.get()
    assistant = await history_queue.get()
    print(assistant[1])
    history.append({"role": "user", "content": user[1]})
    history.append({"role": "assistant", "content": assistant[1]})
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


import time
import asyncio
import threading


def blocking_func(event: threading.Event):
    while not event.is_set():
        asyncio.run(subscribe_event())


# Start NATS listener and Gradio interface
async def start_server():
    """Run the NATS listener and Gradio interface simultaneously."""
    print("here")
    event = threading.Event()
    asyncio.create_task(asyncio.to_thread(blocking_func, event))
    await asyncio.sleep(5)



async def main():
    await start_server()
    app.launch()

asyncio.run(main())

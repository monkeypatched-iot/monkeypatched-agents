import asyncio
import logging
import os
import random
import re
import threading
from dotenv import load_dotenv
import gradio as gr
from langchain_ollama import OllamaEmbeddings
from src.tools.redis import RedisDB
from src.tools.qdrant import qdrant
from src.tools.nats import publish_event, subscribe_event, history_queue
from qdrant_client.models import PointStruct, VectorParams
from qdrant_client.models import NamedVector
import ollama
from sentence_transformers import SentenceTransformer


# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)

# Configuration
OLAMMA_BASE_URL = os.getenv("OLAMMA_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
BASE_API_URL = os.getenv("BASE_API_URL")

QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")

gradio_history = []

redis = RedisDB()

def clean_response(response):
    # Remove <think> tags and everything inside them, including line breaks and spaces
    cleaned_response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)
    
    # Remove leading/trailing whitespace if any
    return cleaned_response.strip()


# Step 1: Generate embeddings from Ollama model
def get_ollama_embedding(text: str) -> list:
    # 1. Load a pretrained Sentence Transformer model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # The sentences to encode
    sentences = [
        text
    ]

    # 2. Calculate embeddings by calling model.encode()
    return model.encode(sentences)

async def responder(message, history):
    # Get document embeddings for the user's message
    message_embeddings = get_ollama_embedding(message)  # Expecting a list of embeddings

    # Search Qdrant for the closest match
    try:
        # Perform search without specifying 'vector_name'
        result = await asyncio.to_thread(qdrant.search, collection_name=QDRANT_COLLECTION, query_vector=message_embeddings[0], limit=1)
        if result:
  
            point = result[0].payload
            if point:
                result_dict = point
            else :
                result_dict = result.__dict__

            if result_dict["question"] == message:
                cleaned_response = result_dict["answer"]
                logging.info(f"Found result in Qdrant: {cleaned_response}")
            else:
                # If not found, publish the event and fetch assistant response
                await publish_event("messages", message)
                user = await history_queue.get()
                assistant = await history_queue.get()
                cleaned_response = clean_response(assistant[1])
                # Prepare data for Qdrant insertion if not found
                points = [
                    PointStruct(
                        id=random.randint(1, 100),  # Generate a random ID
                        vector=message_embeddings[0],  # Using the first vector (from the user's message)
                        payload={"question": message, "answer": cleaned_response}
                    )
                ]
                
                # Insert into Qdrant without specifying 'vector_name'
                await asyncio.to_thread(qdrant.upsert, collection_name=QDRANT_COLLECTION, points=points)
                history.append({"role": "assistant", "content": cleaned_response})
        else:
            cleaned_response = "Sorry, an error occurred while processing your request."
            
    except Exception as e:
        logging.error(f"Error during Qdrant search: {e}")
        cleaned_response = "Sorry, an error occurred while processing your request."

    history.append({"role": "user", "content": message})
    if cleaned_response is not None:
        # Update history with user and assistant messages
        history.append({"role": "assistant", "content": cleaned_response})
    else:
        cleaned_response = "Sorry, an error occurred while processing your request."
        history.append({"role": "assistant", "content": cleaned_response})

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

def blocking_func(event: threading.Event):
    while not event.is_set():
        asyncio.run(subscribe_event())

# Start NATS listener and Gradio interface
async def start_server():
    """Run the NATS listener and Gradio interface simultaneously."""
    event = threading.Event()
    asyncio.create_task(asyncio.to_thread(blocking_func, event))
    await asyncio.sleep(5)

async def main():
    await start_server()
    app.launch()

asyncio.run(main())

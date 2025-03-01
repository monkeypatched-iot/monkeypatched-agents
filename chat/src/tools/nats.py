import asyncio
import json
import os
import re
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from nats.aio.client import Client as NATS
from langchain.prompts import ChatPromptTemplate

from src.tools.requests import post

load_dotenv()  # Load variables from .env

NATS_SERVER_URL = os.getenv("NATS_SERVER_URL", "nats://localhost:4222")  # Default fallback
OLAMMA_BASE_URL = os.getenv("OLAMMA_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
BASE_API_URL = os.getenv("BASE_API_URL")

gradio_history = []

# Global queue to store history
history_queue = asyncio.Queue()

model = OllamaLLM(model=MODEL_NAME, temperature=0.0, base_url=OLAMMA_BASE_URL)

async def publish_event(subject, message):
    """Publish a message to a NATS subject."""
    nc = NATS()
    try:
        await nc.connect(NATS_SERVER_URL)

        json_message = json.dumps(message)
        await nc.publish(subject, json_message.encode())

        print(f"Published message to subject '{subject}': {message}")

        await nc.drain()  # Gracefully close connection
    except Exception as e:
        print(f"Error publishing event: {e}")
    finally:
        await nc.close()


async def message_handler(msg):
    """Callback function to process received messages."""

    global gradio_history  # Access global history
    global model
    global history_queue

    subject = msg.subject
    data = msg.data.decode()
    try:
        if subject != "answers":
            response = model.invoke(ChatPromptTemplate.from_template("{message}").format(message=data))
            response = str(response)  # Ensure response is a string
            print(f"LLM Response: {response}")
            message = f"{data}".replace('"','')
            await history_queue.put(("user", f"{data}".replace('"','')))
            # If message contains "monkeypatched", fetch data from external API
            if "monkeypatched" in message:
                response = post(BASE_API_URL, {"question": f"{data}".replace('"','')})
                message = response.content.decode("utf-8")
            else:
                await history_queue.put(("assistant", f"{response}"))
        else:
            message = f"{data}".replace('"','')
            print(message)
            # Regex pattern to extract the answer value
            pattern = r"{\s*answer\s*:\s*([^}]+)\s*}"
            match = re.search(pattern, message)
            if match:
                answer = str(match.group(1))
                print("Answer:", answer)
                await history_queue.put(("assistant", f"{answer}"))

    except Exception as e:
            print(f"Error with LLM: {e}")
            response = "I couldn't generate a response."
            

async def subscribe_event():
    """Subscribe to a NATS subject and listen for messages."""
    nc = NATS()
    try:
        await nc.connect(NATS_SERVER_URL)

        await nc.subscribe("messages", cb=message_handler)
        print("Subscribed to 'answers'. Waiting for messages...")

        await nc.subscribe("answers", cb=message_handler)
        print("Subscribed to 'answers'. Waiting for messages...")


        # Keep the event loop running
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Error subscribing to event: {e}")
    finally:
        await nc.c
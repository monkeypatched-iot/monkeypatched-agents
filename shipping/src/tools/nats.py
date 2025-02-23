import asyncio
import json
import os
from dotenv import load_dotenv
from nats.aio.client import Client as NATS

load_dotenv()  # Load variables from .env

NATS_SERVER_URL = os.getenv("NATS_SERVER_URL")

async def publish_event(subject,message):
    nc = NATS()
    
    try:
        # Connect to the NATS server
        await nc.connect(NATS_SERVER_URL)

        json_message = json.dumps(message)

        await nc.publish(subject, json_message.encode())

        print(f"Published message to subject '{subject}': {message}")

        # Close the connection
        await nc.drain()
    except Exception as e:
        print(f"Error: {e}")


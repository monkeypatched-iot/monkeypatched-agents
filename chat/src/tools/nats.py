import asyncio
import json
import os
from dotenv import load_dotenv
from nats.aio.client import Client as NATS

load_dotenv()  # Load variables from .env

NATS_SERVER_URL = os.getenv("NATS_SERVER_URL", "nats://localhost:4222")  # Default fallback


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
    subject = msg.subject
    data = msg.data.decode()
    print(f"Received a message on '{subject}': {data}")


async def subscribe_event():
    """Subscribe to a NATS subject and listen for messages."""
    nc = NATS()
    try:
        await nc.connect(NATS_SERVER_URL)

        await nc.subscribe("answers", cb=message_handler)
        print("Subscribed to 'answers'. Waiting for messages...")

        # Keep the event loop running
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Error subscribing to event: {e}")
    finally:
        await nc.c
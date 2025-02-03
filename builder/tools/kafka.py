from confluent_kafka import Producer, Consumer, KafkaException
import json
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_CONSUMER_GROUP_ID = os.getenv("KAFKA_CONSUMER_GROUP_ID")

# kafka consumer config
consumer_config = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "group.id": KAFKA_CONSUMER_GROUP_ID ,
    "auto.offset.reset": "earliest"  # Start from the beginning if no offsets exist
}

# Kafka Producer Configuration
producer_config = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    'client.id': 'client_id'
}


producer = Producer(producer_config)

consumer = Consumer(consumer_config)


# Function to serialize dictionary and send to Kafka
def publish_event(topic, message_dict):
    # Serialize the dictionary to a JSON string
    message_json = json.dumps(message_dict)
    
    # Callback function to confirm message delivery
    def delivery_report(err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} partition {msg.partition()}")

    # Produce message to Kafka topic
    producer.produce(topic, message_json, callback=delivery_report)

    # Flush the producer to ensure the message is sent
    producer.flush()



# Function to consume messages from Kafka
def consume_event(topic):
    # Subscribe to the topic
    consumer.subscribe([topic])

    try:
        while True:
            # Poll for messages
            msg = consumer.poll(timeout=1.0)  # 1 second timeout

            if msg is None:
                # No message available within timeout
                continue
            elif msg.error():
                # If there's an error, print it
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"End of partition reached {msg.partition} at offset {msg.offset}")
                else:
                    raise KafkaException(msg.error())
            else:
                # Successfully received a message
                message_value = msg.value().decode('utf-8')  # Decode the message to a string
                print(f"Received message: {message_value}")

                # Deserialize the JSON message back into a dictionary
                message_dict = json.loads(message_value)

                # Access the 'customer_id' and 'name' from the dictionary
                print(f"Customer ID: {message_dict['customer_id']}")
                print(f"Name: {message_dict['name']}")

    except KeyboardInterrupt:
        print("Consumer interrupted.")
    finally:
        # Close the consumer to commit offsets and clean up
        consumer.close()

import logging
import os
import json
from redis import Redis
from dotenv import load_dotenv
from redis.commands.search.query import Query
from redis.commands.search.field import TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from src.utils.logger import logging as logger

load_dotenv()  # Load variables from .env

logging.basicConfig(level=logging.INFO)

REDIS_URL = os.getenv("REDIS_URL")
INDEX_NAME = os.getenv("INDEX_NAME")  # Index Name
DOC_PREFIX = os.getenv("DOC_PREFIX")  # Redis Prefix for Index

class RedisDB():
    def __init__(self) -> None:
        try:
            logger.info(f'Initializing the Redis connection at {REDIS_URL}')
            self.client = Redis.from_url(REDIS_URL)
            self.prompt_completion_index = self.create_index()  # Create or ensure the index
            logger.info('Redis connection initialized.')
        except RuntimeError as e:
            logger.error('Cannot initialize Redis connection.')
            logger.error(e)

    def put(self, prompt, completion, score=0):
        ''' Adds the prompt, completion, and score to Redis without embedding '''
        try:
            objects = {"prompt": prompt, "completion": completion, "score": score}
            logger.info(f"Adding object {json.dumps(objects)} to Redis DB.")
            key = f"doc:{objects['prompt']}"
            self.client.hset(key, mapping=objects)  # Store as a hash in Redis
            logger.info(f"Data for prompt '{prompt}' stored in Redis.")
        except RuntimeError as e:
            logger.error('Cannot store the data in Redis.')
            logger.error(e)

    def get(self, prompt):
        ''' Retrieves the prompt, completion, and score from Redis by prompt '''
        try:
            key = f"doc:{prompt}"
            data = self.client.hgetall(key)  # Get all fields for the key
            if not data:
                logger.warning(f"No data found for prompt '{prompt}'")
                return None
            logger.info(f"Retrieved data for prompt '{prompt}': {data}")
            return data
        except RuntimeError as e:
            logger.error('Cannot get data from Redis.')
            logger.error(e)

    def create_index(self):
        ''' Creates an index for storing data without vectors in Redis '''
        logger.info(f"Creating index {INDEX_NAME} in Redis.")
        try:
            self.client.ft(INDEX_NAME).info()
            logger.info("Index already exists!")
        except:
            schema = (
                TagField("prompt"),  
                TagField("completion"),    
                TagField("score"),  
            )

            definition = IndexDefinition(prefix=[DOC_PREFIX], index_type=IndexType.HASH)
            index = self.client.ft(INDEX_NAME).create_index(fields=schema, definition=definition)
            logger.info(f"Index {INDEX_NAME} created successfully.")
            return index

    def set(self, prompt, completion, score=0, ex=None):
        ''' Set prompt, completion, and score in Redis with optional TTL (expiration) '''
        try:
            objects = {"prompt": prompt, "completion": completion, "score": score}
            logger.info(f"Setting object {json.dumps(objects)} in Redis DB with TTL {ex} seconds.")
            key = f"doc:{objects['prompt']}"
            self.client.hset(key, mapping=objects)  # Store as a hash in Redis
            if ex:
                self.client.expire(key, ex)  # Set the expiration time (TTL)
            logger.info(f"Data for prompt '{prompt}' set in Redis with TTL.")
        except RuntimeError as e:
            logger.error('Cannot set the data in Redis with TTL.')
            logger.error(e)

    def delete(self, prompt):
        ''' Deletes the prompt data from Redis '''
        try:
            key = f"doc:{prompt}"
            self.client.delete(key)  # Delete the key from Redis
            logger.info(f"Data for prompt '{prompt}' deleted from Redis.")
        except RuntimeError as e:
            logger.error('Cannot delete the data from Redis.')
            logger.error(e)

    def expire(self, prompt, ex):
        ''' Sets the TTL (expiration) for an existing prompt in Redis '''
        try:
            key = f"doc:{prompt}"
            self.client.expire(key, ex)  # Set the expiration time (TTL)
            logger.info(f"TTL for prompt '{prompt}' set to {ex} seconds.")
        except RuntimeError as e:
            logger.error('Cannot set the TTL for the data in Redis.')
            logger.error(e)

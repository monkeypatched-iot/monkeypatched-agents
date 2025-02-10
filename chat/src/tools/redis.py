import redis
from src.utils.logger import logging as logger

class RedisDB():
    def __init__(self, host, port=6379, db=0) -> None:
        ''' connect to Redis database '''
        try:
            self.client = redis.StrictRedis(host=host, port=port, db=db)
            self.client.ping()  # Verify connection
        except redis.ConnectionError as e:
            logger.error('cannot connect to Redis')
            logger.error(e)

    def set_key(self, key, value):
        ''' set a key-value pair in Redis '''
        try:
            self.client.set(key, value)
            return True
        except redis.RedisError as e:
            logger.error(f'can not set key {key}')
            logger.error(e)
            return False

    def get_key(self, key):
        ''' get a value for the given key from Redis '''
        try:
            value = self.client.get(key)
            return value
        except redis.RedisError as e:
            logger.error(f'can not get value for key {key}')
            logger.error(e)
            return None

    def delete_key(self, key):
        ''' delete a key from Redis '''
        try:
            self.client.delete(key)
            return True
        except redis.RedisError as e:
            logger.error(f'can not delete key {key}')
            logger.error(e)
            return False

    def execute_command(self, command, *args):
        ''' execute a generic Redis command '''
        try:
            response = self.client.execute_command(command, *args)
            return response
        except redis.RedisError as e:
            logger.error(f'can not execute command {command}')
            logger.error(e)
            return None

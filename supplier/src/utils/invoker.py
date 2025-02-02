from src.utils.registry import function_registry
import inspect
import logging

logging.basicConfig(level=logging.INFO)

def invoke(function_name, *args, **kwargs):
    if function_name in function_registry:
        func = function_registry[function_name]
        try:
            # Log the function call attempt with parameters
            logging.info(f"Invoking function '{function_name}' with args={args}, kwargs={kwargs}")
            return func(*args, **kwargs)
        except TypeError as e:
            # Fetch and log the expected function signature
            expected_signature = inspect.signature(func)
            logging.error(f"Function signature mismatch for '{function_name}'")
            logging.error(f"Expected: {expected_signature}, Got: args={args}, kwargs={kwargs}")
            raise ValueError(
                f"Error invoking function '{function_name}'. "
                f"Expected: {expected_signature}, Got: args={args}, kwargs={kwargs}. Error: {str(e)}"
            )
    else:
        # Log and raise error if function is not found in registry
        logging.error(f"Function '{function_name}' is not registered.")
        raise ValueError(f"Function '{function_name}' is not registered.")

import requests

def get(url:str):
    # GET request to GeeksforGeeks
    get_response = requests.get(url)

    return get_response

def post(url: str, data: dict, headers: dict = None):
    """Send a POST request to the given URL with optional headers."""
    response = requests.post(url, json=data, headers=headers)
    return response
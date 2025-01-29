
import requests

def get(url:str):
    # GET request to GeeksforGeeks
    get_response = requests.get(url)

    return get_response

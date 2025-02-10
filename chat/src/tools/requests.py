
import requests

def get(url:str):
    # GET request to GeeksforGeeks
    get_response = requests.get(url)

    return get_response

def post(url: str, data: dict):
    # POST request to the given URL with provided data
    post_response = requests.post(url, json=data)

    return post_response


def post_file(url: str, file):
    # Ensure the file is sent as a multipart form-data request
    files = {"file": (file.filename, file.file, file.content_type)}

    post_response = requests.post(url, files=files)

    return post_response
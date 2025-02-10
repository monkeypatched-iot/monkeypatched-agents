import os
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Initialize AWS S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# File reading function
def read_file(file):
    """Reads and extracts content from uploaded files."""
    try:
        if file.filename.endswith(".csv"):
            return pd.read_csv(file.file).to_string()
        else:
            return "Unsupported file format."
    except Exception as e:
        return f"Error reading file: {str(e)}"

# Check if substring exists in response
def check_substring(response: str, substring: str) -> bool:
    return substring in response

# Upload file to S3
def upload_to_s3(file_content, file_name: str):
    try:
        s3_client.put_object(Bucket=S3_BUCKET, Key=file_name, Body=file_content)
        print(f"File {file_name} uploaded successfully to S3.")
        return True
    except NoCredentialsError:
        print("Credentials not available.")
        return False
    except Exception as e:
        print(f"Error uploading file to S3: {str(e)}")
        return False
    



from requests import get

from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

BASE_URL = os.getenv("API_BASE_URL")

def GetComponentDetails(component_id):
    print("getting componeent details")
 
def GetComponentMetadata(component_id):
    print("getting the component data")

def GetComponentMetrics(component_id):
    print("getting component metrics")

def GetComponentPaymentInformation(component_id):
    print("getting the payment information")

def AddComponent(component_id):
    print("adding a new component")
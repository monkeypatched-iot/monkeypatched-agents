from pydantic import BaseModel
from typing import List, Dict

# Define request body schema using Pydantic
class Product(BaseModel):
    id: str
    qty: str

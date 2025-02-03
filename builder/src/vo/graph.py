from pydantic import BaseModel
from typing import List, Dict
from src.vo.product import Product

class KnowledgeGraphRequest(BaseModel):
    customer_id: str
    order_id: str
    products: List[Product]
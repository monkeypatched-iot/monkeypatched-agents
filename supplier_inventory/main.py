from fastapi import FastAPI
from pydantic import BaseModel
from src.api.steps import create_inventory_nodes_in_knowledge_graph_helper

app = FastAPI()

class InventoryRequest(BaseModel):
    component_id: str
    supplier_id: str

@app.post("/v1/supplier/inventory/")
async def create_inventory_nodes(request: InventoryRequest):
    try:
        result = create_inventory_nodes_in_knowledge_graph_helper(request.component_id, request.supplier_id)
        return {"message": "inventory nodes created successfully", "result": result}
    except Exception as e:
        return {"error": str(e)}

from src.api.steps import create_supplier_nodes_in_knowledge_graph_helper, delete_orphan_nodes
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/v1/supplier/{supplier_id}")
def create_supplier_nodes_in_knowledge_graph(supplier_id: str):
    try:
        create_supplier_nodes_in_knowledge_graph_helper(supplier_id)
        return {"message": "Supplier nodes created successfully"}
    except Exception as e:
        # Raise an HTTPException with a clear error message
        raise HTTPException(status_code=500, detail=f"Error occurred while creating supplier nodes: {e}")

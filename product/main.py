from src.api.steps import create_product_nodes_in_knowledge_graph_helper, delete_orphan_nodes
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/v1/product/{product_id}")
def create_product_nodes_in_knowledge_graph(product_id: str):
    try:
        create_product_nodes_in_knowledge_graph_helper(product_id)
        return {"message": "Product nodes created successfully"}
    except Exception as e:
        # Raise HTTP Exception for the main error
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")
    

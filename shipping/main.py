from src.api.steps import create_shipping_provider_nodes_in_knowledge_graph_helper, delete_orphan_nodes
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/v1/shipping_provider/{provider_id}")
def create_shipping_provider_nodes_in_knowledge_graph(provider_id: str):
    try:
        create_shipping_provider_nodes_in_knowledge_graph_helper(provider_id)
        return {"message": "Shipping Provider nodes created successfully"}
    except Exception as e:
        print('clean up orphan nodes')
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")
        

from src.api.steps import create_order_nodes_in_knowledge_graph_helper, delete_orphan_nodes
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/v1/order/{order_id}")
def create_order_nodes_in_knowledge_graph(order_id: str):
    try:
        create_order_nodes_in_knowledge_graph_helper(order_id)
        return {"message": "Order nodes created successfully"}
    except Exception as e:
        print('clean up orphan nodes')
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")
        

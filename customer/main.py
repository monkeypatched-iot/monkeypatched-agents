from src.api.steps import create_customer_nodes_in_knowledge_graph_helper, delete_orphan_nodes
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/v1/customer/{customer_id}")
def create_customer_nodes_in_knowledge_graph(customer_id: str):
    try:
        create_customer_nodes_in_knowledge_graph_helper(customer_id)
        return {"message": "Customer nodes created successfully"}
    except Exception as e:
        # todo: clean up the orphan nodes
        print('clean up orphan nodes')
        try:
            delete_orphan_nodes()
        except Exception as e:
            print('failed to delete orphan nodes')
            raise HTTPException(status_code=500, detail=f"Error occurred: {e}")
        
# todo check  updates to existing customers

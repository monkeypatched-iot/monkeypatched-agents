from src.api.steps import create_product_nodes_in_knowledge_graph_helper, delete_orphan_nodes
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/v1/product/{product_id}")
def create_product_nodes_in_knowledge_graph(product_id: str,location_id:str):
    try:
        create_product_nodes_in_knowledge_graph_helper(product_id,location_id)
        return {"message": "Product nodes created successfully"}
    except Exception as e:
        # Clean up orphan nodes if an error occurs
        print("Cleaning up orphan nodes...")
        try:
            delete_orphan_nodes()
        except Exception as cleanup_error:
            print("Failed to delete orphan nodes")
            raise HTTPException(status_code=500, detail=f"Cleanup error: {cleanup_error}")

        # Raise HTTP Exception for the main error
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")
    

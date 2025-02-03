from src.api.steps import create_supplier_nodes_in_knowledge_graph_helper, delete_orphan_nodes
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/v1/supplier/{supplier_id}/locattion/{location_id}/item/{item_id}")
def create_supplier_nodes_in_knowledge_graph(supplier_id: str,location_id: str,item_id):
    try:
        create_supplier_nodes_in_knowledge_graph_helper(supplier_id)
        return {"message": "Supplier nodes created successfully"}
    except Exception as e:
        print(f"Error creating supplier nodes: {e}")
        try:
            delete_orphan_nodes()
            print("Successfully cleaned up orphan nodes.")
        except Exception as cleanup_error:
            print(f"Failed to delete orphan nodes: {cleanup_error}")

        # Raise an HTTPException with a clear error message
        raise HTTPException(status_code=500, detail=f"Error occurred while creating supplier nodes: {e}")

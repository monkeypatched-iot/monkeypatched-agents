from src.api.steps import create_component_nodes_in_knowledge_graph_helper, delete_orphan_nodes
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/v1/component/{component_id}")
def create_component_nodes_in_knowledge_graph(component_id: str):
    try:
        create_component_nodes_in_knowledge_graph_helper(component_id)
        return {"message": "Component nodes created successfully"}
    except Exception as e:
        print(f"Error creating component nodes: {e}")
        try:
            delete_orphan_nodes()
            print("Successfully cleaned up orphan nodes.")
        except Exception as cleanup_error:
            print(f"Failed to delete orphan nodes: {cleanup_error}")

        # Raise an HTTPException with a clear error message
        raise HTTPException(status_code=500, detail=f"Error occurred while creating component nodes: {e}")

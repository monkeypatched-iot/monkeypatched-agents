import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from monkeypatched_agents.builder.src.vo.graph import KnowledgeGraphRequest
from src.api.steps import create_knowledge_graph_helper, delete_orphan_nodes

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/v1/create/knowledge-graph")
def create_knowledge_graph(request: KnowledgeGraphRequest):
    try:
        create_knowledge_graph_helper(request)
        return {"message": "Knowledge graph created successfully"}
    except Exception as e:
        logger.error(f"Error creating knowledge graph: {e}")
        try:
            delete_orphan_nodes()
            logger.info("Successfully cleaned up orphan nodes.")
        except Exception as cleanup_error:
            logger.error(f"Failed to delete orphan nodes: {cleanup_error}")
            raise HTTPException(
                status_code=500,
                detail=f"Error occurred while creating knowledge graph: {e}. Cleanup failed: {cleanup_error}",
            )
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred while creating knowledge graph: {e}",
        )

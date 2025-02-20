from pydantic import BaseModel
from src.api.rag import ask_question_from_knowledge_graph_helper
from fastapi import FastAPI, HTTPException

app = FastAPI()

class QueryRequest(BaseModel):
    question:str

@app.post("/v1/query/generate")
def ask_question_from_knowledge_graph(question: QueryRequest):
    try:
        answer = ask_question_from_knowledge_graph_helper(question)
        return {"answer":answer}
    except Exception as e:
        print('error occured bro!')
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")
        

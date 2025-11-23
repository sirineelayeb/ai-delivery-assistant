# FastAPI + routes
from fastapi import FastAPI
from app.models import Query
from app.search import search
from app.llm import generate_response

app = FastAPI(title="AI-Powered Delivery Assistant")

@app.post("/ask")
def ask(query: Query):
    """
    Endpoint to handle user queries about deliveries.
    """
    retrieved_info = search(query.question)
    answer = generate_response(retrieved_info)
    return {"answer": answer}

# app/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from app.inference import generate_response

app = FastAPI()

class PromptRequest(BaseModel):
    question: str

class PromptResponse(BaseModel):
    response: str

@app.post("/chat", response_model=PromptResponse)
async def chat_endpoint(request: PromptRequest):
    response = generate_response(request.question)
    return PromptResponse(response=response)

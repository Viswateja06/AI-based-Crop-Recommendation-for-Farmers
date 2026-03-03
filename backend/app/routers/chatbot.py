from fastapi import APIRouter
from app.schemas import ChatRequest, ChatResponse
from app.agent.controller import process_query

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest):
    """
    Receives a farmer's query and routes it via the AI Agent Controller
    """
    result = process_query(request.query, request.lang)
    # Ideally, log the query and response to the DB here
    return result

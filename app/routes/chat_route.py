from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.schemas.chat_schema import ChatRequest
from app.services.rag_service import ask_question

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("/")
async def chat(
    request: ChatRequest,
    current_user=Depends(get_current_user),
):

    answer = await ask_question(
        request.question,
        current_user,
    )

    return {
        "answer": answer
    }
from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.schemas.chat_schema import ChatRequest
from app.services.rag_service import answer_question

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("/")
async def chat(
    request: ChatRequest,
    current_user=Depends(get_current_user),
):

    return await answer_question(
        request.question,
        current_user,
    )
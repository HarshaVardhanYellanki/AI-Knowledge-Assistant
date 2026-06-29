from fastapi import APIRouter, Depends, File, UploadFile

from app.core.security import get_current_user
from app.services.document_service import (
    upload_document,
    list_user_documents,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    return await upload_document(
        file,
        current_user,
    )


@router.get("/")
async def list_documents(
    current_user=Depends(get_current_user),
):
    return {
        "documents": await list_user_documents(
            current_user
        )
    }
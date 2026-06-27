from fastapi import APIRouter, Depends, File, UploadFile

from app.core.security import get_current_user
from app.services.document_service import upload_document

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):
    return await upload_document(
        file,
        current_user
    )
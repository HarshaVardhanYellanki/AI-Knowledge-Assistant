import os
import uuid
from datetime import datetime, UTC

from fastapi import HTTPException, UploadFile, status

from app.database.mongodb import documents_collection


UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}


async def upload_document(
    file: UploadFile,
    current_user: dict
):

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type"
        )

    unique_filename = (
        f"{uuid.uuid4()}{extension}"
    )

    file_path = os.path.join(
        UPLOAD_FOLDER,
        unique_filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(
            await file.read()
        )

    document = {
        "user_id": str(current_user["_id"]),
        "original_filename": file.filename,
        "stored_filename": unique_filename,
        "file_type": extension.replace(".", ""),
        "file_path": file_path,
        "status": "uploaded",
        "uploaded_at": datetime.now(UTC)
    }

    result = await documents_collection.insert_one(
        document
    )

    return {
        "message": "Document uploaded successfully",
        "document_id": str(result.inserted_id)
    }
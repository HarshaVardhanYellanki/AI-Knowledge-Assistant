import os
import uuid
from datetime import datetime, UTC

from fastapi import HTTPException, UploadFile, status

from app.database.mongodb import documents_collection
from app.services.document_processor import extract_text
from app.services.chunking_service import chunk_text
from app.services.embedding_service import generate_embeddings
from app.services.vector_store_service import (
    create_collection,
    store_embeddings,
)


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

    text = extract_text(file_path)

    chunks = chunk_text(text)

    embeddings = await generate_embeddings(chunks)

    await create_collection()

    await store_embeddings(
    chunks,
    embeddings,
    {
        "user_id": str(current_user["_id"]),
        "document_id": str(result.inserted_id),
    },
)

    return {
        "message": "Document uploaded successfully",
        "document_id": str(result.inserted_id)
    }
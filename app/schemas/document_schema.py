from pydantic import BaseModel


class DocumentResponse(BaseModel):
    message: str
    document_id: str
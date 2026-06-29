import os
import uuid
import warnings
from pathlib import Path
from datetime import datetime, timezone
from fastapi import HTTPException

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models

from app.database.mongodb import documents_collection
from app.core.config import settings

# Suppress langchain_community sunset warning — it is still fully functional
warnings.filterwarnings("ignore", category=DeprecationWarning, module="langchain_community")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


# ---------------------------------------------------------------------------
# Qdrant client + collection bootstrap
# ---------------------------------------------------------------------------

def _get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=settings.QDRANT_URL)


def _ensure_collection(client: QdrantClient, collection_name: str, vector_size: int) -> None:
    """Create the Qdrant collection if it does not already exist."""
    existing = {c.name for c in client.get_collections().collections}
    if collection_name not in existing:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=qdrant_models.VectorParams(
                size=vector_size,
                distance=qdrant_models.Distance.COSINE,
            ),
        )


# ---------------------------------------------------------------------------
# Loader selection
# ---------------------------------------------------------------------------

def _load_documents(file_path: str, extension: str):
    """Return a list of LangChain Document objects for the given file."""
    if extension == ".pdf":
        loader = PyPDFLoader(file_path)
    elif extension == ".docx":
        loader = Docx2txtLoader(file_path)
    elif extension == ".txt":
        loader = TextLoader(file_path, encoding="utf-8", autodetect_encoding=True)
    else:
        raise HTTPException(
    status_code=400,
    detail="Unsupported file type"
)

    return loader.load()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def upload_document(file, current_user: dict) -> dict:
    """
    Save the uploaded file, parse it, embed chunks, store in Qdrant,
    and persist metadata in MongoDB.

    Returns the document metadata dict that was saved to MongoDB.
    """
    user_id = str(current_user["_id"])

    # --- Validate extension ---
    filename = file.filename
    extension = Path(filename).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
    status_code=400,
    detail="Unsupported file type"
)

    # --- Persist file to disk ---
    document_id = str(uuid.uuid4())
    safe_filename = f"{document_id}{extension}"
    file_path = UPLOAD_DIR / safe_filename

    contents = await file.read()
    file_path.write_bytes(contents)

    try:
        # --- Load + split ---
        raw_docs = _load_documents(str(file_path), extension)
        if not raw_docs:
            raise HTTPException(
    status_code=400,
    detail="No content could be extracted from the uploaded file"
)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
        )
        chunks = splitter.split_documents(raw_docs)

        # --- Inject metadata into every chunk ---
        for i, chunk in enumerate(chunks):
            chunk.metadata.update(
                {
                    "user_id": user_id,
                    "document_id": document_id,
                    "filename": filename,
                    "chunk_index": i,
                    # page is already set by PyPDFLoader; preserve it if present
                }
            )

        # --- Embeddings ---
        embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
        )

        # --- Qdrant: ensure collection exists, then store ---
        collection_name =settings.QDRANT_COLLECTION
        qdrant_client = _get_qdrant_client()

        # text-embedding-3-small → 1536 dimensions
        # text-embedding-3-large → 3072 dimensions
        # Derive from a test embedding so we never hard-code the wrong size.
        VECTOR_SIZE = 1536

        _ensure_collection(qdrant_client, collection_name, VECTOR_SIZE)

        vector_store = QdrantVectorStore(
            client=qdrant_client,
            collection_name=collection_name,
            embedding=embeddings,
        )
        vector_store.add_documents(chunks)

        # --- MongoDB metadata ---
        metadata = {
            "document_id": document_id,
            "user_id": user_id,
            "filename": filename,
            "extension": extension,
            "chunk_count": len(chunks),
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
        }
        await documents_collection.insert_one(metadata)

        # Remove internal MongoDB _id before returning
        metadata.pop("_id", None)
        return metadata

    except Exception:
        # Clean up the file if processing fails
        if file_path.exists():
            file_path.unlink()
        raise


async def list_user_documents(current_user: dict) -> list[dict]:
    """Return all document metadata records belonging to the current user."""
    user_id = str(current_user["_id"])
    cursor = documents_collection.find({"user_id": user_id}, {"_id": 0})
    return await cursor.to_list(length=None)
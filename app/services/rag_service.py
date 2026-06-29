import os
import warnings

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models

from app.core.config import settings

warnings.filterwarnings("ignore", category=DeprecationWarning, module="langchain_community")

# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """You are an AI knowledgea assistant. Answer the user's question
using ONLY the context provided below. If the context does not contain enough
information to answer the question, say so clearly — do not fabricate details.

Context:
{context}"""

_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", _SYSTEM_PROMPT),
        ("human", "{question}"),
    ]
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=settings.QDRANT_URL)


def _format_docs(docs) -> str:
    """Concatenate retrieved document chunks into a single context string."""
    if not docs:
        return "No relevant documents found."
    return "\n\n---\n\n".join(
        f"[{doc.metadata.get('filename', 'unknown')} "
        f"| chunk {doc.metadata.get('chunk_index', '?')}]\n{doc.page_content}"
        for doc in docs
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def answer_question(question: str, current_user: dict) -> dict:
    """
    Retrieve relevant chunks for *current_user* from Qdrant, then generate
    an answer with ChatOpenAI.

    Returns:
        {
            "answer": str,
            "sources": [{"filename": str, "chunk_index": int}, ...]
        }
    """
    user_id = str(current_user["_id"])

    # --- Embeddings (same model used at upload time) ---
    embeddings = OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        openai_api_key=settings.OPENAI_API_KEY,
    )

    # --- Vector store pointed at the shared collection ---
    collection_name = settings.QDRANT_COLLECTION
    qdrant_client = _get_qdrant_client()

    vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name=collection_name,
        embedding=embeddings,
    )

    # --- Retriever with user_id filter ---
    # QdrantVectorStore passes search_kwargs directly to similarity_search,
    # which accepts a `filter` argument of type qdrant_client.http.models.Filter.
    user_filter = qdrant_models.Filter(
        must=[
            qdrant_models.FieldCondition(
                key="metadata.user_id",
                match=qdrant_models.MatchValue(value=user_id),
            )
        ]
    )

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 5,
            "filter": user_filter,
        }
    )

    # --- LLM ---
    llm = ChatOpenAI(
        model_name=settings.CHAT_MODEL,   # ChatOpenAI uses model_name, not model
        temperature=0,
        openai_api_key=settings.OPENAI_API_KEY,
    )

    # --- LCEL chain ---
    # retrieve → format → prompt → llm → parse
    chain = (
        {
            "context": retriever | _format_docs,
            "question": RunnablePassthrough(),
        }
        | _PROMPT
        | llm
        | StrOutputParser()
    )

    answer = await chain.ainvoke(question)

    # --- Collect sources for the response ---
    retrieved_docs = await retriever.ainvoke(question)
    sources = [
        {
            "filename": doc.metadata.get("filename", "unknown"),
            "chunk_index": doc.metadata.get("chunk_index"),
            "document_id": doc.metadata.get("document_id"),
        }
        for doc in retrieved_docs
    ]

    return {"answer": answer, "sources": sources}
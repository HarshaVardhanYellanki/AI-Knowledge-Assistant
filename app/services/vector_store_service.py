import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)

client = QdrantClient(
    host="localhost",
    port=6333,
    timeout=60,
)

COLLECTION_NAME = "documents"


async def create_collection():

    collections = client.get_collections()

    exists = any(
        collection.name == COLLECTION_NAME
        for collection in collections.collections
    )

    if not exists:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=1536,
                distance=Distance.COSINE,
            ),
        )


async def store_embeddings(
    chunks: list[str],
    embeddings: list[list[float]],
    metadata: dict,
):

    BATCH_SIZE = 50

    for i in range(0, len(chunks), BATCH_SIZE):

        points = []

        batch_chunks = chunks[i:i+BATCH_SIZE]
        batch_embeddings = embeddings[i:i+BATCH_SIZE]

        for chunk, embedding in zip(
            batch_chunks,
            batch_embeddings,
        ):

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        **metadata,
                        "text": chunk,
                    },
                )
            )

        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
        )

async def search(
    query_embedding: list[float],
    user_id: str,
    limit: int = 5,
):

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit,
        query_filter={
            "must": [
                {
                    "key": "user_id",
                    "match": {
                        "value": user_id
                    }
                }
            ]
        }
    )

    return results.points
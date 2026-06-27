import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL"
)


async def generate_embedding(
    text: str
) -> list[float]:

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding


async def generate_embeddings(
    chunks: list[str]
) -> list[list[float]]:

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=chunks
    )

    return [
        item.embedding
        for item in response.data
    ]
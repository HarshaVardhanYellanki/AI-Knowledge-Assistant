import os

from dotenv import load_dotenv
from openai import OpenAI

from app.services.embedding_service import generate_embedding
from app.services.vector_store_service import search

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

CHAT_MODEL = os.getenv("CHAT_MODEL")


async def ask_question(
    question: str,
    current_user: dict,
):

    query_embedding = await generate_embedding(
        question
    )

    results = await search(
        query_embedding,
        str(current_user["_id"])
    )

    context = "\n\n".join(
        point.payload["text"]
        for point in results
    )

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the context below.

If the answer is not present, reply:

"I couldn't find the answer in the uploaded documents."

Context:

{context}

Question:

{question}
"""

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    return response.choices[0].message.content
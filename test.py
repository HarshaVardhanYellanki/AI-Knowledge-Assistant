from app.services.langchain.loader import load_document
from app.services.langchain.splitter import split_documents
from app.services.langchain.vectorstore import (
    add_documents,
    similarity_search,
)

docs = load_document("uploads/python.pdf")

chunks = split_documents(docs)

add_documents(chunks)

results = similarity_search("What is Python?")

print(results[0].page_content)
print(results[0].metadata)
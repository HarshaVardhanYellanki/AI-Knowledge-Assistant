# AI Knowledge Assistant (LangChain)

A secure Retrieval-Augmented Generation (RAG) application built with **FastAPI**, **LangChain**, **OpenAI**, **Qdrant**, and **MongoDB**.

The application enables authenticated users to upload documents and ask natural language questions. Each user's documents remain completely isolated using metadata-based filtering, ensuring private document retrieval.

---

## Features

* JWT Authentication
* User-specific document isolation
* PDF, DOCX and TXT support
* Automatic document chunking
* OpenAI Embeddings
* Qdrant Vector Database
* Semantic Search
* LangChain Retrieval Pipeline
* Source Chunk References
* FastAPI REST API
* MongoDB document metadata storage

---

## Tech Stack

* Python
* FastAPI
* LangChain
* OpenAI
* Qdrant
* MongoDB
* JWT Authentication
* PyMuPDF
* python-docx

---

## Architecture

```text
User
   │
   ▼
Upload Document
   │
   ▼
Document Loader
(PyPDF / DOCX / TXT)
   │
   ▼
RecursiveCharacterTextSplitter
   │
   ▼
OpenAI Embeddings
   │
   ▼
Qdrant Vector Store
   │
   ▼
───────────────
Question
   │
   ▼
Retriever
(User Metadata Filter)
   │
   ▼
Prompt
   │
   ▼
ChatOpenAI
   │
   ▼
Answer + Sources
```

---

## Project Structure

```text
app/
│
├── core/
├── database/
├── routes/
├── schemas/
├── services/
│
├── uploads/
│
main.py
requirements.txt
.env
```

---

## Environment Variables

```env
OPENAI_API_KEY=

CHAT_MODEL=gpt-4.1-mini
EMBEDDING_MODEL=text-embedding-3-small

QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=documents

MONGODB_URI=
DATABASE_NAME=

JWT_SECRET_KEY=
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## Installation

```bash
git clone <repository-url>

cd AI-Knowledge-Assistant

python -m venv venv

source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start MongoDB

Start Qdrant

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Run the application

```bash
uvicorn main:app --reload
```

---

## API Endpoints

### Authentication

```
POST /auth/register

POST /auth/login
```

### User

```
GET /users/me
```

### Documents

```
POST /documents/upload

GET /documents
```

### Chat

```
POST /chat
```

---

## Retrieval Pipeline

1. User uploads a document.
2. Document is parsed using LangChain loaders.
3. Text is split into semantic chunks.
4. Chunks are converted into embeddings.
5. Embeddings are stored in Qdrant.
6. User asks a question.
7. Relevant chunks are retrieved using metadata filtering.
8. Retrieved context is sent to ChatOpenAI.
9. Answer is returned with source references.

---

## Security

* JWT-based authentication
* User-level document isolation
* Metadata-filtered vector search
* Private retrieval per authenticated user

---

## Future Improvements

* Streaming responses
* Hybrid Search
* Reranking
* Document deletion
* Multi-file upload
* AWS deployment

---

## License

MIT

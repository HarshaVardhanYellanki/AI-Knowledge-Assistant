# AI Knowledge Assistant

A production-oriented Retrieval-Augmented Generation (RAG) backend built with FastAPI, MongoDB, OpenAI, and Qdrant.

The application enables authenticated users to upload documents, index them as vector embeddings, and ask natural language questions answered using only their uploaded documents.

---

## Features

* JWT Authentication
* User Registration & Login
* Secure API Endpoints
* Document Upload
* PDF, DOCX and TXT Support
* Automatic Text Extraction
* Text Chunking
* OpenAI Embedding Generation
* Qdrant Vector Database Integration
* Semantic Search
* Retrieval-Augmented Generation (RAG)
* User-wise Document Isolation

---

## Tech Stack

### Backend

* FastAPI
* Python 3.12

### Database

* MongoDB Atlas

### Vector Database

* Qdrant

### AI

* OpenAI Embeddings
* OpenAI Chat Models

### Authentication

* JWT
* Argon2 Password Hashing

---

## Project Structure

```
app
├── core
├── database
├── routes
├── schemas
├── services
├── main.py

uploads/
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/HarshaVardhanYellanki/AI-Knowledge-Assistant.git

cd AI-Knowledge-Assistant
```

Create a virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```
OPENAI_API_KEY=

EMBEDDING_MODEL=

CHAT_MODEL=

SECRET_KEY=

ALGORITHM=

ACCESS_TOKEN_EXPIRE_MINUTES=

MONGODB_URI=

DATABASE_NAME=
```

---

## Running Qdrant

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

Dashboard

```
http://localhost:6333/dashboard
```

---

## Run the API

```bash
uvicorn app.main:app --reload
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

## API Workflow

### 1. Register

```
POST /auth/register
```

### 2. Login

```
POST /auth/login
```

### 3. Upload Document

```
POST /documents/upload
```

Supported formats

* PDF
* DOCX
* TXT

The uploaded document is automatically

* Extracted
* Chunked
* Embedded
* Indexed in Qdrant

### 4. Chat

```
POST /chat
```

Ask questions about your uploaded documents.

The system retrieves the most relevant document chunks and generates answers using Retrieval-Augmented Generation (RAG).

---

## RAG Pipeline

```
User Upload
      │
      ▼
Document Storage
      │
      ▼
Text Extraction
      │
      ▼
Chunking
      │
      ▼
OpenAI Embeddings
      │
      ▼
Qdrant Storage
      │
      ▼
User Question
      │
      ▼
Query Embedding
      │
      ▼
Vector Search
      │
      ▼
Relevant Chunks
      │
      ▼
OpenAI Chat Model
      │
      ▼
Answer
```

---

## Security

* JWT Authentication
* Protected Routes
* Argon2 Password Hashing
* User-level Document Isolation

Each user retrieves information only from their own uploaded documents.

---

## Future Enhancements

* Streaming Responses
* Conversation History
* LangChain Integration
* LangGraph Agents
* Hybrid Search
* Metadata Filtering
* Background Document Processing
* Citations & Source References
* Multi-document Chat

---

## License

This project is intended for educational and research purposes.
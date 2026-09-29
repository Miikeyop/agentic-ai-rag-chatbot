# Agentic AI RAG Chatbot

A Retrieval-Augmented Generation chatbot built using Python, LangGraph, ChromaDB, FastEmbed, Groq, and FastAPI.

The chatbot answers questions strictly using information retrieved from the provided Agentic AI eBook.

## Live Demo

https://agentic-ai-rag-chatbot-z6ea.onrender.com

## 1. Setup Instructions

Clone the repository:

```bash
git clone https://github.com/Miikeyop/agentic-ai-rag-chatbot.git
cd agentic-ai-rag-chatbot
```

Create a virtual environment:

```bash
uv venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
uv pip install -r requirements.txt
```

Create a `.env` file in the project root and add:

```env
GROQ_API_KEY=your_groq_api_key
```

Create the vector database:

```bash
python rag/ingest.py
```

Run the application:

```bash
uv run uvicorn app:app --reload
```

Open the application in your browser:

```text
http://127.0.0.1:8000
```

## 2. Working RAG Chatbot

The chatbot returns:

- Final answer
- Retrieved context chunks
- Page numbers
- Retrieval distance scores
- Overall retrieval confidence

FastAPI documentation:

```text
/docs
```

Main chat endpoint:

```http
POST /chat
```

Example request:

```json
{
  "question": "What is Agentic AI?"
}
```

## 3. Sample Queries

1. What is Agentic AI?
2. How is Agentic AI different from traditional AI?
3. What are the key characteristics of Agentic AI?
4. What are autonomous AI agents?
5. How do multi-agent systems work?
6. What are some real-world applications of Agentic AI?

## 4. Short Architecture Explanation

The application follows this RAG pipeline:

```text
Agentic AI PDF
      |
      v
PyPDFLoader
      |
      v
Recursive Text Chunking
      |
      v
FastEmbed Embeddings
      |
      v
ChromaDB
      |
      v
User Question
      |
      v
LangGraph Retrieve Node
      |
      v
Relevant Context Chunks
      |
      v
LangGraph Generate Node
      |
      v
Groq LLM
      |
      v
Final Grounded Answer
```

The Agentic AI PDF is loaded using `PyPDFLoader` and split into smaller chunks using `RecursiveCharacterTextSplitter`.

Each chunk is converted into an embedding using the `BAAI/bge-small-en-v1.5` embedding model and stored in ChromaDB.

When a user asks a question, the LangGraph retrieve node searches ChromaDB and returns the most relevant chunks.

The retrieved chunks are passed to the generate node, where the Groq LLM generates the final answer using only the provided context.

If the required information is not available in the retrieved context, the chatbot returns:

```text
I could not find enough information in the provided knowledge base.
```

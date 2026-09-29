# Agentic AI RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built using **Python, LangGraph, ChromaDB, FastEmbed, Groq, and FastAPI**.

The chatbot answers questions strictly using information retrieved from the provided **Agentic AI eBook**.

## Live Demo

https://agentic-ai-rag-chatbot-z6ea.onrender.com

## Features

- PDF ingestion and text extraction
- Recursive document chunking
- Vector embeddings using `BAAI/bge-small-en-v1.5`
- ChromaDB vector storage
- Semantic similarity search
- LangGraph-based RAG workflow
- Groq-powered LLM response generation
- Answers grounded only in retrieved eBook context
- Retrieved chunks displayed with page numbers
- Vector distance scores for every retrieved chunk
- Overall retrieval confidence score
- FastAPI REST API
- Interactive dark-theme chatbot UI
- View and download the source PDF
- Swagger API documentation

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| API Framework | FastAPI |
| RAG Orchestration | LangGraph |
| LLM | Groq |
| LLM Model | `openai/gpt-oss-120b` |
| Embeddings | FastEmbed |
| Embedding Model | `BAAI/bge-small-en-v1.5` |
| Vector Database | ChromaDB |
| PDF Loader | PyPDFLoader |
| Text Splitting | RecursiveCharacterTextSplitter |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Render |

## Architecture

The application follows a simple Retrieval-Augmented Generation pipeline:

```text
                     Agentic AI eBook
                            |
                            v
                       PyPDFLoader
                            |
                            v
             RecursiveCharacterTextSplitter
                            |
                            v
                 FastEmbed Embeddings
                            |
                            v
                        ChromaDB
                            |
                            |
User Question               |
     |                      |
     v                      |
 FastAPI /chat              |
     |                      |
     v                      |
  LangGraph                 |
     |                      |
     v                      |
Retrieve Relevant Chunks <--+
     |
     v
Build Grounded Context
     |
     v
Groq LLM
     |
     v
Final Answer
     |
     +--> Retrieved Chunks
     +--> Page Numbers
     +--> Distance Scores
     +--> Retrieval Confidence

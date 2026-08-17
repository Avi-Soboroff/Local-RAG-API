# Local Multi-User RAG API

A locally hosted Retrieval Augmented Generation (RAG) API built using **FastAPI**, **ChromaDB**, and **Ollama**. This service allows users to ingest personal profile documents, generate vector embeddings, and perform semantically grounded Q&A using local LLMs with zero cloud API costs.

## Key Capabilities

- Embeddings: Generates 768-dimension vectors using `nomic-embed-text` and answers queries via local LLMs (`qwen2.5:0.5b`).
- Multi-User Filtering: Uses ChromaDB metadata filtering to isolate document context between users.
- Interaction: Automatically generates interactive API testing pages via SwaggerUI.

## Tech Stack

**Languages:** Python
**API Framework:** FastAPI, Uvicorn, Pydantic
**Vector Database:** ChromaDB
**Local AI Engine:** Ollama (`nomic-embed-text`, `qwen2.5:0.5b`)


## Getting Started

### Prerequisites

1. Ensure **Ollama** is running locally on port `11434`

   ```bash
   curl http://localhost:11434

2. Pull all required models:
 
   ```bash
   ollama pull nomic-embed-text
   ollama pull qwen2.5:0.5b

### Setup and Execution
1. Activate virtual environment and install dependencies

   ```bash
   source venv/bin/activate
   pip install fastapi uvicorn chromadb ollama pydantic

2. Start FastAPI server

   ```bash
   uvicorn main:app --reload

3. Access interactive API in browser using: http://127.0.0.1:8000/docs

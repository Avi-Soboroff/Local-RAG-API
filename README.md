# Local Multi-User RAG API
[![FastAPI & RAG Integration Tests](https://github.com/Avi-Soboroff/Local-RAG-API/actions/workflows/ci.yml/badge.svg)](https://github.com/Avi-Soboroff/Local-RAG-API/actions/workflows/ci.yml)

A locally hosted Retrieval Augmented Generation (RAG) API built using **FastAPI**, **ChromaDB**, and **Ollama**. This service allows users to ingest personal profile documents, generate vector embeddings, and perform semantically grounded Q&A using local LLMs with zero cloud API costs.

## Key Capabilities

- Embeddings: Generates 768-dimension vectors using `nomic-embed-text` and answers queries via local LLMs (`qwen2.5:0.5b`).
- Multi-User Filtering: Uses ChromaDB metadata filtering to isolate document context between users.
- Interaction: Automatically generates interactive API testing pages via SwaggerUI.
- Automated Integration Testing: Uses Pytest and FastAPI's TestClient to verify schema validation, multi-paragraph chunking, and tenant isolation.
- Continuous Integration: A GitHub Actions workflow automatically builds an Ubuntu runner, sets up Python 3.14.3, starts the Ollama daemon, pulls nomic-embed-text / qwen2.5:0.5b, and runs test suites on every push to main.

## Tech Stack

**Languages:** Python
**API Framework:** FastAPI, Uvicorn, Pydantic
**Vector Database:** ChromaDB
**Local AI Engine:** Ollama (`nomic-embed-text`, `qwen2.5:0.5b`)
**Testing & CI/CD:** Pytest, httpx, GitHub Actions


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

## Automated Testing

Run the integration tests locally

```bash
pytest -v

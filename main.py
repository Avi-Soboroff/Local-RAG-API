from fastapi import FastAPI
from pydantic import BaseModel
import ollama
import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)

app = FastAPI()

# connect to the knowledge base
client = chromadb.PersistentClient(path="./myRAGchromaDB")

# Connect to Ollama's servers to convert text into embeddings
embed = OllamaEmbeddingFunction(
    model_name="nomic-embed-text",
    url="http://localhost:11434",
)

# Create collection/table to be reused to find/collect/store data
collection = client.get_or_create_collection(
    name="personal_profile",
    embedding_function=embed,
)

# Every time a user submits a new profile, it must contain a username and a context
class ProfileSubmission(BaseModel):
    user_name: str
    content: str

@app.post("/profiles")
# Splits new profile into chunks and stores each chunk in chromaDB with users name as metadata
def add_profile(submission: ProfileSubmission):
    chunks = [chunk.strip() for chunk in submission.content.split("\n\n") if chunk.strip()]
    collection.add(
        ids=[f"{submission.user_name}-chunk{i}" for i in range(len(chunks))],
        documents=chunks,
        metadatas=[
            {"source": "profile", "user_name": submission.user_name, "chunk_index": i}
            for i in range(len(chunks))  # user_name metadata lets us filter by user later
        ],
    )
    return {
        "message": f"Added {len(chunks)} chunks for user '{submission.user_name}'.",
        "user_name": submission.user_name,
        "chunks_added": len(chunks),
    }

''' Create the GET endpoint at /ask, which will read a question from the URL query, search the chromaDB for the 2 most relevant
    chunks, and then combine those chunks. '''
@app.get("/ask")
def ask(question: str, user: str = None):
    query_params = {
        "query_texts": [question],  
        "n_results": 2,
    }

    # If a user was provided, then search that users chunk in DB   
    if user:
        query_params["where"] = {"user_name": user}

    # Otherwise check for most relevant chunks and unpack data into keyword args
    results = collection.query(**query_params)
    context = "\n\n".join(results["documents"][0])

    # Generates a prompt from the retrived context
    augmented_prompt = f"""Use the following context to answer the question.
If the context doesn't contain relevant information, say so.

Context:
{context}

Question: {question}"""
    
    # Send prompt to LLM, which is ollama in this case
    response = ollama.chat(
        model="qwen2.5:0.5b",
        messages=[{"role": "user", "content": augmented_prompt}],
    )

    # Returns the answer along with context so users can verify
    return {
        "question": question,
        "answer": response["message"]["content"],
        "context_used": results["documents"][0],
        "filtered_by_user": user,
    }

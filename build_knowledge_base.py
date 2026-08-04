import chromadb
# allows chromadb to caluate vector coordinates on it own and connect the database to my ollama server
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)

with open("profile.txt", "r") as f:
    text = f.read()

# splits document into paragraph and ensures no emoty strings are added
chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
print(f"Loaded {len(chunks)} chunks from profile.txt")

# Intialize ChromaDB database and keep files and data existant even after restarts
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

# Add the chunks of texts to the embeddings by creating a unique id for each chunk, providing the raw/whole text, creating filters for those chunks
collection.add(
    ids=[f"chunk{i}" for i in range(len(chunks))],  
    documents=chunks,  # The actual text content
    metadatas=[{"source": "profile", "chunk_index": i} for i in range(len(chunks))],
)
print(f"Added {len(chunks)} chunks to the 'personal_profile' collection.")
print("Knowledge base built successfully!")

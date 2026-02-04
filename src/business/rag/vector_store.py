"""Chroma vector store wrapper."""
"""
For the production level RAG - Chatbot system, the vector databases like weaviate or pinecone are preferred.
Replace the ChromaDB with those vector DBs for better scalability and performace in Production systems.
"""
from __future__ import annotations

from typing import List, Dict, Any
import chromadb
from chromadb.utils import embedding_functions


class VectorStore:
    def __init__(self, persist_dir: str, collection_name: str = "pdf_chunks", dim: int | None = None):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=None,  # we supply embeddings manually
        )
        self.dim = dim

    def reset(self):
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(self.collection.name)

    def upsert(
        self,
        ids: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]],
        documents: List[str],
    ):
        # check the lengths matches for ids, embeddings, metadatas, documents
        if len(ids) != len(embeddings):
            raise ValueError("ids and embeddings length mismatch")
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents,
        )
    # Run the similarity search and return top_k results
    def query(self, query_embedding: List[float], top_k: int = 15):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

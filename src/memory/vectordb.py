from typing import List, Dict, Optional
from chromadb import Client
from chromadb.config import Settings


class VectorDB:
    """
    Low-level vector database adapter.
    No AI logic. No memory semantics.
    """

    def __init__(
        self,
        collection_name: str,
        persist_directory: str = "./chroma",
    ):
        self.client = Client(
            Settings(persist_directory=persist_directory)
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add(
        self,
        ids: List[str],
        embeddings: List[List[float]],
        documents: List[str],
        metadatas: List[Dict],
    ) -> None:
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def search(
        self,
        embedding: List[float],
        top_k: int = 5,
        filters: Optional[Dict] = None,
    ) -> List[Dict]:
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            where=filters,
        )

        return [
            {
                "text": doc,
                "metadata": meta,
                "score": score,
            }
            for doc, meta, score in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ]

    def delete(self, filters: Dict) -> None:
        self.collection.delete(where=filters)
"""Embedding interfaces and OpenAI implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from openai import OpenAI


class Embedder(ABC):
    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        ...

    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        ...
    
    def embed(self, text: str) -> List[float]:
        """
        Alias for embed_query() for backward compatibility with LongTermMemory.
        """
        return self.embed_query(text)


class OpenAIEmbedder(Embedder):
    """
    Thin wrapper over OpenAI embeddings.
    Uses text-embedding-3-small by default (fast, 1536 dims).
    """

    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def _embed(self, inputs: List[str]) -> List[List[float]]:
        res = self.client.embeddings.create(model=self.model, input=inputs)
        return [item.embedding for item in res.data]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        return self._embed(texts)

    def embed_query(self, text: str) -> List[float]:
        return self._embed([text])[0]

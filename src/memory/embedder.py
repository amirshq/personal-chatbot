# Here is the implementation of an embedding model using Hugging Face sentence-transformers.
# we gonna use the 'sentence-transformers/all-MiniLM-L6-v2' model for generating embeddings instead of 
# Raw Hugging Face Embedding model because if we use raw model we have to do pre and post processing of text manually like 
# tokenization, padding etc. but sentence-transformers library handle all these things internally and provide us easy to use interface.

from typing import List
import torch 
from sentence_transformers import SentenceTransformer
class Embedder:
    """
    Embedding model using Hugging Face sentence-transformers.
    """

    def __init__(self, model_name: str = "BAAI/bge-large-en-v1.5", device: str | None = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = SentenceTransformer(model_name, device = self.device)

    def embed_text(self, text: List[str]) -> List[List[float]]:
        """
        Embed a single text string.
        """
        embeddings = self.model.encode(text, normalize_embeddings=True, convert_to_tensor=True)
        return embeddings.tolist()

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of text strings.
        """
        embeddings = self.model.encode(texts, batch_size=32, normalize_embeddings=True, convert_to_tensor=True)
        return embeddings.tolist()
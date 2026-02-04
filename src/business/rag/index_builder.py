"""Index builder:
Ingests PDFs → extracts text and tables
Chunks → splits into smaller pieces
Embeds → converts text to vectors
Stores → saves to vector database (line 78)
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Tuple

from dotenv import load_dotenv

from .pdfingest.unstructure_pdf_digest import ingest_directory, IngestedDocument
from .pdfingest.chunk import Chunker, Chunk
from ..core.embedding import OpenAIEmbedder
from .vector_store import VectorStore


def _chunk_document(doc: IngestedDocument, chunker: Chunker, table_start_idx: int | None) -> List[Chunk]:
    source_metadata = {"source_id": doc.source_id}
    chunks = chunker.split(doc.combined_text, source_metadata=source_metadata)
    enriched = []
    for ch in chunks:
        md = dict(ch.metadata)
        section = "table" if table_start_idx is not None and md.get("chunk_start", 0) >= table_start_idx else "text"
        md.update({"source_id": doc.source_id, "section": section})
        enriched.append(Chunk(chunk_id=ch.chunk_id, text=ch.text, metadata=md))
    return enriched


def build_index(
    data_dir: Path,
    persist_dir: Path,
    max_context_chars: int = 12_000,
    include_table_images: bool = True,
    chunk_size: int = 800,
    overlap: int = 100,
    top_k_store: int | None = None,
) -> Tuple[int, int]:
    """
    Build or rebuild the vector index from PDFs.
    Returns (docs_indexed, chunks_indexed).
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY missing in environment")

    docs = ingest_directory(
        data_dir=data_dir,
        max_context_chars=max_context_chars,
        include_table_images=include_table_images,
    )

    embedder = OpenAIEmbedder(api_key=api_key)
    vstore = VectorStore(persist_dir=str(persist_dir))
    chunker = Chunker(chunk_size=chunk_size, overlap=overlap)

    all_chunks: List[Chunk] = []
    for doc in docs:
        table_marker = None
        if doc.table_text:
            # compute start idx of table section for provenance tagging
            marker = "\n\n" + "=" * 80 + "\nTABLES FROM DOCUMENT IMAGES:\n" + "=" * 80 + "\n"
            table_marker = doc.combined_text.find(marker)
            if table_marker == -1:
                table_marker = None
        doc_chunks = _chunk_document(doc, chunker, table_start_idx=table_marker)
        all_chunks.extend(doc_chunks)

    if top_k_store:
        all_chunks = all_chunks[:top_k_store]

    texts = [c.text for c in all_chunks]
    embeddings = embedder.embed_documents(texts)
    ids = [c.chunk_id for c in all_chunks]
    metadatas = [c.metadata for c in all_chunks]

    vstore.upsert(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=texts)

    return len(docs), len(all_chunks)
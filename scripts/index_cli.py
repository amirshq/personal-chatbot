#You don’t need the CLI entrypoint if you don’t plan to trigger indexing from the terminal. 
# It’s just a convenience wrapper around build_index() for ad‑hoc/manual runs (or automation/cron). 
# If you always trigger indexing from code, you can ignore or remove scripts/index_cli.py.
"""
This is the CLI entrypoint to build or rebuild the RAG index using Terminal commands.
The rebuild command is the CLI entrypoint: you can run it from the terminal to 
rebuild the vector index with custom options. For example:

python scripts/rebuild_index.py rebuild \
  --data-dir src/business/rag/data \
  --persist-dir src/business/rag/vectorstore \
  --max-context-chars 12000 \
  --chunk-size 800 \
  --overlap 100 \
  --include-table-images true

This ingests your PDFs, chunks them, embeds them, and saves the index to the specified persist_dir.
"""
from pathlib import Path
import typer
from src.business.rag.index_builder import build_index

app = typer.Typer(add_completion=False)
"""
persist_dir is the folder on disk where the Chroma vector database is persisted. 
When build_index() runs, it writes the collection data there—chunk IDs, embeddings, 
documents (chunk text), and metadata—so the vector store survives restarts. 
By default (in rebuild_index.py) it points to src/business/rag/vectorstore, 
but you can change it via the CLI option.
"""

@app.command()
def rebuild(
    data_dir: Path = typer.Option("src/business/rag/data", help="Directory with PDFs"),
    persist_dir: Path = typer.Option("src/business/rag/vectorstore", help="Chroma persistence directory"),
    max_context_chars: int = typer.Option(12_000, help="Max combined text per document"),
    include_table_images: bool = typer.Option(True, help="Process table images via Unstructured API if configured"),
    chunk_size: int = typer.Option(800, help="Chunk size (characters)"),
    overlap: int = typer.Option(100, help="Chunk overlap (characters)"),
):
    docs, chunks = build_index(
        data_dir=data_dir,
        persist_dir=persist_dir,
        max_context_chars=max_context_chars,
        include_table_images=include_table_images,
        chunk_size=chunk_size,
        overlap=overlap,
    )
    typer.echo(f"Indexed {docs} document(s), {chunks} chunk(s) → {persist_dir}")


if __name__ == "__main__":
    app()

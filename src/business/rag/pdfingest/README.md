# PDF Ingestion Pipeline
After benchmarking multiple PDF extraction strategies, this approach demonstrated the highest reliability and structural fidelity. The Unstructured library substantially improves document ingestion by preserving layout, sections, and tables, making it a foundational component of the RAG pipeline.
You can read the Unstructured library here: [https://github.com/Unstructured-IO/unstructured](https://github.com/Unstructured-IO/unstructured)

This module implements a comprehensive PDF processing pipeline that extracts both text content and table data from PDF documents for use in RAG (Retrieval-Augmented Generation) systems.

## Overview

The PDF ingestion process uses a two-stage approach:
1. **Primary Extraction**: Uses the `unstructured` library to extract main text content directly from the PDF
2. **Table Processing**: Extracts tables as images, then processes them using the Unstructured API to convert table images into structured JSON data

## Architecture

```
PDF Document
    ↓
unstructured.partition_pdf()
    ↓
┌─────────────────────────┬─────────────────────────┐
│   Main PDF Text         │   Table Images (JPG)     │
│   (Title, Narrative,    │   (Extracted to         │
│    List Items, Tables)  │    artifacts/images/)   │
└─────────────────────────┴─────────────────────────┘
    ↓                              ↓
Combined Text              process_table_images.py
    ↓                              ↓
DOCUMENT_TEXT              Table JSON Files
    ↓                    (artifacts/tables_json/)
    ↓
GPT Q&A System
```

## Components

### 1. `unstructure_pdf_digest.py`

Main script that orchestrates the PDF ingestion process.

**Responsibilities:**
- Extracts text content from PDF using `unstructured.partition.pdf`
- Extracts table images and saves them as JPG files
- Processes table images using `process_table_images.py`
- Combines PDF text and table content into a single document
- Provides interactive Q&A interface using GPT

**Key Features:**
- Uses `hi_res` strategy for high-quality extraction
- Extracts images and tables to `artifacts/images/`
- Automatically processes table images when `UNSTRUCTURED_API_KEY` is set
- Combines all content for comprehensive Q&A

**Usage:**
```bash
python src/business/rag/pdfingest/unstructure_pdf_digest.py
```

### 2. `process_table_images.py`

Processes JPG images containing tables and extracts structured table content.

**Responsibilities:**
- Processes all JPG images in `artifacts/images/`
- Uses Unstructured API to extract table content from images
- Converts table images to structured JSON format
- Extracts table text for inclusion in document context

**Key Functions:**
- `extract_table_text_from_images()`: Main function that processes images and returns table text
- `process_image()`: Processes a single image using Unstructured API
- `filter_tables()`: Filters elements to extract only table data
- `save_to_json()`: Saves table data to JSON files for reference

**Output:**
- JSON files saved to `artifacts/tables_json/` (one per image)
- Table text content returned for inclusion in document

**Usage:**
```bash
python src/business/rag/pdfingest/process_table_images.py
```

## Workflow

### Step 1: PDF Processing

The `unstructured` library processes the PDF:

```python
elements = partition_pdf(
    filename=PDF_PATH,
    strategy="hi_res",                    # High-resolution extraction
    skip_infer_table_types=False,         # Extract table types
    languages=["eng"],                     # English language
    extract_images_in_pdf=True,            # Extract images
    extract_image_block_types=["Image", "Table"],  # Extract tables as images
    extract_image_block_output_dir=IMAGE_DIR,      # Save to artifacts/images/
)
```

**What it extracts:**
- **Text Elements**: Title, NarrativeText, ListItem, Table (direct text)
- **Table Images**: Tables saved as JPG files in `artifacts/images/`

### Step 2: Table Image Processing

When `UNSTRUCTURED_API_KEY` is configured, the script automatically:

1. Finds all JPG images in `artifacts/images/`
2. Processes each image using Unstructured API
3. Extracts table content from images
4. Saves structured JSON to `artifacts/tables_json/`
5. Returns table text for document inclusion

**Why this approach?**
- PDF tables are often complex with merged cells, formatting, etc.
- Extracting tables as images preserves visual structure
- Unstructured API's `hi_res` strategy provides better table recognition
- JSON format allows structured access to table data

### Step 3: Document Assembly

The final document combines:

1. **PDF Text Content**: Title, NarrativeText, ListItem, Table elements
2. **Table Content from Images**: Text extracted from table images

```python
DOCUMENT_TEXT = PDF_TEXT + "\n\n" + "TABLES FROM DOCUMENT IMAGES:\n" + TABLE_TEXT
```

### Step 4: Q&A Interface

The combined document is used for question answering:

- Users can ask questions about PDF content
- GPT has access to both PDF text and table data
- Answers are based on the complete document context

## Dependencies

### Required Libraries

- **unstructured**: PDF parsing and text extraction
  ```bash
  pip install unstructured
  ```

- **unstructured-client**: API client for table image processing
  ```bash
  pip install unstructured-client
  ```

- **openai**: GPT integration for Q&A
  ```bash
  pip install openai
  ```

- **python-dotenv**: Environment variable management
  ```bash
  pip install python-dotenv
  ```

### Environment Variables

Create a `.env` file in the project root:

```env
# Required for Q&A functionality
OPENAI_API_KEY=your_openai_api_key_here

# Required for table image processing
UNSTRUCTURED_API_KEY=your_unstructured_api_key_here
```

## Directory Structure

```
src/business/rag/pdfingest/
├── README.md                          # This file
├── unstructure_pdf_digest.py         # Main PDF processing script
├── process_table_images.py            # Table image processing
├── chunk.py                           # Text chunking utilities
├── artifacts/
│   ├── images/                       # Extracted table images (JPG)
│   │   ├── table-5-1.jpg
│   │   ├── table-6-2.jpg
│   │   └── ...
│   └── tables_json/                   # Processed table data (JSON)
│       ├── table-5-1_tables.json
│       ├── table-6-2_tables.json
│       └── ...
└── data/                              # Input PDF files
    └── kthproject.pdf
```

## How It Works

### Why Two-Stage Processing?

1. **Main Text Extraction**: The `unstructured` library efficiently extracts text content directly from PDF. This works well for:
   - Paragraphs and narrative text
   - Simple tables with clear structure
   - Lists and headings

2. **Table Image Processing**: Complex tables are better handled as images because:
   - PDF table structure can be inconsistent
   - Visual layout is preserved in images
   - Unstructured API's vision models excel at table recognition
   - Better handling of merged cells, formatting, and complex layouts

### Integration Flow

When `unstructure_pdf_digest.py` runs:

1. **PDF Processing** → Extracts text and saves table images
2. **Automatic Table Processing** → Calls `process_table_images.py` if API key is set
3. **Content Combination** → Merges PDF text and table content
4. **Q&A Ready** → Complete document available for questions

## Example Usage

### Basic Usage

```bash
# Run the main script
python src/business/rag/pdfingest/unstructure_pdf_digest.py

# The script will:
# 1. Process PDF and extract images
# 2. Process table images (if API key set)
# 3. Start interactive Q&A session
```

### Interactive Q&A

```
💬 Ask questions about the PDF (type 'exit' to quit)
   Type 'debug' before your question to see what's sent to GPT

❓ Question: What is the conclusion of this paper?
🧠 Answer: [GPT response based on PDF content]

❓ Question: debug What data is in table 5-1?
🧠 Answer: [Shows debug info + GPT response]
```

## Output Formats

### Table JSON Structure

Each table JSON file contains:

```json
[
  {
    "type": "Table",
    "element_id": "abc123...",
    "text": "Raw table text content...",
    "metadata": {
      "text_as_html": "<table><tbody>...</tbody></table>",
      "filetype": "image/jpeg",
      "page_number": 1,
      "filename": "table-5-1.jpg"
    }
  }
]
```

**Key Fields:**
- `text`: Plain text representation of the table
- `metadata.text_as_html`: HTML table structure for structured access
- `metadata.filename`: Source image filename

## Limitations

1. **API Dependency**: Table image processing requires `UNSTRUCTURED_API_KEY`
2. **Context Limits**: Document text is truncated to 12,000 characters by default
3. **Image Quality**: Table extraction quality depends on image resolution
4. **Language Support**: Currently optimized for English (`languages=["eng"]`)

## Troubleshooting

### Tables Not Being Processed

- Check if `UNSTRUCTURED_API_KEY` is set in `.env`
- Verify images exist in `artifacts/images/`
- Check API key validity and quota

### PDF Text Not Included

- Check debug output for extracted categories
- Verify PDF contains expected text elements
- Review truncation warnings in output

### Import Errors

- Ensure all dependencies are installed
- Check Python path if running as script
- Verify relative imports work correctly

## Future Improvements

- [ ] Support for multiple languages
- [ ] Configurable context length limits
- [ ] Batch processing for multiple PDFs
- [ ] Caching of processed table data
- [ ] Integration with vector database for RAG
- [ ] Support for other document formats (DOCX, etc.)

## References

- [Unstructured Documentation](https://unstructured.io/)
- [Unstructured API](https://unstructured.io/api)
- [OpenAI API](https://platform.openai.com/docs)

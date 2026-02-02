"""
Process the tables were extracted as jpg 
Process JPG images containing tables and save table content to JSON files.

This script processes all JPG images in the artifacts/images directory,
extracts table content using the Unstructured API, and saves the results
to JSON files.
"""
import os
import json
from pathlib import Path
from typing import List, Dict, Any

from dotenv import load_dotenv
import unstructured_client
from unstructured_client.models import operations, shared

# ============================================================
# Environment Setup
# ============================================================
load_dotenv()
UNSTRUCTURED_API_KEY = os.getenv("UNSTRUCTURED_API_KEY")

# Initialize client lazily (only when needed)
_client = None

def get_client():
    """Get or create Unstructured API client."""
    global _client
    if _client is None:
        if not UNSTRUCTURED_API_KEY:
            raise ValueError("UNSTRUCTURED_API_KEY not found in .env")
        _client = unstructured_client.UnstructuredClient(
            api_key_auth=UNSTRUCTURED_API_KEY
        )
    return _client


# ============================================================
# Path Configuration
# ============================================================
# Images directory relative to script location
SCRIPT_DIR = Path(__file__).parent
IMAGE_DIR = SCRIPT_DIR / "artifacts" / "images"
OUTPUT_DIR = SCRIPT_DIR / "artifacts" / "tables_json"

# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Image Processing Functions
# ============================================================
def process_image(image_path: Path) -> List[Dict[str, Any]]:
    """
    Process a single image file and extract table content.
    Args:
        image_path: Path to the JPG image file
    Returns:
        List of element dictionaries containing table data
    """
    print(f"📸 Processing: {image_path.name}")
    
    # This Try  builds and sends a typed Unstructured API request to parse an image using HI_RES OCR + layout detection.
    #It returns the structured elements (tables, text, layout blocks) extracted from that image.

    try:
        client = get_client()
        req = operations.PartitionRequest(
            partition_parameters=shared.PartitionParameters(
                files=shared.Files(
                    content=open(image_path, "rb"),
                    file_name=image_path.name,
                ),
                strategy=shared.Strategy.HI_RES,  # Required for images
                languages=['eng'],
            ),
        )
        
        res = client.general.partition(request=req)
        element_dicts = [element for element in res.elements]
        
        return element_dicts
        # element_dicts contains all elements from the image (tables, text, etc.)
        
    except Exception as e:
        print(f"❌ Error processing {image_path.name}: {e}")
        return []

#element_dicts contains all elements from the image (tables, text, etc.) but we only want the tables, so
# we filter them out in the next function.
def filter_tables(elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        element for element in elements
        if element.get("type") == "Table"
    ]

def save_to_json(elements: List[Dict[str, Any]], output_path: Path) -> None:
    """
    Save elements to a JSON file.
    Args:
        elements: List of element dictionaries
        output_path: Path to save JSON file
    """
    json_content = json.dumps(elements, indent=2, default=str) 
    
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(json_content)
    
    print(f"✅ Saved: {output_path.name} ({len(elements)} tables)")
    
# ============================================================
# Table Text Extraction Function
# ============================================================
# Now that we have the tables seperately, we can extract the text from them.

def extract_table_text_from_images(image_dir: Path = None) -> str:
    """
    Process all JPG images containing tables and extract table text content.
    Args:
        image_dir: Directory containing images (defaults to IMAGE_DIR)
    Returns:
        Combined text content from all tables found in images
    """
    if image_dir is None:
        image_dir = IMAGE_DIR
    
    # Find all JPG/JPEG images
    image_extensions = [".jpg", ".jpeg", ".JPG", ".JPEG"]
    image_files = [
        f for f in image_dir.iterdir()
        if f.is_file() and f.suffix in image_extensions
    ]
    
    if not image_files:
        print(f"⚠️  No JPG images found in {image_dir}")
        return ""
    
    print(f"\n🔍 Processing {len(image_files)} table image(s)...\n")
    
    all_table_texts = []
    total_tables = 0
    
    for image_path in image_files:
        # Process image
        elements = process_image(image_path)
        
        # Filter for tables only
        tables = filter_tables(elements)
        
        if tables:
            # Extract text from each table
            for table in tables:
                table_text = table.get("text", "")
                if table_text:
                    all_table_texts.append(f"\n[Table from {image_path.name}]\n{table_text}")
                    total_tables += 1
            
            # Optionally save to JSON
            output_filename = image_path.stem + "_tables.json"
            output_path = OUTPUT_DIR / output_filename
            save_to_json(tables, output_path)
        else:
            print(f"⚠️  No tables found in {image_path.name}")
    
    combined_text = "\n\n".join(all_table_texts)
    print(f"\n✅ Extracted {total_tables} table(s) from images")
    
    return combined_text


# ============================================================
# Main Processing Function
# ============================================================
def process_all_images() -> None:
    """
    Use functions process_image, filter_tables, and save_to_json to:
    Process all JPG images in the images directory and save table content to JSON.
    Extracts all elements from images, filters to keep only table text, and saves to JSON.
    """
    image_extensions = [".jpg", ".jpeg", ".JPG", ".JPEG"]
    image_files = [
        f for f in IMAGE_DIR.iterdir()
        if f.is_file() and f.suffix in image_extensions
    ]
    
    if not image_files:
        print(f"⚠️  No JPG images found in {IMAGE_DIR}")
        return
    
    for image_path in image_files:
        elements = process_image(image_path)
        tables = filter_tables(elements)
        
        if tables:
            output_filename = image_path.stem + "_tables.json"
            output_path = OUTPUT_DIR / output_filename
            save_to_json(tables, output_path)


# ============================================================
# Entry Point
# ============================================================
if __name__ == "__main__":
    process_all_images()

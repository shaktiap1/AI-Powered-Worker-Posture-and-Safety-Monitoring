"""
Chunker
Build semantic chunks + metadata from clean PDFs
Run:
    python -m ingestion.chunker
"""

import json
import uuid
from pathlib import Path

from ingestion.loader import load_pdf_elements
from ingestion.cleaner import clean_text, is_valid_chunk


# =========================
# CONFIG
# =========================

MAX_CHARS = 2000
MIN_CHARS = 40


# =========================
# PATHS
# =========================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

PDF_FILE = DATA_DIR / "vectors_notes.pdf"   # ⭐ changed
OUTPUT_FILE = DATA_DIR / "chunks.json"


# Metadata for each chunk will include page number, section title (if available), and source document name, 
# which will help in providing context to the LLM when generating answers based on the retrieved chunks.

def make_chunk(text, meta):
    return {
        "id": str(uuid.uuid4()),
        "text": text.strip(),
        "metadata": meta.copy(),
        "length": len(text)
    }


# MAIN function to build chunks from the PDF file, which reads the PDF, extracts elements, cleans the text, 
# and creates chunks based on the defined MAX_CHARS limit, while also maintaining metadata for each chunk. 
# The resulting chunks are saved to a JSON file for later use in the RAG pipeline.


def build_chunks(pdf_path: Path, output_path: Path):

    print(f"Reading → {pdf_path}")

    elements = load_pdf_elements(str(pdf_path))
    print(f"Loaded {len(elements)} elements")

    chunks = []

    current_text = ""
    current_meta = {
        "page": None,
        "section": "",
        "source": pdf_path.name
    }

    for el in elements: # here we will loop through each element extracted from the PDF, clean the text, and check if it meets the minimum character requirement for a valid chunk.
                        #  If it does, we will update the current chunk text and metadata accordingly, and if adding the new text exceeds the maximum character limit, we will save the current chunk and start a new one. 
                         # We will also handle section titles by updating the metadata when we encounter elements categorized as "Title".

        text = clean_text(str(el))
        if not is_valid_chunk(text, MIN_CHARS):
            continue
        
        meta = getattr(el, "metadata", {})
        page = getattr(meta, "page_number", None)
        category = getattr(el, "category", "")

        if category == "Title":
            current_meta["section"] = text

        if len(current_text) + len(text) > MAX_CHARS:
            chunks.append(make_chunk(current_text, current_meta))
            current_text = ""

        current_text += text + "\n"
        current_meta["page"] = page

    if current_text:
        chunks.append(make_chunk(current_text, current_meta)) # this will ensure that any remaining text that has not been saved as a chunk due to not reaching the maximum character limit will be saved as a final chunk after the loop.

    unique = list({c["text"]: c for c in chunks}.values())

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(unique, f, indent=2, ensure_ascii=False)  # this will save the unique chunks to a JSON file at the specified output path, with indentation for readability and ensuring that non-ASCII characters are preserved correctly in the output file.

    print(f"Saved {len(unique)} chunks → {output_path}")


if __name__ == "__main__":
    build_chunks(PDF_FILE, OUTPUT_FILE)

# THANKYOU JI FOR REVIEWING MY CODE HOPING TO CONNECT WITH U FOR THE NEXT ROUND OF INTERVIEW :) SHAKTESH
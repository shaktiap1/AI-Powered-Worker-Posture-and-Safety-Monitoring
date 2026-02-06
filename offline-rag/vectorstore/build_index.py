"""
Build FAISS index from chunks.json

Run:
    python -m vectorstore.build_index
"""

import json
from pathlib import Path
import numpy as np

from embeddings.embedder import Embedder
from vectorstore.faiss_store import FAISSStore


# =========================
# PATHS
# =========================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
INDEX_DIR = PROJECT_ROOT / "indexes"

CHUNKS_FILE = DATA_DIR / "chunks.json"
INDEX_FILE = INDEX_DIR / "faiss.index"
META_FILE = INDEX_DIR / "metadata.pkl"


# =========================
# MAIN
# =========================

def main():

    print("Loading chunks...")

    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    texts = [c["text"] for c in chunks]

    embedder = Embedder()

    print("Encoding chunks...")
    vectors = embedder.encode(texts)

    dim = vectors.shape[1]

    print(f"Vector dim = {dim}")
    print("Building FAISS index...")

    store = FAISSStore(dim)
    store.add(vectors)

    INDEX_DIR.mkdir(exist_ok=True)

    store.save(INDEX_FILE, META_FILE, chunks)

    print(f"\n✅ Saved index → {INDEX_FILE}")
    print(f"✅ Saved metadata → {META_FILE}")


if __name__ == "__main__":
    main()

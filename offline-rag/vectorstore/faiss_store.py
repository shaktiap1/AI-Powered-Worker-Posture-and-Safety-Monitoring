"""
FAISS Store
------------

Handles creation + saving + loading of FAISS index
"""

import faiss
import numpy as np
import pickle
from pathlib import Path


class FAISSStore:

    def __init__(self, dim: int):
        self.index = faiss.IndexFlatIP(dim)  # exact cosine similarity

    def add(self, vectors: np.ndarray):
        self.index.add(vectors)

    def search(self, query_vec, top_k=5):
        scores, ids = self.index.search(query_vec, top_k)
        return scores, ids

    def save(self, index_path: Path, meta_path: Path, metadata):
        faiss.write_index(self.index, str(index_path))

        with open(meta_path, "wb") as f:
            pickle.dump(metadata, f)

    @staticmethod
    def load(index_path: Path, meta_path: Path):
        index = faiss.read_index(str(index_path))

        with open(meta_path, "rb") as f:
            metadata = pickle.load(f)

        return index, metadata

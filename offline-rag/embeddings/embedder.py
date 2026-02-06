# Embedder :- This encodes chunks into dense vectors using SentenceTransformers

import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


MODEL_NAME = "BAAI/bge-small-en"


class Embedder: # this class initializes the SentenceTransformer model and provides a method to encode a list of texts into dense vectors, which will be used for creating embeddings of the text chunks in the RAG pipeline. The encode method takes a list of texts and returns a NumPy array of their corresponding embedding vectors, with options for batch processing and normalization for cosine similarity or inner product calculations.

    def __init__(self): # this will initialize the Embedder class by loading the specified SentenceTransformer model, which will be used for encoding text into dense vectors. The model is loaded during initialization to ensure that it is ready for use when the encode method is called.
        print(f"Loading embedding model → {MODEL_NAME}")
        self.model = SentenceTransformer(MODEL_NAME)

    def encode(self, texts, batch_size=32): # this method encodes a list of texts into dense vectors using the SentenceTransformer model, with support for batch processing to handle large lists of texts efficiently. The resulting vectors are returned as a NumPy array of type float32, which is suitable for use in the RAG pipeline for similarity search and retrieval based on the generated embeddings.
        vectors = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            normalize_embeddings=True   # ⭐ important for cosine/IP
        )
        return np.array(vectors, dtype=np.float32)


# CLI test - here we will create an instance of the Embedder class, encode a sample list of texts (in this case, a single text "hello world"), and print the shape of the resulting embedding vector to verify that the encoding process is working correctly and producing the expected output shape for the generated embeddings.
if __name__ == "__main__":
    emb = Embedder()
    vec = emb.encode(["hello world"])
    print(vec.shape)

# THANKYOU JI FOR REVIEWING MY CODE HOPING TO CONNECT WITH U FOR THE NEXT ROUND OF INTERVIEW :) SHAKTESH

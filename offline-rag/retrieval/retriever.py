"""
Retriever
-----------

Query → embeddings → FAISS → rerank → best chunks

Run test:
    python -m retrieval.retriever
"""

import numpy as np
from pathlib import Path
import pickle

from embeddings.embedder import Embedder
from vectorstore.faiss_store import FAISSStore
from retrieval.reranker import Reranker


# PATHS- here we define the paths for the FAISS index file and its corresponding metadata file, 
# which will be loaded by the Retriever class to perform similarity search and retrieval of relevant documents based on query embeddings. 
# The INDEX_FILE is the path to the FAISS index that contains the vector representations of the document chunks,
# while the META_FILE is a pickle file that contains metadata information for each chunk, such as page number and section title,
# which can be used to provide context when retrieving and reranking documents in response to user queries.

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INDEX_DIR = PROJECT_ROOT / "indexes"

INDEX_FILE = INDEX_DIR / "faiss.index"
META_FILE = INDEX_DIR / "metadata.pkl"


# RETRIEVER - this class defines the Retriever component of the RAG pipeline, which is responsible for processing user queries, 
# generating query embeddings, performing similarity search using a FAISS index, 
# and reranking the retrieved documents based on their relevance to the query. 

class Retriever:

    def __init__(self, top_k=8, rerank_k=4):

        self.top_k = top_k
        self.rerank_k = rerank_k

        print("Loading embedder...")
        self.embedder = Embedder()

        print("Loading FAISS index...")
        self.index, self.metadata = FAISSStore.load(INDEX_FILE, META_FILE)

        print("Loading reranker...")
        self.reranker = Reranker()

    def search(self, query: str): # this method takes a user query as input, generates an embedding vector for the query using the embedder,
                               # performs a similarity search using the FAISS index to retrieve relevant documents based on the query.

        print(f"\n Query → {query}")

        query_vec = self.embedder.encode([query])

        scores, ids = self.index.search(query_vec, self.top_k)

        candidates = [self.metadata[i] for i in ids[0]]

        print(f"Retrieved {len(candidates)} candidates")

        best = self.reranker.rerank(query, candidates, self.rerank_k)

        return best # this will return the top_k most relevant documents from the input list, sorted by their relevance scores
                    # as predicted by the CrossEncoder model. Each document in the returned list is a dictionary containing the original document information
                    # along with its associated relevance score. The sorting is done in descending order to ensure that the most relevant documents are returned at the top of the list.


# CLI TEST - here we will create an instance of the Retriever class and enter a loop to continuously accept user queries from the command line.

if __name__ == "__main__":

    retriever = Retriever()

    while True:
        q = input("\nAsk: ")
        if not q:
            break

        results = retriever.search(q)

        for i, r in enumerate(results):
            print("\n RESULT", i + 1)
            print("Page:", r["metadata"]["page"])
            print(r["text"][:400])

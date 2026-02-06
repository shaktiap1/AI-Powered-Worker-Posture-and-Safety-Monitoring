# This code defines a Reranker class that uses a CrossEncoder model from the sentence_transformers library
# to rerank a list of documents based on their relevance to a given query. The rerank method takes a query string,
# a list of document dictionaries (each containing a "text" field), and an optional top_k parameter
# that specifies how many of the top-ranked documents to return. The method creates pairs of the query and each document's text, 
# predicts relevance scores using the CrossEncoder model, sorts the documents based on these scores, and returns the top_k most relevant documents.

import torch
from sentence_transformers import CrossEncoder


MODEL_NAME = "BAAI/bge-reranker-base" # this is the name of the CrossEncoder model that will be loaded for reranking documents based on their relevance to a query.


class Reranker: # this class defines a Reranker that utilizes a CrossEncoder model to evaluate the relevance of a list of documents to a given query.

    def __init__(self):
        print(f"Loading reranker → {MODEL_NAME}")
        self.model = CrossEncoder(MODEL_NAME)

    def rerank(self, query: str, docs: list, top_k: int = 4): # this method takes a query string, a list of document dictionaries (each containing a "text" field), and an optional top_k parameter that specifies how many of the top-ranked documents to return.
                                                              # It creates pairs of the query and each document's text, predicts relevance scores using the CrossEncoder model, sorts the documents based on these scores, and returns the top_k most relevant documents from the input list.
        """
        docs = list of chunk dicts
        returns best top_k chunks
        """

        pairs = [(query, d["text"]) for d in docs]

        scores = self.model.predict(pairs)

        scored = list(zip(scores, docs))
        scored.sort(key=lambda x: x[0], reverse=True)

        return [d for _, d in scored[:top_k]] # this will return the top_k most relevant documents from the input list, sorted by their relevance scores as predicted by the CrossEncoder model. 
                                            # Each document in the returned list is a dictionary containing the original document information along with its associated relevance score. The sorting is done in descending order to ensure that the most relevant documents are returned at the top of the list.

# THANKYOU JI FOR REVIEWING MY CODE HOPING TO CONNECT WITH U FOR THE NEXT ROUND OF INTERVIEW :) SHAKTESH    
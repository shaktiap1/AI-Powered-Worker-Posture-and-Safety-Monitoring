"""
Full RAG Pipeline : query → cache → retrieval → rerank → prompt → LLM → cache

To Run this pipeline run the command in your terminal from the root directory: python -m pipeline.rag_pipeline
"""

import numpy as np

from embeddings.embedder import Embedder
from retrieval.retriever import Retriever
from cache.redis_cache import RedisCache
from llm.ollama_client import OllamaClient
from llm.prompt import build_prompt


class RAGPipeline: # this class defines the main RAG pipeline that integrates the embedding, retrieval, caching, and language model components to process user queries and generate responses. 
   
    def __init__(self):# this will initialize the RAGPipeline class by creating instances of the Embedder, Retriever, RedisCache, and OllamaClient classes, which will be used for encoding queries, retrieving relevant documents, caching results, and generating responses from the language model, respectively. This setup allows the RAG pipeline to efficiently handle user queries by leveraging these components in a cohesive manner.

        self.embedder = Embedder()
        self.retriever = Retriever()
        self.cache = RedisCache()
        self.llm = OllamaClient()



    def ask(self, query: str): # this method takes a user query as input and processes it through the RAG pipeline. 
                               # It first generates an embedding vector for the query using the embedder,
                               # then checks the Redis cache for a cached answer using the query vector as the key. 
                               # If a cached answer is found, it returns that answer. If not, it performs a retrieval search to find relevant documents based on the query, 
                               # constructs a context from the retrieved documents, builds a prompt using the context and query, generates an answer using the language model, 
                               # and finally caches the result in Redis before returning it.

        # embed query for cache key
        query_vec = self.embedder.encode([query])[0]

        cached = self.cache.get(query_vec)

        if cached:
            return cached

        docs = self.retriever.search(query)

        context = "\n\n".join([d["text"] for d in docs])

        prompt = build_prompt(context, query)

        answer = self.llm.generate(prompt)

        result = {
            "answer": answer,
            "sources": [
                {
                    "page": d["metadata"]["page"],
                    "section": d["metadata"]["section"]
                }
                for d in docs
            ]
        }

        self.cache.set(query_vec, result)

        return result 


# CLI test - here we will create an instance of the RAGPipeline class and enter a loop to continuously accept user queries from the command line. 
# For each query entered by the user, we will call the ask method of the RAGPipeline instance to process the query through the pipeline and generate a response. 
# The generated answer and its sources will then be printed to the console for the user to see. This allows us to interactively test the RAG pipeline by asking questions
# and receiving answers based on the retrieved context and language model generation.

if __name__ == "__main__":

    rag = RAGPipeline()

    while True:
        q = input("\nAsk: ")
        if not q:
            break

        result = rag.ask(q)

        print("\nAnswer:\n", result["answer"])
        print("\nSources:", result["sources"])

# THANKYOU JI FOR REVIEWING MY CODE HOPING TO CONNECT WITH U FOR THE NEXT ROUND OF INTERVIEW :) SHAKTESH

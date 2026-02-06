"""
FastAPI Server for my Offline RAG

To Run: Paste this command in the terminal: uvicorn api.server:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import ChatRequest, ChatResponse
from pipeline.rag_pipeline import RAGPipeline

# INIT- FastAPI app and RAG pipeline instance

app = FastAPI(title="Offline RAG API")

rag = RAGPipeline()

# CORS (for frontend later)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # this will allow requests from any origin, which is useful during development when the frontend and backend may be running on different domains or ports, but in production, you may want to restrict this to specific origins for security reasons.
    allow_credentials=True,    # this will allow cookies and authentication headers to be included in cross-origin requests, which is important for maintaining user sessions and secure communication between the frontend and backend.
    allow_methods=["*"],       # this will allow all HTTP methods (GET, POST, PUT, DELETE, etc.) to be used in cross-origin requests, which is necessary for the frontend to interact with the backend API without restrictions on the types of requests it can make.
    allow_headers=["*"],       # this will allow all headers to be included in cross-origin requests, which is important for allowing the frontend to send necessary headers (like Content-Type, Authorization, etc.) when making requests to the backend API.
)

# ROUTES - here we will define the API endpoints for the FastAPI server, including a health check endpoint at the root ("/") that returns a simple JSON response indicating that the server is running, and a POST endpoint at "/chat" that accepts a ChatRequest object as input, processes the query using the RAG pipeline, and returns a ChatResponse object containing the generated answer and source information.

@app.get("/") # this is a simple health check endpoint that can be used to verify that the FastAPI server is running and responsive, and it returns a JSON response with a "status" key indicating "running".
def health():
    return {"status": "running"} 


@app.post("/chat", response_model=ChatResponse)# this endpoint will handle POST requests to the "/chat" URL, and it expects a request body that matches the ChatRequest schema defined in api/schemas.py, which includes a "query" field containing the user's input query. The endpoint will process the query using the RAG pipeline and return a response that matches the ChatResponse schema, which includes an "answer" field with the generated answer from the AI assistant and a "sources" field with information about the sources used to generate the answer.
def chat(req: ChatRequest):

    result = rag.ask(req.query)

    return result


# THANKYOU JI FOR REVIEWING MY CODE HOPING TO CONNECT WITH U FOR THE NEXT ROUND OF INTERVIEW :) SHAKTESH
# API Schemas : Defining request/response contracts for schema validation and documentation in FastAPI.

from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel): # this defines the expected structure of the request body for the chat endpoint, 
    query: str                # which includes a single field "query" of type string that represents the user's input query to the AI assistant.


class Source(BaseModel): # this defines the structure of the source information that will be included in the response from the chat endpoint, 
    page: Optional[int] #  which includes fields for the source document name, page number, and section name, all of which are optional since not all sources may have this information available.
    section: Optional[str]
    


class ChatResponse(BaseModel): # this defines the expected structure of the response body from the chat endpoint, which includes an "answer" field of type string that contains the generated answer from the AI assistant
    answer: str                # based on the user query and retrieved context, and a "sources" field which is a list of Source objects that provide information about the sources used to generate the answer, such as document name, page number, and section name.
    sources: List[Source]
    

# THANKYOU JI FOR REVIEWING MY CODE HOPING TO CONNECT WITH U FOR THE NEXT ROUND OF INTERVIEW :) SHAKTESH
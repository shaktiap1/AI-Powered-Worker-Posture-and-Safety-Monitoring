# This code defines an OllamaClient class that interacts with an Ollama language model API to generate responses based on user prompts.
# The class initializes with a specified model name and provides a generate method that sends a POST request to the Ollama API with the user prompt 
# and returns the generated response. The method also includes error handling for timeouts and other exceptions that may occur during the API request.

import requests
import json


MODEL_NAME = "phi3:mini"  # this is the name of the Ollama model that we want to use for generating responses. You can replace "phi3:mini" with the name of any other model that you have set up in your Ollama environment, depending on your requirements for response quality and speed. 
                          # The model name is included in the payload sent to the Ollama API to specify which model should be used for generating the response based on the user prompt.
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"


class OllamaClient: # this class defines a client for interacting with the Ollama language model API. It includes an initializer that sets up the model name and a generate method that takes a user prompt as input, constructs a payload for the API request, and sends a POST request to the Ollama API endpoint. 

    def __init__(self):
        print(f"Using Ollama model → {MODEL_NAME}")

    def generate(self, prompt: str) -> str: # this method takes a user prompt as input and generates a response by sending a POST request to the Ollama API. The payload includes the model name, the user prompt formatted as a message, and options for temperature and number of tokens to predict. 
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "options": {
                "temperature": 0.2,
                "num_predict": 512
            },
            "stream": False
        }

        try: # here we will send a POST request to the Ollama API endpoint with the constructed payload, and we will set a timeout of 180 seconds (3 minutes) to prevent hanging in case of issues with the API. If the request is successful, we will parse the JSON response and extract the generated content from the "message" field, 
             # which contains the response from the language model based on the user prompt. 
            response = requests.post(
                OLLAMA_URL,
                json=payload,
                timeout=180   # ⭐ important
            )

            data = response.json() # this will parse the JSON response returned by the Ollama API, which is expected to have a structure that includes a "message" field containing the generated response from the language model. We will extract the content of the message to return as the final response to the user prompt.
            return data["message"]["content"] # this will return the generated response from the Ollama language model based on the user prompt, which is extracted from the "message" field in the JSON response returned by the API. The content of the message is what we want to provide back to the user as the answer to their query.

        except requests.exceptions.Timeout: # this will catch any timeout exceptions that occur during the API request, which can happen if the Ollama API takes too long to respond or if there are network issues. In case of a timeout, we will return a message indicating that the LLM timed out and suggest trying again.
            return "LLM timed out. Please try again." # this will return a string message indicating that the language model (LLM) timed out, which can occur if the API request takes longer than the specified timeout duration. This message can be used to inform the user that their request could not be processed within the expected time frame and that they should try again later.

        except Exception as e: # this will catch any other exceptions that may occur during the API request, such as network errors, invalid responses, or issues with the payload. In case of any exceptions, we will return a message indicating that there was an error with the LLM and include the error message for debugging purposes.
            return f"LLM error: {str(e)}" # this will return a string message indicating that there was an error with the language model (LLM) during the API request, and it will include the specific error message for debugging purposes. This can help identify issues with the API request or response and provide feedback for troubleshooting.

# THANKYOU JI FOR REVIEWING MY CODE HOPING TO CONNECT WITH U FOR THE NEXT ROUND OF INTERVIEW :) SHAKTESH
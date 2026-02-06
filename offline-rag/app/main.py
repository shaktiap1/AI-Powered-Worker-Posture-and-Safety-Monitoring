import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

# Page Style: Set title, icon, layout, and add CSS for cleaner chat bubbles.
st.set_page_config(
    page_title="Offline AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    max-width: 900px;
}

.chat-bubble-user {
    background-color: #2563eb;
    color: white;
    padding: 12px 16px;
    border-radius: 14px;
    margin-bottom: 10px;
}

.chat-bubble-ai {
    background-color: #f3f4f6;
    padding: 12px 16px;
    border-radius: 14px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)


# State: Initializing chat messages in session state if not already present.

if "messages" not in st.session_state:
    st.session_state.messages = []


# Header: This will display the main title and caption for the app.

st.title("Offline AI Assistant")
st.caption("Local RAG | Fast | Private | No Internet")

# DISPLAY CHAT- here we will loop through the chat messages stored in session state and display them in the chat interface with different styles for user and assistant messages using the CSS classes defined earlier, and we will use unsafe_allow_html=True to render the HTML content for the chat bubbles.

for role, msg in st.session_state.messages:

    if role == "user":
        st.markdown(
            f'<div class="chat-bubble-user">{msg}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="chat-bubble-ai">{msg}</div>',
            unsafe_allow_html=True
        )

# USER INPUT - here we will take input from the user using Streamlit's chat_input widget.

query = st.chat_input("Ask anything from your document...")

if query:

    st.session_state.messages.append(("user", query))

    with st.spinner("Thinking..."):  # this will show a spinner while waiting for the response from the API

        try: # here we will make a POST request to the API endpoint with the user query as JSON payload, and we will set a timeout of 300 seconds (5 minutes) to prevent hanging,
             # in case of issues with the API, and if the request is successful, we will extract the answer from the JSON response, otherwise we will catch any exceptions and set the answer to an error message.
            response = requests.post(
                API_URL,
                json={"query": query},
                timeout=300
            )

            answer = response.json()["answer"] # this will extract the answer from the JSON response returned by the API, which is expected to have a key "answer" containing the generated answer,
                                               #from the LLM based on the user query and the retrieved context from the local RAG system.

        except Exception as e:
            answer = f"Error: {e}" # in case of any exceptions during the API request, we will set the answer to a string that includes the error message for debugging purposes.

    st.session_state.messages.append(("assistant", answer)) # this will append the assistant's answer to the chat messages stored in session state, which will then be displayed in the chat interface on the next rerun of the Streamlit app.

    st.rerun()


# THANKYOU JI FOR REVIEWING MY CODE HOPING TO CONNECT WITH U FOR THE NEXT ROUND OF INTERVIEW :) SHAKTESH
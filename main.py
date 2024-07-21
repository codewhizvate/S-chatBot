import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# loading the enviroment variable
load_dotenv()

# configuring the streamlit page settings
st.set_page_config(
    page_title="Chat with Bot",
    page_icon=":brain:",
    layout="centered"
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# setting up the gemini model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# function to translate roles between gemini-pro and streamlit terminology
def translate_role_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role
    
# initialiting the chat session in streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# display the page title
st.title("🤖 S-chatBot")

# displaying the above chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# inputting field for user's message
user_prompt = st.chat_input("Ask S-Bot")
if user_prompt:
    # adding user msg to chat and displaying it
    st.chat_message("user").markdown(user_prompt)

    # sending the user request to gemini and getting the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # displaying the gemini response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
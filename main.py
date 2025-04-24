import streamlit as st
from system_prompts import system_prompts
from openai import OpenAI

st.title("AI Chit Chat")
st.write("I tried making a role-playing AI chatbot with different characters. Select your character and start chating")

# Set OpenAI API key from Streamlit secrets
try:
    client = OpenAI(api_key=st.secrets["GEMINI_API_KEY"], base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
except:
    st.error("Connection Error")

# Labels for Selectbox
raw_labels = ["Indian Mom: (A typical desi mom)", "Baburao: (From Hera Pheri)", "Poo: (From K3G)", "Gabbar Singh: (From Sholay)", "Thanos: (From Infinity War)"]
labels = ["Indian_Mom", "Baburao", "Poo", "Gabbar", "Thanos"]

# Formating of the labels
def format_func(label):
    idx = labels.index(label)
    return raw_labels[idx]

# Reset messages when charaters are reset
def reset_character():
    st.session_state.pop("messages", None)

if "selected_character" not in st.session_state:
    st.session_state.selected_character = None

st.session_state.selected_character = st.selectbox("Select any character ...", labels, format_func=format_func, index=None, on_change=reset_character)

# Chat Implemenation
if st.session_state.selected_character:
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_prompts[st.session_state.selected_character]}]

    # Display chat messages from history on app rerun (excluding system_prompt)
    for i in range(1, len(st.session_state.messages)):
        message = st.session_state.messages[i]
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

    # Display assistant response in chat message container
    try:
        with st.chat_message("assistant"):
            if len(st.session_state.messages) > 1:
                stream = client.chat.completions.create(
                    model="gemini-2.0-flash",
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )
                response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})
    except:
        st.warning("Sorry! The unable to generate response due to high traffic 🥹")
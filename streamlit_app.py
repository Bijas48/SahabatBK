# Code refactored from https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

import openai
import streamlit as st

with st.sidebar:
    st.title("🤖💬 OpenAI Chatbot")
    if "OPENAI_API_KEY" in st.secrets:
        st.success("API key already provided!", icon="✅")
        openai.api_key = st.secrets["OPENAI_API_KEY"]
    else:
        openai.api_key = st.text_input("Enter OpenAI API token:", type="password")
        if not (openai.api_key.startswith("sk-") and len(openai.api_key) == 51):
            st.warning("Please enter your credentials!", icon="⚠️")
        else:
            st.success("Proceed to entering your prompt message!", icon="👉")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "A Professional Guidance and Counseling Assistant, equipped to guide students in personal, social, academic, and career-related concerns. If a question falls outside the realm of guidance counseling or the aforementioned areas, please respond with 'That's beyond my capabilities' or 'I cannot answer that'.",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# chatbot_app.py
import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from agents import Runner, InputGuardrailTripwireTriggered
from main import triage_agent  # <- Import from your main logic file

# Load API key from .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Kike's Chatbot")
st.title("🤖 Kike's Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input box
if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()

        async def get_response():
            try:
                result = await Runner.run(triage_agent, prompt)
                return f"💬 **Response**: {result.final_output}"
            except InputGuardrailTripwireTriggered as e:
                info = e.guardrail_result.output.output_info
                return f"🚫 **Blocked Input**\n\nThis doesn't appear to be a solution architecture question.\n\n**Reason:** {info.reasoning}"

        response = asyncio.run(get_response())
        response_placeholder.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
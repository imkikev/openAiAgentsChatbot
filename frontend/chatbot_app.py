# chatbot_app.py
import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from agents import Runner, InputGuardrailTripwireTriggered
from openai.types.responses import ResponseTextDeltaEvent
from backend.main import triage_agent

# Load API key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Kike's Chatbot")
st.title("🤖 Kike's Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()

        async def stream_response():
            try:
                result = Runner.run_streamed(triage_agent, prompt)
                full_response = ""
                async for event in result.stream_events():
                    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                        delta = event.data.delta
                        full_response += delta
                        response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)
                return full_response
            except InputGuardrailTripwireTriggered as e:
                info = e.guardrail_result.output.output_info
                blocked_msg = f"🚫 **Blocked Input**\n\nThis doesn't appear to be a solution architecture question.\n\n**Reason:** {info.reasoning}"
                response_placeholder.markdown(blocked_msg)
                return blocked_msg

        response = asyncio.run(stream_response())
        st.session_state.messages.append({"role": "assistant", "content": response})
# chatbot_app.py

import streamlit as st
import asyncio
import os
from dotenv import load_dotenv

# Robust Patch: Avoid crashes on any missing optional attributes like `.usage`, `.refusal`
from pydantic import BaseModel
_original_getattr = BaseModel.__getattr__
def safe_fallback_getattr(self, name):
    try:
        return _original_getattr(self, name)
    except AttributeError as e:
        if name in {"usage", "refusal", "logprobs", "tool_calls", "_hidden_params"}:
            return None
        raise e
BaseModel.__getattr__ = safe_fallback_getattr
#end Robust Patch

# Agents SDK imports
from agents import Runner, InputGuardrailTripwireTriggered
from openai.types.responses import ResponseTextDeltaEvent
from backend.main import triage_agent

# Load API key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Page settings
st.set_page_config(page_title="OpenAI Agents Chatbot", layout="centered")
st.title("🤖 OpenAI Agents Chatbot")

# Load and inject custom CSS
base_dir = os.path.dirname(os.path.abspath(__file__))
styles_dir = os.path.join(base_dir, '../frontend/styles')
with open(os.path.join(styles_dir, 'main.css'), 'r') as f:
    css = f"<style>{f.read()}</style>"
    st.markdown(css, unsafe_allow_html=True)

# Session messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Handle new prompt
if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        response_placeholder = st.empty()

        async def stream_response():
            try:
                result = Runner.run_streamed(triage_agent, prompt)
                full_response = ""
                agent_name = "Unknown Agent"

                async for event in result.stream_events():
                    if event.type == "agent_updated_stream_event":
                        agent_name = event.new_agent.name
                        print(f"Agent updated: {agent_name}")

                    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                        delta = event.data.delta
                        full_response += delta
                        response_placeholder.markdown(full_response + "▌")

                response_with_agent = f"**🧠 Agent: {agent_name}**\n\n{full_response}"
                response_placeholder.markdown(response_with_agent)
                return response_with_agent

            except InputGuardrailTripwireTriggered as e:
                info = e.guardrail_result.output.output_info
                blocked_msg = f"🚫 **Blocked Input**\n\nThis doesn't appear to be a solution architecture question.\n\n**Reason:** {info.reasoning}"
                response_placeholder.markdown(blocked_msg)
                return blocked_msg

        # Run the async stream and store final response
        response = asyncio.run(stream_response())
        st.session_state.messages.append({"role": "assistant", "content": response})
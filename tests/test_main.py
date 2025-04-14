import pytest
from dotenv import load_dotenv
import os
from backend.main import triage_agent, Runner, InputGuardrailTripwireTriggered

# Load environment variables from .env
load_dotenv()

@pytest.mark.asyncio
async def test_triage_agent():
    # Ensure OPENAI_API_KEY is loaded
    assert os.getenv("OPENAI_API_KEY") is not None, "OPENAI_API_KEY is not set"

    # Define test inputs
    user_inputs = [
        "How do I reduce my AWS bill using automation?",
        "How can I use Claude with Amazon Bedrock and store embeddings in RDS?",
        "How can I design a monitoring strategy for a multi-region system?",
        "is bedrock a good approach for generative ai?"
    ]

    for user_input in user_inputs:
        try:
            # Run the triage agent
            result = await Runner.run(triage_agent, user_input)
            assert result.final_output is not None  # Example assertion
        except InputGuardrailTripwireTriggered as e:
            assert e.guardrail_result.output.output_info.reasoning is not None
from agents import Agent, Runner, InputGuardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import asyncio
import yaml

# Load environment variables
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# Load prompts
with open('prompts/sa_operations_instructions.yaml', 'r') as file:
    sa_operations_instructions = yaml.safe_load(file)['instructions']

with open('prompts/sa_genai_agent_instructions.yaml', 'r') as file:
    sa_genai_agent_instructions = yaml.safe_load(file)['instructions']

# Define output model for the guardrail
class architectureOutput(BaseModel):
    is_architecture: bool
    topic: str
    reasoning: str

# Guardrail agent
guardrail_agent = Agent(
    name="Guardrail Agent",
    instructions="""
Detect if the user input is related to solution architecture.

If NOT architecture:
- is_architecture: false
- topic: ""
- reasoning: explain why

If YES:
- is_architecture: true
- topic: "operations" or "genai"
- reasoning: explain why
""",
    output_type=architectureOutput,
    model="gpt-4o"
)

@InputGuardrail
async def architecture_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(architectureOutput)

    # Fix: ensure context is dict
    if ctx.context is None:
        ctx.context = {}
    elif not isinstance(ctx.context, dict):
        ctx.context = dict(ctx.context)

    ctx.context["architecture_topic"] = final_output.topic

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_architecture,
    )

# Specialist agents
sa_operations_agent = Agent(
    name="SA Operations Specialist",
    instructions=sa_operations_instructions,
    model="gpt-4o"
)

sa_genai_agent = Agent(
    name="SA Generative AI Specialist",
    instructions=sa_genai_agent_instructions,
    model="gpt-4o"
)

# Triage agent with lambda handoffs
triage_agent = Agent(
    name="SA Triage Agent",
    instructions="""
You are a triage agent. Route input to the correct agent based on the topic in 'architecture_topic'.
""",
    input_guardrails=[architecture_guardrail],
    handoffs=[sa_operations_agent, sa_genai_agent],
)

# Optional test runner
async def main():
    user_inputs = [
        "How do I reduce my AWS bill using automation?",
        "How can I use Claude with Amazon Bedrock and store embeddings in RDS?",
        "How can I design a monitoring strategy for a multi-region system?",
        "is bedrock a good approach for generative ai?"
    ]

    for user_input in user_inputs:
        try:
            result = await Runner.run(triage_agent, user_input)
            print(f"✅ Input: {user_input}")
            print(f"💬 Response: {result.final_output}\n")
        except InputGuardrailTripwireTriggered as e:
            output = e.guardrail_result.output.output_info
            print(f"🚫 Blocked Input: {user_input}")
            print(f"🛡️ Reason: {output.reasoning}\n")

if __name__ == "__main__":
    asyncio.run(main())
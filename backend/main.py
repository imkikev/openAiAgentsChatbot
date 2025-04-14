from agents import Agent, Runner, InputGuardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, WebSearchTool, ModelSettings
from pydantic import BaseModel
from dotenv import load_dotenv
from backend.agents.sa_genai_agent import sa_genai_agent
from backend.agents.sa_operations_agent import sa_operations_agent

import os
import asyncio
import yaml

# Load environment variables
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# Load prompts
base_dir = os.path.dirname(os.path.abspath(__file__))
prompts_dir = os.path.join(base_dir, 'prompts')

with open(os.path.join(prompts_dir, 'guardrails.yaml'), 'r') as file:
    guardrails_instructions = yaml.safe_load(file)['instructions']

with open(os.path.join(prompts_dir, 'triage_agent_instructions.yaml'), 'r') as file:    
    triage_agent_instructions = yaml.safe_load(file)['instructions']

# Define output model for the guardrail
class architectureOutput(BaseModel):
    is_architecture: bool
    topic: str
    reasoning: str

# Guardrail agent
guardrail_agent = Agent(
    name="Guardrail Agent",
    instructions=guardrails_instructions,
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

# Triage agent with lambda handoffs
triage_agent = Agent(
    name="SA Triage Agent",
    instructions=triage_agent_instructions,
    input_guardrails=[architecture_guardrail],
    handoffs=[sa_operations_agent, sa_genai_agent],
)
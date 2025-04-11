from agents import Agent, Runner, InputGuardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered
from pydantic import BaseModel
from dotenv import load_dotenv

import os
import asyncio
import yaml

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

with open('prompts/sa_operations_instructions.yaml', 'r') as file:
      data = yaml.safe_load(file)
      sa_operations_instructions = data['instructions']

with open('prompts/sa_genai_agent_instructions.yaml', 'r') as file:
      data = yaml.safe_load(file)
      sa_genai_agent_instructions = data['instructions']

with open('prompts/guardrails.yaml', 'r') as file:
      data = yaml.safe_load(file)
      sa_genai_agent_instructions = data['instructions']      

# Define guardrail output model
class architectureOutput(BaseModel):
    is_architecture: bool
    reasoning: str

# Guardrail Agent to detect homework questions
guardrail_agent = Agent(
    name="Guardrail Agent",
    instructions="Evaluate the user's input to determine if it pertains to solution architecture questions or actions. Respond with 'is_architecture': true if it is, otherwise false. doesdt answer and said that question is not alloed.",
    output_type=architectureOutput,
)

@InputGuardrail
async def architecture_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(architectureOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.is_architecture,
    )

# Solution Architect - Operations Agent
sa_operations_agent = Agent(
    name="SA Operations Specialist",
    instructions=sa_operations_instructions,
    model="gpt-4o"
)

# Solution Architect - Generative AI Agent
sa_genai_agent = Agent(
    name="SA Generative AI Specialist",
    instructions=sa_genai_agent_instructions,
    model="gpt-4o"
)

# Triage agent to route questions
triage_agent = Agent(
    name="SA Triage Agent",
    instructions="""
You are a triage agent. Based on the user's question, decide whether the topic is more related to:
- Operations architecture (cost, security, logging, monitoring, scalability)
- Generative AI architecture (LLMs, embeddings, Bedrock, LangChain, vector DBs)

Then forward the question to the appropriate specialist agent.
""",
    handoffs=[sa_operations_agent, sa_genai_agent],
    input_guardrails=[architecture_guardrail],
)

# Run the orchestration
async def main():
    if not openai_api_key:
        raise ValueError("The OpenAI API key is not set. Please check your .env file.")

    user_inputs = [
        "How do I reduce my AWS bill using automation?",
        "How can I use Claude with Amazon Bedrock and store embeddings in RDS?",
        "How can I design a monitoring strategy for a multi-region system?",
        "Can you help me write a project for AWS SA certification?"
    ]

    for user_input in user_inputs:
        try:
            result = await Runner.run(triage_agent, user_input)
            print(f"User Input: {user_input}")
            print(f"Agent Response: {result.final_output}\n")
        except InputGuardrailTripwireTriggered as e:
            guardrail_output = e.guardrail_result.output.output_info
            print(f"User Input: {user_input}")
            print(f"Input identified as homework: {guardrail_output.reasoning}")
            print(f"Agent Response: {e.guardrail_result.output}\n")
            print("Please study the topic instead of submitting homework prompts directly.\n")

if __name__ == "__main__":
    asyncio.run(main())
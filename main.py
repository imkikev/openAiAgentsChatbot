from agents import Agent, Runner, InputGuardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables from .env file
load_dotenv()

# Retrieve the OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

# Define the output model for the guardrail
class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

# Define the guardrail agent
guardrail_agent = Agent(
    name="Guardrail Agent",
    instructions="Determine if the user's input is a homework question. Respond with 'is_homework': true if it is, otherwise false. Provide reasoning.",
    output_type=HomeworkOutput,
)

# Implement the input guardrail function
@InputGuardrail
async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.is_homework,
    )

# Define the tutor agents
math_tutor_agent = Agent(
    name="Math Tutor",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples.",
    model="o3-mini"
)

history_tutor_agent = Agent(
    name="History Tutor",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
    model="gpt-4o"
)

# Define the triage agent with handoffs and input guardrails
triage_agent = Agent(
    name="Triage Agent",
    instructions="Determine which agent to use based on the user's question.",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[homework_guardrail],
)

# Run the agent orchestration
async def main():
    # Ensure the OpenAI API key is set
    if not openai_api_key:
        raise ValueError("The OpenAI API key is not set. Please check your .env file.")
    
    user_inputs = [
        "Can you solve this equation: 2x + 3 = 7?",
        "Who was the first president of the United States?",
        "What is the capital of France?",
        "give me a name popular tiktoker"
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
            print("Providing guidance without directly solving the problem.\n")

if __name__ == "__main__":
    asyncio.run(main())
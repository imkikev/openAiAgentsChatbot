from agents import Agent, WebSearchTool, ModelSettings
import os
import yaml


# Load prompts
base_dir = os.path.dirname(os.path.abspath(__file__))
prompts_dir = os.path.join(base_dir, '../prompts')

with open(os.path.join(prompts_dir, 'sa_operations_instructions.yaml'), 'r') as file:
    sa_operations_instructions = yaml.safe_load(file)['instructions']


# configurate agent
sa_operations_agent = Agent(
    name="SA Operations Specialist",
    instructions=sa_operations_instructions,
    model="gpt-4o"
)    
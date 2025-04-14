from agents import Agent, WebSearchTool, ModelSettings
import os
import yaml

# Load prompts
base_dir = os.path.dirname(os.path.abspath(__file__))
prompts_dir = os.path.join(base_dir, '../prompts')

with open(os.path.join(prompts_dir, 'sa_genai_agent_instructions.yaml'), 'r') as file:
    sa_genai_agent_instructions = yaml.safe_load(file)['instructions']

# tools
web_search_tool = WebSearchTool()

# configurate agent
sa_genai_agent = Agent(
    name="SA Generative AI Specialist",
    instructions=sa_genai_agent_instructions,
    model="gpt-4o",
    model_settings=ModelSettings(tool_choice="required"),
    tools=[web_search_tool]
)
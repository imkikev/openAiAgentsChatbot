from agents import Agent, WebSearchTool, ModelSettings
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv
from backend.tools.chatgpt_actions_tool import get_chatgpt_actions
import os
import yaml
import litellm

# Retrieve credentials (they're either from the environment or just loaded from .env)
load_dotenv()
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION_NAME") 

# # Optionally set them again to ensure libraries depending on os.environ see them
os.environ["AWS_ACCESS_KEY_ID"] = aws_access_key
os.environ["AWS_SECRET_ACCESS_KEY"] = aws_secret_key
os.environ["AWS_REGION_NAME"] = aws_region

# Set modify_params to True to handle Bedrock's tool parameter requirement
litellm.modify_params = True
#litellm.set_verbose = True # Optional: set to True for debugging

# Load prompts and models
base_dir = os.path.dirname(os.path.abspath(__file__))
prompts_dir = os.path.join(base_dir, '../prompts')

with open(os.path.join(prompts_dir, 'sa_genai_agent_instructions.yaml'), 'r') as file:
    config = yaml.safe_load(file)
    sa_genai_agent_instructions = config['instructions']
    model_openai = config['model_openai']
    model_aws = config['model_aws']

# Detect if AWS credentials are available
use_bedrock = bool(aws_access_key)

# Conditionally configure the model
if use_bedrock:
    selected_model = LitellmModel(model=model_aws)
    selected_model_settings = ModelSettings()  # Optional: adjust as needed
    selected_tools = []  # Optionally enable tools if Bedrock supports them
else:
    # OpenAI Tools
    web_search_tool = WebSearchTool()
    selected_model = model_openai
    selected_model_settings = ModelSettings(tool_choice="required")
    selected_tools = [web_search_tool,get_chatgpt_actions]

# Create agent based on config
sa_genai_agent = Agent(
    name="SA Generative AI Specialist",
    instructions=sa_genai_agent_instructions,
    model=selected_model,
    model_settings=selected_model_settings,
    tools=selected_tools,
)


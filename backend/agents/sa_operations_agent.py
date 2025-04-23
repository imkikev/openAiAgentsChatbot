from agents import Agent, FileSearchTool
from dotenv import load_dotenv
import os
import yaml
from openai import OpenAI
from openai import OpenAIError

# Load environment variables from .env file
load_dotenv()

# Retrieve the vector store ID
vector_store_id = os.getenv("VECTOR_STORE_ID")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize list of tools
tools = []

# Attempt to retrieve the vector store and initialize FileSearchTool
if vector_store_id:
    try:
        # Attempt to retrieve the vector store
        vector_store = client.vector_stores.retrieve(vector_store_id=vector_store_id)        

        # If retrieval is successful, add FileSearchTool to tools
        file_search_tool = FileSearchTool(
            vector_store_ids=[vector_store_id],
            max_num_results=5,
            include_search_results=True,            
            ranking_options={"score_threshold": 0.75}
        )
        tools.append(file_search_tool)

    except OpenAIError as e:
        print(f"Vector store not found or inaccessible: {e}")
        # Proceed without adding FileSearchTool
else:
    print("VECTOR_STORE_ID environment variable is not set.")
    # Proceed without adding FileSearchTool

# Load prompts
base_dir = os.path.dirname(os.path.abspath(__file__))
prompts_dir = os.path.join(base_dir, '../prompts')

with open(os.path.join(prompts_dir, 'sa_operations_instructions.yaml'), 'r') as file:
    sa_operations_instructions = yaml.safe_load(file)['instructions']

# Configure agent
sa_operations_agent = Agent(
    name="SA Operations Specialist",
    instructions=sa_operations_instructions,
    tools=tools,
    model="gpt-4o"
)
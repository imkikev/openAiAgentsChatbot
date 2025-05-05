# Multi-Provider AI Agent Chatbot with OpenAI SDK

This project is an AI chatbot powered by the [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/), capable of using different LLM providers, including OpenAI and AWS Bedrock. It features multi-agent orchestration, guardrails, and a Streamlit-based interface for interaction. The project supports secure configuration via `.env` and seamless provider switching using [LiteLLM](https://github.com/BerriAI/litellm).

## 🔧 Powered by OpenAI Agents SDK

This project leverages the [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/), a lightweight and powerful framework for building multi-agent workflows. The SDK simplifies the development of agentic applications by providing:

- **Agents**: LLMs equipped with instructions and tools.
- **Handoffs**: Mechanisms that allow agents to delegate tasks to other agents.
- **Guardrails**: Input validations and checks that run in parallel to agents.
- **Function Tools**: Python functions turned into tools with automatic schema generation and validation.
- **Tracing**: Built-in tracing to visualize and debug agentic flows.

For more details, refer to the [official documentation](https://openai.github.io/openai-agents-python/).

## 🚀 Getting Started
---

## Features

- **Chatbot Interface**: A user-friendly chatbot built with Streamlit.
- **Agent Management**: Backend logic for managing multiple agents, including a triage agent and specialized agents.
- **Guardrails**: Input validation and routing using guardrails.
- **Asynchronous Execution**: Supports asynchronous operations for efficient processing.
- **Multi-Provider Support**: Automatically switches between OpenAI and AWS Bedrock (Anthropic Claude 3) using LiteLLM, based on available environment credentials.
- **Testing**: Includes unit tests for backend logic using `pytest` and `pytest-asyncio`.
- **Custom Tools with Function Calling**: Create Python functions (like fetching ChatGPT IP whitelist) and expose them to LLMs using `@function_tool`.
- **File Retrieval with Vector Store (Optional)**: Retrieve relevant information from your uploaded documents using OpenAI’s `FileSearchTool`.  
  If no `VECTOR_STORE_ID` is provided, the agent will still function normally using only the base model.

## Model Provider Flexibility with LiteLLM

The `sa_genai_agent` is designed to dynamically select between different LLM providers:

- If `MODEL_PROVIDER` is set to "bedrock" and `AWS_ACCESS_KEY_ID` and related AWS credentials are found in your environment or `.env`, it uses **Anthropic Claude 3 Sonnet** via **AWS Bedrock**.
- If not, it defaults to **OpenAI’s GPT-4o model** — no configuration changes needed.

This is enabled using the [LiteLLM](https://github.com/BerriAI/litellm) integration, making the agent flexible and cost-efficient depending on your cloud environment.

### Example `.env`

```env
OPENAI_API_KEY=your_openai_api_key_here
VECTOR_STORE_ID=your_vector_store_id_here (optional)
AWS_ACCESS_KEY_ID=your_aws_access_key_id_here (optional)
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key_here (optional)
AWS_REGION_NAME=eu-west-1 (optional)
MODEL_PROVIDER=openai  # "openai" or "bedrock"
```
---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/openAiAgentText.git
   cd openAiAgentText
   ```

2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your credentials. The app will use OpenAI by default, but if AWS credentials are present, it will use AWS Bedrock with the Anthropic Claude 3 model:
   ```bash   
   OPENAI_API_KEY=your_openai_api_key_here
   VECTOR_STORE_ID=your_vector_store_id_here (optional)
   AWS_ACCESS_KEY_ID=your_aws_access_key_id_here (optional)
   AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key_here (optional)
   AWS_REGION_NAME=eu-west-1 (optional)
   MODEL_PROVIDER=openai  # "openai" or "bedrock"
   ```
   - **To obtain a `VECTOR_STORE_ID`** (optional – the app will still work even if you don't provide a vector store):

      - **Upload files via the OpenAI Platform UI:**

         1. Navigate to [OpenAI's platform](https://platform.openai.com/).
         2. Go to the **"Files"** section.      
         3. Create a new vector store and attach your uploaded file.
         4. Retrieve the `VECTOR_STORE_ID` from the vector store details.

      - **Or use the OpenAI CLI:**

         ```bash
         openai file create -p assistants -f my_document.pdf
         openai vector-store create -f <file_id>
         ```
---
## Usage

### Run the Chatbot
#### To execute the Chatbot logic:
```bash
python3 -m streamlit run frontend/chatbot_app.py
```
#### To execute the backend logic (optional):
```bash
python3 backend/main.py
```

### Run Tests    
To execute the test suite:
```bash
python3 -m pytest tests/test_main.py
```

To save test results to a file:
```bash
python3 -m pytest tests/test_main.py > test_results.txt
```

---
### 🤖 Agent Routing Examples

These examples show how user inputs are routed to the correct agent or rejected, based on the triage logic and guardrails.


#### 💬 Example 1
```text
User Input: How can I integrate Amazon Bedrock with LangChain?
```
- 🔍 **Summary**: A question about using generative AI tools and orchestration frameworks.  
- 🤖 **Routed Agent**: `SA Generative AI Specialist (sa_genai_agent)`

#### 💬 Example 2
```text
User Input: How can I automate deployment pipelines using GitHub Actions and AWS CodePipeline?
```
- 🔍 **Summary**: A DevOps/operations-related question about CI/CD automation.  
- 🤖 **Routed Agent**: `SA Operations Specialist (sa_operations_agent)`

#### 💬 Example 3
```text
User Input: Regarding my Generative AI Chatbot architecture, I need to whitelist an IP address for ChatGPT. Could you provide one?
```
- 🔍 **Summary**: Generative AI architecture with a specific technical requirement (ChatGPT IPs). will call a Custom Tool (chatgpt_actions_tool.py)   
- 🤖 **Routed Agent**: `SA Generative AI Specialist (sa_genai_agent)`

#### 💬 Example 4
```text
User Input: What is 1 + 1?
```
- 🔍 **Summary**: A general question not related to architecture.  
- ❌ **Routed Agent**: ` None – blocked by guardrail (is_architecture: false)`

---
## 🔌 Custom Tool Example

This project includes a custom tool (`get_chatgpt_actions`) that uses a public OpenAI API to fetch the latest [ChatGPT IP whitelist](https://openai.com/chatgpt-actions.json). 

The tool is implemented as a Python function and exposed to the LLM via the `@function_tool` decorator.

---
## Project Structure

```
openAiAgentsChatbot/
├── backend/                    # Backend logic
│   ├── agents/                 # Agent definitions
│   │   ├── sa_genai_agent.py   # Generative AI specialist agent
│   │   ├── sa_operations_agent.py # Operations specialist agent
│   ├── tools/
│   │   ├── chatgpt_actions_tool.py  # Tool to fetch ChatGPT IP whitelist
│   ├── prompts/                # agent instructions
│   │   ├── guardrails.yaml
│   │   ├── sa_operations_instructions.yaml
│   │   └── sa_genai_agent_instructions.yaml
│   │   └── triage_agent_instructions.yaml
│   ├── [main.py](http://_vscodecontentref_/3) # Backend entry point
├── frontend/                   # Frontend logic
│   ├── [chatbot_app.py](http://_vscodecontentref_/4) # Streamlit chatbot application
├── tests/                      # Unit and integration tests
│   ├── test_main.py            # Tests for backend logic
├── .env                        # Environment variables (ignored by Git)
├── requirements.txt            # Python dependencies
├── [README.md](http://_vscodecontentref_/5) # Project documentation
```
---
## Dependencies

Install the following Python packages:

- `openai-agents`
- `python-dotenv`
- `pyyaml`
- `openai`
- `streamlit`
- `pytest`
- `pytest-asyncio`

You can install all dependencies using:
```bash
pip3 install -r requirements.txt
```
or one by one:
```bash
pip3 install openai-agents  
pip3 install python-dotenv
pip3 install pyyaml    
pip3 install openai streamlit
pip3 install pytest
pip3 install pytest-asyncio
pip3 install "openai-agents[litellm]"
pip3 install litellm
pip3 install boto3
```

## Author

Developed by imKikev.

---

### Key Improvements
1. **Detailed Usage Instructions**: Includes commands for running the backend, chatbot, and tests.
2. **Project Structure**: Provides an overview of the folder structure for better understanding.
3. **Environment Variables**: Explains how to configure the [.env](http://_vscodecontentref_/9) file.
4. **Testing**: Includes commands for running tests and generating reports.
5. **Troubleshooting**: Addresses common issues like missing environment variables or dependencies.

Let me know if you'd like to customize this further!

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

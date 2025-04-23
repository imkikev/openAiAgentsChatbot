# OpenAI Agents SDK Chatbot by Kike

This project is a chatbot application powered by OpenAI agents. It includes a backend for managing agents and guardrails, and a frontend built with Streamlit for user interaction. The project also supports testing with `pytest` and uses environment variables for secure configuration.

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
- **Testing**: Includes unit tests for backend logic using `pytest` and `pytest-asyncio`.
- **File Retrieval with Vector Store**: Retrieve relevant information from your uploaded documents using OpenAI’s FileSearchTool.


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

3. Create a .env file in the root directory and add your OpenAI API key and Vector Store ID::
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   VECTOR_STORE_ID=your_vector_store_id_here
   ```
   - **To obtain a `VECTOR_STORE_ID`, you can:**

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


## Project Structure

```
openAiAgentsChatbot/
├── backend/                    # Backend logic
│   ├── agents/                 # Agent definitions
│   │   ├── sa_genai_agent.py   # Generative AI specialist agent
│   │   ├── sa_operations_agent.py # Operations specialist agent
│   ├── prompts/                # YAML files for agent instructions
│   │   ├── guardrails.yaml
│   │   ├── sa_operations_instructions.yaml
│   │   └── sa_genai_agent_instructions.yaml
│   ├── [main.py](http://_vscodecontentref_/3)                 # Backend entry point
├── frontend/                   # Frontend logic
│   ├── [chatbot_app.py](http://_vscodecontentref_/4)          # Streamlit chatbot application
├── tests/                      # Unit and integration tests
│   ├── test_main.py            # Tests for backend logic
├── .env                        # Environment variables (ignored by Git)
├── requirements.txt            # Python dependencies
├── [README.md](http://_vscodecontentref_/5)                   # Project documentation
```

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
```

## Author

Developed by Kike.

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

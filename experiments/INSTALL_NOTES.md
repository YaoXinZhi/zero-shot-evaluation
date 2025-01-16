# Setup Ollama

Instructions [here](https://github.com/RamiKrispin/ollama-poc?tab=readme-ov-file#setting-up-ollama).

[API doc](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-completion).

```sh

# Download Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start server -- restart if computer has been shutdown
ollama serve

# Download Mistral
ollama pull mistral

# Create virtual environment
python3 -m venv llm-env

# Activate environment
source llm-env/bin/activate

# Install client API
pip install ollama

```

# Setup GPT

Instructions [here](https://platform.openai.com/docs/quickstart?language-preference=python)

```sh

# Set API key
export OPENAI_API_KEY='xoxoxoxo'

# Use same environment
source llm-env/bin/activate

# Install client API
pip install openai

```

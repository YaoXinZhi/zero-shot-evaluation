# Ollama+GPT tests

## Setup Ollama

Instructions [here](https://github.com/RamiKrispin/ollama-poc?tab=readme-ov-file#setting-up-ollama).

[API doc](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-completion).

```sh

# Download Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start server -- restart if computer has been shutdown
ollama serve

# Download Mistral
ollama pull mistral

# Create Ollama environment
python3 -m venv ollama-env

# Activate environment
source ollama-env/bin/activate

# Install client API
pip install ollama

```

## Setup GPT

Instructions [here](https://platform.openai.com/docs/quickstart?language-preference=python)

```sh

# Set API key
export OPENAI_API_KEY='xoxoxoxo'

# Use same environment
source ollama-env/bin/activate

# Install client API
pip install openai

```

## Run script


```sh
./run.py -i INSTRUCTION -d DOC -o OUTPUT -m MODEL
```

Models:
- `mistral` (Ollama server)
- `gpt-4o-mini` (OpenAI server)


## Experiments


### Repetition

```sh
. repetition.sh
```

Repeat prompt+document five fold and observe stochastic differences.

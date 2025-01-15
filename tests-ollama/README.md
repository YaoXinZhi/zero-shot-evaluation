# Ollama tests

## Setup

Following instructions [here](https://github.com/RamiKrispin/ollama-poc?tab=readme-ov-file#setting-up-ollama).

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
source ollama/bin/activate

# Install client API
pip install ollama

```

## Run script

```sh
./run.py
```

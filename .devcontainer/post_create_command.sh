MODEL_NAME=nomic-embed-text

uv sync --frozen

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama server
ollama serve &

ollama pull ${MODEL_NAME}

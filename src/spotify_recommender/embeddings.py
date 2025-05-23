"""Module to store embeddings."""

import ollama
import torch


OLLAMA_MODEL_NAME = "nomic-embed-text"


def compute_text_embedding(input_text: str | list[str]) -> torch.Tensor:
    """Returns the embedding of the given input text, as a PyTorch column tensor of shape (n, d) with d the dimension of the embedding space, and n the number of strings in the input text."""
    embedding_response = ollama.embed(OLLAMA_MODEL_NAME, input=input_text)
    return torch.tensor(embedding_response.embeddings)

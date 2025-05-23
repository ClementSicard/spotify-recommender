"""Module to store the querying logic for recommendation."""

from spotify_recommender.embeddings import compute_text_embedding

from typing import Any


def find_recommendations(
    input_prompt: str, number_of_results: int = 30
) -> list[Any]:
    """Main function to return music recommendations based on the input prompt.

    Args:
        input_prompt (str): The input prompt, e.g. "Energetic music for fast-paced running."
        number_of_results (int): The number of recommendations to return for the given prompt. This corresponds to the `number_of_results` closest results.
    """
    prompt_embedding = compute_text_embedding(input_text=input_prompt)
    return []

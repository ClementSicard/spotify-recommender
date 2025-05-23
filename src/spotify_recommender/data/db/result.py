"""Recommendation results."""

import pydantic as pyd

from spotify_recommender.data.source.types import SpotifyTrack


class RecommendationResult(pyd.BaseModel):
    """Class to represent a recommendation result, being fetched from the vector database."""

    spotify_track: SpotifyTrack

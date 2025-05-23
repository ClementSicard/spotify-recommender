"""Data types from the dataset."""

from enum import Enum
from enum import StrEnum

import pydantic as pyd

from typing import Annotated, Any


class TrackMode(StrEnum):
    """Enum to represent the mode of a track."""

    MAJOR = "major scale"
    MINOR = "minor scale"


class DiscreteValue(Enum):
    """Labels to discretize values."""

    NOT_AT_ALL = 1
    VERY_LITTLE = 2
    LIMITEDLY = 3
    SLIGHTLY = 4
    MODERABLY = 5
    PRETTY = 6
    VERY = 7
    HIGHLY = 8
    SUPER = 9
    EXCEPTIONALLY = 10

    def to_string(self) -> str:
        """Returns a natural language string for the enum label."""
        return self.name.replace("_", " ").lower()


class DiscretizableField(pyd.BaseModel):
    """Pydantic model to represent a field that can be discretized.

    We assume the data is normalized beforehand (using min-max normalization).
    """

    value: Annotated[float, pyd.Field(ge=0.0, le=1.0)]

    @pyd.model_validator(mode="before")
    @classmethod
    def convert_float_to_model_input(
        cls,
        data: float | int | dict[str, Any],
    ) -> dict[str, float]:
        """Allow instantiation from a raw float by wrapping it in a dict."""
        if isinstance(data, float | int):
            return {"value": float(data)}

        # If it's already a dict (e.g., {'value': 0.5}) or an instance,
        # Pydantic will handle it.
        return data

    def discretize(self) -> DiscreteValue:
        """Discretize the float value to a natural language appreciation."""
        reverse_mapping = {
            v.value: v for _, v in DiscreteValue.__members__.items()
        }
        for val in sorted(
            reverse_mapping
        ):  # Get thresholds in increasing order
            if self.value * 10 <= val:
                return reverse_mapping[val]

        raise ValueError(
            f"Function should have returned for value {self.value}."
        )


class SpotifyTrack(pyd.BaseModel):
    """Class to represent a Spotify track, as present in the dataset."""

    # Track metadata
    name: str
    """Name (title) of the track."""

    album_name: str
    """Name of the album."""

    artists: str
    """Artists present on the track."""

    # Musical properties
    key: str | None
    """The key in which the track is."""

    mode: TrackMode | None
    """The mode in which the track is."""

    danceability: DiscretizableField
    """Danceability score of the track - inherited from Spotify API."""

    energy: DiscretizableField
    """Energy score of the track - inherited from Spotify API."""

    loudness: pyd.FiniteFloat
    """Loudness of the track - inherited from Spotify API."""

    normalized_loudness: DiscretizableField
    """Loudness of the track - inherited from Spotify API."""

    speechiness: DiscretizableField
    """Speechiness score of the track - inherited from Spotify API."""

    acousticness: DiscretizableField
    """Accousticness score of the track - inherited from Spotify API."""

    instrumentalness: DiscretizableField
    """Instrumentalness score of the track - inherited from Spotify API."""

    liveness: DiscretizableField
    """Instrumentalness score of the track - inherited from Spotify API."""

    valence: DiscretizableField
    """Valence score of the track - inherited from Spotify API."""

    tempo: Annotated[int, pyd.Field(ge=0)]
    """Tempo of the track."""

    normalized_tempo: DiscretizableField

    lyrics: str | None
    """Lyrics of the track. Could be `None`."""

    duration: Annotated[int, pyd.Field(ge=0)]
    """Duration of the track, in seconds."""

    normalized_duration: DiscretizableField

    def __str__(self) -> str:
        """String representation of the object."""
        return repr(self)

"""Module for loading data."""

from collections.abc import Iterator

from etils.epath import Path as HFPath
import polars as pl

from spotify_recommender.data.source.types import SpotifyTrack
from spotify_recommender.data.splits import Split

from typing import ClassVar


class Dataset:
    """Class to load the Spotify dataset."""

    HF_DATASET_NAME: ClassVar[str] = "abhiramag/spotify-data-960k"
    SPLITS: ClassVar[dict[str, str]] = {
        Split.TRAIN: "data/train-00000-of-00001.parquet",
        Split.VALIDATION: "data/validation-00000-of-00001.parquet",
        Split.TEST: "data/test-00000-of-00001.parquet",
    }

    COLUMNS_TO_NORMALIZE: ClassVar[list[str]] = [
        "duration",
        "loudness",
        "tempo",
    ]

    @classmethod
    def load(
        cls, split: Split, dataset_path: HFPath | None = None
    ) -> pl.DataFrame:
        """Load the dataset."""
        if not dataset_path:
            match split:
                case Split.TRAIN:
                    split_path = cls.SPLITS[Split.TRAIN]
                case Split.VALIDATION:
                    split_path = cls.SPLITS[Split.VALIDATION]
                case Split.TEST:
                    split_path = cls.SPLITS[Split.TEST]
                case Split.ALL:
                    return pl.concat(
                        [
                            cls.load(Split.TRAIN),
                            cls.load(Split.VALIDATION),
                            cls.load(Split.TEST),
                        ],
                        how="vertical",
                    )
                case _:
                    raise ValueError(f"Unknown split: {split}")
            dataset_path = (
                HFPath("hf://datasets") / cls.HF_DATASET_NAME / split_path
            )

        return cls._clean(cls, pl.read_parquet(str(dataset_path)))  # type: ignore

    def _clean(self, loaded_df: pl.DataFrame) -> pl.DataFrame:
        """Cleans the dataframe."""
        for col in self.COLUMNS_TO_NORMALIZE:
            loaded_df = loaded_df.with_columns(
                **{f"normalized_{col}": min_max_normalize(loaded_df[col])}
            )

        return loaded_df

    @classmethod
    def iterator(
        cls, split: Split = Split.ALL, dataset_path: HFPath | None = None
    ) -> Iterator[SpotifyTrack]:
        """Makes an iterator of the dataset."""
        loaded_df = cls.load(split=split, dataset_path=dataset_path)
        for row_dict in loaded_df.iter_rows(named=True):
            yield SpotifyTrack.model_validate(row_dict)


def min_max_normalize(series: pl.Series) -> pl.Series:
    """Normalize a DataFrame series."""
    return (series - series.min()) / (series.max() - series.min())  # type: ignore

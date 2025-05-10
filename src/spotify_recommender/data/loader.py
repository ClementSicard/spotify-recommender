"""Module for loading data."""

from etils.epath import Path as HFPath
import polars as pl

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

    def load(self, split: Split) -> pl.DataFrame:
        """Load the dataset."""
        match split:
            case Split.TRAIN:
                split_path = self.SPLITS[Split.TRAIN]
            case Split.VALIDATION:
                split_path = self.SPLITS[Split.VALIDATION]
            case Split.TEST:
                split_path = self.SPLITS[Split.TEST]
            case Split.ALL:
                return pl.concat(
                    [
                        self.load(Split.TRAIN),
                        self.load(Split.VALIDATION),
                        self.load(Split.TEST),
                    ],
                    how="vertical",
                )
            case _:
                raise ValueError(f"Unknown split: {split}")
        dataset_path = (
            HFPath("hf://datasets") / self.HF_DATASET_NAME / split_path
        )
        return pl.read_parquet(str(dataset_path))  # type: ignore

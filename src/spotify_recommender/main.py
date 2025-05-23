"""Entrypoint."""

from loguru import logger

from spotify_recommender.data.source.loader import Dataset
from spotify_recommender.data.splits import Split


def main() -> None:
    """Main entry point for the application script."""
    logger.info("Loading data...")

    dataset = Dataset().load(split=Split.ALL)
    logger.debug(dataset.shape)


if __name__ == "__main__":
    main()

"""Dataset splits enum."""

from enum import StrEnum


class Split(StrEnum):
    """Enum for the different splits of the dataset."""

    TRAIN = "TRAIN"
    TEST = "TEST"
    VALIDATION = "VALIDATION"
    ALL = "ALL"

    def __str__(self) -> str:
        """Return the string representation of the split."""
        return self.value

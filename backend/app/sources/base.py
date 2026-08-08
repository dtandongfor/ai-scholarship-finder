from abc import ABC, abstractmethod
from typing import Any


class ScholarshipSource(ABC):
    """
    Base interface for scholarship data sources.

    Every scholarship source should inherit from this class
    and implement the fetch() method.
    """

    name: str

    @abstractmethod
    def fetch(self) -> list[dict[str, Any]]:
        """
        Retrieve raw scholarship records from the source.

        Returns:
            A list of dictionaries containing raw scholarship data.
        """
        raise NotImplementedError
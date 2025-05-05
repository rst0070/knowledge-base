from abc import ABC, abstractmethod


class Embedder(ABC):
    """
    Initialized a base embedding class
    """

    def __init__(self, config = None):
        pass

    @abstractmethod
    def embed(self, text:str) -> list[float]:
        """
        Get the embedding for the given text.
        """
        pass
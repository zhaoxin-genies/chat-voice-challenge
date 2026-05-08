from abc import ABC, abstractmethod


class LLMService(ABC):
    """Base class for LLM providers."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

from abc import ABC, abstractmethod
from typing import Optional
import os
from dataclasses import dataclass
import asyncio

@dataclass
class LLMConfig:
    api_key: str
    model: str
    max_tokens: int = 100
    temperature: float = 0.7

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""

    def __init__(self, config: LLMConfig):
        self.config = config

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Generate a response from the LLM"""
        pass

class OpenAIProvider(LLMProvider):
    """OpenAI provider implementation"""

    async def generate(self, prompt: str) -> str:
        # Stubbed implementation - replace with actual OpenAI API call
        await asyncio.sleep(0.1)  # Simulate API latency
        return f"OpenAI response to: {prompt[:50]}..."

class TogetherProvider(LLMProvider):
    """Together AI provider implementation"""

    async def generate(self, prompt: str) -> str:
        # Stubbed implementation - replace with actual Together API call
        await asyncio.sleep(0.1)  # Simulate API latency
        return f"Together response to: {prompt[:50]}..."

class AnthropicProvider(LLMProvider):
    """Anthropic provider implementation"""

    async def generate(self, prompt: str) -> str:
        # Stubbed implementation - replace with actual Anthropic API call
        await asyncio.sleep(0.1)  # Simulate API latency
        return f"Anthropic response to: {prompt[:50]}..."

class LLMFactory:
    """Factory class for creating and managing LLM providers"""

    def __init__(self):
        self.providers = {}
        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize all available providers with configuration"""
        # Load from environment variables
        openai_config = LLMConfig(
            api_key=os.getenv("OPENAI_API_KEY", "fake-openai-key"),
            model="gpt-3.5-turbo"
        )

        together_config = LLMConfig(
            api_key=os.getenv("TOGETHER_API_KEY", "fake-together-key"),
            model="meta-llama/Llama-2-7b-chat-hf"
        )

        anthropic_config = LLMConfig(
            api_key=os.getenv("ANTHROPIC_API_KEY", "fake-anthropic-key"),
            model="claude-3-haiku-20240307"
        )

        self.providers = {
            "openai": OpenAIProvider(openai_config),
            "together": TogetherProvider(together_config),
            "anthropic": AnthropicProvider(anthropic_config)
        }

    async def generate(self, prompt: str, provider_name: str = "openai") -> str:
        """Generate a response using the specified provider"""
        if provider_name not in self.providers:
            raise ValueError(f"Unknown provider: {provider_name}")

        provider = self.providers[provider_name]
        return await provider.generate(prompt)

    def get_available_providers(self) -> list[str]:
        """Get list of available provider names"""
        return list(self.providers.keys())

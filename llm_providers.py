from dataclasses import dataclass

import requests

from llm_service import LLMService


@dataclass
class LLMConfig:
    api_key: str
    model: str
    base_url: str = ""
    max_tokens: int = 100
    temperature: float = 0.7


class OpenAIProvider(LLMService):
    def __init__(self, config: LLMConfig):
        self.config = config

    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{self.config.base_url}/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.config.api_key}"},
            json={
                "model": self.config.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": self.config.max_tokens,
                "temperature": self.config.temperature,
            },
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]


class TogetherProvider(LLMService):
    def __init__(self, config: LLMConfig):
        self.config = config

    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{self.config.base_url}/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.config.api_key}"},
            json={
                "model": self.config.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": self.config.max_tokens,
                "temperature": self.config.temperature,
            },
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]


class AnthropicProvider(LLMService):
    def __init__(self, config: LLMConfig):
        self.config = config

    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{self.config.base_url}/v1/messages",
            headers={
                "x-api-key": self.config.api_key,
                "anthropic-version": "2023-06-01",
            },
            json={
                "model": self.config.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": self.config.max_tokens,
            },
        )
        response.raise_for_status()
        return response.json()["content"][0]["text"]

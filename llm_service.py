import asyncio


class LLMService:
    """
    Stubbed LLM service -- returns mock responses.
    In production, this would call OpenAI, Anthropic, etc.
    """

    async def generate(self, prompt: str, provider: str = "openai") -> str:
        await asyncio.sleep(0.05)  # Simulate API latency
        return f"LLM response to: {prompt[:50]}"

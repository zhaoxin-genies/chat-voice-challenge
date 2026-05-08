import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="LLM Chat Service")


class ChatRequest(BaseModel):
    user_id: str
    prompt: str
    provider: Optional[str] = "openai"


class ChatResponse(BaseModel):
    response: str
    user_id: str


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint that processes user prompts and returns LLM responses.
    """
    try:
        if request.provider == "openai":
            from llm_providers import LLMConfig, OpenAIProvider
            config = LLMConfig(
                api_key=os.getenv("OPENAI_API_KEY", "fake-openai-key"),
                model="gpt-3.5-turbo",
                base_url=os.getenv("OPENAI_BASE_URL", "http://localhost:11200"),
            )
            provider = OpenAIProvider(config)
        elif request.provider == "together":
            from llm_providers import LLMConfig, TogetherProvider
            config = LLMConfig(
                api_key=os.getenv("TOGETHER_API_KEY", "fake-together-key"),
                model="meta-llama/Llama-2-7b-chat-hf",
                base_url=os.getenv("TOGETHER_BASE_URL", "http://localhost:11200"),
            )
            provider = TogetherProvider(config)
        elif request.provider == "anthropic":
            from llm_providers import LLMConfig, AnthropicProvider
            config = LLMConfig(
                api_key=os.getenv("ANTHROPIC_API_KEY", "fake-anthropic-key"),
                model="claude-3-haiku-20240307",
                base_url=os.getenv("ANTHROPIC_BASE_URL", "http://localhost:11200"),
            )
            provider = AnthropicProvider(config)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown provider: {request.provider}",
            )

        response = provider.generate(request.prompt)

        return ChatResponse(
            response=response,
            user_id=request.user_id,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

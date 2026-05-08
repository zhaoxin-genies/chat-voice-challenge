"""
Mock LLM server.

Handles OpenAI-compatible /v1/chat/completions and Anthropic /v1/messages formats.

Usage:
    python3 mock_servers/llm_server.py
    # Runs on http://localhost:11200
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Mock LLM Server")


class Message(BaseModel):
    role: str
    content: str


class OpenAIChatRequest(BaseModel):
    model: str
    messages: List[Message]
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7


class AnthropicChatRequest(BaseModel):
    model: str
    messages: List[Message]
    max_tokens: Optional[int] = 100


@app.post("/v1/chat/completions")
async def chat_completions(request: OpenAIChatRequest):
    prompt = request.messages[-1].content if request.messages else ""
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": f"Mock {request.model} response to: {prompt[:50]}...",
                }
            }
        ]
    }


@app.post("/v1/messages")
async def messages(request: AnthropicChatRequest):
    prompt = request.messages[-1].content if request.messages else ""
    return {
        "content": [
            {
                "type": "text",
                "text": f"Mock {request.model} response to: {prompt[:50]}...",
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=11200)

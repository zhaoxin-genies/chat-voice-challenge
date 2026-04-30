from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

from llm_factory import LLMFactory

app = FastAPI(title="LLM Chat Service")

# Initialize components
llm_factory = LLMFactory()


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
        response = await llm_factory.generate(request.prompt, request.provider)
        return ChatResponse(
            response=response,
            user_id=request.user_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

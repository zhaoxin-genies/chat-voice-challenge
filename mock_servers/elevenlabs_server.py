"""
Mock ElevenLabs TTS server.

Mimics the ElevenLabs API: accepts text and voice settings, returns raw MP3 bytes.

Usage:
    python3 mock_servers/elevenlabs_server.py
    # Runs on http://localhost:11100

Error paths (deterministic, so you can exercise each one in tests):
    - 401 Unauthorized : omit the `xi-api-key` header, or send the sentinel
                         key "invalid-key".
    - 429 Too Many     : request the sentinel voice_id "rate-limited-voice".
    - 400 Bad Request  : send empty `text`.
Any other non-empty api key + voice_id + text returns 200 with MP3 bytes.
"""

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Mock ElevenLabs TTS")

# Sentinels that deterministically trigger error responses.
INVALID_API_KEY = "invalid-key"
RATE_LIMITED_VOICE_ID = "rate-limited-voice"


class VoiceSettings(BaseModel):
    stability: float = 0.5
    similarity_boost: float = 0.75


class TTSRequest(BaseModel):
    text: str
    model_id: Optional[str] = "eleven_multilingual_v2"
    voice_settings: Optional[VoiceSettings] = None


@app.post("/v1/text-to-speech/{voice_id}")
async def text_to_speech(
    voice_id: str,
    request: TTSRequest,
    xi_api_key: Optional[str] = Header(None),
):
    # 401: missing or invalid API key.
    if not xi_api_key or xi_api_key == INVALID_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # 429: rate limit exceeded (triggered by the sentinel voice_id).
    if voice_id == RATE_LIMITED_VOICE_ID:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # 400: invalid request.
    if not request.text:
        raise HTTPException(status_code=400, detail="text is required")

    # Generate fake MP3 bytes (MP3 frame header + readable content)
    mp3_header = b"\xff\xfb\x90\x00"
    content = f"[elevenlabs|voice={voice_id}|model={request.model_id}|text={request.text}]".encode()
    audio_data = mp3_header + content

    return Response(content=audio_data, media_type="audio/mpeg")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=11100)

"""
Mock ElevenLabs TTS server.

Mimics the ElevenLabs API: accepts text and voice settings, returns raw MP3 bytes.

Usage:
    python3 mock_servers/elevenlabs_server.py
    # Runs on http://localhost:11100
"""

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Mock ElevenLabs TTS")


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

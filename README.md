# LLM Chat Service - Voice Feature

## Background

This is a simple LLM chat service with a `/chat` endpoint. It supports multiple LLM providers (OpenAI, Together, Anthropic).

## Your Task

**Add voice generation to the `/chat` endpoint using ElevenLabs TTS.**

A **mock ElevenLabs server** is provided so you can make real HTTP calls during development.

## Current Architecture

```
├── main.py                          # FastAPI app with /chat endpoint
├── llm_service.py                   # LLM provider base class
├── llm_providers.py                 # LLM provider implementations (OpenAI, Together, Anthropic)
├── mock_servers/
│   ├── llm_server.py                # Mock LLM API (runs on localhost:11200)
│   └── elevenlabs_server.py         # Mock ElevenLabs API (runs on localhost:11100)
├── tests/                           # Integration tests
└── requirements.txt
```

## Getting Started

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Start the mock LLM server (in a separate terminal, required for tests)
make mock-llm

# Run tests
make test

# Start the mock ElevenLabs server (in a separate terminal)
make mock-elevenlabs

# Start the dev server
make dev
```

---

## ElevenLabs API Reference

### Endpoint

```
POST {base_url}/v1/text-to-speech/{voice_id}
```

Production base URL: `https://api.elevenlabs.io`
Mock server base URL: `http://localhost:11100`

### Headers

```
xi-api-key: {ELEVENLABS_API_KEY}
Content-Type: application/json
```

### Request Body

```json
{
  "text": "Hello, how are you today?",
  "model_id": "eleven_multilingual_v2",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.75
  }
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `voice_id` | string (URL path) | yes | Voice identifier (e.g., `"21m00Tcm4TlvDq8ikWAM"`) |
| `text` | string | yes | Text to convert to speech |
| `model_id` | string | no | TTS model (default: `"eleven_multilingual_v2"`) |

### Response

```
HTTP 200
Content-Type: audio/mpeg

<raw MP3 bytes>
```

The response body is raw MP3 audio data (binary, not JSON).

### Error Responses

```
HTTP 401  - Invalid API key
HTTP 429  - Rate limit exceeded
HTTP 400  - Invalid request (empty text, invalid voice_id, etc.)
```

---

## Success Criteria

1. All existing tests still pass
2. `/chat` can generate and return audio when requested
3. Come up with a plan to verify your implementation works end-to-end

## Notes

- You may modify any existing files and create new ones as needed
- Feel free to use any tools, Google, AI coding assistants, etc.
- Ask questions if anything is unclear!

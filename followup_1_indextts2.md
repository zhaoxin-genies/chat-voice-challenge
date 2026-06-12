# Follow-up: Add IndexTTS2 Support

We now have a second TTS provider available called **IndexTTS2**. It's a self-hosted model running on GPU infrastructure with a different API from ElevenLabs.

---

## IndexTTS2 API Reference

### Endpoint

```
POST {INDEXTTS2_BASE_URL}/invocations
```

### Headers

```
Authorization: Bearer {INDEXTTS2_API_KEY}
Content-Type: application/json
```

### Request Body

```json
{
  "request_type": "tts",
  "text": "Hello, how are you today?",
  "voice_id": "voice_abc123",
  "model_id": "indextts2-v2"
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `request_type` | string | yes | Always `"tts"` |
| `text` | string | yes | Text to synthesize |
| `voice_id` | string | yes | Voice identifier |
| `model_id` | string | no | Model variant (default: `indextts2-v2`) |

### Response

```
HTTP 200
Content-Type: audio/mpeg

<raw MP3 bytes>
```

The response body is raw MP3 audio data (binary, not JSON).

### Error Responses

```
HTTP 401  - Invalid or missing Bearer token
HTTP 400  - Invalid request (missing required fields)
HTTP 503  - Model endpoint unavailable
```

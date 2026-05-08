import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestChatEndpoint:
    """Tests for the /chat endpoint."""

    def test_chat_basic(self):
        """Test basic chat functionality"""
        response = client.post(
            "/chat",
            json={"user_id": "test_user", "prompt": "Hello, how are you?"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["user_id"] == "test_user"

    def test_chat_with_provider(self):
        """Test chat with specific LLM provider"""
        response = client.post(
            "/chat",
            json={
                "user_id": "test_user",
                "prompt": "Hello!",
                "provider": "anthropic",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "claude-3-haiku" in data["response"]


class TestHealthEndpoint:
    """Test the health check endpoint."""

    def test_health(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

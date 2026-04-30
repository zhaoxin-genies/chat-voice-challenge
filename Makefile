PYTHON = ./venv/bin/python

.PHONY: install test dev mock-elevenlabs curl-test

install:
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m pytest tests/ -v

dev:
	$(PYTHON) -m uvicorn main:app --reload --port 8000

mock-elevenlabs:
	$(PYTHON) mock_servers/elevenlabs_server.py

curl-test:
	@echo "--- Text only ---"
	@curl -s -X POST http://localhost:8000/chat \
		-H "Content-Type: application/json" \
		-d '{"user_id": "alice", "prompt": "Hello!"}' | $(PYTHON) -m json.tool

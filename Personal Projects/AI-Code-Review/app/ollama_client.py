import os

import requests


class OllamaClient:
    """Minimal client used by the legacy file-based flow (generate_report.py).
    The PR pipeline uses app.providers instead, which adds health checks,
    fallback, retries and output validation."""

    def __init__(self, model=None, timeout=600):
        self.model = model or os.getenv("OLLAMA_PRIMARY_MODEL", "qwen2.5-coder:7b")
        base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
        self.url = f"{base}/api/generate"
        self.timeout = timeout

    def generate(self, prompt: str):
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=self.timeout
        )

        response.raise_for_status()

        return response.json()["response"]

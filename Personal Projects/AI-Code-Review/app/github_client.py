import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GitHubClient:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        token = self.token

        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }

    def get(self, url: str):
        if not self.token:
            raise RuntimeError("GITHUB_TOKEN is not set")

        response = requests.get(url, headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()
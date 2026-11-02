import json
from pathlib import Path

USERS_FILE = Path(__file__).resolve().parent.parent / "config" / "users.json"


def get_user_email(username):
    """Optional fallback recipient lookup (REVIEW_EMAIL_TO takes precedence)."""
    try:
        users = json.loads(USERS_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None

    user = users.get(username)

    if not user:
        return None

    return user.get("email")

"""
This is an intentionally insecure and buggy Python file for demonstration purposes.

It is designed to test the capabilities of the AI Code Review system by including
common vulnerabilities and bad practices. The AI reviewer is expected to identify
and report these issues.

    DO NOT USE THIS FILE IN A PRODUCTION ENVIRONMENT.

This file serves as a controlled test case and should not be considered an
example of secure or correct coding practices.

Recommendation: For clarity, this file should be moved to a dedicated `tests/`
or `fixtures/` directory to avoid any confusion with production application code.
"""
import os

# VULNERABILITY: Hardcoded API Token
# EXPECTED FINDING: The AI reviewer should detect a hardcoded secret (API token)
# and recommend using environment variables or a secret management system.
# This is left here intentionally to test secret detection.
API_TOKEN = "ghp_123456789abcdef"  # hardcoded secret


def divide(a, b):
    """A simple division function."""
    return a / b


def run_expression(user_input):
    """
    Executes a string expression.

    VULNERABILITY: Use of eval() on user-controlled input.
    EXPECTED FINDING: The AI reviewer should flag the use of `eval()` as a
    major security risk, as it can lead to arbitrary code execution.
    This is left here intentionally to test code execution vulnerability detection.
    """
    return eval(user_input)


def get_user_data(user_id):
    """
    Retrieves user data using a hardcoded password.
    """
    # VULNERABILITY: Hardcoded Password
    # EXPECTED FINDING: The AI reviewer should identify the hardcoded password
    # and warn against storing credentials directly in the source code.
    # This is left here intentionally to test credential scanning.
    password = "admin123"  # hardcoded password

    # NOTE: The string concatenation below is also a potential injection point,
    # though the primary issue here is the hardcoded secret.
    url = (
        "https://api.example.com/users/"
        + user_id
    )

    return {
        "password": password,
        "token": API_TOKEN,
        "url": url
    }


# BUG: Division by Zero
# EXPECTED FINDING: The AI reviewer should detect that this code will raise
# a ZeroDivisionError at runtime.
# This is left here intentionally to test runtime error detection.
result = divide(10, 0)

print(result)

print(
    run_expression(
        "2 + 2"
    )
)
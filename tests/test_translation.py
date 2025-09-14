import os
import re
import time
import httpx

BASE_URL = os.getenv("TRANSLATION_BASE_URL", "http://127.0.0.1:8000")


def wait_for_server(timeout: int = 180) -> None:
    """Poll the server's OpenAPI endpoint until it's ready or timeout."""
    deadline = time.time() + timeout
    url = f"{BASE_URL}/openapi.json"
    last_err = None
    while time.time() < deadline:
        try:
            r = httpx.get(url, timeout=5)
            if r.status_code == 200:
                return
        except Exception as e:
            last_err = e
        time.sleep(2)
    raise AssertionError(f"Server at {BASE_URL} not ready after {timeout}s. Last error: {last_err}")


def test_translate_endpoint():
    """Happy path: translate English to Hebrew via running server."""
    wait_for_server()

    response = httpx.post(
        f"{BASE_URL}/translate",
        json={
            "text": "Hello, world!",
            "source_lang": "en",
            "target_lang": "he",
        },
        timeout=180,
    )
    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    text = data["translated_text"]
    # Ensure it's a real translation (non-empty, not an internal error, contains Hebrew chars)
    assert isinstance(text, str) and text.strip()
    assert not text.startswith("[Translation Error")
    assert re.search(r"[\u0590-\u05FF]", text), f"Expected Hebrew letters in: {text}"


def test_translate_endpoint_invalid_language():
    """Invalid language should return 400 with a helpful message."""
    wait_for_server()

    response = httpx.post(
        f"{BASE_URL}/translate",
        json={
            "text": "Hello, world!",
            "source_lang": "en",
            "target_lang": "xx",
        },
        timeout=60,
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not supported" in data["detail"].lower()

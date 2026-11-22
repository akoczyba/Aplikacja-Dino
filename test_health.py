import os
import requests

BASE_URL = os.getenv("API_URL", "http://localhost:8000")


def test_health_check():
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    assert response.status_code == 200
    assert response.json().get("status") == "ok"

import pytest
import subprocess
import time
import requests
import sys

from framework.auth.token_manager import TokenManager
from framework.client.api_client import APIClient

BASE_URL = "http://localhost:5050"


def wait_for_server(url: str, retries: int = 10, delay: float = 0.5) -> bool:
    for _ in range(retries):
        try:
            requests.get(f"{url}/health", timeout=1)
            return True
        except Exception:
            time.sleep(delay)
    return False


@pytest.fixture(scope="session", autouse=True)
def mock_server():
    proc = subprocess.Popen(
        [sys.executable, "mock_server/server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if not wait_for_server(BASE_URL):
        proc.terminate()
        raise RuntimeError("Mock server did not start in time.")
    yield proc
    proc.terminate()
    proc.wait()


@pytest.fixture(scope="session")
def token():
    return TokenManager().get_token()


@pytest.fixture(scope="session")
def client(token):
    return APIClient(base_url=BASE_URL, token=token)


@pytest.fixture
def created_order(client):
    payload = {
        "customer_id": "CUST-001",
        "items": [{"sku": "ITEM-A", "quantity": 2, "price": 49.99}],
        "shipping_address": {
            "line1": "123 Main St",
            "city": "Cape Town",
            "postal_code": "8001",
            "country": "ZA"
        }
    }
    response = client.post("/orders", payload)
    assert response.status_code == 201
    return response.json()

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def valid_ad():
    return {
        "seller_id": 1,
        "is_verified_seller": False,
        "item_id": 100,
        "name": "Велосипед",
        "description": "Горный велосипед в хорошем состоянии",
        "category": 3,
        "images_qty": 2,
    }
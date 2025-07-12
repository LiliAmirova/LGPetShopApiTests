import pytest
import requests

BASE_URL = "http://5.181.109.28:9090/api/v3"

@pytest.fixture(scope="function")
def create_pet():
    """Фикстура для создания питомца, при этом наполнение не проверяем, т.к. это не тест"""
    payload = {
        "id": 1,
        "name": "Buddy",
        "status": "available"
    }

    response = requests.post(f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200
    return response.json()  # возвращаемый json будем использовать в тестах

@pytest.fixture(scope="function")
def create_order_store():
    """Фикстура для создания заказа, при этом наполнение не проверяем, т.к. это не тест"""
    payload = {
        "id": 1,
        "petId": 1,
        "quantity": 1,
        "status": "placed",
        "complete": True
    }

    response = requests.post(f"{BASE_URL}/store/order", json=payload)
    assert response.status_code == 200
    return response.json()  # возвращаемый json будем использовать в тестах
import pytest
from fastapi.testclient import TestClient
from mock import patch

from tests.test_data import IDS, ORDERS
from traiding_app.main import app
from traiding_app.models.constants import Status

client = TestClient(app)


def test_create_order():
    response = client.post(
        "/orders", json={"ticker": "TEST", "amount": 100, "order_type": "BUY"}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert "orderId" in json_response
    assert json_response["status"] == "PENDING"


@patch("traiding_app.main.orders", ORDERS)
def test_get_orders():
    response = client.get("/orders")
    assert response.status_code == 200


@patch("traiding_app.main.orders", ORDERS)
@pytest.mark.parametrize("test_input", [IDS[0], IDS[1], IDS[2]])
def test_get_order(test_input):
    response = client.get(f"/orders/{test_input}")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["id"] == test_input


@patch("traiding_app.main.orders", ORDERS)
def test_delete_order():
    response = client.delete("/orders/9c9db998-1401-4838-bdcd-ffe99a9e765f")
    assert response.status_code == 200
    deleted_response = client.get("/orders/9c9db998-1401-4838-bdcd-ffe99a9e765f")
    assert deleted_response.json().get("status") == Status.CANCELED


@patch("traiding_app.main.orders", ORDERS)
def test_delete_invalid_id():
    response = client.delete("/orders/invalid")
    assert response.status_code == 404
    response = client.delete("/orders/d7982f91-482f-421a-9274-9e8a1b031e45")
    assert response.status_code == 409


def test_invalid_order_fetch():
    response = client.get("/orders/invalid_id")
    assert response.status_code == 404

from fastapi.testclient import TestClient

from traiding_app.main import app
from traiding_app.models.constants import Status

client = TestClient(app)


# client doesn't support async, don't know what to do about it. Async client doesn't have websocket
def test_create_order_with_ws():
    with client.websocket_connect("/ws") as ws:
        response = client.post(
            "/orders", json={"ticker": "TEST", "amount": 100, "order_type": "BUY"}
        )
        assert response.status_code == 200
        json_response = response.json()
        assert "orderId" in json_response
        assert json_response["status"] == "PENDING"
        # ws receive two messages
        receive_pending = ws.receive_json()
        receive_executed = ws.receive_json()
        assert receive_pending["status"] == Status.PENDING
        assert receive_executed["status"] == Status.EXECUTED


def test_websocket():
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("Hello!")
        websocket.close()

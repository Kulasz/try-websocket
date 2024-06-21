import json
import time

from locust import HttpUser, TaskSet, constant, task
from locust_plugins.users.socketio import SocketIOUser


class TradingPlatformTasks(TaskSet):

    def on_start(self):
        self.order_ids = []

    @task(1)
    def place_order(self):
        response = self.client.post(
            "/orders",
            json={"ticker": "AAPL", "amount": 10, "order_type": "BUY"},
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        if response.status_code == 200:
            order_id = response.json()["orderId"]
            self.order_ids.append(order_id)


class TradingPlatformUser(HttpUser):
    tasks = [TradingPlatformTasks]
    wait_time = constant(0)


# Doesn't work properly on docker
# class MySocketIOUser(SocketIOUser):
#     # https://github.com/SvenskaSpel/locust-plugins/blob/master/examples/socketio_ex.py
#     fixed_count = 1  # one user in websocket just getting updates
#
#     @task
#     def my_task(self):
#         self.my_value = None
#
#         self.connect("ws://localhost:8000/ws")
#
#         # wait until I get a push message to on_message
#         while not self.my_value:
#             time.sleep(0.1)
#
#         # wait for additional pushes, while occasionally sending heartbeats, like a real client would
#         self.sleep_with_heartbeat(10)
#
#     def on_message(self, message):
#         self.my_value = json.loads(message)

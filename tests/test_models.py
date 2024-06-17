from traiding_app.models.order import Order


class TestOrderModels:

    def test_order(self):
        Order(id="1", status="PENDING", details={"123": 123})

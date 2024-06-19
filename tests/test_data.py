from traiding_app.models.order import Order, OrderDetails, Status

ORDERS = {
    "82a8c936-df42-4b83-a762-3d8d932648d4": Order(
        id="82a8c936-df42-4b83-a762-3d8d932648d4",
        status=Status.PENDING,
        details=OrderDetails(ticker="TEST1", amount=10, order_type="BUY"),
    ),
    "9c9db998-1401-4838-bdcd-ffe99a9e765f": Order(
        id="9c9db998-1401-4838-bdcd-ffe99a9e765f",
        status=Status.EXECUTED,
        details=OrderDetails(ticker="TEST2", amount=10, order_type="BUY"),
    ),
    "d7982f91-482f-421a-9274-9e8a1b031e45": Order(
        id="d7982f91-482f-421a-9274-9e8a1b031e45",
        status=Status.CANCELED,
        details=OrderDetails(ticker="TEST3", amount=10, order_type="SELL"),
    ),
}
IDS = list(ORDERS.keys())

"""Models for order"""

from typing import Literal

from pydantic import BaseModel, Field

from traiding_app.models.constants import Status

AVAILABLE_STATUS = Literal[Status.PENDING, Status.EXECUTED, Status.CANCELED]
ORDER_TYPE = Literal["BUY", "SELL"]


class OrderDetails(BaseModel):
    """Model for order details"""

    ticker: str = Field(examples=["AAPL"])
    amount: int = Field(examples=[10])
    order_type: ORDER_TYPE


class Order(BaseModel):
    """Model for basic order"""

    id: str
    status: AVAILABLE_STATUS = Status.PENDING
    details: OrderDetails

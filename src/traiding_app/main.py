"""Main"""

import asyncio
import random
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import JSONResponse

from traiding_app.models.order import Order, OrderDetails, Status

app = FastAPI()

orders: Dict[str, Order] = {}  # temp database


@app.post("/orders")
async def create_order(order_details: OrderDetails, background_tasks: BackgroundTasks):
    """Create order"""
    order_id = str(uuid4())
    order = Order(id=order_id, details=order_details)
    orders[order_id] = order
    background_tasks.add_task(change_order_status, order_id)
    return JSONResponse(content={"orderId": order_id, "status": Status.PENDING})


async def change_order_status(order_id: str):
    """Run order and notify about sucesss"""
    await asyncio.sleep(5)  # simulate delay
    order: Optional[Order] = orders.get(order_id)
    if order:
        new_status = random.choice([Status.EXECUTED, Status.CANCELED])
        order.status = new_status
        print(order)
        # await notify_clients(order) # Notify clients somehow


@app.get("/orders/{order_id}")
async def get_order(order_id: str) -> Order:
    """Get order details"""
    await asyncio.sleep(2)
    order = orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.delete("/orders/{order_id}")
async def delete_order(order_id: str):
    """Delete order by setting status to cancelled"""
    await asyncio.sleep(2)
    if order_id in orders and orders[order_id].status != Status.CANCELED:
        orders[order_id].status = Status.CANCELED
        return {"detail": "Order cancelled"}
    if order_id in orders and orders[order_id].status == Status.CANCELED:
        raise HTTPException(status_code=409, detail="Order already cancelled")
    raise HTTPException(status_code=404, detail="Order not found")


@app.get("/orders")
async def get_orders() -> List[Order]:
    """Get all orders"""
    await asyncio.sleep(2)
    return list(orders.values())

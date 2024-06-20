"""Main"""

import asyncio
import random
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import BackgroundTasks, FastAPI, HTTPException, WebSocket
from fastapi.responses import JSONResponse
from starlette.exceptions import WebSocketException
from starlette.websockets import WebSocketDisconnect

from traiding_app.models.order import Order, OrderDetails, Status
from traiding_app.websocket_receiver_endpoint import router

app = FastAPI()
app.include_router(router)  # frontend endpoint to see websocket orders

orders: Dict[str, Order] = {}  # temp database
clients: List[WebSocket] = []


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
    await notify_receiving(order_id)
    await asyncio.sleep(random.uniform(0.1, 1.0))  # simulate delay
    order: Optional[Order] = orders.get(order_id)
    if order:
        new_status = Status.EXECUTED
        order.status = new_status
        print(order)
        await notify_finish(order)


async def notify_receiving(order_id: str):
    for client in clients:
        await client.send_json({"orderId": order_id, "status": Status.PENDING})


async def notify_finish(order: Order):
    for client in clients:
        await client.send_json({"orderId": order.id, "status": order.status})


@app.get("/orders/{order_id}")
async def get_order(order_id: str) -> Order:
    """Get order details"""
    await asyncio.sleep(random.uniform(0.1, 1.0))
    order = orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.delete("/orders/{order_id}")
async def delete_order(order_id: str):
    """Delete order by setting status to cancelled"""
    await asyncio.sleep(random.uniform(0.1, 1.0))
    if order_id in orders and orders[order_id].status != Status.CANCELED:
        orders[order_id].status = Status.CANCELED
        return {"detail": "Order cancelled"}
    if order_id in orders and orders[order_id].status == Status.CANCELED:
        raise HTTPException(status_code=409, detail="Order already cancelled")
    raise HTTPException(status_code=404, detail="Order not found")


@app.get("/orders")
async def get_orders() -> List[Order]:
    """Get all orders"""
    await asyncio.sleep(random.uniform(0.1, 1.0))
    return list(orders.values())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketException as e:
        print(f"Error: {e}")
    except WebSocketDisconnect as e:
        print(f"Disconected: {e}")
    finally:
        clients.remove(websocket)

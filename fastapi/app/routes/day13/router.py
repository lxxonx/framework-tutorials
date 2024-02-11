from fastapi import APIRouter, Body, Depends, Response
import sqlite3
from app.routes.day13.db.models import Order

from app.routes.day13.order_service import OrderService

day_13_router = APIRouter(prefix="/13")

db = sqlite3.connect("app/routes/day13/db/day_13.sqlite")


def load_order_service():
    return OrderService(db=db)


@day_13_router.get("/sql")
async def select_sql():
    cursor = db.execute("SELECT 20231213;")
    data = cursor.fetchone()
    return data[0]


@day_13_router.post("/reset")
async def reset_sql(order_service: OrderService = Depends(load_order_service)):
    order_service.reset()
    return Response(status_code=200)


@day_13_router.post("/orders")
async def create_orders(
    orders: list[Order] = Body(...),
    order_service: OrderService = Depends(load_order_service),
):
    order_service.create_many(orders)

    return Response(status_code=200)


@day_13_router.get("/orders/total")
async def get_orders_sum(
    order_service: OrderService = Depends(load_order_service),
):
    total = order_service.get_total()

    return {"total": total}


@day_13_router.get("/orders/popular")
async def get_popular_order(
    order_service: OrderService = Depends(load_order_service),
):
    popular_item = order_service.get_popular_order()

    return {"popular": popular_item}

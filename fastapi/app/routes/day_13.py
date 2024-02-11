from fastapi import APIRouter, Body, Response
import sqlite3

from pydantic import BaseModel

day_13_router = APIRouter(prefix="/13")

db = sqlite3.connect("app/db/day_13.db")


@day_13_router.get("/sql")
async def select_sql():
    cursor = db.execute("SELECT 20231213;")

    data = cursor.fetchone()

    return data[0]


@day_13_router.post("/reset")
async def reset_sql():
    db.execute("DROP TABLE IF EXISTS orders;")
    db.executescript(
        """
        CREATE TABLE orders (
          id INT PRIMARY KEY,
          region_id INT,
          gift_name VARCHAR(50),
          quantity INT
        );
        """
    )

    return Response(status_code=200)


class Order(BaseModel):
    id: int
    region_id: int
    gift_name: str
    quantity: int


@day_13_router.post("/orders")
async def create_orders(
    orders: list[Order] = Body(...),
):
    for order in orders:
        db.execute(
            "INSERT INTO orders (id, region_id, gift_name, quantity) VALUES (?, ?, ?, ?);",
            (order.id, order.region_id, order.gift_name, order.quantity),
        )

    return Response(status_code=200)


@day_13_router.get("/orders/total")
async def get_orders_sum():
    orders_sum = db.execute(
        "SELECT SUM(orders.quantity) FROM orders;",
    )
    result = orders_sum.fetchone()

    total = result[0]

    return {"total": total}


@day_13_router.get("/orders/popular")
async def get_popular_order():
    orders_sum = db.execute(
        "SELECT orders.gift_name FROM orders GROUP BY orders.gift_name ORDER BY SUM(orders.quantity) DESC LIMIT 1;",
    )
    result = orders_sum.fetchone()
    if result is None:
        popular_item = None
    else:
        popular_item = result[0]

    return {"popular": popular_item}

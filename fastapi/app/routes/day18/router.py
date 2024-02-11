from fastapi import APIRouter, Body, Depends, Response
import sqlite3


from app.routes.day18.db.models import Order, Region
from app.routes.day18.order_service import OrderService
from app.routes.day18.region_service import RegionService

day_18_router = APIRouter(prefix="/18")

db = sqlite3.connect("app/routes/day18/db/day_18.sqlite")


def load_order_service():
    return OrderService(db=db)


def load_region_service():
    return RegionService(db=db)


@day_18_router.post("/reset")
async def reset_sql(
    order_service: OrderService = Depends(load_order_service),
    region_service: RegionService = Depends(load_region_service),
):
    order_service.reset()
    region_service.reset()

    return Response(status_code=200)


@day_18_router.post("/orders")
async def create_orders(
    orders: list[Order] = Body(...),
    order_service: OrderService = Depends(load_order_service),
):
    order_service.create_many(orders)
    return Response(status_code=200)


@day_18_router.get("/orders/total")
async def get_orders_sum(
    order_service: OrderService = Depends(load_order_service),
):
    total = order_service.get_total()

    return {"total": total}


@day_18_router.post("/regions")
async def create_regions(
    regions: list[Region] = Body(...),
    region_service: RegionService = Depends(load_region_service),
):
    region_service.create_many(regions)

    return Response(status_code=200)


@day_18_router.get("/regions/total")
async def get_region_total(
    region_service: RegionService = Depends(load_region_service),
):
    result = region_service.get_total()

    result = [{"region": region, "total": total} for region, total in result]

    return result


@day_18_router.get("/regions/top_list/{limit}")
async def get_region_top_list(
    limit: int,
    region_service: RegionService = Depends(load_region_service),
):
    result = region_service.get_top_list(limit)

    result = [
        {"region": region, "top_gifts": top_gifts if top_gifts else []}
        for region, top_gifts in result
    ]

    return result


@day_18_router.get("/orders/popular")
async def get_popular_order(
    order_service: OrderService = Depends(load_order_service),
):
    popular_item = order_service.get_popular_order()

    return {"popular": popular_item}

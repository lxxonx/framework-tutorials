from functools import reduce
from fastapi import APIRouter, Body
from app.routes.day4.request_models import ContestRequestModel, StrengthRequestModel


day_4_router = APIRouter(prefix="/4")  # noqa: F821


@day_4_router.post("/strength")
def read_strength(body: list[StrengthRequestModel] = Body(...)):
    _sum = reduce(lambda x, y: x + y.strength, body, 0)

    return _sum


@day_4_router.post("/contest")
def read_contest(body: list[ContestRequestModel] = Body(...)):
    fastest = max(body, key=lambda x: x.speed)
    tallest = max(body, key=lambda x: x.height)
    magician = max(body, key=lambda x: x.snow_magic_power)
    consumer = max(body, key=lambda x: x.candies)

    result = {
        "fastest": f"Speeding past the finish line with a strength of {fastest.strength} is {fastest.name}",
        "tallest": f"{tallest.name} is standing tall with his {tallest.antler_width} cm wide antlers",
        "magician": f"{magician.name} could blast you away with a snow magic power of {magician.snow_magic_power}",
        "consumer": f"{consumer.name} ate lots of candies, but also some {consumer.favorite_food}",
    }
    return result

from functools import reduce
from fastapi import APIRouter, Body
from pydantic import BaseModel, Field


day_4_router = APIRouter(prefix="/4")


class StrengthModel(BaseModel):
    strength: int
    name: str


@day_4_router.post("/strength")
def read_strength(body: list[StrengthModel] = Body(...)):
    _sum = reduce(lambda x, y: x + y.strength, body, 0)

    return _sum


class ContestModel(BaseModel):
    strength: int
    name: str
    speed: float
    height: int
    antler_width: int
    snow_magic_power: int
    favorite_food: str
    candies: int = Field(..., alias="cAnD13s_3ATeN-yesT3rdAy")


@day_4_router.post("/contest")
def read_contest(body: list[ContestModel] = Body(...)):
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

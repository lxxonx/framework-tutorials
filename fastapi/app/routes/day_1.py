from functools import reduce
from fastapi import APIRouter


day_1_router = APIRouter(prefix="/1")


@day_1_router.get("/{numbers:path}")
def read_numbers(numbers: str):
    numbers = numbers.split("/")
    result = reduce(lambda x, y: int(x) ^ int(y), numbers) ** 3

    return result

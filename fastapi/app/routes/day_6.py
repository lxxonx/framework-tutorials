from fastapi import APIRouter, Body, Request
from pydantic import BaseModel


day_6_router = APIRouter(prefix="/6")


class TextRequest(BaseModel):
    text: bytes


# !MARK: Body로 plain text 받기 어떻게 하지?
@day_6_router.post("/text")
async def read_numbers(body: str = Body(...)):
    splitted = body.split(b"elf")

    return {"elf": len(splitted) - 1}


def _count_overlapping_substring(string, substring):
    count = 0
    start = 0
    while start < len(string):
        index = string.find(substring, start)
        if index != -1:
            count += 1
            start = index + 1
        else:
            break
    return count


@day_6_router.post("")
async def count_elves(request: Request = Request):
    body = await request.body()
    splitted = _count_overlapping_substring(body, b"elf")
    elves_on_a_self = _count_overlapping_substring(body, b"elf on a shelf")
    shelves = _count_overlapping_substring(body, b"shelf")

    result = {
        "elf": splitted,
        "elf on a shelf": elves_on_a_self,
        "shelf with no elf on it": shelves - elves_on_a_self,
    }

    return result

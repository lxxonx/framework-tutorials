import datetime
from fastapi import APIRouter, Body
import ulid

day_12_router = APIRouter(prefix="/12")


class CacheStore:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._data = {}
        return cls._instance

    def set(self, key, value):
        self._data[key] = value

    def get(self, key):
        return self._data.get(key)


@day_12_router.post("/save/{packet}")
async def save_packet(
    packet: str,
):
    now: datetime.datetime = datetime.datetime.now()
    CacheStore().set(packet, now)
    return now


@day_12_router.get("/load/{packet}")
async def load_packet(
    packet: str,
):
    now: datetime.datetime = datetime.datetime.now()
    data: datetime.datetime = CacheStore().get(packet)
    if data is None:
        return "Not found"

    diff: datetime.datetime = now - data
    return diff.seconds


@day_12_router.post("/ulids")
async def ulids_to_uuids(
    ulids: list[str] = Body(...),
):
    result = []
    for uid in ulids:
        value = ulid.from_str(uid)
        result.append(value.uuid)
    result.reverse()
    return result


@day_12_router.post("/ulids/{weekday_index}")
async def ulids_calculation(
    weekday_index: int,
    ulids: list[str] = Body(...),
):
    now = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)
    christmas_eve = 0
    weekday = 0
    in_the_future = 0
    lsb_is_1 = 0
    for uid in ulids:
        value = ulid.from_str(uid)
        binay = int(value.bin, 2)
        datetime_value = value.timestamp().datetime
        if datetime_value.weekday() == weekday_index:
            weekday += 1
        if datetime_value > now:
            in_the_future += 1
        if datetime_value.month == 12 and datetime_value.day == 24:
            christmas_eve += 1
        if binay & 1:
            lsb_is_1 += 1

    result = {
        "christmas eve": christmas_eve,
        "weekday": weekday,
        "in the future": in_the_future,
        "LSB is 1": lsb_is_1,
    }

    return result

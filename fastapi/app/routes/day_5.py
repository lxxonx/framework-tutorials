from fastapi import APIRouter, Body


day_5_router = APIRouter(prefix="/5")

Names = list[str]


@day_5_router.post("")
def read_numbers(
    offset: int = 0, limit: int | None = None, split: int = 0, names: Names = Body([])
):
    if limit is not None:
        names = names[offset : offset + limit]
    else:
        names = names[offset:]
    if split:
        name_group = []
        for i in range(0, len(names), split):
            name_group.append(names[i : i + split])
        return name_group

    return names

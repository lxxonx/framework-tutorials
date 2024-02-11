from fastapi import APIRouter


example_router = APIRouter(prefix="")


@example_router.get("/")
def read_root():
    return {"Hello": "World"}


@example_router.get("/-1/error")
def error_route():
    1 / 0

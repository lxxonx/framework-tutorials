from fastapi import APIRouter

from .example import example_router

router = APIRouter()

router.include_router(router=example_router)

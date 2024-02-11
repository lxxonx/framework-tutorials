from fastapi import APIRouter
from .day_1 import day_1_router
from .day_4 import day_4_router
from .day_5 import day_5_router
from .example import example_router

router = APIRouter()

router.include_router(router=example_router)
router.include_router(router=day_1_router)
router.include_router(router=day_4_router)
router.include_router(router=day_5_router)

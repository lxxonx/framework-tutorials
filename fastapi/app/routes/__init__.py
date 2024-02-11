from fastapi import APIRouter
from .day_1 import day_1_router
from .day4 import day_4_router
from .day_5 import day_5_router
from .day_6 import day_6_router
from .day_7 import day_7_router
from .day_8 import day_8_router
from .day_11 import day_11_router, static_router
from .day_12 import day_12_router
from .day_13 import day_13_router
from .day_14 import day_14_router
from .day_15 import day_15_router
from .day18 import day_18_router
from .example import example_router

router = APIRouter()

router.include_router(router=example_router)
router.include_router(router=day_1_router)
router.include_router(router=day_4_router)
router.include_router(router=day_5_router)
router.include_router(router=day_6_router)
router.include_router(router=day_7_router)
router.include_router(router=day_8_router)
router.include_router(router=day_11_router)
router.include_router(router=day_12_router)
router.include_router(router=day_13_router)
router.include_router(router=day_14_router)
router.include_router(router=day_15_router)
router.include_router(router=day_18_router)

__all__ = [
    "router",
    "static_router",
]

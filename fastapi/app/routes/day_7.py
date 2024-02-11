import base64
import json
from fastapi import APIRouter, Cookie
from pydantic import BaseModel


day_7_router = APIRouter(prefix="/7")


@day_7_router.get("/decode")
async def get_some_cookies(
    recipe: str = Cookie(""),
):
    res = base64.b64decode(recipe).decode("utf-8")
    json_res = json.loads(res)

    return json_res


class DecodedCookieModel(BaseModel):
    recipe: dict
    pantry: dict


def _is_cookie_bakable(recipe: dict, pantry: dict):
    bakable = True
    for [ingredient, amount] in recipe.items():
        if amount == 0:
            continue
        pantry_amount = pantry.get(ingredient)
        if amount > pantry_amount:
            bakable = False

    if not bakable:
        return False

    for [ingredient, amount] in recipe.items():
        if amount == 0:
            continue
        pantry_amount = pantry.get(ingredient)
        pantry[ingredient] = pantry_amount - amount
    return True


@day_7_router.get("/bake")
async def bake_cookies(
    recipe: str = Cookie(""),
):
    res = base64.b64decode(recipe)
    cookie_model = DecodedCookieModel.model_validate_json(res)

    cookie_count = 0
    while _is_cookie_bakable(cookie_model.recipe, cookie_model.pantry):
        cookie_count += 1

    result = {"cookies": cookie_count, "pantry": cookie_model.pantry}

    return result

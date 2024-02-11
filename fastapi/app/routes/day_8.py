from fastapi import APIRouter
from httpx import AsyncClient


day_8_router = APIRouter(prefix="/8")


BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
G = 9.825  # m/s^2


class CacheStore:
    def __init__(self):
        self.instance = {}

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(CacheStore, cls).__new__(cls)
        return cls.instance

    def get(self, key):
        return self.instance.get(key)

    def set(self, key, value):
        self.instance[key] = value


@day_8_router.get("/weight/{pokedex_number}")
async def get_pokemon_weight(
    pokedex_number: int,
):
    pokemon_data = CacheStore().get(pokedex_number)
    if not pokemon_data:
        async with AsyncClient() as client:
            response = await client.get(f"{BASE_URL}{pokedex_number}")
            pokemon_data = response.json()
            CacheStore().set(pokedex_number, pokemon_data)
    weight = pokemon_data["weight"]
    to_kg = weight / 10
    return to_kg


@day_8_router.get("/drop/{pokedex_number}")
async def get_pokemon_drop_speed(
    pokedex_number: int,
):
    pokemon_data = CacheStore().get(pokedex_number)
    if not pokemon_data:
        async with AsyncClient() as client:
            response = await client.get(f"{BASE_URL}{pokedex_number}")
            pokemon_data = response.json()
            CacheStore().set(pokedex_number, pokemon_data)
    freefall_speed = (2 * G * 10) ** 0.5
    weight = pokemon_data["weight"]
    to_kg = weight / 10
    return freefall_speed * to_kg

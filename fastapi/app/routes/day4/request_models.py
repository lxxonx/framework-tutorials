from pydantic import BaseModel, Field


class StrengthRequestModel(BaseModel):
    strength: int
    name: str


class ContestRequestModel(BaseModel):
    strength: int
    name: str
    speed: float
    height: int
    antler_width: int
    snow_magic_power: int
    favorite_food: str
    candies: int = Field(..., alias="cAnD13s_3ATeN-yesT3rdAy")
